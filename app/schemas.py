"""Modelos de resposta da API do AtendeAI (documentam o /orchestrate no Swagger)."""
from typing import Literal

from pydantic import BaseModel


class FaqMatch(BaseModel):
    question: str
    answer: str
    matched_terms: list[str]
    score: float


class CustomerResult(BaseModel):
    agent: str
    category: str
    priority: str
    suggested_reply: str


class ResearchResult(BaseModel):
    agent: str
    found: bool
    query: str
    results: list[FaqMatch]


class ExecutorResult(BaseModel):
    agent: str
    authorized: bool
    requires_human: bool
    action: str
    reason: str


class SupervisorResult(BaseModel):
    agent: str
    approved: bool
    requires_human: bool
    decision: str


class AgentsResult(BaseModel):
    customer: CustomerResult
    research: ResearchResult
    executor: ExecutorResult
    supervisor: SupervisorResult


class OrchestrationResponse(BaseModel):
    project: str
    version: str
    agents: AgentsResult
    suggested_reply: str
    reply_source: Literal["llm", "faq", "rules"]
    faq_reference: FaqMatch | None
    human_review_required: bool
