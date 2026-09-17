# Contrato de Despertar do Runtime V0.1

## Objetivo

Criar uma fronteira durável entre eventos externos e a execução do Projeto, para que uma interface aberta não seja necessária para iniciar ou retomar trabalho.

## Princípio

A conversa é uma interface. O pedido de trabalho pertence ao Projeto.

Um evento externo pode gerar um `PedidoDespertar` persistente contendo:

- identidade do pedido;
- missão a ser despertada;
- origem;
- correlação;
- estado;
- momento de criação;
- momento de processamento;
- detalhes e evidências de falha.

## Estados

```text
PENDENTE → PROCESSANDO → CONCLUIDO
                    ↘
                     FALHOU
```

Pedidos processados não devem voltar a ser tratados como novos despertares sem uma nova identidade. A execução efetiva continua sujeita ao lease, à idempotência e à política de autonomia do runtime.

## Fontes possíveis

O contrato é independente do fornecedor. A origem pode ser:

- interface humana;
- GitHub;
- webhook;
- agenda;
- outro agente;
- outro sistema;
- monitoramento;
- evento interno do próprio Projeto.

## Relação com execução contínua

```text
EVENTO EXTERNO
      ↓
PEDIDO DE DESPERTAR
      ↓
ORQUESTRADOR
      ↓
MISSÃO
      ↓
RUNTIME + LEASE + HEARTBEAT
      ↓
CICLO
      ↓
AGENTE / EXECUTOR
      ↓
RESULTADO + EVIDÊNCIA
      ↓
CÉREBRO
```

## Limites atuais

Este contrato não afirma que o Projeto já possui operação 24/7 hospedada. Ele fornece a fronteira persistente necessária para essa evolução. Ainda são necessários um worker persistente, mecanismo de disparo externo, observabilidade operacional e integração segura com agentes/ferramentas.

## Direção evolutiva

GitHub Actions pode atuar como mecanismo de despertar/control-plane, e runtimes de agentes ou servidores persistentes podem atuar como workers. Nenhuma dessas tecnologias é a identidade do Sistema; são recursos substituíveis.
