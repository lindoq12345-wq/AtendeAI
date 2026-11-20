from app.agents.customer_agent import run_customer_agent
from app.agents.executor_agent import run_executor_agent
from app.agents.research_agent import run_research_agent
from app.agents.supervisor_agent import run_supervisor_agent
from app.llm import generate_reply

VERSION = "0.5.0"


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
    requires_human = supervisor["requires_human"]

    # Fallback determinístico: FAQ (quando seguro) ou resposta por regras.
    if faq_match and not requires_human:
        reply, source = faq_match["answer"], "faq"
    else:
        reply, source = customer["suggested_reply"], "rules"

    llm_reply = generate_reply(
        message=message,
        category=customer["category"],
        faq_answer=faq_match["answer"] if faq_match else None,
        requires_human=requires_human,
    )
    if llm_reply:
        reply, source = llm_reply, "llm"

    return {
        "project": "AtendeAI",
        "version": VERSION,
        "agents": {
            "customer": customer,
            "research": research,
            "executor": executor,
            "supervisor": supervisor,
        },
        "suggested_reply": reply,
        "reply_source": source,
        "faq_reference": faq_match,
        "human_review_required": requires_human,
    }
