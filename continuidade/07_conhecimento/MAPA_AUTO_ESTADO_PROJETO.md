# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: f5a39de0a99d4efa69bd323066d0b1cef98199b6
Momento da revisão: 2026-09-24T00:36:48-03:00

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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:2c55edf396c4
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:2c55edf396c4, evidence:test:fec060a8f804
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:2c55edf396c4

## Eventos
- event:repository-scan:2c55edf396c4 — repository_scanned — revisão: f5a39de0a99d4efa69bd323066d0b1cef98199b6
- event:commit-observed:f5a39de0a99d — commit_observed — revisão: f5a39de0a99d4efa69bd323066d0b1cef98199b6
- event:test:fec060a8f804 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:2c55edf396c4 — repository_scan — observed — 307 files indexed at revision f5a39de0a99d4efa69bd323066d0b1cef98199b6
- evidence:test:fec060a8f804 — test — tested — 101 passed in 6.30s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
