from app.triage import analyze_message


def run_customer_agent(message: str) -> dict:
    """Analisa a mensagem e prepara uma resposta inicial ao cliente."""
    result = analyze_message(message)

    return {
        "agent": "customer",
        "category": result["category"],
        "priority": result["priority"],
        "suggested_reply": result["suggested_reply"],
    }
