# Referência da API

A documentação OpenAPI interativa é disponibilizada localmente em `/docs` quando a aplicação está em execução.

Base URL local: `http://127.0.0.1:8000`

## `GET /` — saúde da aplicação

Exemplo:

```bash
curl http://127.0.0.1:8000/
```

Retorna o nome do projeto, a versão e uma mensagem de disponibilidade.

## `POST /analyze` — classificar mensagem

Corpo da requisição:

```json
{ "message": "Meu pedido está atrasado" }
```

A mensagem deve conter entre 3 e 1000 caracteres. A resposta inclui `category`, `priority` e `suggested_reply`. Categorias atualmente configuradas: `atraso_entrega`, `pedido_errado`, `pagamento`, `cancelamento` e `outros`.

## `GET /faq` — pesquisar perguntas frequentes

Parâmetro obrigatório `q`, com 2 a 200 caracteres. Exemplo:

```bash
curl "http://127.0.0.1:8000/faq?q=acompanhar%20pedido"
```

A resposta contém a consulta original, a quantidade de resultados e uma lista de itens com pergunta, resposta, termos coincidentes e pontuação lexical.

## Códigos de resposta

- `200`: consulta processada.
- `422`: entrada inválida segundo as regras de validação.

As rotas são demonstrativas e não consultam serviços externos.

## `POST /assist` — atendimento inicial combinado

Corpo da requisição:

```json
{ "message": "Meu pedido está atrasado e ainda não chegou" }
```

A resposta combina a categoria e prioridade da triagem com a melhor correspondência lexical encontrada na FAQ. Os campos principais são `category`, `priority`, `suggested_reply`, `faq_match`, `human_review_required` e `review_reason`. Quando não há correspondência adequada, ou quando o assunto envolve pagamento ou cancelamento, a resposta sinaliza revisão humana. O endpoint não executa ações nem consulta sistemas externos.

Exemplo reduzido de resposta para uma mensagem sobre atraso:

```json
{
  "category": "atraso_entrega",
  "priority": "alta",
  "suggested_reply": "Sinto muito pela demora. Vou verificar o andamento da entrega e ajudar você a encontrar uma solução.",
  "faq_match": {
    "question": "Como acompanhar meu pedido?",
    "answer": "O cliente pode acompanhar o status do pedido na área de pedidos do aplicativo.",
    "matched_terms": ["acompanhar", "pedido"],
    "score": 1.0
  },
  "human_review_required": false,
  "review_reason": null
}
```

A pontuação `score` é lexical e não representa confiança estatística.
