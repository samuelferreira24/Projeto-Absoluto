# INVENTÁRIO E CLASSIFICAÇÃO DOCUMENTAL — V0.1

## Objetivo

Registrar a primeira classificação profissional da informação do Projeto Absoluto antes de realizar migrações físicas.

Regra desta fase:
**INVENTARIAR → CLASSIFICAR → DETERMINAR AUTORIDADE → REFERENCIAR → MIGRAR CONTROLADAMENTE**

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
| continuidade/06_interface/ | tema de interface | mista | CLASSIFY/MOVE LATER |
| continuidade/07_conhecimento/ | estado/continuidade estruturada | atual | KEEP/CANONICAL |
| docs/01_operacao/ | operação | atual | KEEP |
| docs/02_arquitetura/ | arquitetura | atual/evolução | KEEP + CROSS-REFERENCE |
| docs/03_planejamento/ | planejamento | evolução | KEEP + CROSS-REFERENCE |
| docs/04_referencia/ | referência | atual/evolução | KEEP |
| docs/architecture/ | arquitetura existente | mista | CONSOLIDATE LATER |
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

### 3. Planejamento

Há sobreposição potencial entre docs/03_planejamento/, cerebro/mapas/, documentos de continuidade e mapas históricos.

**Ação:** mapas permanecem instrumentos de navegação/planejamento; não devem ser tratados como fila ou estado operacional.

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