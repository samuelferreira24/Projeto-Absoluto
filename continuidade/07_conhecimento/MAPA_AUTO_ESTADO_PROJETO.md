# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 8c32e9f6c7d4c6a4c26275493297c7c3aa423f13
Momento da revisão: 2026-09-23T18:01:48-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (46 arquivos)
- component:continuity — continuity (20 arquivos)
- component:docs — docs (35 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:0749f8d81686
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:0749f8d81686, evidence:test:4e361f8ba842
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:0749f8d81686

## Eventos
- event:repository-scan:0749f8d81686 — repository_scanned — revisão: 8c32e9f6c7d4c6a4c26275493297c7c3aa423f13
- event:commit-observed:8c32e9f6c7d4 — commit_observed — revisão: 8c32e9f6c7d4c6a4c26275493297c7c3aa423f13
- event:test:4e361f8ba842 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:0749f8d81686 — repository_scan — observed — 299 files indexed at revision 8c32e9f6c7d4c6a4c26275493297c7c3aa423f13
- evidence:test:4e361f8ba842 — test — tested — 101 passed in 6.37s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
