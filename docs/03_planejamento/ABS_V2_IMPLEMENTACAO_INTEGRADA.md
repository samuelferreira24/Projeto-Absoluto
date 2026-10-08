# ABS V2 — IMPLEMENTAÇÃO INTEGRADA

**Estado:** V2 integrada no `main` e operacional no VPS.

## O que foi construído

A V2 não substituiu o ABS por outro framework. Ela transformou a infraestrutura V1 em um núcleo de controle soberano e adicionou:

- Authority Core;
- Policy Engine;
- Risk Governor;
- Budget Governor;
- Mode Selector;
- Work V2 metadata;
- Executor Router;
- DIRECT;
- WORKFLOW;
- AGENT;
- MULTIAGENT;
- OpenClaw Executor;
- Observation Ledger;
- Evidence Ledger;
- Verification;
- Provenance;
- durable idempotency;
- checkpoints;
- replanning/fallback;
- admission control;
- MCP protocol boundary;
- A2A protocol boundary;
- V1 LocalABS compatibility.

## Componentes externos

### OpenClaw

É executor, não núcleo.

Fluxo validado:

`ABS Work → Mode Selector → Executor Router → OpenClaw → OpenAI/gpt-5.6-luna → resultado → verificação`

### MCP

Disponível como fronteira de tools/resources via JSON-RPC configurável por ambiente.

### A2A

Disponível como fronteira de tasks/agentes via endpoint HTTP configurável por ambiente.

### Codex

Permanece capability/executor existente.

### Outros runtimes

OpenAI Agents SDK, Microsoft Agent Framework, Temporal e LangGraph permanecem substituíveis como executores/adapters opcionais; nenhum foi transformado em dependência estrutural.

## Evidência de testes

Validação real no VPS:

- **ABS V2 suite: 168/168 testes passando**
- `compileall`: PASS
- V2 DIRECT: PASS
- V2 WORKFLOW: PASS
- V2 MULTIAGENT + admission: PASS
- autoridade não escalável: PASS
- high-risk approval gate: PASS
- failure/UNKNOWN behavior: PASS
- idempotência persistente: PASS
- compatibilidade LocalABS V1: PASS
- OpenClaw standalone: PASS
- OpenClaw integrado ao Work V2: PASS
- API `/works` real: PASS
- health do serviço: `version: v2`

## Prova integrada do OpenClaw

Work real observado no VPS:

- estado: `completed`;
- modo: `agent`;
- executor: `openclaw`;
- tentativa: 1;
- retorno do OpenClaw: sucesso;
- verification: `accepted=true`;
- evidence IDs presentes;
- provenance registrada.

O OpenClaw retornou a resposta esperada através do modelo configurado `openai/gpt-5.6-luna`.

## Compatibilidade

A interface V1 continua disponível.

A fachada `LocalABS` preserva o formato antigo de resultado e também expõe o registro V2 completo.

O banco operacional existente não foi usado como banco de teste da suíte; a validação completa usa banco temporário para impedir que estado histórico contamine os testes.

## Estado arquitetural

O ABS agora opera conceitualmente como:

`Imperador → Work → Authority/Policy → Strategy/Mode → Capability/Resource → Executor → Observation → Evidence → Verification → State → Recovery/Replanning`

Executores externos continuam substituíveis.

A autoridade continua no ABS/Imperador.

Nenhum executor, modelo ou protocolo possui autoridade para redefinir o ABS.

## Próximo estado natural

A construção da V2 está encerrada como uma base integrada.

A partir daqui, novas capacidades podem ser adicionadas ao fabric existente sem reabrir o molde arquitetural.
