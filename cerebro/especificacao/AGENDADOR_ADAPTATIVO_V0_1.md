# Agendador Adaptativo — V0.1

## Objetivo

Transformar o grafo de tarefas em uma capacidade de planejamento adaptativo: selecionar o próximo trabalho considerando dependências, prioridade, conflitos de recursos e orçamento, e permitir replanejamento depois de cada resultado.

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
AGENDADOR
   ├── prioridade
   ├── recursos
   ├── conflitos
   ├── orçamento
   └── limite do lote
   ↓
LOTE DE EXECUÇÃO
   ↓
RESULTADOS
   ↓
REPLANEJAMENTO
   ↺
```

## Princípios

1. O plano é uma decisão atual, não uma promessa permanente.
2. O estado do grafo é a fonte para o próximo planejamento.
3. Tarefas independentes podem ser executadas em paralelo quando não disputam recursos.
4. Dependências duras bloqueiam a execução até serem concluídas.
5. Recursos compartilhados impedem paralelismo incompatível.
6. O orçamento limita o conjunto de tarefas selecionado.
7. Resultados podem alterar o próximo plano sem apagar o histórico.
8. A evolução futura deve permitir risco, prazo, valor esperado, custo real, confiabilidade, modelos/agentes disponíveis e custo de comunicação.

## Próxima evolução

O V0.1 é deliberadamente simples. A próxima camada deve incorporar:

- risco e incerteza;
- prazos e urgência;
- valor esperado e valor marginal;
- custo/consumo de combustível por capacidade;
- seleção de motor, modelo ou agente;
- retry, fallback e cancelamento;
- dependências suaves e preferências;
- custo de coordenação entre agentes;
- aprendizado de políticas de agendamento;
- registro das razões de cada mudança de plano;
- detecção de sinergias entre capacidades;
- integração com a memória de experiência e com o Meta-Cérebro.

O objetivo não é construir um planejador rígido, mas uma capacidade que aprenda progressivamente a combinar recursos e capacidades para produzir mais resultado com menos desperdício.
