# Orquestração e Execução Contínua — V0.2

## Capacidade consolidada

O Projeto passa a modelar a execução como um ciclo orientado ao estado e à missão, e não como uma lista fixa de tarefas.

```text
MISSÃO
  ↓
ESTADO ATUAL
  ↓
CÉREBRO + REDE
  ↓
SINAIS / CAMINHOS POSSÍVEIS
  ↓
DECISÃO CONTEXTUAL
  ↓
POLÍTICA DE AUTONOMIA
  ↓
EXECUÇÃO
  ↓
RESULTADO / EVIDÊNCIA
  ↓
REGISTRO
  ↓
ATUALIZAÇÃO DO ESTADO
  ↓
NOVO CICLO
```

## Regra de não travamento

A seleção de um caminho é contextual e reversível. O sinal de maior relevância não constitui prioridade permanente, fila fixa ou sequência obrigatória. Novos resultados podem mudar a escolha do próximo caminho.

## Continuidade real

A missão e seu histórico são persistidos fora da interface conversacional. Uma futura infraestrutura persistente poderá recuperar a missão e continuar os ciclos mesmo após encerramento de navegador, sessão ou agente.

## Limite atual

Esta versão implementa o mecanismo de ciclo e persistência em software, mas ainda não constitui uma operação 24/7 hospedada. Para isso será necessária uma infraestrutura persistente de execução, com recuperação, leases/heartbeat, observabilidade, filas/eventos e integração com agentes e ferramentas reais.

## Evolução

A infraestrutura futura pode usar GitHub Actions, servidores, serviços cloud, runtimes de agentes ou outras tecnologias. Nenhuma tecnologia específica é parte obrigatória da identidade do Projeto.
