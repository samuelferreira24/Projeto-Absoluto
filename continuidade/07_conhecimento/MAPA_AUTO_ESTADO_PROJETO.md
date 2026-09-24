# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 5c7de8b64fc2cb8fe58dfd4c4e4c7c5f9b3e1454
Momento da revisão: 2026-09-24T00:37:33-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (45 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:8df69d7967a6
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:8df69d7967a6, evidence:test:d8db7f8011cf
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:8df69d7967a6

## Eventos
- event:repository-scan:8df69d7967a6 — repository_scanned — revisão: 5c7de8b64fc2cb8fe58dfd4c4e4c7c5f9b3e1454
- event:commit-observed:5c7de8b64fc2 — commit_observed — revisão: 5c7de8b64fc2cb8fe58dfd4c4e4c7c5f9b3e1454
- event:test:d8db7f8011cf — tests_observed — revisão: n/a

## Evidências
- evidence:repository:8df69d7967a6 — repository_scan — observed — 307 files indexed at revision 5c7de8b64fc2cb8fe58dfd4c4e4c7c5f9b3e1454
- evidence:test:d8db7f8011cf — test — tested — 101 passed in 6.31s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
