# Orquestração e Execução Contínua — V0.3

## Capacidade consolidada

O Projeto modela a execução como um ciclo orientado ao estado e à missão, e não como uma lista fixa de tarefas.

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

A seleção de um caminho é contextual e reversível. O sinal de maior relevância é um sinal de decisão, não uma prioridade permanente, fila fixa ou sequência obrigatória. Novos resultados podem mudar a escolha do próximo caminho.

## Identidade de ciclo

Cada ciclo recebe um `ciclo_id` estável e uma `idempotency_key` derivada da missão e do ciclo.

Isso permite distinguir uma nova execução da missão, uma retomada de um ciclo interrompido e uma repetição causada por recuperação.

Quando um processo cai depois de registrar `CICLO/INICIADO`, a próxima execução pode recuperar o mesmo `ciclo_id` em vez de criar uma identidade nova.

## Idempotência

A identidade do ciclo não garante, sozinha, que um efeito externo ocorrerá uma única vez. Ações com efeitos externos devem aceitar ou derivar uma chave idempotente, usar operações naturalmente repetíveis, upsert, deduplicação ou outro mecanismo apropriado.

Execução durável normalmente trata workers e transporte como passíveis de repetição; efeitos externos precisam de uma estratégia explícita de idempotência. citeturn0search2turn0search7

## Lease e heartbeat

O runtime utiliza claim atômico, lock interprocessos, expiração do lease, heartbeat periódico durante ciclos longos, recuperação de worker abandonado e identidade própria do runtime.

O heartbeat impede que um ciclo legítimo de longa duração seja confundido com um worker abandonado. A expiração continua sendo o mecanismo de recuperação quando o processo realmente desaparece.

## Persistência

A persistência atual é baseada em arquivos locais e é portátil para desenvolvimento e testes. Ela ainda não oferece as garantias de uma infraestrutura distribuída de produção.

Execução durável madura normalmente persiste checkpoints, timers e histórico em uma camada durável e define explicitamente a política de recuperação. citeturn0search2turn0search13

## Continuidade real

A missão e seu histórico são persistidos fora da interface conversacional. Uma futura infraestrutura persistente poderá recuperar a missão e continuar os ciclos mesmo após encerramento de navegador, sessão ou agente.

```text
INTERFACE
   ≠
EXECUÇÃO
   ≠
ESTADO DO PROJETO
```

A conversa pode ser uma interface de comando, mas não deve ser o mecanismo que mantém o processo vivo.

## Limite atual

Esta versão implementa um núcleo recuperável de ciclo, persistência, identidade, idempotência, lease e heartbeat em software. Ainda **não constitui uma operação 24/7 hospedada**.

Para atingir esse nível serão necessários ambiente persistente, armazenamento durável compartilhado, mecanismo de despertar/eventos/timers, workers reais, observabilidade, retry/recuperação, integração com agentes e ferramentas, controle de custos, autenticação/autorização, validação de efeitos externos e governança.

## Infraestrutura possível

A camada de execução pode futuramente utilizar GitHub Actions, servidores próprios, serviços cloud, runtimes de agentes ou outras tecnologias. A nova Agents API da OpenAI já oferece infraestrutura gerenciada para agentes de longa duração, contexto entre janelas, ferramentas, subagentes e ambientes de execução. citeturn0search0turn0search8

Isso é uma **opção de infraestrutura**, não uma definição da identidade do Projeto.

GitHub Actions pode funcionar como mecanismo de despertar/agendamento/eventos, mas workflows agendados têm intervalo mínimo de cinco minutos e não devem ser tratados isoladamente como o runtime contínuo definitivo. citeturn0search1turn0search6

## Próxima evolução

A próxima capacidade deve conectar o runtime a Estado do Sistema, Cérebro, Tabuleiro dinâmico, Executor de ferramentas, agentes substituíveis, evidências/auditoria, mecanismo externo de despertar e recuperação ponta a ponta.

Essa evolução permanece aberta: os caminhos podem ser desenvolvidos em paralelo quando um caminho aumentar a capacidade de outros.
