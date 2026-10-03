# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: dc686f309a31b8fdf571508d9f1482eedf98907b
Momento da revisão: 2026-10-03T15:15:34-03:00

## Componentes
- component:abs_core — abs_core (49 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (19 arquivos)
- component:docs — docs (54 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:8003d980acea
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:8003d980acea, evidence:test:828bcf564c74
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:8003d980acea

## Eventos
- event:repository-scan:8003d980acea — repository_scanned — revisão: dc686f309a31b8fdf571508d9f1482eedf98907b
- event:commit-observed:dc686f309a31 — commit_observed — revisão: dc686f309a31b8fdf571508d9f1482eedf98907b
- event:test:828bcf564c74 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:8003d980acea — repository_scan — observed — 330 files indexed at revision dc686f309a31b8fdf571508d9f1482eedf98907b
- evidence:test:828bcf564c74 — test — tested — 113 passed in 6.20s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
