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

**Estado: preparar contrato semântico antes de automatizar.**

Depois de validar o modelo, adicionar classificação assistida, extração de relações, indexação semântica e rotinas de atualização.

A próxima etapa técnica é definir e testar a representação semântica intermediária, mantendo separação entre conteúdo de fonte e inferência derivada, proveniência, estado e confiança.

## Critério de passagem

Nenhuma fase deve ser considerada concluída apenas porque o código executa. Deve existir evidência de que a capacidade preserva informação e melhora a recuperação sem destruir contexto ou proveniência.
