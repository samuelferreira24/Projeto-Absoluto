# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 1f329e166d048480e7396cee706fc3f0a82453a8
Momento da revisão: 2026-09-23T23:08:38-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (47 arquivos)
- component:continuity — continuity (23 arquivos)
- component:docs — docs (45 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:400f58e0d4f2
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:400f58e0d4f2, evidence:test:ec33f32c29ae
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:400f58e0d4f2

## Eventos
- event:repository-scan:400f58e0d4f2 — repository_scanned — revisão: 1f329e166d048480e7396cee706fc3f0a82453a8
- event:commit-observed:1f329e166d04 — commit_observed — revisão: 1f329e166d048480e7396cee706fc3f0a82453a8
- event:test:ec33f32c29ae — tests_observed — revisão: n/a

## Evidências
- evidence:repository:400f58e0d4f2 — repository_scan — observed — 313 files indexed at revision 1f329e166d048480e7396cee706fc3f0a82453a8
- evidence:test:ec33f32c29ae — test — tested — 101 passed in 6.34s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
