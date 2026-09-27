# Experimento 08 — Persistência e recuperação

Objetivo: testar o contrato do protótipo contra a persistência real do ABS, sem modificar o núcleo.

Valida:
- objetivo persistido;
- contexto/identidade do plano persistido;
- resultado persistido;
- provenance persistida;
- reabertura do trabalho por novo WorkStore;
- recuperação de trabalho RUNNING para PAUSED após reinício.

Resultado pretendido: demonstrar que o molde pode ser tratado como plano/estado externo ao executor, aproveitando a continuidade já existente do ABS.

Limite: ainda não persiste uma máquina completa de composição de moldes; apenas valida a base real de WorkStore/Orchestrator que o futuro adaptador poderá utilizar.
