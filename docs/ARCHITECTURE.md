# Arquitetura e decisões técnicas

## Visão geral

Na versão 0.3.0, o AtendeAI é uma API monolítica pequena construída com FastAPI. A separação por módulos mantém as responsabilidades simples e explícitas.

```text
Cliente HTTP
    |
    v
FastAPI (app/main.py)
    |-------------------------------|
    v                               v
Triagem                         Orquestração
(app/triage.py)                 (app/assistant.py)
                                    |
                                    v
                                Busca FAQ
                                (app/faq.py)
                                    |
                                    v
                               data/faq.json
```

## Responsabilidades

- `app/main.py`: cria a aplicação, define os modelos de entrada e expõe as rotas HTTP.
- `app/triage.py`: aplica regras de palavras-chave para definir categoria, prioridade e texto sugerido.
- `app/faq.py`: normaliza o texto, carrega o arquivo JSON e calcula sobreposição de termos.
- `app/assistant.py`: combina triagem e busca FAQ e sinaliza casos que precisam de revisão humana.
- `data/faq.json`: contém conteúdo demonstrativo editável.
- `tests/`: verifica os comportamentos essenciais.

## Fluxo de triagem

1. O cliente envia uma mensagem para `POST /analyze`.
2. Pydantic valida o tamanho mínimo e máximo do texto.
3. A função `analyze_message` procura palavras-chave nas categorias configuradas.
4. A API devolve categoria, prioridade e resposta sugerida.
5. Se nenhuma regra corresponder, a mensagem recebe a categoria `outros`.

## Fluxo da FAQ

1. O cliente envia termos pela query string `q` em `GET /faq`.
2. A consulta e o conteúdo da FAQ são normalizados: minúsculas, sem acentos e sem pontuação.
3. Palavras comuns são removidas da consulta.
4. O sistema calcula a proporção de termos da consulta encontrados na pergunta ou resposta.
5. Resultados abaixo do limiar de 0,60 são descartados e os demais são ordenados pela pontuação.

A pontuação é uma medida heurística de correspondência lexical, não uma probabilidade nem uma avaliação semântica.

## Decisões e trade-offs

- **FAQ em JSON:** reduz a complexidade inicial e facilita edição; não é ideal para múltiplos usuários ou grandes volumes.
- **Regras explícitas:** são simples de entender e testar; têm cobertura limitada e exigem manutenção manual.
- **FastAPI:** oferece validação e documentação OpenAPI automática; é adequado para um protótipo de API.
- **Sem LLM nesta versão:** evita custos, dependências externas e respostas generativas não verificadas enquanto os fluxos básicos ainda estão sendo construídos.

## Segurança e privacidade

Use apenas mensagens fictícias nos testes e demonstrações. Não inclua nomes, telefones, endereços, credenciais, números de pedido ou outros dados pessoais em exemplos públicos. A versão atual não implementa autenticação, autorização, limitação de requisições nem política de retenção; portanto, não deve ser exposta como serviço de produção.

## Fluxo de atendimento combinado (`POST /assist`)

1. A API valida a mensagem recebida.
2. A triagem identifica categoria e prioridade por palavras-chave.
3. Uma consulta curta associada à categoria procura a FAQ correspondente.
4. A API retorna a resposta candidata e indica revisão humana para pagamentos, cancelamentos ou ausência de correspondência adequada.

Essa indicação é apenas informativa: não existe fila de atendimento nem encaminhamento real nesta versão.
