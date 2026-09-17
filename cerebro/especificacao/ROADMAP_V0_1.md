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

**Estado: implementada e validada no núcleo V0.1; recuperação expandida em evolução.**

- armazenamento local portátil;
- criação/atualização de registros;
- busca textual;
- consulta por metadados;
- recuperação lexical normalizada;
- priorização por título/tipo/conteúdo;
- expansão por relações do grafo.

A recuperação avançada deve permanecer modular para receber posteriormente embeddings, reranking e busca vetorial sem substituir a recuperação determinística existente.

## Fase 4 — Calibração

**Estado: concluída para os materiais definidos nesta versão.**

Usar os três materiais atuais como conjunto de teste. Medir se a base consegue preservar origem, estrutura, relações e distinção entre fato, hipótese, interpretação e decisão.

A calibração demonstrou preservação estrutural, origem, integridade e conteúdo. Relações semânticas e classificação de conhecimento permanecem como responsabilidade de uma camada posterior.

## Fase 5 — Acervo bagunçado

**Estado: piloto validado; migração ampla ainda não autorizada pelo próprio critério técnico.**

Testar um lote pequeno e representativo de arquivos antigos. Não migrar tudo de uma vez.

O lote piloto cobriu MHT, TXT e DOCX e confirmou a preservação das fontes e a utilização de adaptadores distintos.

## Fase 6 — Semântica e automação assistida

**Estado: contrato semântico + auditoria determinística + orquestração de modelos implementados; automação de inferência em escala ainda não ativada.**

A representação semântica intermediária foi definida em `REPRESENTACAO_SEMANTICA_V0_1.md` e implementada em `cerebro/semantica.py`. O contrato preserva separadamente fonte, unidade semântica, classificação, confiança, estado, relações e proveniência.

A auditoria em `cerebro/auditoria.py` verifica integridade do grafo semântico, proveniência, referências e inconsistências básicas antes de aceitar resultados derivados.

A camada `cerebro/modelos.py` permite conectar diferentes provedores/modelos por papel e executar consenso entre modelos sem acoplar o Cérebro a um fornecedor específico.

A classificação automática por IA, extração automática de relações e indexação semântica continuam condicionadas a testes com casos reais e ambíguos. Não transformar uma saída plausível de IA em fato sem proveniência, confiança e validação.

## Fase 7 — Contexto temporal e recuperação avançada

**Estado: especificada como próxima expansão arquitetural.**

A evolução deve incorporar, sem quebrar a base:

- histórico temporal de fatos e relações;
- distinção entre quando algo ocorreu e quando o Cérebro aprendeu;
- busca lexical + semântica + relações;
- reranking independente;
- recuperação orientada à pergunta;
- escopo por projeto/área/contexto;
- preservação de versões antigas em vez de apagamento;
- métricas de qualidade de recuperação.

Essa direção é coerente com arquiteturas atuais de memória de agentes que usam grafos temporais, proveniência e recuperação híbrida. A implementação deve continuar própria e substituível, podendo incorporar bibliotecas externas apenas como componentes intercambiáveis.

## Fase 8 — Consolidação automática

**Estado: planejada.**

Depois de validar a recuperação e a semântica, implementar rotinas para:

1. detectar novos registros;
2. propor unidades semânticas;
3. propor relações;
4. detectar possíveis contradições;
5. enviar itens ambíguos para verificação independente;
6. registrar resultado e confiança;
7. consolidar somente o que passou pelos critérios;
8. preservar sempre a fonte e o histórico.

## Fase 9 — Cérebro operacional

**Estado: objetivo de integração.**

Unificar ingestão, registro, semântica, recuperação, auditoria, modelos e histórico em um fluxo operacional único, acessível por CLI e futuramente por API/MCP ou outra interface. Interfaces são camadas substituíveis; o núcleo do Cérebro permanece independente delas.

## Próxima etapa executável

Construir um conjunto pequeno de exemplos semânticos reais e ambíguos, provenientes dos materiais já calibrados, e medir:

- classificação;
- proveniência;
- relações;
- confiança;
- detecção de inconsistência;
- recuperação direta;
- recuperação por relações;
- comportamento diante de informação contraditória.

Somente depois dessa medição ativar automação assistida com modelos reais.

## Critério de passagem

Nenhuma fase deve ser considerada concluída apenas porque o código executa. Deve existir evidência de que a capacidade preserva informação e melhora a recuperação sem destruir contexto, proveniência, histórico ou possibilidade de revisão.
