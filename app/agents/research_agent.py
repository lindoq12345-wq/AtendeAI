from app.assistant import CATEGORY_FAQ_QUERY
from app.faq import search_faq


def run_research_agent(message: str, category: str | None = None) -> dict:
    """Pesquisa respostas relevantes na base FAQ, priorizando a consulta da categoria."""
    query = CATEGORY_FAQ_QUERY.get(category, message) if category else message
    results = search_faq(query, limit=3)

    return {
        "agent": "research",
        "found": bool(results),
        "query": query,
        "results": results,
    }
