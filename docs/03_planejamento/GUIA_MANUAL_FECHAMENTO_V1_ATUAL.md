# GUIA MANUAL — FECHAMENTO DA V1 OPERACIONAL

## O que já foi preparado

O repositório agora possui:
- Data Layer do ABS sobre SQLite;
- verificação V1 integrada ao Orchestrator;
- OpenRouter como adaptador opcional;
- suporte a vários modelos locais via registros separados;
- gateway OpenAI-compatible para interfaces auxiliares;
- preflight da V1;
- checklist manual abaixo.

## 1. Modelos locais

Escolha um ou mais runtimes locais compatíveis com OpenAI Chat Completions.

Um modelo:

    ABS_LOCAL_AI_URL=http://127.0.0.1:PORT
    ABS_LOCAL_AI_MODEL=nome-do-modelo

Vários modelos:

    ABS_LOCAL_AI_MODELS=id1|http://127.0.0.1:PORT|modelo1,id2|http://127.0.0.1:PORT|modelo2

O ABS cria uma inteligência separada para cada item. Assim, trocar o modelo não exige alterar o núcleo.

## 2. IAs externas

Configure somente as que quiser usar:

- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GEMINI_API_KEY
- OPENROUTER_API_KEY

Nunca grave chaves no repositório.

## 3. Preflight

No Termux:

    cd ~/Projeto-Absoluto
    python -m scripts.abs_v1_acceptance

O resultado deve mostrar PASS e listar as inteligências detectadas.

## 4. Gateway para interface auxiliar

Inicie:

    python -m abs_core.openai_compat

Gateway padrão:

    http://127.0.0.1:8788/v1

Ele expõe:

- GET /v1/models
- POST /v1/chat/completions

Isso permite conectar uma interface OpenAI-compatible sem alterar o ABS Core.

## 5. Open WebUI

Se escolher Open WebUI, crie uma conexão OpenAI-compatible apontando para o gateway do ABS. A documentação atual do Open WebUI confirma suporte a endpoints OpenAI-compatible e seleção de múltiplas conexões/modelos. citeturn0search0turn0search4

## 6. Testes de aceitação

Depois do preflight:

1. missão online;
2. troca de modelo;
3. falha de provedor;
4. recuperação após interrupção;
5. missão offline usando modelo local;
6. confirmação de memória local;
7. confirmação do Data Layer;
8. confirmação do histórico versionado;
9. ciclo completo pelo celular.

## 7. Critério final

A V1 somente passa quando houver evidência do ciclo:

Imperador → interface → ABS → inteligência → planejamento → autorização → execução → verificação → memória → resultado

### Checklist

- [ ] preflight PASS
- [ ] pelo menos um modelo local funcionando
- [ ] segundo modelo local funcionando, se o hardware permitir
- [ ] uma IA externa funcionando
- [ ] OpenRouter funcionando ou dispensado conscientemente
- [ ] troca de modelo funcionando
- [ ] gateway/interface auxiliar funcionando, se desejado
- [ ] missão online funcionando
- [ ] missão offline funcionando
- [ ] recuperação funcionando
- [ ] Data Layer registrando resultados
- [ ] GitHub preservando conhecimento consolidado
- [ ] ciclo end-to-end aprovado

## Observação

A interface própria do ABS continua sendo desenvolvida como projeto de longo prazo. Ela não bloqueia a operação da V1.
