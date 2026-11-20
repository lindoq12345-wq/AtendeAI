# Histórico de versões

## 0.3.0 — Atendimento inicial combinado

- Adicionado `POST /assist` para combinar triagem por palavras-chave e consulta à FAQ.
- Incluídas respostas demonstrativas para pedido incorreto, pagamento e cancelamento.
- Adicionada indicação de revisão humana para pagamentos, cancelamentos e casos sem FAQ adequada.
- Ampliados os testes automatizados e atualizada a documentação.

## 0.2.0 — FAQ inicial

- Adicionado endpoint `GET /faq` para busca lexical na base local em JSON.
- Adicionadas normalização de texto, documentação e testes da FAQ.

## 0.1.0 — Estrutura inicial

- Criada API FastAPI com verificação de saúde e classificação básica por regras.

## 0.4.0
- Fluxo multiagente (customer, research, executor, supervisor) e endpoint POST /orchestrate.
- Research agent usa a consulta por categoria, como o /assist.
- Ações sensíveis (pagamento, cancelamento) continuam bloqueadas e vão para revisão humana.

## 0.5.0
- Resposta ao cliente via LLM (Gemini ou Anthropic) com fallback para FAQ/regras; campo reply_source.
- response_model no /orchestrate.
- Executor e supervisor seguem determinísticos; o LLM nunca decide ações.
