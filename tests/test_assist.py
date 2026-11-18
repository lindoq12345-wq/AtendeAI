from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_assist_finds_faq_for_delivery_delay():
    response = client.post(
        "/assist",
        json={"message": "Meu pedido está atrasado e ainda não chegou"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "atraso_entrega"
    assert body["priority"] == "alta"
    assert body["faq_match"]["question"] == "Como acompanhar meu pedido?"
    assert body["human_review_required"] is False


def test_assist_requires_human_review_for_payment():
    response = client.post("/assist", json={"message": "Tive um problema com o pagamento"})
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "pagamento"
    assert body["faq_match"]["question"] == "Como consultar um problema de pagamento?"
    assert body["human_review_required"] is True
    assert body["review_reason"]


def test_assist_requires_human_review_when_faq_has_no_match():
    response = client.post(
        "/assist",
        json={"message": "Preciso de ajuda com uma situação diferente"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "outros"
    assert body["faq_match"] is None
    assert body["human_review_required"] is True


def test_assist_validates_message_length():
    response = client.post("/assist", json={"message": "oi"})
    assert response.status_code == 422


def test_assist_finds_faq_for_wrong_order_item():
    response = client.post("/assist", json={"message": "Meu pedido veio errado"})
    body = response.json()
    assert body["category"] == "pedido_errado"
    assert body["faq_match"]["question"] == "Como informar que o pedido veio errado?"
    assert body["human_review_required"] is False


def test_assist_flags_cancellation_for_human_review():
    response = client.post("/assist", json={"message": "Preciso cancelar meu pedido"})
    body = response.json()
    assert body["category"] == "cancelamento"
    assert body["faq_match"]["question"] == "Como solicitar o cancelamento de um pedido?"
    assert body["human_review_required"] is True
