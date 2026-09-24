# INVENTÁRIO E CLASSIFICAÇÃO DOCUMENTAL — V0.1

## Objetivo

Registrar a primeira classificação profissional da informação do Projeto Absoluto antes de realizar migrações físicas.

Regra desta fase:
**INVENTARIAR → CLASSIFICAR → DETERMINAR AUTORIDADE → REFERENCIAR → MIGRAR CONTROLADAMENTE → VALIDAR**

Nenhum conteúdo é apagado apenas por parecer duplicado.

## Taxonomia aplicada

Cada documento é analisado por função, autoridade, temporalidade, origem, público e relação com outras fontes.

## Fontes de maior autoridade por pergunta

| Pergunta | Fonte prioritária |
|---|---|
| O que existe agora? | código + testes + CI + evidências |
| Qual é o estado estruturado? | Project Knowledge |
| Qual é a visão/direção? | registros autorizados do Imperador + fontes-base |
| Qual é a arquitetura? | arquitetura atual + código + contratos |
| O que foi decidido? | registro de decisão |
| Como operar? | documentação operacional |
| O que foi provado? | evidências/testes/execuções |
| O que aconteceu antes? | histórico preservado |
| Como retomar uma sessão? | continuidade/checkpoint |

## Classificação inicial das áreas

| Área | Função dominante | Temporalidade | Ação |
|---|---|---|---|
| abs_core/ | implementação | atual | KEEP |
| tests/ | verificação | atual | KEEP |
| scripts/ | operação/automação | atual | KEEP |
| cerebro/mapas/ | mapas/navegação | evolução | KEEP + INDEX |
| cerebro/especificacao/ | conhecimento/especificação | mista | CLASSIFY |
| cerebro/00_estado/ | estado e snapshots | mista | CLASSIFY |
| cerebro/data/ | dados/conhecimento | evolução | CLASSIFY |
| continuidade/ | transferência | atual + histórico | CLASSIFY |
| continuidade/06_interface/ | tema de interface | mista | MIGRATED / EMPTY |
| continuidade/07_conhecimento/ | estado/continuidade estruturada | atual | KEEP/CANONICAL |
| docs/01_operacao/ | operação | atual | KEEP |
| docs/02_arquitetura/ | arquitetura | atual/evolução | KEEP + CROSS-REFERENCE |
| docs/03_planejamento/ | planejamento | evolução | KEEP + CROSS-REFERENCE |
| docs/04_referencia/ | referência | atual/evolução | KEEP |
| docs/architecture/ | arquitetura existente | — | REMOVED / CONSOLIDATED |
| docs/api/ | referência API | atual | KEEP |
| docs/90_fontes/ | fontes | histórica/origem | KEEP |
| docs/06_auditoria/ | avaliação | temporal | KEEP |
| mini-cerebro/ | auxiliar/histórico | mista | KEEP + CLASSIFY |
| 20_interface/ | implementação/interface | atual | KEEP |
| 50_frentes/ | frentes futuras | futura | KEEP |
| 99_arquivo/ | patrimônio | histórico | KEEP |

## Concorrências que precisam de auditoria

### 1. Arquitetura

Há três áreas que podem responder parcialmente à mesma pergunta: docs/02_arquitetura/, docs/architecture/ e cerebro/especificacao/.

**Ação:** não mover ainda. Mapear documento por documento e determinar qual é arquitetura atual, referência, especificação histórica ou fonte.

### 2. Estado

Há múltiplos mecanismos: cerebro/00_estado/, continuidade/02_estado/, handoffs, project_knowledge.json e MAPA_AUTO_ESTADO_PROJETO.md.

**Ação:** Project Knowledge deve ser o estado estruturado derivado atual. Os demais devem ser classificados como fonte, projeção, checkpoint ou histórico.

### 3. Planejamento × mapas

A auditoria documento a documento desta zona concluiu que há sobreposição temática, mas não duplicação funcional suficiente para fundir as áreas.

- `docs/03_planejamento/` é a entrada documental e abriga planejamentos específicos;
- `cerebro/mapas/` é a representação em rede de capacidades, dependências, pendências e caminhos;
- `cerebro/00_estado/` fica fora do planejamento porque registra estado/snapshots.

**Ação:** manter as áreas separadas, reforçar referências cruzadas e não criar uma nova camada intermediária.

### 4. Continuidade

continuidade/ contém material de transferência e também material temático.

**Ação:** manter a infraestrutura de transferência; classificar e posteriormente retirar material que pertence estruturalmente a operação, arquitetura, planejamento ou referência.

### 5. Histórico

Há patrimônio em docs/90_fontes/, mini-cerebro/, 99_arquivo/ e históricos dentro de cerebro/especificacao/.

**Ação:** não apagar. Identificar origem, período, função e relação com o presente.

## Classes de ação

- KEEP — permanece no caminho atual.
- INDEX — permanece, mas precisa de índice/ponte.
- LINK — permanece e ganha referência para a autoridade correta.
- CLASSIFY — precisa de análise documento a documento.
- CONSOLIDATE — candidato a unificação depois de comparar função e autoridade.
- MOVE LATER — candidato a migração controlada após dependências.
- DERIVED — projeção gerada de outra fonte.
- HISTORICAL — preservado como passado.
- OBSOLETE — só usar após evidência de substituição.

## Regra sobre os arquivos-base

Os arquivos-base que contêm a visão original do Projeto Absoluto devem ser tratados como **fontes de origem da visão**, e não como simples documentação técnica do ABS.

Nesta fase, não reescrever nem substituir os arquivos-base. Primeiro catalogá-los e estabelecer seus papéis. Uma documentação derivada pode explicar sua relação, mas não deve apagar ou alterar a fonte original.

## Resultado da auditoria planejamento × mapas

Não foi identificada migração física necessária nesta zona. O único arquivo que estava funcionalmente fora de lugar era o quadro de status ABS, já reclassificado para `cerebro/00_estado/STATUS_ABS_V1_2026-09-22.md`.

As áreas de planejamento permanecem separadas por função e agora apontam umas para as outras sem duplicar conteúdo.

## Atualização pós-auditoria — PRs #74–#76

A etapa de referências e órfãos documentais foi executada. Os seguintes casos comprovados foram resolvidos:
- cópias antigas em áreas de continuidade já migradas para destinos canônicos;
- referência obsoleta a `docs/architecture/`;
- quadro de status duplicado em `cerebro/mapas/`;
- snapshot de transferência duplicado em `cerebro/00_estado/`.

O resultado foi validado contra a árvore atual do `main`. Nenhum código, teste ou fonte-base foi alterado nessa limpeza.

O restante deste documento preserva a classificação e o histórico da fase inicial; não deve ser interpretado como inventário físico em tempo real.

## Próxima etapa

A próxima auditoria deve ser documento a documento, com pelo menos:

```
CAMINHO
FUNÇÃO
AUTORIDADE
TEMPORALIDADE
ORIGEM
PÚBLICO
DUPLICAÇÃO
REFERÊNCIAS
AÇÃO
DESTINO
```

Só depois disso executar migrações em lotes pequenos, verificáveis e reversíveis.

## Migração seguinte — estado, continuidade e interface

### Interface
- `continuidade/06_interface/01_PESQUISA_REFERENCIAL_INTERFACE_ADAPTATIVA.md` → `docs/90_fontes/INTERFACE_ADAPTATIVA_PESQUISA_2026-09-22.md` — MOVE / fonte de pesquisa.
- `continuidade/06_interface/02_DEFINICAO_INTERFACE_ADAPTATIVA_ABS.md` → `docs/02_arquitetura/INTERFACE_ADAPTATIVA_ABS_V0_1.md` — MOVE / arquitetura de protótipo.
- `continuidade/06_interface/03_PLANEJAMENTO_ATUAL_INTERFACE_ABS_P0.md` → `docs/03_planejamento/INTERFACE_ADAPTATIVA_ABS_P0.md` — MOVE / planejamento.

### Estado e construção
- `continuidade/02_estado/01_ESTADO_ATUAL_PROJETO.md` → `continuidade/99_legado/ESTADO_ATUAL_PROJETO_SNAPSHOT_2026-09-19.md` — HISTORICAL SNAPSHOT.
- `continuidade/04_construcao/01_PONTO_EXATO_DE_PARADA.md` → `continuidade/99_legado/PONTO_EXATO_DE_PARADA_SNAPSHOT.md` — HISTORICAL SNAPSHOT.
- `continuidade/04_construcao/02_HANDOFF_CONSTRUCAO_ABS_V1.md` → `continuidade/05_handoffs/03_HANDOFF_CONSTRUCAO_ABS_V1_SNAPSHOT_2026-09-21.md` — HANDOFF SNAPSHOT.

## Estado após a classificação

`Project Knowledge` permanece como estado estruturado derivado. `cerebro/00_estado/` permanece para estado/snapshots do Cérebro. `continuidade/05_handoffs/` contém checkpoints de transferência. Material histórico de continuidade fica em `continuidade/99_legado/`.

A antiga `continuidade/06_interface/` não deve voltar a ser usada como área temática. Novos documentos de interface devem ser classificados por função.

A antiga `docs/architecture/` não deve voltar a ser usada; arquitetura atual fica em `docs/02_arquitetura/`.
