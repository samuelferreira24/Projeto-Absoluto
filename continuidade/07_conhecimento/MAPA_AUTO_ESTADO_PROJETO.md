# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: fb8cdc92655998cd9335e9df85fc71d58ce6363b
Momento da revisão: 2026-09-23T17:52:29-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (46 arquivos)
- component:continuity — continuity (20 arquivos)
- component:docs — docs (34 arquivos)
- component:historical_mini_cerebro — historical_mini_cerebro (12 arquivos)
- component:project — project (103 arquivos)
- component:tests — tests (41 arquivos)

## Capacidades
- capability:codex — Codex code engineering — estado: observed
- capability:internet-http — Internet HTTP — estado: observed
- capability:orchestrator — ABS orchestration — estado: observed

## Recursos
- resource:repository — Projeto-Absoluto — estado: observed

## Ferramentas
- tool:file:abs_core/bridge.py — abs_core/bridge.py — estado: present
- tool:file:abs_core/codex_adapter.py — abs_core/codex_adapter.py — estado: present
- tool:file:abs_core/tool_catalog.py — abs_core/tool_catalog.py — estado: present
- tool:file:abs_core/tool_discovery.py — abs_core/tool_discovery.py — estado: present
- tool:file:abs_core/tool_knowledge.py — abs_core/tool_knowledge.py — estado: present
- tool:file:abs_core/tool_knowledge_store.py — abs_core/tool_knowledge_store.py — estado: present
- tool:file:abs_core/tool_learning.py — abs_core/tool_learning.py — estado: present
- tool:file:abs_core/tool_planner.py — abs_core/tool_planner.py — estado: present

## Nós

## Caminhos
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:24989a0fa69e
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:24989a0fa69e, evidence:test:cdf4df78d8ab
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:24989a0fa69e

## Eventos
- event:repository-scan:24989a0fa69e — repository_scanned — revisão: fb8cdc92655998cd9335e9df85fc71d58ce6363b
- event:commit-observed:fb8cdc926559 — commit_observed — revisão: fb8cdc92655998cd9335e9df85fc71d58ce6363b
- event:test:cdf4df78d8ab — tests_observed — revisão: n/a

## Evidências
- evidence:repository:24989a0fa69e — repository_scan — observed — 298 files indexed at revision fb8cdc92655998cd9335e9df85fc71d58ce6363b
- evidence:test:cdf4df78d8ab — test — tested — 101 passed in 7.07s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
