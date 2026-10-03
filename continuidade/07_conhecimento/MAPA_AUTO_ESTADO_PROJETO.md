# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: a4c6c156ab2199154ae077132b7fbb0de3238241
Momento da revisão: 2026-10-03T15:28:41-03:00

## Camadas de continuidade
- source:vision — vision_principles — continuidade/01_contexto/01_MODELO_ABS_E_PRINCIPIOS.md — present — autoridade: human_authority — temporalidade: current
- source:decisions — decisions — continuidade/03_decisoes/01_DECISOES_CORRECOES_E_REGRAS.md — present — autoridade: human_authority — temporalidade: current
- source:research — research — docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md — present — autoridade: research_reference — temporalidade: current
- source:evidence — evidence_contract — continuidade/07_conhecimento/03_CONTRATO_DE_PROVA.md — present — autoridade: project_governance — temporalidade: current
- source:state — derived_state — continuidade/07_conhecimento/project_knowledge.json — present — autoridade: derived_observation — temporalidade: current
- source:session — session_state — continuidade/07_conhecimento/SESSAO_ATUAL.md — present — autoridade: continuity — temporalidade: current
- source:handoff — handoff — continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md — present — autoridade: continuity — temporalidade: current
- source:navigation — navigation — 00_IA_NAVEGACAO.md — present — autoridade: project_governance — temporalidade: current
- source:history — history_archive — 99_arquivo/README.md — present — autoridade: historical_archive — temporalidade: historical

## Componentes
- component:abs_core — abs_core (49 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (19 arquivos)
- component:docs — docs (55 arquivos)
- component:historical_mini_cerebro — historical_mini_cerebro (12 arquivos)
- component:project — project (105 arquivos)
- component:tests — tests (46 arquivos)

## Capacidades
- capability:codex — Codex code engineering — estado: observed
- capability:internet-http — Internet HTTP — estado: observed
- capability:orchestrator — ABS orchestration — estado: observed

## Recursos
- resource:repository — Projeto-Absoluto — estado: observed

## Ferramentas
- tool:file:abs_core/bridge.py — abs_core/bridge.py — estado: present
- tool:file:abs_core/codex_adapter.py — abs_core/codex_adapter.py — estado: present
- tool:file:abs_core/github_adapter.py — abs_core/github_adapter.py — estado: present
- tool:file:abs_core/tool_catalog.py — abs_core/tool_catalog.py — estado: present
- tool:file:abs_core/tool_discovery.py — abs_core/tool_discovery.py — estado: present
- tool:file:abs_core/tool_knowledge.py — abs_core/tool_knowledge.py — estado: present
- tool:file:abs_core/tool_knowledge_store.py — abs_core/tool_knowledge_store.py — estado: present
- tool:file:abs_core/tool_learning.py — abs_core/tool_learning.py — estado: present
- tool:file:abs_core/tool_planner.py — abs_core/tool_planner.py — estado: present

## Nós

## Caminhos
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:11a1a781e9b5
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:11a1a781e9b5, evidence:test:01acc21a3a66
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:11a1a781e9b5

## Eventos
- event:repository-scan:11a1a781e9b5 — repository_scanned — revisão: a4c6c156ab2199154ae077132b7fbb0de3238241
- event:commit-observed:a4c6c156ab21 — commit_observed — revisão: a4c6c156ab2199154ae077132b7fbb0de3238241
- event:test:01acc21a3a66 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:11a1a781e9b5 — repository_scan — observed — 331 files indexed at revision a4c6c156ab2199154ae077132b7fbb0de3238241
- evidence:test:01acc21a3a66 — test — tested — 115 passed in 6.51s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
