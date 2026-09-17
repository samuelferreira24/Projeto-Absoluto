# Agendamento Adaptativo V0.2

## Objetivo

O Cérebro não deve apenas escolher uma sequência de tarefas. Deve aprender com a execução e usar essa experiência para melhorar os próximos planos.

## Fluxo

```text
OBJETIVO
  ↓
GRAFO DE TAREFAS
  ↓
TAREFAS PRONTAS
  ↓
PONTUAÇÃO MARGINAL
  ├─ valor
  ├─ custo
  ├─ risco
  ├─ prazo
  ├─ recursos
  └─ experiência observada
  ↓
PLANO
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ├─ sucesso/falha
  ├─ custo real
  ├─ tempo real
  └─ qualidade
  ↓
PERFIL DE EXPERIÊNCIA
  ↓
REPLANEJAMENTO
  ↺
```

## O que mudou

O `AgendadorAdaptativo` passou a manter, por tarefa, um perfil de experiência contendo execuções, sucessos, confiabilidade observada e fator de tempo observado.

A pontuação futura utiliza esse perfil. Uma tarefa que repetidamente falha perde prioridade relativa; uma tarefa cujo tempo real fica acima do estimado passa a carregar essa informação nos próximos planos.

O histórico continua preservado. Aprender não apaga a decisão anterior.

## Princípios

1. Planejamento é uma hipótese, não uma ordem imutável.
2. Resultados alteram o planejamento seguinte.
3. Falhas são dados de aprendizagem, não motivo para apagar a tarefa.
4. Retry preserva a ocorrência da falha e registra a nova tentativa.
5. Custo e tempo reais devem poder corrigir estimativas futuras.
6. O agendador deve preferir decisões que aumentem valor esperado sob os recursos disponíveis.
7. Paralelismo continua limitado por dependências e conflitos de recursos.
8. O histórico explica por que o plano mudou.
9. A experiência do agendamento deve futuramente alimentar a memória permanente do Cérebro.
10. A camada futura de Meta-Cérebro poderá aprender estratégias de orquestração além dos parâmetros fixos desta versão.

## Limitações deliberadas da V0.2

Ainda não há, nesta camada, aprendizado global entre tarefas semanticamente equivalentes, previsão de caminho crítico, capacidade quantitativa de recursos, custo de comunicação entre agentes, descoberta automática de novas topologias ou otimização multiobjetivo completa.

Esses pontos permanecem como próximas frentes de evolução e não devem ser tratados como resolvidos.
