SENSITIVE_CATEGORIES = {"pagamento", "cancelamento"}


def run_executor_agent(category: str) -> dict:
    """Controla ações que podem exigir execução."""

    if category in SENSITIVE_CATEGORIES:
        return {
            "agent": "executor",
            "authorized": False,
            "requires_human": True,
            "action": "blocked",
            "reason": "Ação sensível exige validação humana.",
        }

    return {
        "agent": "executor",
        "authorized": False,
        "requires_human": False,
        "action": "not_needed",
        "reason": "Nenhuma execução externa é necessária.",
    }
