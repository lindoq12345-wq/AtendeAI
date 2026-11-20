def run_supervisor_agent(
    research: dict,
    executor: dict,
    category: str,
) -> dict:
    """Supervisiona os resultados dos agentes."""

    requires_human = (
        not research["found"]
        or executor["requires_human"]
        or category in {"pagamento", "cancelamento"}
    )

    return {
        "agent": "supervisor",
        "approved": not requires_human,
        "requires_human": requires_human,
        "decision": "human_review" if requires_human else "approved",
    }
