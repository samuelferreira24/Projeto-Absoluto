# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 876eb68ded069d4cc5d3c776f0ecb4290a18aa61
Momento da revisão: 2026-09-25T14:47:13-03:00

## Componentes
- component:abs_core — abs_core (46 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (18 arquivos)
- component:docs — docs (51 arquivos)
- component:historical_mini_cerebro — historical_mini_cerebro (12 arquivos)
- component:project — project (104 arquivos)
- component:tests — tests (42 arquivos)

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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:6bd60e1fae1a
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:6bd60e1fae1a, evidence:test:6be8b3d6f30f
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:6bd60e1fae1a

## Eventos
- event:repository-scan:6bd60e1fae1a — repository_scanned — revisão: 876eb68ded069d4cc5d3c776f0ecb4290a18aa61
- event:commit-observed:876eb68ded06 — commit_observed — revisão: 876eb68ded069d4cc5d3c776f0ecb4290a18aa61
- event:test:6be8b3d6f30f — tests_observed — revisão: n/a

## Evidências
- evidence:repository:6bd60e1fae1a — repository_scan — observed — 318 files indexed at revision 876eb68ded069d4cc5d3c776f0ecb4290a18aa61
- evidence:test:6be8b3d6f30f — test — tested — 103 passed in 6.33s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
