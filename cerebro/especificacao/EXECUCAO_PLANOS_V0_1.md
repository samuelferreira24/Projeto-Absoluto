# EXECUÇÃO DE PLANOS V0.1

## Objetivo

Criar uma fronteira explícita entre a decisão de orquestração e a execução real de tarefas.

## Princípio

```
OBJETIVO
  ↓
GRAFO
  ↓
SCHEDULER
  ↓
PLANO
  ↓
CLAIM / AUTORIZAÇÃO
  ↓
EXECUTOR
  ↓
RESULTADO
  ↓
APRENDIZADO
  ↓
REPLANEJAMENTO
```

O scheduler decide **o que** deve ser executado sob as restrições conhecidas. O executor decide **como** uma tarefa autorizada será realizada. A camada de controle impede dispatch duplicado e registra o estado recuperável.

## Separações obrigatórias

- conhecimento não executa;
- memória preserva;
- pesquisa produz evidência;
- experiência registra episódios;
- aprendizado abstrai resultados;
- sabedoria generaliza princípios;
- orquestração decide planos;
- execução realiza ações;
- recursos/fuel limitam o que pode ser realizado;
- capacidades/motores fornecem meios de execução.

## V0.1

A ponte mínima é `cerebro/execucao_plano.py`.

Ela:

1. recebe um `PlanoExecucao`;
2. exige um handler explícito para cada tarefa;
3. cria claim persistente antes da execução;
4. passa a ação pela política de execução;
5. executa o handler;
6. registra sucesso/falha no scheduler;
7. conclui ou falha o claim;
8. deixa histórico disponível para replanejamento;
9. registra aprendizado sobre a execução.

## Segurança

A ponte não concede autorização por si mesma. Ela herda os limites de `PoliticaExecucao` e pode receber `ControleAgente` por meio do `ExecutorCerebro`.

A pesquisa atual reforça que segurança deve verificar alinhamento da tarefa, alinhamento da ação, autorização da fonte e isolamento de dados, e que workflows duráveis precisam tratar retries e idempotência explicitamente. 

## Limitações atuais

- V0.1 executa as tarefas do plano em sequência mesmo quando o plano foi classificado como paralelo.
- A execução paralela real será implementada somente após definir semântica de cancelamento, falha parcial, concorrência por recurso e tolerância de falhas.
- Handlers ainda são fornecidos pelo chamador; não existe descoberta automática de executores.
- Claims são locais ao runtime/repositório e usam lock de processo/sistema de arquivos.
- Sandbox forte e isolamento de rede continuam pendentes.

## Próxima evolução

Implementar um dispatcher de lotes que respeite:

- `modo_execucao`;
- capacidade de concorrência;
- recursos compartilhados;
- falhas parciais;
- retry por tarefa;
- cancelamento;
- idempotência;
- checkpoint;
- replanejamento após cada lote.

Depois disso, avaliar isolamento semântico do plano e do ambiente de execução antes de ampliar autonomia.
