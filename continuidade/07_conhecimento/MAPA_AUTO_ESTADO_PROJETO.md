# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: d11da20f827732b956aaf934e5a9567edd53152e
Momento da revisão: 2026-09-26T11:49:12-03:00

## Componentes
- component:abs_core — abs_core (47 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (18 arquivos)
- component:docs — docs (52 arquivos)
- component:historical_mini_cerebro — historical_mini_cerebro (12 arquivos)
- component:project — project (105 arquivos)
- component:tests — tests (43 arquivos)

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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:4001805eccf1
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:4001805eccf1, evidence:test:649802aa819f
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:4001805eccf1

## Eventos
- event:repository-scan:4001805eccf1 — repository_scanned — revisão: d11da20f827732b956aaf934e5a9567edd53152e
- event:commit-observed:d11da20f8277 — commit_observed — revisão: d11da20f827732b956aaf934e5a9567edd53152e
- event:test:649802aa819f — tests_observed — revisão: n/a

## Evidências
- evidence:repository:4001805eccf1 — repository_scan — observed — 322 files indexed at revision d11da20f827732b956aaf934e5a9567edd53152e
- evidence:test:649802aa819f — test — tested — 105 passed in 6.35s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
