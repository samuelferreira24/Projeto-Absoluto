# ABS — GitHub ↔ Termux Bridge V1

Ponte persistente entre GitHub e o ABS executando no Termux.

Fluxo: Interface do Imperador / ABS → GitHub Issue [ABS] → Bridge no Termux → ABS → Codex ou outra capability → resultado no GitHub.

O GitHub funciona como fila e registro. O Termux é o executor local.

## Tarefa

Issue aberta com título iniciado por [ABS] e contendo:

ABS_TASK_JSON:
{"id":"task-0001","objective":"Responda somente ABS_BRIDGE_OK","capability":"codex","approved":true,"context":{}}

Apenas tarefas com status=pending (ou sem campo status) são processadas.

## Instalação

No diretório do projeto:

    export ABS_GITHUB_REPO="samuelferreira24/Projeto-Absoluto"
    export ABS_GITHUB_TOKEN="SEU_TOKEN_DO_GITHUB"
    export ABS_BRIDGE_INTERVAL="15"

Depois:

    python -m abs_core.bridge

O bridge observa o GitHub. Quando uma Issue [ABS] chega, cria um Work no ABS, executa a capability solicitada e publica o resultado na própria Issue.

## Segurança

- O token fica somente no ambiente do Termux; nunca no repositório.
- O bridge não executa Issues comuns.
- A execução passa pelo Orchestrator.
- Capabilities não-test exigem approved=true.
- Não habilitar globalmente o bypass do sandbox do Codex.
- Escrita no Termux/proot deve continuar sendo explicitamente autorizada.

## Evolução

Leases, retomada, múltiplos executores, roteamento por capability, resultados estruturados, autenticação própria e Interface do Imperador entram sobre esta base.
