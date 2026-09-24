# INVENTÁRIO E CLASSIFICAÇÃO DOCUMENTAL — V0.1

## Objetivo

Registrar a classificação profissional da informação do Projeto Absoluto antes de novas migrações físicas.

Regra:
**INVENTARIAR → CLASSIFICAR → DETERMINAR AUTORIDADE → REFERENCIAR → MIGRAR CONTROLADAMENTE → VALIDAR**

Nenhum conteúdo é apagado apenas por parecer duplicado.

## Taxonomia aplicada

Cada documento é analisado por:
**função + autoridade + temporalidade + origem + público + relação com outras fontes**.

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

## Classificação atual das áreas

| Área | Função dominante | Estado | Ação |
|---|---|---|---|
| `abs_core/` | implementação | atual | KEEP |
| `tests/` | verificação | atual | KEEP |
| `scripts/` | operação/automação | atual | KEEP |
| `cerebro/mapas/` | mapas/navegação | evolução | KEEP + INDEX |
| `cerebro/especificacao/` | especificação/conhecimento | mista | CLASSIFY |
| `cerebro/00_estado/` | estado/snapshots | mista | CLASSIFY |
| `cerebro/data/` | dados/conhecimento | evolução | CLASSIFY |
| `continuidade/` | transferência | atual + histórico | CLASSIFY |
| `continuidade/06_interface/` | material temático de interface | mista | MOVE LATER |
| `continuidade/07_conhecimento/` | continuidade/estado estruturado | atual | KEEP / CANONICAL |
| `docs/01_operacao/` | operação | atual | KEEP |
| `docs/02_arquitetura/` | arquitetura | atual/evolução | KEEP + INDEX |
| `docs/03_planejamento/` | planejamento | evolução | KEEP + CROSS-REFERENCE |
| `docs/04_referencia/` | referência | atual/evolução | KEEP |
| `docs/06_auditoria/` | auditoria | temporal | KEEP |
| `docs/90_fontes/` | fontes | origem/histórico | KEEP |
| `docs/api/` | referência API | atual | KEEP |
| `20_interface/` | implementação/interface | atual | KEEP |
| `mini-cerebro/` | recuperação/patrimônio | mista | KEEP + CLASSIFY |
| `50_frentes/` | frentes futuras | futura | KEEP |
| `99_arquivo/` | patrimônio histórico | histórico | KEEP |

## Migração concluída nesta etapa

A antiga concorrência `docs/architecture/` foi eliminada.

Movidos, sem alteração de conteúdo:

- `docs/architecture/ABS_INTEGRATION_V1.md`
  → `docs/02_arquitetura/ABS_INTEGRATION_V1.md`
- `docs/architecture/PROJECT_KNOWLEDGE_V1.md`
  → `docs/02_arquitetura/PROJECT_KNOWLEDGE_V1.md`
- `docs/06_ROTEAMENTO_DE_RECURSOS_V1.md`
  → `docs/02_arquitetura/ROTEAMENTO_DE_RECURSOS_V1.md`
- `docs/04_EVOLUCAO_AUTONOMA_ASSISTIDA_ABS.md`
  → `docs/02_arquitetura/EVOLUCAO_AUTONOMA_ASSISTIDA_ABS.md`
- `docs/05_CONTROLE_DE_EVOLUCAO_PELA_INTERFACE.md`
  → `docs/02_arquitetura/CONTROLE_DE_EVOLUCAO_PELA_INTERFACE.md`
- `docs/07_CONHECIMENTO_E_DESCOBERTA_DE_FERRAMENTAS_V1.md`
  → `docs/02_arquitetura/CONHECIMENTO_E_DESCOBERTA_DE_FERRAMENTAS_V1.md`
- `docs/08_PLANEJAMENTO_E_APRENDIZAGEM_DE_FERRAMENTAS_V1.md`
  → `docs/02_arquitetura/PLANEJAMENTO_E_APRENDIZAGEM_DE_FERRAMENTAS_V1.md`
- `docs/09_MEMORIA_PERSISTENTE_DE_FERRAMENTAS_V1.md`
  → `docs/02_arquitetura/MEMORIA_PERSISTENTE_DE_FERRAMENTAS_V1.md`

Essa migração resolve uma duplicação estrutural clara: havia duas áreas destinadas à arquitetura atual.

## Concorrências ainda abertas

### Arquitetura
`docs/02_arquitetura/` × `cerebro/especificacao/`

A próxima análise deve separar:
- arquitetura operacional atual;
- especificação de conhecimento;
- legado reintegrado;
- histórico de investigação.

### Estado
`cerebro/00_estado/` × `continuidade/02_estado/` × Project Knowledge × handoffs.

Project Knowledge permanece como estado estruturado derivado; os demais precisam ser classificados como fonte, projeção, checkpoint ou histórico.

### Planejamento
`docs/03_planejamento/` × `cerebro/mapas/`.

Mapas continuam instrumentos de navegação/planejamento, não fila de tarefas.

### Continuidade
`continuidade/06_interface/` contém material temático que pode pertencer à documentação de arquitetura/planejamento da interface.

Não mover até comparar referências e função.

### Histórico
`docs/90_fontes/` × `cerebro/especificacao/07_historico/` × `mini-cerebro/` × `99_arquivo/`.

Não apagar. Determinar origem, período, função e relação com o presente.

## Regra sobre os arquivos-base

Os arquivos-base da visão original do Projeto Absoluto são **fontes de origem da visão**. Não devem ser reescritos como documentação técnica do ABS.

A rastreabilidade atual está registrada em `continuidade/07_conhecimento/SESSAO_ATUAL.md` e na documentação de auditoria.

## Próxima etapa

Continuar por **estado e continuidade**, depois planejamento e histórico. Só migrar documentos quando sua função e autoridade estiverem comprovadas.
