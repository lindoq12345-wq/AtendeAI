from fastapi.testclient import TestClient

from app import llm
from app.agents.orchestrator import run_orchestrator
from app.main import app

client = TestClient(app)


class _Block:
    type = "text"

    def __init__(self, text):
        self.text = text


class _Resp:
    def __init__(self, text):
        self.content = [_Block(text)]


def _fake_client(text=None, error=False):
    class _Messages:
        def create(self, **kwargs):
            if error:
                raise RuntimeError("falha simulada")
            return _Resp(text)

    class _Client:
        def __init__(self, **kwargs):
            self.messages = _Messages()

    return _Client


class _HttpResp:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_sem_chave_retorna_none():
    assert llm.generate_reply("oi tudo bem", "outros", None, True) is None


def test_anthropic_resposta_valida(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-falsa")
    monkeypatch.setattr(llm, "Anthropic", _fake_client("Vamos encaminhar para a equipe."))
    assert llm.generate_reply("x", "pagamento", None, True) == "Vamos encaminhar para a equipe."


def test_resposta_longa_demais_e_rejeitada(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-falsa")
    monkeypatch.setattr(llm, "Anthropic", _fake_client("x" * 1000))
    assert llm.generate_reply("x", "outros", None, False) is None


def test_anthropic_erro_cai_no_fallback(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "chave-falsa")
    monkeypatch.setattr(llm, "Anthropic", _fake_client(error=True))
    assert llm.generate_reply("x", "outros", None, False) is None


def test_gemini_resposta_valida(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "chave-falsa")
    payload = {"candidates": [{"content": {"parts": [{"text": "Vamos encaminhar para a equipe."}]}}]}
    monkeypatch.setattr(llm.httpx, "post", lambda *a, **k: _HttpResp(payload))
    assert llm.generate_reply("x", "pagamento", None, True) == "Vamos encaminhar para a equipe."


def test_gemini_erro_cai_no_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "chave-falsa")

    def falha(*args, **kwargs):
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(llm.httpx, "post", falha)
    assert llm.generate_reply("x", "outros", None, False) is None


def test_gemini_resposta_malformada_cai_no_fallback(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "chave-falsa")
    monkeypatch.setattr(llm.httpx, "post", lambda *a, **k: _HttpResp({"candidates": []}))
    assert llm.generate_reply("x", "outros", None, False) is None


def test_orchestrator_sem_llm_usa_regras_ou_faq():
    result = run_orchestrator("Meu pagamento foi cobrado duas vezes")
    assert result["reply_source"] in {"rules", "faq"}


def test_orchestrator_com_llm_nao_altera_decisoes_de_seguranca(monkeypatch):
    monkeypatch.setattr(
        "app.agents.orchestrator.generate_reply",
        lambda **kwargs: "Resposta gerada pelo modelo.",
    )
    result = run_orchestrator("Meu pagamento foi cobrado duas vezes")
    assert result["reply_source"] == "llm"
    assert result["suggested_reply"] == "Resposta gerada pelo modelo."
    assert result["agents"]["executor"]["action"] == "blocked"
    assert result["agents"]["supervisor"]["decision"] == "human_review"
    assert result["human_review_required"] is True


def test_openapi_documenta_resposta_do_orchestrate():
    schema = client.get("/openapi.json").json()
    ref = schema["paths"]["/orchestrate"]["post"]["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    assert ref.endswith("OrchestrationResponse")
