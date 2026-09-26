# Integração Open WebUI ↔ Gateway ABS

## Objetivo

O Open WebUI usa a API Chat Completions compatível com OpenAI. O Gateway ABS mantém essa porta como uma interface substituível, sem transferir a autoridade do sistema para o Open WebUI.

## Compatibilidade implementada

- `GET /v1/models`
- `POST /v1/chat/completions`
- mensagens no formato OpenAI
- `stream=true` com SSE compatível
- `tools` aceito no request
- `tool_choice` aceito no request
- registro dos nomes de ferramentas solicitadas na proveniência ABS
- execução automática das capacidades conversacionais já suportadas pelo ABS
- resposta final continua sendo gerada pelo motor de inteligência selecionado

## Regra arquitetural

```
Imperador
  ↓
Open WebUI
  ↓
Gateway ABS
  ↓
CognitiveRuntime
  ↓
ABS Tool Runtime / Orchestrator
  ↓
capacidades
  ↓
resultado
  ↓
motor de inteligência
```

Open WebUI é interface. ABS continua sendo o núcleo de decisão, roteamento, execução, verificação e proveniência.

## Limite atual

O Qwen 0.5B local não deve ser tratado como um modelo de function calling confiável. Por isso, o ABS mantém roteamento conversacional próprio para intenções que já consegue identificar, como URLs e GitHub.

A compatibilidade de `tools` não transforma automaticamente o Qwen em um agente de function calling. Para isso, futuramente pode ser usado um modelo com tool calling mais confiável ou um adaptador especializado.

## Configuração do Open WebUI

Conexão OpenAI:

- URL: `http://127.0.0.1:8788/v1`
- API key: `abs`
- modelo: `intelligence:local-ai`

Depois da atualização, o teste deve ser feito no chat normal. Para validar streaming, usar uma conversa que produza uma resposta maior.

## Próxima evolução

A próxima camada é expor as capacidades ABS como ferramentas formais para modelos que suportem function calling, mantendo o mesmo contrato interno e permitindo trocar Open WebUI ou o modelo sem reconstruir o ABS.
