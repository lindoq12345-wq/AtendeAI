# Roadmap do AtendeAI

O roadmap é uma proposta de evolução. Os itens futuros não devem ser apresentados como funcionalidades concluídas.

## Concluído — versão 0.3.0

- [x] Estrutura inicial em Python e API com FastAPI.
- [x] Endpoint de triagem por regras.
- [x] Base FAQ em JSON e endpoint de consulta lexical.
- [x] `POST /assist` combina triagem e FAQ.
- [x] Sinalização de revisão humana para pagamentos, cancelamentos e ausência de resposta adequada.
- [x] Testes automatizados para o fluxo combinado.
- [x] Documentação técnica e instruções locais atualizadas.

## Etapas posteriores

### Qualidade e robustez
- [ ] Expandir casos de teste e medir cobertura.
- [ ] Melhorar normalização e classificação de mensagens.
- [ ] Adicionar logging sem registrar dados pessoais.
- [ ] Adicionar CI para executar testes em cada atualização.

### Dados e recuperação
- [ ] Avaliar persistência em banco de dados.
- [ ] Organizar FAQ com identificadores, categorias e fontes.
- [ ] Implementar recuperação semântica e avaliar RAG com citações das fontes recuperadas.

### IA generativa com responsabilidade
- [ ] Avaliar integração com um LLM usando variáveis de ambiente para segredos.
- [ ] Restringir a resposta ao contexto recuperado quando apropriado.
- [ ] Definir fallback, limites, validação e encaminhamento humano.
- [ ] Criar conjunto de avaliação para medir relevância, precisão e respostas sem suporte.

### Entrega e publicação
- [ ] Preparar README final com evidências reais de execução.
- [ ] Publicar repositório no GitHub.
- [ ] Avaliar deploy demonstrativo sem dados reais.

## Critério para considerar uma etapa concluída

Uma funcionalidade só deve ser marcada como concluída depois de implementada, testada e documentada. Registre limitações e resultados observados; não invente métricas ou resultados.
