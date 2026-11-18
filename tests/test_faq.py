from app.faq import search_faq


def test_finds_order_tracking_answer():
    results = search_faq("Como acompanhar meu pedido?")
    assert results
    assert results[0]["question"] == "Como acompanhar meu pedido?"
    assert "área de pedidos" in results[0]["answer"]


def test_finds_refund_answer_without_accent():
    results = search_faq("reembolso")
    assert results
    assert "reembolso" in results[0]["question"].lower()


def test_returns_empty_when_no_term_matches():
    assert search_faq("assunto completamente desconhecido") == []
