# Experimento 09 — Composição, ordem e verificação

Este experimento ataca duas fragilidades identificadas na bateria anterior.

1. Uma lista de moldes precisa carregar ordem mínima de execução para composições como RESEARCH → MULTIAGENT e WORKFLOW → AGENT.
2. Resultado do executor não equivale automaticamente a objetivo atingido.

O teste usa um executor sandbox e uma verificação explícita de goal_achieved.

Resultado:
- composição ordenada;
- replanejamento após mudança de contexto;
- sucesso falso não encerra a missão.

Conclusão provisória: o contrato do futuro protótipo precisa separar ExecutionResult de GoalVerification.
