"""Busca simples na base local de perguntas frequentes do AtendeAI."""
import json
import re
import unicodedata
from pathlib import Path

FAQ_PATH = Path(__file__).resolve().parent.parent / "data" / "faq.json"
STOPWORDS = {
    "a", "ao", "aos", "as", "com", "como", "da", "das", "de", "do", "dos",
    "e", "em", "o", "os", "ou", "para", "por", "que", "um", "uma", "meu",
    "minha", "se", "no", "na", "nos", "nas", "eu", "me", "sobre",
}


def normalize(text: str) -> str:
    """Remove acentos e pontuação e padroniza letras minúsculas."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def load_faq() -> list[dict]:
    """Carrega as perguntas frequentes do arquivo JSON."""
    with FAQ_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def search_faq(query: str, limit: int = 3) -> list[dict]:
    """Retorna as perguntas com maior sobreposição de termos com a busca."""
    query_terms = {
        term for term in normalize(query).split()
        if len(term) > 1 and term not in STOPWORDS
    }
    if not query_terms:
        return []

    results = []
    for item in load_faq():
        content_terms = set(normalize(item["question"] + " " + item["answer"]).split())
        matched_terms = sorted(query_terms & content_terms)
        if matched_terms:
            score = len(matched_terms) / len(query_terms)
            # Evita sugerir respostas com correspondência muito fraca.
            if score < 0.6:
                continue
            results.append({
                "question": item["question"],
                "answer": item["answer"],
                "matched_terms": matched_terms,
                "score": round(score, 2),
            })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]
