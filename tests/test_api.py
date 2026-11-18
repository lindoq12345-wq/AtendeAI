from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_faq_endpoint_returns_results():
    response = client.get("/faq", params={"q": "acompanhar pedido"})
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["question"] == "Como acompanhar meu pedido?"


def test_faq_endpoint_validates_short_query():
    response = client.get("/faq", params={"q": "a"})
    assert response.status_code == 422
