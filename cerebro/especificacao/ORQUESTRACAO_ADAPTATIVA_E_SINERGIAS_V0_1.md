# Orquestração Adaptativa e Sinergias — V0.1

## Objetivo

Transformar o grafo de tarefas em uma camada de decisão adaptativa capaz de escolher o que executar, em que ordem, com quais recursos e quando replanejar, preservando o histórico das decisões.

## Princípios

1. Dependências determinam o que é possível; prioridade e valor ajudam a decidir o que é conveniente.
2. Recursos compartilhados limitam paralelismo.
3. Custo, tempo, risco, prazo e valor devem ser considerados conjuntamente.
4. O resultado de uma execução pode alterar o próximo plano.
5. Replanejamento não apaga o plano anterior: registra uma nova decisão.
6. Falhas permanecem como experiência e podem gerar retry ou fallback.
7. Combinações de capacidades devem ser testadas e medidas, não presumidas como sinérgicas.
8. Ganhos repetidos de uma combinação devem poder virar conhecimento reutilizável.

## Ciclo

```text
OBJETIVO
  ↓
DECOMPOSIÇÃO
  ↓
GRAFO DE TAREFAS
  ↓
SCHEDULER
  ├─ dependências
  ├─ recursos
  ├─ custo
  ├─ valor
  ├─ risco
  ├─ prazo
  └─ paralelismo
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
REPLANEJAMENTO
  ↓
REGISTRO DA EXPERIÊNCIA
  ↓
DETECÇÃO DE SINERGIA
  ↓
CONSOLIDAÇÃO
  ↺
```

## Sinergia

Uma combinação é candidata a sinergia quando apresenta ganho relativo sobre referências individuais comparáveis. O ganho não é tratado como prova definitiva: a confiança cresce com a quantidade de evidências e o resultado deve permanecer associado ao contexto.

## Evolução futura

- dependências rígidas e preferências suaves;
- orçamento por recurso/fuel;
- deadlines reais e janelas temporais;
- seleção dinâmica de motor/modelo/agente;
- custo de comunicação;
- retry, fallback e cancelamento;
- execução contínua com eventos;
- aprendizado de políticas de agendamento;
- descoberta de novas capacidades emergentes;
- Meta-Cérebro para aprender a própria orquestração.
