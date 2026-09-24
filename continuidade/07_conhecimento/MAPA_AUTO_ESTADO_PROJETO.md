# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: d248bad33754c087007d91759b5c52a647896022
Momento da revisão: 2026-09-24T00:41:26-03:00

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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:c2103e3d7617
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:c2103e3d7617, evidence:test:58658bd08cdd
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:c2103e3d7617

## Eventos
- event:repository-scan:c2103e3d7617 — repository_scanned — revisão: d248bad33754c087007d91759b5c52a647896022
- event:commit-observed:d248bad33754 — commit_observed — revisão: d248bad33754c087007d91759b5c52a647896022
- event:test:58658bd08cdd — tests_observed — revisão: n/a

## Evidências
- evidence:repository:c2103e3d7617 — repository_scan — observed — 307 files indexed at revision d248bad33754c087007d91759b5c52a647896022
- evidence:test:58658bd08cdd — test — tested — 101 passed in 6.29s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
