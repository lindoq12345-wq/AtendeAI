from evals.run_eval import evaluate, load_cases


def test_casos_sem_limitacao_conhecida_passam():
    """Protege contra regressões: casos que hoje funcionam não podem piorar."""
    cases = [c for c in load_cases() if not c.get("known_limitation")]
    results = evaluate(cases)
    falhas = [
        r for r in results
        if not (r["category_ok"] and r["review_ok"] and r["safety_ok"])
    ]
    assert not falhas, falhas


def test_arquivo_de_casos_tem_campos_obrigatorios():
    for case in load_cases():
        assert case["message"] and case["expected_category"]
