# Persistência da Orquestração — V0.1

## Objetivo

A continuidade do Projeto Absoluto exige que o estado estrutural da orquestração sobreviva ao encerramento do processo.

A persistência desta camada cobre:

- tarefas e dependências;
- estados das tarefas;
- parâmetros relevantes de planejamento;
- resultados observados de combinações;
- memória de resultados usada para detectar sinergias.

O histórico do scheduler continua separado em seu próprio arquivo. Este snapshot não substitui o histórico: ele reconstrói o estado operacional atual.

## Separação de responsabilidades

```text
GRAFO DE TAREFAS
      ↓
estado operacional persistido
      ↓
SCHEDULER
      ↓
histórico de decisões
      ↓
MEMÓRIA DO CÉREBRO
      ↓
aprendizado consolidado

RESULTADOS DE COMBINAÇÕES
      ↓
MEMÓRIA DE SINERGIA
      ↓
novas combinações
```

A persistência não transforma sinergia em conhecimento definitivo. Resultado observado continua sendo evidência até ser avaliado e consolidado.

## Regras

1. Reabrir o Cérebro deve reconstruir o grafo antes de planejar novas tarefas.
2. Estados de tarefa não podem desaparecer entre sessões.
3. Resultados de combinações devem permanecer disponíveis para detectar sinergias futuras.
4. O snapshot é derivado e pode ser reconstruído; fontes de aprendizado permanecem intactas.
5. Mudanças estruturais continuam auditáveis pelo histórico do scheduler e pelo Git.
6. Alterações futuras do schema devem ser versionadas, nunca interpretadas silenciosamente como se fossem o schema atual.

## Limite V0.1

Ainda não existe armazenamento transacional nem concorrência multi-processo para esse snapshot. O próximo avanço deverá tratar escrita concorrente, recuperação após interrupção no meio da escrita, versionamento de snapshots e reconciliação com o histórico.
