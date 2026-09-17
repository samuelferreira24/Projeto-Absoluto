# Coleta Unificada Multiplataforma V0.1

## Objetivo

Fazer com que o Cérebro consiga receber conhecimento, contexto, experiências e eventos produzidos por diferentes chats, IAs, plataformas, ferramentas e processos sem depender de uma plataforma específica.

## Princípio central

Nenhuma plataforma externa deve ser o lugar onde o conhecimento do Projeto reside.

As plataformas são fontes. O Projeto possui a memória, a identidade, a proveniência, as relações, o histórico e as regras de organização.

## Arquitetura

```text
FONTE EXTERNA
(chat / IA / GitHub / API / arquivo / humano / ferramenta)
        |
        v
ADAPTADOR DA FONTE
        |
        v
ENVELOPE PADRÃO
        |
        +--> evento bruto preservado
        |
        v
IDEMPOTÊNCIA + PROVENIÊNCIA
        |
        v
CLASSIFICAÇÃO INICIAL
        |
        v
CÉREBRO
        |
        +--> memória
        +--> relações
        +--> histórico
        +--> entendimento
        +--> descobertas
        +--> progresso
        +--> decisões
        +--> experiências
        +--> aprendizado
        +--> sabedoria
        |
        v
AGENTES DE ORGANIZAÇÃO
        |
        v
APLICAÇÃO / PLANEJAMENTO / EXECUÇÃO
```

## O que é automático

A camada de coleta deve automatizar:

1. recebimento;
2. identificação da fonte;
3. identificação da sessão/conversa quando disponível;
4. preservação do conteúdo bruto;
5. geração de idempotência;
6. registro de proveniência;
7. classificação inicial;
8. criação da memória derivada;
9. relação com registros existentes;
10. encaminhamento para análise mais profunda;
11. registro do resultado da análise;
12. atualização do estado e do histórico.

A interpretação profunda não deve ser confundida com a captura. Primeiro preservamos; depois interpretamos. Isso evita que uma IA destrua informação original ao resumir ou classificar.

## Envelope padrão

O envelope mínimo contém:

- `event_id`
- `idempotency_key`
- `source_type`
- `source_id`
- `occurred_at`
- `actor`
- `conversation_id`
- `session_id`
- `event_type`
- `content`
- `metadata`
- `raw`

## Fontes previstas

- ChatGPT/OpenAI
- Claude
- Gemini
- GitHub
- MCP
- APIs próprias
- arquivos/exportações
- ações humanas
- outros sistemas
- fontes futuras ainda desconhecidas

A lista é extensível e não representa dependência tecnológica.

## Regra para múltiplas IAs

A IA que produz uma informação não se torna dona dessa informação.

Exemplo:

```text
Claude produz descoberta
        |
        v
coleta
        |
        v
Cérebro registra origem=CLAUDE
        |
        v
GPT verifica
        |
        v
outro agente relaciona
        |
        v
experiência valida/refuta
```

## Conflitos

Se duas fontes produzirem entendimentos diferentes, nenhum deve ser apagado automaticamente.

Registrar:

- afirmação A;
- afirmação B;
- origem de cada uma;
- evidências;
- contexto;
- relação de contradição;
- resultado da verificação;
- decisão posterior.

## Coleta contínua

A coleta deve poder ser acionada por:

- webhook;
- API;
- `repository_dispatch`;
- agendamento;
- fila/evento;
- ação de um agente;
- importação de arquivo;
- captura direta de uma interface futura.

GitHub Actions pode funcionar como mecanismo operacional de disparo, mas não deve ser confundido com o Cérebro nem com a camada de memória. O GitHub pode ser um executor/transportador entre muitos outros.

## MCP

MCP é um candidato importante para padronizar fronteiras entre agentes, dados e ferramentas. A especificação 2026-07-28 tornou o núcleo stateless e incluiu extensões para tarefas de longa duração. Ainda assim, o Projeto deve manter seu próprio envelope e modelo de memória para não ficar dependente do MCP.

## Captura bruta e memória derivada

São camadas diferentes:

```text
RAW
  |
  +-- nunca substituir automaticamente
  |
  v
DERIVADOS
  |
  +-- classificação
  +-- resumo
  +-- relações
  +-- entendimento
  +-- aprendizado
  +-- sabedoria
```

Se uma interpretação posterior estiver errada, o bruto continua disponível para reprocessamento.

## Segurança e autorização

Coleta automática não significa acesso ilimitado.

Cada adaptador deve declarar:

- quais dados pode ler;
- quais ações pode executar;
- qual identidade possui;
- qual nível de autonomia possui;
- quais dados são sensíveis;
- quando precisa de autorização humana.

## Evolução

V0.1: envelope + captura bruta + idempotência + memória derivada.

V0.2: adaptadores reais para fontes selecionadas.

V0.3: ingestão por webhook/API/eventos.

V0.4: organização automática por agentes.

V0.5: relações e consolidação automática.

V1: coleta contínua multiplataforma com observabilidade, recuperação, autorização e portabilidade.

Nenhuma dessas versões deve ser tratada como arquitetura definitiva.
