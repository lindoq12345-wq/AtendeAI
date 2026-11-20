import pytest


@pytest.fixture(autouse=True)
def sem_chaves_de_llm(monkeypatch):
    """Garante que nenhum teste chame uma API real por acidente."""
    for name in ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "ATENDEAI_PROVIDER", "ATENDEAI_MODEL"):
        monkeypatch.delenv(name, raising=False)
