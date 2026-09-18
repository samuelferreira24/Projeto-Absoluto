# Agendamento Adaptativo e Orquestração Dinâmica — V0.1

## Objetivo

Transformar o grafo de tarefas em um mecanismo capaz de escolher o que executar agora, respeitando dependências, recursos, orçamento, tempo, risco e experiência acumulada, e recalcular o plano quando o estado do sistema mudar.

A agenda não é uma rota fixa. É uma hipótese operacional que pode ser reavaliada.

## Fluxo

```
OBJETIVO
  ↓
DECOMPOSIÇÃO
  ↓
GRAFO DE TAREFAS
  ↓
TAREFAS PRONTAS
  ↓
AVALIAÇÃO DE VALOR / CUSTO / RISCO / TEMPO
  ↓
SELEÇÃO DE PLANO
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
APRENDIZADO
  ↓
REPLANEJAMENTO
  ↺
```

## Princípios

1. Dependências duras bloqueiam execução.
2. Recursos são restrições reais, não apenas metadados.
3. Tarefas independentes podem ser executadas em paralelo quando os recursos permitirem.
4. Paralelismo deve considerar capacidade do recurso e não somente conflito binário.
5. Orçamento pode impedir uma combinação mesmo quando ela possui alto valor.
6. Prazo e capacidade temporal alteram a seleção.
7. Risco e incerteza reduzem valor esperado, mas podem ser compensados por oportunidade ou valor de aprendizado.
8. Experiência real altera decisões futuras.
9. Falhas não são apagadas quando ocorre retry ou fallback.
10. Toda mudança relevante de plano deve preservar motivo e contexto.
11. Fallbacks são alternativas explícitas; não são substituição silenciosa da história.
12. O scheduler deve poder gerar alternativas antes de escolher uma.
13. O histórico das decisões é parte do conhecimento do Cérebro.

## Valor esperado

A pontuação atual usa uma aproximação:

```
valor_esperado =
(valor + oportunidade)
× (1 - risco)
× (1 - incerteza)
× confiabilidade_observada
```

O resultado é então ajustado por custo, tempo, urgência e comunicação conforme a estratégia escolhida.

Isso é deliberadamente uma função inicial e substituível. O objetivo da V0.1 é tornar os fatores explícitos para que o sistema possa aprender modelos melhores depois.

## Replanejamento

O replanejamento ocorre quando, por exemplo:

- uma tarefa termina;
- uma tarefa falha;
- um fallback é ativado;
- um retry é solicitado;
- um recurso fica disponível ou indisponível;
- uma estimativa de tempo muda;
- uma nova evidência muda a prioridade;
- uma combinação produz resultado inesperado;
- o objetivo ou orçamento muda.

O plano anterior permanece no histórico. O novo plano é uma nova decisão.

## Aprendizado do scheduler

O scheduler registra perfis observados por tarefa, incluindo:

- número de execuções;
- número de sucessos;
- confiabilidade observada;
- fator observado de tempo.

Esses dados podem alterar a seleção futura sem alterar retroativamente os registros históricos.

## Alternativas

O scheduler pode gerar planos candidatos usando diferentes objetivos:

- valor;
- eficiência;
- conclusão;
- rapidez;
- aprendizado.

As alternativas devem ser preservadas antes da seleção final. Isso permite que o Meta-Cérebro descubra posteriormente em quais contextos cada estratégia funciona melhor.

## Próxima evolução

A V0.1 ainda usa heurísticas determinísticas. Próximas camadas:

1. custo marginal;
2. valor da informação;
3. risco de bloqueio de caminho crítico;
4. dependências suaves e preferências;
5. seleção de motor/modelo/agente;
6. comunicação entre agentes;
7. simulação de cenários;
8. Pareto entre valor, tempo, custo e risco;
9. aprendizado de política de agendamento;
10. descoberta automática de novas combinações;
11. detecção de sinergia;
12. meta-aprendizado do próprio orquestrador.

## Regra de preservação

```
PLANO ANTERIOR ≠ PLANO ATUAL
```

O plano anterior continua sendo evidência histórica. O plano atual representa o melhor entendimento operacional disponível naquele momento.

A evolução do scheduler deve melhorar decisões futuras sem reescrever o passado.
