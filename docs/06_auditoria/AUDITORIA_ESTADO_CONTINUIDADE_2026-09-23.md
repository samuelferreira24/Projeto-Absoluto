# AUDITORIA DE ESTADO E CONTINUIDADE — 2026-09-23

## Objetivo

Auditar a concorrência entre estado, continuidade, handoffs e Project Knowledge antes de novas migrações.

## Resultado

A análise confirmou que o repositório já possui uma fonte estruturada de estado derivado:

- `continuidade/07_conhecimento/project_knowledge.json` — estado estruturado derivado;
- `continuidade/07_conhecimento/MAPA_AUTO_ESTADO_PROJETO.md` — projeção humana do estado derivado;
- `continuidade/07_conhecimento/SESSAO_ATUAL.md` — checkpoint da sessão;
- `cerebro/00_estado/` — estados observados e snapshots do Cérebro;
- `continuidade/05_handoffs/` — handoffs/checkpoints para transferência;
- `continuidade/03_decisoes/` — decisões e regras autorizadas.

A concorrência não deve ser resolvida apagando essas fontes. Cada uma tem função diferente.

## Autoridade por pergunta

| Pergunta | Fonte |
|---|---|
| O que existe agora? | código + testes + CI + evidências |
| Qual é o estado estruturado derivado? | Project Knowledge |
| Qual é a projeção legível desse estado? | MAPA_AUTO_ESTADO_PROJETO.md |
| O que foi decidido? | decisões autorizadas |
| Como uma nova IA retoma? | handoff/checkpoint + fontes canônicas |
| O que aconteceu em uma data anterior? | snapshots/histórico |
| Qual é a visão do Projeto Absoluto? | modelo do Projeto + fontes-base |

## Classificação realizada

### Estado

`cerebro/00_estado/` permanece como área de estado/snapshot do Cérebro.

`continuidade/02_estado/01_ESTADO_ATUAL_PROJETO.md` era um snapshot antigo e foi reclassificado para:

`continuidade/99_legado/ESTADO_ATUAL_PROJETO_SNAPSHOT_2026-09-19.md`

Não é mais apresentado como estado atual.

### Construção

`continuidade/04_construcao/01_PONTO_EXATO_DE_PARADA.md` era um ponto de parada histórico e foi preservado em:

`continuidade/99_legado/PONTO_EXATO_DE_PARADA_SNAPSHOT.md`

`continuidade/04_construcao/02_HANDOFF_CONSTRUCAO_ABS_V1.md` foi reclassificado como snapshot de handoff em:

`continuidade/05_handoffs/03_HANDOFF_CONSTRUCAO_ABS_V1_SNAPSHOT_2026-09-21.md`

O handoff operacional atual continua sendo `continuidade/05_handoffs/01_HANDOFF_ATUAL_OPERACIONAL.md`, mas deve sempre apontar para o estado vivo antes de afirmar o estado atual.

### Interface

`continuidade/06_interface/` continha documentação temática, não infraestrutura de transferência. Os três documentos foram classificados por função:

- pesquisa → `docs/90_fontes/INTERFACE_ADAPTATIVA_PESQUISA_2026-09-22.md`;
- definição arquitetural → `docs/02_arquitetura/INTERFACE_ADAPTATIVA_ABS_V0_1.md`;
- planejamento P0 → `docs/03_planejamento/INTERFACE_ADAPTATIVA_ABS_P0.md`.

A migração preservou o conteúdo e removeu a mistura entre continuidade e documentação temática.

## Regra resultante

`continuidade/` deve responder principalmente:

**"O que uma nova sessão precisa recuperar para continuar?"**

Não deve ser um segundo `docs/`.

`cerebro/00_estado/` responde:

**"Quais estados/snapshots do Cérebro foram registrados?"**

Project Knowledge responde:

**"O que o mecanismo consegue derivar/observar do repositório e das evidências?"**

## O que não foi feito

- nenhum código movido;
- nenhum teste movido;
- nenhuma fonte-base alterada;
- nenhum histórico apagado;
- nenhuma decisão do Imperador reinterpretada;
- nenhum snapshot transformado em estado atual.

## Próxima frente

Depois desta consolidação, a próxima auditoria deve ser:

**planejamento × mapas**

e somente depois:

**fontes × histórico × Mini-Cérebro × 99_arquivo**.

A organização continua seguindo:

**INVENTARIAR → CLASSIFICAR → DETERMINAR AUTORIDADE → REFERENCIAR → MIGRAR CONTROLADAMENTE → VALIDAR.**
