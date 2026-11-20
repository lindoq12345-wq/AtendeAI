from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from app.agents.orchestrator import run_orchestrator
from app.assistant import assist_message
from app.faq import search_faq
from app.triage import analyze_message

app = FastAPI(
    title="AtendeAI",
    description="Assistente de atendimento para classificar solicitações e consultar perguntas frequentes.",
    version="0.4.0",
)


class MessageRequest(BaseModel):
    message: str = Field(min_length=3, max_length=1000, description="Mensagem enviada pelo cliente")


@app.get("/")
def home():
    return {
        "project": "AtendeAI",
        "version": "0.4.0",
        "message": "API de atendimento está funcionando.",
    }


@app.post("/analyze")
def analyze(request: MessageRequest):
    return analyze_message(request.message)


@app.get("/faq")
def faq_search(q: str = Query(min_length=2, max_length=200, description="Termos para buscar na FAQ")):
    results = search_faq(q)
    return {"query": q, "count": len(results), "results": results}


@app.post("/assist")
def assist(request: MessageRequest):
    """Combina classificação, FAQ relacionada e indicação de revisão humana."""
    return assist_message(request.message)



@app.post("/orchestrate")
def orchestrate(request: MessageRequest):
    """Executa o fluxo multiagente: cliente, pesquisa, executor e supervisor."""
    return run_orchestrator(request.message)
