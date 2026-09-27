# Experimento 05 — Varredura combinatória

Foram combinadas oito condições booleanas relevantes para produzir 256 estados de contexto.

O objetivo não é provar optimalidade. O objetivo é procurar violações sistemáticas de invariantes:

- recuperação tem precedência sobre execução normal;
- autorização pendente não vira execução;
- capacidade ausente entra em descoberta;
- contexto incompleto não vira execução cega;
- moldes proibidos não aparecem;
- orçamento de complexidade não é ultrapassado.

Também foram testados 20 cenários de orçamento máximo de complexidade.

A varredura é um teste de consistência, não uma prova de que o seletor encontrou a estratégia semanticamente perfeita para cada combinação.
