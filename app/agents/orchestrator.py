from app.agents.customer_agent import run_customer_agent
from app.agents.research_agent import run_research_agent
from app.agents.executor_agent import run_executor_agent
from app.agents.supervisor_agent import run_supervisor_agent


def run_orchestrator(message: str) -> dict:
    """Coordena os agentes do AtendeAI."""

    customer = run_customer_agent(message)
    research = run_research_agent(message, customer["category"])

    executor = run_executor_agent(customer["category"])

    supervisor = run_supervisor_agent(
        research=research,
        executor=executor,
        category=customer["category"],
    )

    faq_match = research["results"][0] if research["results"] else None

    return {
        "project": "AtendeAI",
        "version": "0.4.0",
        "agents": {
            "customer": customer,
            "research": research,
            "executor": executor,
            "supervisor": supervisor,
        },
        "suggested_reply": (
            faq_match["answer"]
            if faq_match and not supervisor["requires_human"]
            else customer["suggested_reply"]
        ),
        "faq_reference": faq_match,
        "human_review_required": supervisor["requires_human"],
    }


