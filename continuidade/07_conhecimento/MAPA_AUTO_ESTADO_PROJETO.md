# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: c0bb4994753506b435ee148b7b12062e5b2e0e64
Momento da revisão: 2026-09-24T00:08:51-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (46 arquivos)
- component:continuity — continuity (18 arquivos)
- component:docs — docs (46 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:ece3c78690ba
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:ece3c78690ba, evidence:test:e9724c8a85e5
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:ece3c78690ba

## Eventos
- event:repository-scan:ece3c78690ba — repository_scanned — revisão: c0bb4994753506b435ee148b7b12062e5b2e0e64
- event:commit-observed:c0bb49947535 — commit_observed — revisão: c0bb4994753506b435ee148b7b12062e5b2e0e64
- event:test:e9724c8a85e5 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:ece3c78690ba — repository_scan — observed — 308 files indexed at revision c0bb4994753506b435ee148b7b12062e5b2e0e64
- evidence:test:e9724c8a85e5 — test — tested — 101 passed in 6.14s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
