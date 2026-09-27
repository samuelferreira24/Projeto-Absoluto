# Experimento 07 — Sandbox contra runtime ABS

Objetivo: verificar se a família de moldes pode ficar acima das capacidades/recursos reais do ABS sem transformar o registry ou router em seletor estratégico.

Este experimento é isolado. Não altera abs_core e não executa ações externas.

Fluxo:
OBJETIVO → MOLDE → CAPACIDADE → RECURSO → EXECUTOR → RESULTADO

Os componentes reais usados são CapabilityRegistry e ResourceRouter. O executor é um adaptador sandbox determinístico.
