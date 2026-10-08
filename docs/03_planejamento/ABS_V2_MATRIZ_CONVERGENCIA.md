# ABS V2 — MATRIZ DE CONVERGÊNCIA PRÉ-CONSTRUÇÃO

**Baseline auditado:** `main @ dee0b582249b22b0549e3994e982a36298c15e2a`  
**Objetivo:** decidir o destino das peças antes de qualquer refatoração estrutural.

## Legenda

- **MANTER:** já atende ao papel; integrar/refinar sem substituir.
- **CONSOLIDAR:** existe, mas deve ganhar contrato/posição mais clara.
- **ADAPTAR:** manter a capacidade, mudar a fronteira.
- **INCORPORAR EXTERNO:** usar implementação madura por trás do contrato ABS.
- **AVALIAR:** só incorporar depois de prova de necessidade.
- **RETIRAR:** somente após substituição + testes.
- **NOVO:** responsabilidade ainda não suficientemente materializada.

## 1. Núcleo atual

| Responsabilidade V2 | Estado V1 observado | Decisão | Destino |
|---|---|---|---|
| Work | Work/modelos/store já existem | CONSOLIDAR | unidade soberana de missão/execução |
| Estados | WorkState e transições existem | CONSOLIDAR | ampliar para lifecycle V2 sem quebrar V1 |
| Eventos | emit/persistência já existem | CONSOLIDAR | event ledger/auditoria |
| Orchestrator | existe e executa capability | ADAPTAR | executor do ciclo, não dono de toda a arquitetura |
| Capability Registry | existe | MANTER/CONSOLIDAR | catálogo soberano de capacidades |
| Intelligence Registry | existe | ADAPTAR | registrar recursos cognitivos/executores, sem autoridade |
| Agent Registry | existe | MANTER/CONSOLIDAR | identidade ≠ autoridade |
| Connections | existe | MANTER/CONSOLIDAR | acesso a recursos |
| Resource Router | existe | CONSOLIDAR | seleção de recurso |
| Resource Dispatcher | existe | ADAPTAR | execução via rota, sempre sob Work/policy |
| Tool Discovery | existe | MANTER/CONSOLIDAR | descoberta ≠ confiança |
| Tool Knowledge | existe | MANTER/CONSOLIDAR | conhecimento operacional baseado em evidência |
| Tool Planner | existe | ADAPTAR | planejamento de ferramentas subordinado ao Strategy/Mode |
| Tool Learning | existe | MANTER/CONSOLIDAR | aprender apenas de resultado/evidência |
| Verification | existe | ADAPTAR | sair de checks genéricos para verificação proporcional ao risco |
| Provenance | existe no Work | CONSOLIDAR | evidência/proveniência soberana |
| Conflicts | existe | CONSOLIDAR | detector não decide verdade sozinho |
| Idempotency | existe, hoje em memória | ADAPTAR | ledger durável para efeitos relevantes |
| Continuity | existe | CONSOLIDAR | recovery/checkpoint |
| Data Layer | existe | CONSOLIDAR | separar estado operacional de conhecimento/evidência |
| Cognitive Context | existe | CONSOLIDAR | Context Engine |
| Cognitive Runtime | existe na camada de inteligência | ADAPTAR | runtime cognitivo, não autoridade |
| API/interface runtime | existe | MANTER/ADAPTAR | superfície de acesso, não núcleo |
| Update/Rollback | existe | MANTER | mecanismo operacional da infraestrutura |
| GitHub Bridge | existe | MANTER COMO ADAPTADOR | executor/infra externa |
| Codex adapter | existe | MANTER COMO EXECUTOR | capacidade especializada substituível |

## 2. Lacunas arquiteturais

| Responsabilidade | Situação | Decisão |
|---|---|---|
| Authority Core explícito | princípio existe, mas está distribuído | NOVO/CONSOLIDAR |
| Policy Engine | aprovação existe, política ainda distribuída | NOVO |
| Objective Interpreter | parcialmente implícito no runtime/orchestrator | NOVO |
| Strategy Engine | planner existe, estratégia global não | NOVO |
| Mode/Architecture Selector | ainda não é uma fronteira explícita | NOVO |
| Budget/Risk Governor | não suficientemente materializado | NOVO |
| Evidence Ledger | evidência existe dispersa | NOVO/CONSOLIDAR |
| Observation layer | ainda misturada ao resultado | NOVO |
| Replanner | fallback existe, replanejamento geral não | NOVO |
| Recovery policy | continuidade existe, política V2 ainda não | CONSOLIDAR |
| Autonomy controller | aprovação existe, autonomia contextual não | NOVO |
| Admission control | necessário para multiagente/recursão | NOVO |
| Durable idempotency | V1 é memória | ADAPTAR |
| Typed handoffs | ainda não são contrato central | NOVO |
| Executor Router | partes existem em Resource Router/Dispatcher | CONSOLIDAR |
| External protocol boundary | MCP/A2A ainda não são contratos centrais | NOVO/ADAPTAR |

## 3. Peças externas

| Sistema | Papel | Decisão V2 |
|---|---|---|
| OpenClaw | executor de agente/operador | **INCORPORAR COMO EXECUTOR** |
| MCP | tools/resources/prompts interoperability | **INCORPORAR COMO PROTOCOLO** |
| A2A | agent-to-agent interoperability | **INCORPORAR COMO PROTOCOLO** |
| OpenAI Agents SDK | executor agentic opcional | **ADAPTADOR OPCIONAL** |
| Microsoft Agent Framework | executor/workflow opcional | **ADAPTADOR OPCIONAL** |
| Temporal | durable execution | **AVALIAR QUANDO CONTRATO DE DURABILIDADE ESTIVER FECHADO** |
| LangGraph | runtime de graph/agent | **NÃO BASE; opcional futuro** |
| Codex | executor de engenharia | **MANTER** |

## 4. O que será reaproveitado do OpenClaw

Não vamos importar o OpenClaw inteiro.

As peças de maior interesse são:

1. gateway/control plane do executor;
2. sessões;
3. tool execution;
4. shell;
5. filesystem;
6. browser;
7. nodes;
8. tool policy;
9. exec approvals;
10. sandbox;
11. plugins/integrations;
12. agent execution/sub-agents quando necessários.

O contrato será:

`ABS Work/Policy → Executor Adapter → OpenClaw → ferramentas → observações`

OpenClaw nunca será o dono do Work soberano.

## 5. O que não será duplicado

Se uma responsabilidade já tiver implementação madura e compatível, não será recriada apenas para "ser própria".

Especialmente:

- execução de agente;
- sandbox;
- protocolos de interoperabilidade;
- durable execution;
- integrações externas.

O ABS preserva o **contrato e a autoridade**, não precisa possuir cada linha de implementação.

## 6. Primeira estimativa de composição

Não tratar como contagem final de arquivos.

### Peças internas V1 reaproveitáveis diretamente ou com pequena adaptação
**~20 responsabilidades** já possuem material implementado.

### Peças internas que exigem consolidação/refatoração
**~12 responsabilidades**.

### Responsabilidades V2 novas ou ainda insuficientemente materializadas
**~12–15**.

### Sistemas externos principais
**7 candidatos**, mas somente 3 entram como infraestrutura conceitualmente prioritária desde o início:

- OpenClaw;
- MCP;
- A2A.

Agents SDK, Agent Framework, Temporal, LangGraph e outros entram somente quando uma necessidade concreta justificar.

Portanto, a arquitetura não será uma colcha de retalhos de dezenas de frameworks.

## 7. Ordem de migração

### Fase A — contratos
- Work;
- State;
- Authority;
- Policy;
- Capability;
- Resource;
- Executor;
- Observation;
- Evidence;
- Verification.

### Fase B — controle
- Objective Interpreter;
- Strategy;
- Mode Selector;
- Risk/Budget;
- Executor Router.

### Fase C — execução
- adaptar Orchestrator;
- adaptar Resource Dispatcher;
- conectar OpenClaw;
- manter Codex;
- criar adapters externos.

### Fase D — confiabilidade
- Evidence Ledger;
- durable idempotency;
- checkpoint/recovery;
- replanning;
- conflict handling;
- admission control.

### Fase E — interoperabilidade
- MCP;
- A2A;
- demais executores somente quando necessários.

### Fase F — limpeza
- remover duplicações;
- retirar código antigo somente após testes;
- manter rollback.

## 8. Testes que devem existir antes da remoção de qualquer peça

- direct path;
- workflow path;
- agent path;
- multiagent admission;
- approval;
- denied action;
- unknown result;
- failed verification;
- executor substitution;
- executor unavailable;
- retry;
- duplicate retry;
- conflict;
- concurrent Work;
- partial success;
- checkpoint/recovery;
- budget exhaustion;
- risk escalation;
- prompt/tool injection;
- stale memory;
- malicious executor;
- protocol/schema mismatch;
- degraded mode.

## 9. Critério de substituição

Nenhuma peça V1 será removida porque "a V2 tem algo melhor".

Para retirar uma peça:

`novo contrato → implementação substituta → testes equivalentes → testes de regressão → prova operacional → remoção`

Se a prova não existir, a peça antiga permanece.

## 10. Conclusão da matriz

A V1 não deve ser jogada fora.

A estratégia correta é:

`V1 operacional → contratos V2 → integração → migração progressiva → V1 reduzida → V2 consolidada`

O maior ganho esperado não é simplesmente adicionar mais agentes.

É transformar as capacidades já existentes em um sistema coerente de:

`objetivo → estratégia → modo → capacidade → recurso → executor → observação → verificação → evidência → estado → replanejamento`

Esse é o eixo de engenharia da V2.
