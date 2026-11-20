from fastapi.testclient import TestClient

from app.agents.orchestrator import run_orchestrator
from app.main import app

client = TestClient(app)


def test_pagamento_exige_revisao_humana_e_executor_bloqueado():
    result = run_orchestrator("Meu pagamento foi cobrado duas vezes")
    assert result["agents"]["customer"]["category"] == "pagamento"
    assert result["agents"]["executor"]["action"] == "blocked"
    assert result["agents"]["supervisor"]["decision"] == "human_review"
    assert result["human_review_required"] is True


def test_mensagem_sem_faq_vai_para_humano():
    result = run_orchestrator("xyzzy qwerty plugh")
    assert result["agents"]["customer"]["category"] == "outros"
    assert result["agents"]["research"]["found"] is False
    assert result["human_review_required"] is True


def test_executor_nunca_autoriza_no_prototipo():
    for msg in ["Meu pedido está atrasado", "Quero cancelar", "Meu pagamento falhou"]:
        assert run_orchestrator(msg)["agents"]["executor"]["authorized"] is False


def test_endpoint_orchestrate():
    response = client.post("/orchestrate", json={"message": "Quero cancelar meu pedido"})
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "0.5.0"
    assert body["human_review_required"] is True


def test_endpoint_orchestrate_valida_mensagem_curta():
    assert client.post("/orchestrate", json={"message": "oi"}).status_code == 422


def test_faq_reference_disponivel_para_revisor_humano():
    result = run_orchestrator("Meu pagamento foi cobrado duas vezes")
    assert result["human_review_required"] is True
    assert result["faq_reference"] is not None
    assert result["faq_reference"]["score"] >= 0.6

