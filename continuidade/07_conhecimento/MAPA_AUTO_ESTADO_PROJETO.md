# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 45ff454cfe8ad1cf4e44b168f1d0a4b9fc66b0d9
Momento da revisão: 2026-09-24T00:08:04-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (47 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:186bfd1cc31a
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:186bfd1cc31a, evidence:test:5cca0f4ff6f4
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:186bfd1cc31a

## Eventos
- event:repository-scan:186bfd1cc31a — repository_scanned — revisão: 45ff454cfe8ad1cf4e44b168f1d0a4b9fc66b0d9
- event:commit-observed:45ff454cfe8a — commit_observed — revisão: 45ff454cfe8ad1cf4e44b168f1d0a4b9fc66b0d9
- event:test:5cca0f4ff6f4 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:186bfd1cc31a — repository_scan — observed — 309 files indexed at revision 45ff454cfe8ad1cf4e44b168f1d0a4b9fc66b0d9
- evidence:test:5cca0f4ff6f4 — test — tested — 101 passed in 6.55s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
