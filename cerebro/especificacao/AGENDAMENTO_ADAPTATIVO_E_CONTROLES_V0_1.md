# Agendamento Adaptativo e Controles V0.1

## Objetivo

Transformar o grafo de tarefas em uma camada de decisão adaptativa que escolha o próximo trabalho considerando valor, prioridade, custo, risco, tempo, prazo, dependências e conflitos de recursos.

## Fluxo

```text
OBJETIVO
  ↓
DECOMPOSIÇÃO
  ↓
GRAFO DE TAREFAS
  ↓
VALIDAÇÃO
  ↓
TAREFAS PRONTAS
  ↓
AGENDAMENTO
  ├─ valor marginal
  ├─ custo
  ├─ risco
  ├─ prioridade
  ├─ prazo
  └─ recursos
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
REPLANEJAMENTO
  ↓
APRENDIZADO
  ↺
```

## Custos

O código de planejamento é local e não exige, por si só, pagamento de API ou serviço externo. Custo real aparece quando uma tarefa utiliza motores externos, como modelos pagos, APIs, computação em nuvem, GPU, armazenamento ou outras capacidades cobradas.

O campo `custo_estimado` representa custo relativo/estimado da tarefa e permite impor `orcamento` ao planejamento. Ele não representa automaticamente dinheiro real; a camada futura de economia deverá associar o recurso consumido a preço, quota, créditos ou outra unidade de combustível.

## Riscos

O agendador não deve executar automaticamente ações de alto impacto apenas porque possuem pontuação alta. Antes da execução real, devem existir controles para:

- validar dependências;
- verificar recursos disponíveis;
- respeitar orçamento;
- limitar paralelismo quando houver conflito de recurso;
- registrar decisões e replanejamentos;
- permitir falha e recuperação sem apagar histórico;
- distinguir tarefas reversíveis de ações irreversíveis;
- exigir aprovação humana para ações de alto impacto, quando aplicável;
- preservar proveniência dos resultados;
- impedir que uma estimativa de valor substitua regras de segurança.

## Estado atual

A V0.1 implementa planejamento heurístico e replanejamento sobre o estado atual do grafo. Ela ainda não constitui um executor autônomo universal nem deve ser tratada como tal.

A pontuação atual combina valor/prioridade, custo e risco e registra o motivo das decisões. O histórico é preservado para futura aprendizagem do Meta-Cérebro.

## Próxima evolução

1. orçamento por tipo de combustível;
2. custo monetário e custo computacional separados;
3. deadlines e tempo restante reais;
4. capacidade parcial de recursos;
5. retry/fallback/cancelamento;
6. dependências duras e preferências suaves;
7. custo de comunicação entre agentes;
8. seleção de motor/capacidade;
9. medição de resultado real contra estimativa;
10. aprendizado das políticas de agendamento;
11. detecção de sinergias entre capacidades;
12. auditoria de decisões do agendador.

## Princípio

> O agendador deve otimizar o uso dos recursos sem transformar uma heurística em autoridade. Ele propõe a melhor ação conhecida sob as restrições atuais, registra por que a escolheu e permanece capaz de mudar de rota quando novos resultados, riscos ou informações aparecem.
