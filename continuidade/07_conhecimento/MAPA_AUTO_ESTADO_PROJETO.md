# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: eefb3adbc29761bc331cbe0d637a82278321a0e9
Momento da revisão: 2026-09-26T14:49:12-03:00

## Componentes
- component:abs_core — abs_core (49 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (18 arquivos)
- component:docs — docs (53 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:5c978ff56dde
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:5c978ff56dde, evidence:test:b78668ae9cbd
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:5c978ff56dde

## Eventos
- event:repository-scan:5c978ff56dde — repository_scanned — revisão: eefb3adbc29761bc331cbe0d637a82278321a0e9
- event:commit-observed:eefb3adbc297 — commit_observed — revisão: eefb3adbc29761bc331cbe0d637a82278321a0e9
- event:test:b78668ae9cbd — tests_observed — revisão: n/a

## Evidências
- evidence:repository:5c978ff56dde — repository_scan — observed — 328 files indexed at revision eefb3adbc29761bc331cbe0d637a82278321a0e9
- evidence:test:b78668ae9cbd — test — tested — 113 passed in 6.36s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
