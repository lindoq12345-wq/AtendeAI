"""Orquestra a triagem inicial e a busca na FAQ do AtendeAI.

Esta etapa usa regras determinísticas; não chama um modelo de linguagem.
"""

from app.faq import search_faq
from app.triage import analyze_message

# Consultas curtas e controladas ajudam a localizar a FAQ ligada à categoria.
CATEGORY_FAQ_QUERY = {
    "atraso_entrega": "acompanhar pedido",
    "pedido_errado": "pedido veio errado",
    "pagamento": "problema pagamento",
    "cancelamento": "cancelamento pedido",
}

# O protótipo não pode consultar transações nem executar cancelamentos.
CATEGORIES_REQUIRING_HUMAN_REVIEW = {"pagamento", "cancelamento"}


def assist_message(message: str) -> dict:
    """Classifica a mensagem, procura uma FAQ relacionada e indica revisão humana."""
    triage = analyze_message(message)
    category = triage["category"]
    faq_query = CATEGORY_FAQ_QUERY.get(category, message)
    matches = search_faq(faq_query, limit=1)
    faq_match = matches[0] if matches else None

    human_review_required = (
        faq_match is None or category in CATEGORIES_REQUIRING_HUMAN_REVIEW
    )

    if category in CATEGORIES_REQUIRING_HUMAN_REVIEW:
        review_reason = (
            "A solicitação envolve pagamento ou cancelamento e precisa de validação humana; "
            "o protótipo não executa transações nem cancela pedidos."
        )
    elif faq_match is None:
        review_reason = (
            "Nenhuma resposta suficientemente relacionada foi encontrada na FAQ; "
            "a solicitação deve ser analisada por uma pessoa."
        )
    else:
        review_reason = None

    return {
        "category": category,
        "priority": triage["priority"],
        "suggested_reply": triage["suggested_reply"],
        "faq_match": faq_match,
        "human_review_required": human_review_required,
        "review_reason": review_reason,
    }
