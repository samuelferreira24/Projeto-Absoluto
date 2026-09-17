# Roadmap de implementação da BASE V0.1

## Fase 1 — Fundação

**Estado: validada.**

- identidade dos registros;
- contrato JSON;
- estados;
- relações;
- proveniência;
- versionamento.

## Fase 2 — Ingestão

**Estado: validada para o conjunto inicial de formatos testados.**

- detector de formato;
- adaptadores;
- representação intermediária;
- catálogo de fontes;
- preservação de originais.

## Fase 3 — Registro e recuperação

**Estado: implementada e validada no núcleo V0.1.**

- armazenamento local portátil;
- criação/atualização de registros;
- busca textual;
- consulta por metadados.

## Fase 4 — Calibração

**Estado: concluída para os materiais definidos nesta versão.**

Usar os três materiais atuais como conjunto de teste. Medir se a base consegue preservar origem, estrutura, relações e distinção entre fato, hipótese, interpretação e decisão.

A calibração demonstrou preservação estrutural, origem, integridade e conteúdo. Relações semânticas e classificação de conhecimento permanecem como responsabilidade de uma camada posterior.

## Fase 5 — Acervo bagunçado

**Estado: piloto validado; migração ampla ainda não autorizada pelo próprio critério técnico.**

Testar um lote pequeno e representativo de arquivos antigos. Não migrar tudo de uma vez.

O lote piloto cobriu MHT, TXT e DOCX e confirmou a preservação das fontes e a utilização de adaptadores distintos.

## Fase 6 — Automação

**Estado: contrato semântico definido e validado em unidade; automação de classificação ainda não ativada.**

A representação semântica intermediária foi definida em `REPRESENTACAO_SEMANTICA_V0_1.md` e implementada em `cerebro/semantica.py`. O contrato preserva separadamente fonte, unidade semântica, classificação, confiança, estado, relações e proveniência.

A classificação automática por IA, extração automática de relações e indexação semântica continuam condicionadas a testes com casos reais e ambíguos. Não automatizar inferências antes de validar esse comportamento.

## Próxima etapa

Construir um conjunto pequeno de exemplos semânticos reais e ambíguos, provenientes dos materiais já calibrados, e testar classificação, relações e proveniência contra critérios explícitos. A etapa deve produzir evidência antes de qualquer automação em escala.

## Critério de passagem

Nenhuma fase deve ser considerada concluída apenas porque o código executa. Deve existir evidência de que a capacidade preserva informação e melhora a recuperação sem destruir contexto ou proveniência.
