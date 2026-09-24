# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 421f3c08304a7ac1c8e155292962c23763eaec7e
Momento da revisão: 2026-09-23T23:05:52-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (46 arquivos)
- component:continuity — continuity (20 arquivos)
- component:docs — docs (41 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:c412e74abec0
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:c412e74abec0, evidence:test:14a1bd14438f
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:c412e74abec0

## Eventos
- event:repository-scan:c412e74abec0 — repository_scanned — revisão: 421f3c08304a7ac1c8e155292962c23763eaec7e
- event:commit-observed:421f3c08304a — commit_observed — revisão: 421f3c08304a7ac1c8e155292962c23763eaec7e
- event:test:14a1bd14438f — tests_observed — revisão: n/a

## Evidências
- evidence:repository:c412e74abec0 — repository_scan — observed — 305 files indexed at revision 421f3c08304a7ac1c8e155292962c23763eaec7e
- evidence:test:14a1bd14438f — test — tested — 101 passed in 5.80s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
