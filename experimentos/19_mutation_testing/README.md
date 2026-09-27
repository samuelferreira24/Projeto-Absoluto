# Experimento 19 — Mutation Testing

Verifica se a bateria detecta mutações deliberadas em regras críticas dos protótipos.

Mutantes:
- precedência de RECOVERY removida;
- autorização deixa de bloquear;
- capacidade ausente deixa de bloquear;
- sucesso do executor passa a significar sucesso do objetivo.

Critério: cada mutação precisa ser detectada por uma expectativa independente.
