# Agendamento Adaptativo V0.1

## Objetivo

Transformar o grafo de tarefas em um mecanismo de decisão operacional capaz de escolher dinamicamente o próximo trabalho considerando valor, custo, risco, tempo, dependências e recursos.

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
PONTUAÇÃO ADAPTATIVA
  ├─ valor esperado
  ├─ prioridade
  ├─ custo
  ├─ risco
  └─ urgência/prazo
  ↓
SELEÇÃO DO LOTE
  ├─ orçamento
  ├─ limite
  └─ conflitos de recursos
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
3. Valor e prioridade orientam a seleção; risco e custo reduzem a pontuação.
4. Um orçamento pode limitar o consumo planejado.
5. O plano é recalculado após resultados; não existe rota permanente.
6. O histórico dos planos, resultados e replanejamentos permanece registrado para futura aprendizagem.
7. Falha de uma tarefa não apaga o grafo nem o histórico.
8. A camada é separada do executor: decidir e executar são responsabilidades distintas.
9. O agendador pode selecionar tarefas independentes para execução paralela quando os recursos não entram em conflito.

## Dados adicionais da tarefa

`NoTarefa` suporta:
- `valor_estimado`
- `custo_estimado`
- `tempo_estimado`
- `risco`
- `prazo`
- `preferencias`

## Próxima evolução

Integrar orçamento de combustível real, capacidade quantitativa dos recursos, deadlines temporais, custo de comunicação, retry/fallback/cancelamento, seleção dinâmica de motor/modelo/capacidade, medição de resultados e detecção de sinergias.

```text
AGENDADOR
   ↓
ESCOLHA DE MOTOR / AGENTE / FERRAMENTA
   ↓
ALOCAÇÃO DE FUEL
   ↓
EXECUÇÃO
   ↓
MEDIÇÃO
   ↓
DETECÇÃO DE SINERGIA
   ↓
MEMÓRIA DE EXPERIÊNCIA
   ↓
META-CÉREBRO
   ↓
MELHOR AGENDAMENTO FUTURO
```
