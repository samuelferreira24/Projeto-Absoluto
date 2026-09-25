# MAPA AUTOMÁTICO — ESTADO OBSERVÁVEL DO PROJETO

Gerado automaticamente; não substitui autoridade humana.

Revisão observada: 29ef2905299b997affa4faed53113bc0bb3b37a3
Momento da revisão: 2026-09-25T14:46:20-03:00

## Componentes
- component:abs_core — abs_core (46 arquivos)
- component:cerebro — cerebro (45 arquivos)
- component:continuity — continuity (18 arquivos)
- component:docs — docs (50 arquivos)
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
- PATH-ABS-ORCHESTRATOR — route an ABS work request through the operational core — estado: observed — evidências: evidence:repository:d5e0aacc96f0
- PATH-ABS-CODEX — execute code-engineering work through Codex adapter — estado: tested — evidências: evidence:repository:d5e0aacc96f0, evidence:test:7c666501bb50
- PATH-ABS-INTERNET-HTTP — execute an HTTP request through the Internet adapter — estado: observed — evidências: evidence:repository:d5e0aacc96f0

## Eventos
- event:repository-scan:d5e0aacc96f0 — repository_scanned — revisão: 29ef2905299b997affa4faed53113bc0bb3b37a3
- event:commit-observed:29ef2905299b — commit_observed — revisão: 29ef2905299b997affa4faed53113bc0bb3b37a3
- event:test:7c666501bb50 — tests_observed — revisão: n/a

## Evidências
- evidence:repository:d5e0aacc96f0 — repository_scan — observed — 315 files indexed at revision 29ef2905299b997affa4faed53113bc0bb3b37a3
- evidence:test:7c666501bb50 — test — tested — 101 passed in 6.33s

## Regra
Mudança observável → evento → conhecimento estruturado → evidência → reavaliação de caminhos → projeções.

Conteúdo autoritativo humano não é sobrescrito.
