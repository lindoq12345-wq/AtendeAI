# AtendeAI — Assistente inteligente de atendimento

> Projeto de portfólio acadêmico desenvolvido para demonstrar fundamentos de Engenharia de Software e Inteligência Artificial aplicados a atendimento digital.

**Autor:** Lindomar Amarildo Quintao Olimpio  
**Formação:** Engenharia de Software — Faculdade Anhanguera  
**Objetivo:** compor portfólio para candidatura a oportunidades de estágio em Engenharia de Software/IA, incluindo processos seletivos previstos para 2027.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)](https://fastapi.tiangolo.com/) [![Status](https://img.shields.io/badge/status-protótipo%20acadêmico-orange)]()

## Sobre o projeto

O AtendeAI é um protótipo de API que recebe mensagens de clientes, classifica solicitações por regras simples e consulta uma base local de perguntas frequentes (FAQ). A proposta é evoluir o projeto em pequenas entregas, aplicando boas práticas de desenvolvimento, testes e documentação antes de integrar recursos mais avançados de IA.

**Importante:** este é um projeto independente e demonstrativo, sem vínculo, parceria ou integração oficial com o iFood. Não acessa pedidos, contas, pagamentos nem dados reais de clientes. O cenário de atendimento é fictício e inspirado em problemas comuns de comércio eletrônico e delivery.

## Funcionalidades da versão 0.3.0

- `GET /` — verifica se a API está disponível.
- `POST /analyze` — classifica uma mensagem por palavras-chave e sugere uma resposta.
- `GET /faq?q=...` — pesquisa uma base local de perguntas frequentes em JSON.
- `POST /assist` — combina triagem e FAQ e indica quando é necessária revisão humana.
- Normalização de texto para busca, incluindo remoção de acentos e pontuação.
- Validação de entradas com Pydantic.
- Testes automatizados com Pytest e FastAPI TestClient.
- Documentação interativa dos endpoints em `/docs`.

### Tecnologias utilizadas

- **Python 3.10+** — linguagem principal.
- **FastAPI** — construção da API REST.
- **Pydantic** — validação dos dados de entrada.
- **Pytest** — testes automatizados.
- **JSON** — armazenamento inicial da FAQ.

## Como executar no Windows 11

1. Instale Python 3.10 ou superior e marque a opção para adicionar Python ao PATH.
2. Extraia o repositório e abra o PowerShell na pasta `atendeai`.
3. Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Se a política do PowerShell impedir a ativação, execute os comandos usando o Python do ambiente virtual diretamente:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Com o ambiente ativado, instale as dependências e inicie a API:

```powershell
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse `http://127.0.0.1:8000/docs` para experimentar a API.

## Exemplos de uso

### Classificar uma solicitação

`POST /analyze` com o corpo JSON:

```json
{
  "message": "Meu pedido está atrasado e ainda não chegou"
}
```

A API retorna uma categoria, prioridade e resposta sugerida. A classificação atual é baseada em palavras-chave, não em um modelo de aprendizado de máquina.

### Combinar triagem e FAQ

`POST /assist` com o mesmo corpo JSON de `/analyze`. A resposta reúne categoria, prioridade, texto sugerido, melhor correspondência da FAQ (quando encontrada) e `human_review_required`. Pagamentos, cancelamentos e mensagens sem resposta adequada na FAQ são sinalizados para revisão humana. O endpoint não executa ações.

### Consultar a FAQ

`GET /faq?q=acompanhar%20pedido`

A resposta contém a pergunta encontrada, a resposta, os termos coincidentes e uma pontuação de correspondência. Essa pontuação representa sobreposição de palavras, não uma probabilidade de acerto.

## Executar os testes

Com as dependências instaladas, execute:

```powershell
python -m pytest -q
```

Os testes cobrem a busca na FAQ, a validação das entradas, a triagem e o fluxo combinado de atendimento. Consulte o resultado real do comando no seu ambiente; não considere o projeto validado em outro computador sem executar os testes nele.

## Estrutura do projeto

```text
atendeai/
├── app/
│   ├── __init__.py
│   ├── main.py       # rotas e configuração da API
│   ├── faq.py        # carregamento e busca na FAQ
│   └── triage.py     # classificação por palavras-chave
├── data/
│   └── faq.json      # perguntas e respostas demonstrativas
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── ROADMAP.md
│   └── PORTFOLIO.md
├── tests/
│   ├── test_api.py
│   ├── test_assist.py
│   └── test_faq.py
├── CHANGELOG.md
├── .gitignore
├── requirements.txt
└── README.md
```

## Histórico de versões

Consulte o [CHANGELOG](CHANGELOG.md) para ver as entregas por versão.

## Documentação adicional

- [Arquitetura e decisões técnicas](docs/ARCHITECTURE.md)
- [Referência da API](docs/API.md)
- [Plano de evolução](docs/ROADMAP.md)
- [Resumo para portfólio e candidatura](docs/PORTFOLIO.md)

## Limitações conhecidas

- A classificação usa correspondência de palavras-chave e pode falhar diante de gírias, erros de digitação, ironia ou mensagens com mais de um problema.
- A busca da FAQ usa sobreposição de termos; ainda não é busca semântica nem RAG.
- As respostas são exemplos estáticos e não executam ações.
- Não há autenticação, banco de dados, monitoramento, integração externa ou tratamento de dados reais.
- Não existe integração com sistemas do iFood.

## Próximas etapas

Veja o [roadmap](docs/ROADMAP.md). A evolução planejada inclui melhorar a triagem, ampliar os testes, adicionar persistência e, em etapas posteriores, avaliar integração com LLM e recuperação RAG com fontes rastreáveis.

## Contexto acadêmico e profissional

O projeto é desenvolvido como iniciativa individual de aprendizagem no curso de Engenharia de Software da Faculdade Anhanguera. Seu propósito é demonstrar evolução prática, capacidade de decompor problemas, construir APIs, testar funcionalidades e documentar decisões técnicas. Não representa experiência profissional nem participação em processo seletivo ou programa oficial do iFood.
