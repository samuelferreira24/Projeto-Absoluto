# Identidade e Eventos V0.1

## Objetivo

Criar uma camada mínima, portável e independente de fornecedor para identificar entidades do Projeto e registrar acontecimentos de forma rastreável.

## Princípios

1. A identidade pertence ao Projeto, não à conta ou plataforma.
2. Agentes e sessões são participantes substituíveis.
3. Eventos devem permitir reconstruir causalidade e correlação.
4. A idempotência evita processamento duplicado.
5. O histórico não depende de GitHub.
6. A estrutura deve poder ser transportada para outro ambiente.

## Identidades iniciais

- `PA-PROJETO-ABSOLUTO`: identidade estável do Projeto.
- `PA-AGENTE-*`: agente participante.
- `PA-SESSAO-*`: sessão operacional.
- `PA-<TIPO>-*`: recurso identificado pelo Projeto.

## Evento

Cada evento possui, quando aplicável:

- `event_id`
- `correlation_id`
- `causation_id`
- `origem`
- `destino`
- `tipo`
- `timestamp`
- `versao`
- `status`
- `payload`
- `idempotency_key`

## Fluxo

`EVENTO → CORRELAÇÃO → CAUSA → AÇÃO → RESULTADO → EVIDÊNCIA → APRENDIZADO`

## Limites desta versão

Esta camada não pretende resolver ainda registro distribuído, mensageria, autenticação, autorização, filas, consenso ou operação 24/7. Ela cria os contratos mínimos para que essas capacidades possam ser construídas posteriormente sem perder identidade e rastreabilidade.
