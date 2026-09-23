# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 3e8187466a988e4559adc380ff3c5a27a2c26dc7
Momento da revisão: 2026-09-23T18:54:53-03:00

## Componentes
- component:abs_core — abs_core (42 arquivos)
- component:cerebro — cerebro (46 arquivos)
- component:continuity — continuity (20 arquivos)
- component:docs — docs (39 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:005149ddc392
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:005149ddc392, evidence:test:6d83cbb42ba7
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:005149ddc392

## Eventos
- event:repository-scan:005149ddc392 — repository_scanned — revisão: 3e8187466a988e4559adc380ff3c5a27a2c26dc7
- event:commit-observed:3e8187466a98 — commit_observed — revisão: 3e8187466a988e4559adc380ff3c5a27a2c26dc7
- event:test:6d83cbb42ba7 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:005149ddc392 — repository_scan — observed — 303 files indexed at revision 3e8187466a988e4559adc380ff3c5a27a2c26dc7
- evidence:test:6d83cbb42ba7 — test — tested — 101 passed in 6.29s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
