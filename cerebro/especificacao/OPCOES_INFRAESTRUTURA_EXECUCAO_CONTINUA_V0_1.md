# Opções de Infraestrutura para Execução Contínua V0.1

Este documento registra uma decisão arquitetural importante: o mecanismo de execução do Projeto Absoluto deve ser portátil e não pode depender de uma única plataforma.

## Propriedades desejadas

A infraestrutura futura deve permitir:

- processo persistente ou reativável;
- armazenamento durável do estado;
- despertar por evento ou tempo;
- recuperação após falha;
- múltiplos workers quando necessário;
- leases/heartbeat;
- idempotência;
- observabilidade;
- execução de ferramentas e agentes;
- controle de permissões e custos;
- troca do provedor de IA sem perda do estado do Projeto.

## Famílias de solução

### 1. Runtime próprio em servidor/cloud

O Projeto controla o processo, o armazenamento e o mecanismo de execução.

**Vantagens:** máximo controle, independência de fornecedor, liberdade arquitetural.

**Custos:** mais responsabilidade operacional: disponibilidade, filas, recuperação, segurança, deploy e observabilidade.

### 2. Motor de execução durável

Motores especializados oferecem checkpoints, timers, retries, recuperação e coordenação de workers.

A pesquisa atual confirma que os elementos centrais desse modelo são persistência de checkpoints, recuperação explícita e idempotência para efeitos externos. Não existe garantia universal de “efeito externo exatamente uma vez” apenas porque o workflow é durável.

### 3. Plataforma de agentes de longa duração

As plataformas modernas de agentes já oferecem harness, contexto persistente, ferramentas, ambientes de execução e subagentes. A API de Agentes da OpenAI, anunciada em 10 de setembro de 2026, é um exemplo atual: permite agentes de longa duração, ambientes hospedados ou próprios e execução de subagentes em paralelo. citeturn1search0

Ela pode ser um **provedor de capacidade de execução**, mas não deve ser confundida com a identidade do Projeto Absoluto.

### 4. GitHub Actions como mecanismo auxiliar

GitHub Actions pode atuar como:

- validação;
- disparador por evento;
- despertar periódico;
- execução de ciclos curtos e controlados;
- publicação de evidências.

Workflows agendados têm intervalo mínimo de cinco minutos e executam no branch padrão; eventos externos podem usar `repository_dispatch`. Portanto, Actions é útil como parte da infraestrutura, mas não resolve sozinho todos os requisitos de um runtime 24/7. citeturn0search1turn0search6

## Direção atual

Não escolher uma tecnologia definitiva agora.

Construir primeiro o **contrato de execução** e manter adaptadores para diferentes infraestruturas.

```text
             CONTRATO DO PROJETO
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   runtime       motor durável   agente cloud
    próprio          externo       hospedado
       │             │             │
       └─────────────┼─────────────┘
                     ▼
                MESMA MISSÃO
                MESMO ESTADO
                MESMO CÉREBRO
                MESMO HISTÓRICO
```

## Regra de projeto

> A infraestrutura pode mudar. A capacidade do Projeto de continuar uma missão, preservar o histórico, recuperar-se de falhas e trocar agentes deve permanecer.

## Próxima validação

Antes de declarar execução 24/7, validar experimentalmente:

1. iniciar missão;
2. adquirir lease;
3. executar ação;
4. interromper o worker em pontos diferentes;
5. reiniciar outro worker;
6. recuperar estado;
7. impedir duplicação indevida;
8. confirmar idempotência de efeitos externos;
9. registrar evidência completa;
10. repetir com mais de um worker.

O resultado desses experimentos deve decidir quais componentes precisam permanecer próprios e quais podem ser delegados a infraestrutura externa.
