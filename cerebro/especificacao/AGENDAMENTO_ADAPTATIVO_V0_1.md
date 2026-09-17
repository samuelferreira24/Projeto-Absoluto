# Agendamento Adaptativo V0.1

## Objetivo
Transformar o grafo de tarefas em uma camada de decisão operacional que escolha o próximo trabalho sem depender de uma rota fixa.

## Fluxo

```text
OBJETIVO
  ↓
DECOMPOSIÇÃO
  ↓
GRAFO DE TAREFAS
  ↓
TAREFAS PRONTAS
  ↓
AGENDAMENTO
  ├─ prioridade
  ├─ dependências
  ├─ recursos disponíveis
  ├─ conflitos de recurso
  └─ orçamento
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
REPLANEJAMENTO
  ↺
```

## Regras V0.1

1. Dependências bloqueiam tarefas até que sejam concluídas.
2. Recursos compartilhados impedem a seleção simultânea de tarefas conflitantes.
3. Prioridade influencia a seleção do próximo lote.
4. Um orçamento pode limitar o plano.
5. O plano é recalculado após resultados; não existe rota permanente.
6. O histórico dos planos permanece registrado para futura aprendizagem.
7. Falha de uma tarefa não apaga o grafo nem o histórico.
8. A camada é separada do executor: decidir e executar são responsabilidades distintas.

## Limitações conhecidas

Esta versão ainda não possui estimativa real de custo/tempo por tarefa, risco probabilístico, valor esperado, deadlines, custo de comunicação entre agentes, políticas de retry/fallback ou seleção dinâmica de motor/modelo. Esses elementos devem ser adicionados como evolução, sem quebrar a interface atual.

## Próxima evolução

Integrar orçamento de combustível, risco, valor marginal, seleção de capacidades/motores e aprendizado de estratégias de agendamento. O Meta-Cérebro deverá aprender quais políticas de composição produzem melhores resultados em cada contexto.
