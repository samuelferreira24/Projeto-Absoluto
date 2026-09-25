# GUIA MANUAL — FECHAMENTO DA V1 OPERACIONAL

Este arquivo contém somente as etapas que dependem do ambiente do Imperador. A implementação estrutural já foi preparada no repositório.

## 1. Preparar modelos locais

Escolher e instalar um ou mais runtimes locais compatíveis com OpenAI Chat Completions. O ABS aceita um endpoint local por modelo.

Configuração-base:

- `ABS_LOCAL_AI_URL`
- `ABS_LOCAL_AI_MODEL`
- para múltiplos modelos: `ABS_LOCAL_AI_MODELS`

Formato de múltiplos modelos:

`id_do_modelo=url|nome_do_modelo,id2=url|nome2`

> Não coloque chaves de API no GitHub.

## 2. Configurar IAs externas (opcional)

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GEMINI_API_KEY`
- `OPENROUTER_API_KEY`

O OpenRouter entra como uma rota adicional, não como dependência estrutural.

## 3. Testar o ABS localmente

Executar a suíte existente e depois a aceitação da V1.

## 4. Interface auxiliar

Pode-se instalar uma interface OpenAI-compatible, como Open WebUI, apontando para:

`http://127.0.0.1:8788/v1`

O gateway do ABS expõe `/v1/models` e `/v1/chat/completions`.

## 5. Teste online

Executar uma missão simples com uma IA externa.

## 6. Teste de troca

Executar a mesma missão com outro modelo/provedor.

## 7. Teste offline

Desconectar a Internet e executar uma missão que use apenas ferramentas locais + modelo local.

## 8. Teste de recuperação

Interromper o processo durante uma missão controlada e verificar se o Work é recuperado como PAUSED e pode continuar.

## 9. Aceitação final

Considerar a V1 operacional somente quando o ciclo abaixo tiver evidência real:

`Imperador → interface → ABS → inteligência → planejamento → autorização → execução → verificação → memória → resultado`

### Checklist

- [ ] modelo local instalado
- [ ] pelo menos dois modelos locais cadastrados, se o hardware permitir
- [ ] pelo menos uma IA externa configurada
- [ ] OpenRouter testado ou explicitamente dispensado
- [ ] interface auxiliar conectada (opcional, mas recomendada)
- [ ] missão online concluída
- [ ] troca de modelo concluída
- [ ] missão offline concluída
- [ ] falha/timeout testado
- [ ] recuperação testada
- [ ] memória local confirmada
- [ ] memória versionada confirmada
- [ ] Data Layer confirmada
- [ ] ciclo end-to-end aprovado
