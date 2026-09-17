# Contrato de Despertar do Runtime V0.1

## Objetivo

Criar uma fronteira durável entre eventos externos e a execução do Projeto, para que uma interface aberta não seja necessária para iniciar ou retomar trabalho.

## Princípio

A conversa é uma interface. O pedido de trabalho pertence ao Projeto.

Um evento externo pode gerar um `PedidoDespertar` persistente contendo identidade, missão, origem, correlação, estado, timestamps, tentativas e detalhes/evidências.

## Estados e recuperação

```text
PENDENTE → PROCESSANDO → CONCLUIDO
                    ↘
                     FALHOU
```

Um pedido em `PROCESSANDO` possui um momento de início. Se o worker desaparecer e o timeout expirar, o pedido volta a ser elegível para processamento. Isso evita que uma interrupção deixe uma missão permanentemente presa.

A recuperação não significa que efeitos externos serão repetidos com segurança automaticamente. Cada executor deve usar a identidade do ciclo e sua chave de idempotência para deduplicar efeitos colaterais quando necessário.

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
CICLO + IDEMPOTÊNCIA
      ↓
AGENTE / EXECUTOR
      ↓
RESULTADO + EVIDÊNCIA
      ↓
CÉREBRO
```

## Worker agnóstico

O Projeto possui um worker que pode entregar uma missão a um comando externo configurável. O worker não assume OpenAI, Claude, Gemini ou qualquer outro fornecedor. O executor recebe contexto estruturado por `stdin` e deve devolver JSON por `stdout`.

Essa fronteira permite trocar o agente sem trocar o núcleo do Projeto.

## Mecanismo de despertar

O repositório possui um workflow de despertar por:

- agenda;
- `repository_dispatch`;
- execução manual.

O workflow só executa um agente quando um executor externo estiver configurado. Sem ele, registra o estado e permanece em espera.

## Limites atuais

Isso estabelece a infraestrutura de continuidade, mas não significa que o Projeto já esteja operando 24/7 em produção. Ainda é necessário hospedar/configurar um worker persistente e conectar um executor de IA/ferramentas reais com as permissões e guardrails apropriados.

Além disso, o workflow agendado do GitHub só atua sobre o branch padrão e tem intervalo mínimo de cinco minutos; portanto ele é um mecanismo auxiliar de despertar, não a definição do runtime definitivo.

## Direção evolutiva

GitHub Actions, servidores próprios, runtimes de agentes, sandboxes e serviços de terceiros podem atuar como recursos de execução. A arquitetura deve permanecer substituível e preservar a identidade, estado, histórico, proveniência e conhecimento do Projeto fora do fornecedor.

A infraestrutura atual da API de Agentes da OpenAI demonstra que agentes de longa duração, subagentes, ambientes persistentes e recuperação já podem ser fornecidos como serviço; isso é uma opção futura de infraestrutura, não uma decisão arquitetural definitiva do Projeto.
