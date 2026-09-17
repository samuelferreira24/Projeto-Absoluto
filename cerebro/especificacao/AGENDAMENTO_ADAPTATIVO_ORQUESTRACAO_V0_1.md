# Agendamento Adaptativo e Orquestração V0.1

## Objetivo

Transformar o grafo de tarefas em uma capacidade de decisão dinâmica: escolher o próximo conjunto de tarefas considerando valor esperado, prioridade, custo, risco, tempo, recursos e dependências, e recalcular o plano quando o estado real mudar.

## Princípios

1. Planejamento é hipótese, não compromisso imutável.
2. Dependências fortes bloqueiam execução; resultados liberam novas tarefas.
3. Recursos compartilhados impedem paralelismo incompatível.
4. Orçamento limita consumo de recursos econômicos.
5. Valor deve ser considerado em relação a custo e risco.
6. Falhas não apagam o histórico; geram informação para replanejamento.
7. O histórico registra por que uma decisão foi tomada e quando o plano mudou.
8. O agendador deve poder escolher alternativas futuras sem apagar o caminho anterior.

## Ciclo

```text
OBJETIVO
  ↓
GRAFO DE TAREFAS
  ↓
VALIDAÇÃO
  ↓
CANDIDATAS PRONTAS
  ↓
PONTUAÇÃO
  ↓
RECURSOS + ORÇAMENTO
  ↓
PLANO
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
REPLANEJAMENTO
  ↺
```

## Critério inicial

A pontuação V0.1 usa uma aproximação de valor marginal:

```text
pontuação = valor × urgência × (1 − risco) / custo
```

Quando não há valor explícito, a prioridade funciona como aproximação. O custo zero recebe custo unitário para evitar divisão por zero.

## Evolução prevista

- distinguir dependências fortes de preferências suaves;
- representar capacidade e demanda de recursos;
- tratar deadlines temporais explicitamente;
- estimar ganho marginal e custo de oportunidade;
- registrar tentativas, falhas, retry e fallback;
- aprender quais estratégias de agendamento funcionam em cada contexto;
- detectar sinergias entre capacidades executadas em combinação;
- alimentar a memória de experiências e o Meta-Cérebro;
- otimizar a própria política de orquestração.

## Preservação

Cada replanejamento é registrado como evento. O novo plano não substitui silenciosamente os planos anteriores. Assim, o Cérebro pode aprender não apenas o que foi executado, mas também por que uma determinada rota foi escolhida ou abandonada.
