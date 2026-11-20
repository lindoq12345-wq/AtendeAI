"""Avaliação offline do AtendeAI: mede triagem e segurança sem chamar nenhum LLM.

Uso:
    python -m evals.run_eval            # imprime o resumo
    python -m evals.run_eval --report   # também grava docs/EVAL.md
"""
import json
import os
import sys
from pathlib import Path

# Resultado determinístico: nunca usar LLM na avaliação.
for _name in ("GEMINI_API_KEY", "ANTHROPIC_API_KEY", "ATENDEAI_PROVIDER", "ATENDEAI_MODEL"):
    os.environ.pop(_name, None)

from app.agents.orchestrator import run_orchestrator  # noqa: E402

CASES_PATH = Path(__file__).resolve().parent / "cases.json"
REPORT_PATH = Path(__file__).resolve().parent.parent / "docs" / "EVAL.md"
SENSITIVE = {"pagamento", "cancelamento"}


def load_cases() -> list[dict]:
    # utf-8-sig tolera o BOM que o PowerShell 5 grava.
    with CASES_PATH.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def evaluate(cases: list[dict]) -> list[dict]:
    results = []
    for case in cases:
        output = run_orchestrator(case["message"])
        category = output["agents"]["customer"]["category"]
        review = output["human_review_required"]

        expected_review = case.get("expect_human_review")
        results.append({
            "message": case["message"],
            "expected_category": case["expected_category"],
            "category": category,
            "review": review,
            "category_ok": category == case["expected_category"],
            "review_ok": expected_review is None or review == expected_review,
            # Segurança: intenção sensível real nunca pode ficar sem revisão humana.
            "safety_ok": not (case["expected_category"] in SENSITIVE and not review),
            "known_limitation": bool(case.get("known_limitation")),
            "note": case.get("note", ""),
        })
    return results


def summarize(results: list[dict]) -> dict:
    total = len(results)
    review_checked = [r for r in results if r["review_ok"] is not None]
    return {
        "total": total,
        "category_hits": sum(r["category_ok"] for r in results),
        "review_hits": sum(r["review_ok"] for r in review_checked),
        "review_total": len(review_checked),
        "safety_misses": sum(not r["safety_ok"] for r in results),
        "regressions": [
            r for r in results
            if not r["known_limitation"] and not (r["category_ok"] and r["review_ok"] and r["safety_ok"])
        ],
    }


def render(results: list[dict], summary: dict) -> str:
    pct = round(100 * summary["category_hits"] / summary["total"])
    lines = [
        "# Avaliação offline (sem LLM)",
        "",
        f"- Casos: {summary['total']}",
        f"- Categoria correta: {summary['category_hits']}/{summary['total']} ({pct}%)",
        f"- Decisão de revisão humana correta: {summary['review_hits']}/{summary['review_total']}",
        f"- **Falhas de segurança** (pagamento/cancelamento sem revisão humana): {summary['safety_misses']}",
        "",
        "| Mensagem | Esperado | Obtido | Revisão humana | Resultado |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        ok = r["category_ok"] and r["review_ok"] and r["safety_ok"]
        status = "ok" if ok else ("limitação conhecida" if r["known_limitation"] else "FALHA")
        lines.append(
            f"| {r['message']} | {r['expected_category']} | {r['category']} | {'sim' if r['review'] else 'não'} | {status} |"
        )
    notes = [f"- \"{r['message']}\": {r['note']}" for r in results if r["note"]]
    if notes:
        lines += ["", "## Limitações observadas", *notes]
    return "\n".join(lines) + "\n"


def main() -> int:
    results = evaluate(load_cases())
    summary = summarize(results)
    report = render(results, summary)
    print(report)
    if "--report" in sys.argv:
        REPORT_PATH.write_text(report, encoding="utf-8")
        print(f"Relatório gravado em {REPORT_PATH}")
    return 1 if summary["regressions"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
