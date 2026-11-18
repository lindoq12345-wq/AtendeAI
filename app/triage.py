"""Classificação inicial por palavras-chave; etapa futura: IA/LLM e RAG."""
CATEGORIES = {
    "atraso_entrega": {"keywords": ["atrasado", "atraso", "demorando", "não chegou", "nao chegou", "entrega"], "priority": "alta", "reply": "Sinto muito pela demora. Vou verificar o andamento da entrega e ajudar você a encontrar uma solução."},
    "pedido_errado": {"keywords": ["pedido errado", "veio errado", "faltou", "item faltando", "produto errado"], "priority": "alta", "reply": "Peço desculpas pelo ocorrido. Vou registrar o problema com seu pedido para que a equipe possa analisar e orientar a solução."},
    "pagamento": {"keywords": ["cobrança", "cobranca", "pagamento", "pix", "cartão", "cartao", "estorno", "reembolso"], "priority": "media", "reply": "Entendi sua dúvida sobre pagamento. Vou direcionar a solicitação para conferência dos dados e orientação sobre os próximos passos."},
    "cancelamento": {"keywords": ["cancelar", "cancelamento", "quero cancelar"], "priority": "media", "reply": "Posso ajudar com sua solicitação de cancelamento. Vou verificar as condições do pedido antes de confirmar qualquer ação."},
}
DEFAULT_RESULT = {"category": "outros", "priority": "baixa", "suggested_reply": "Obrigado por entrar em contato. Pode explicar um pouco mais o que aconteceu para que eu possa ajudar?"}

def analyze_message(message: str) -> dict:
    normalized = " ".join(message.lower().strip().split())
    for category, rules in CATEGORIES.items():
        if any(keyword in normalized for keyword in rules["keywords"]):
            return {"category": category, "priority": rules["priority"], "suggested_reply": rules["reply"]}
    return DEFAULT_RESULT.copy()
