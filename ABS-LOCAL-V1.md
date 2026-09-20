# ABS Local V1

Primeira versão própria do ABS para execução local no Android/Termux.

## Fluxo

Interface → ABS local → Orchestrator → Capability → resultado → memória SQLite

GitHub continua como fonte de atualização e como ponte externa já existente.

## Endpoints

- GET /health
- GET /capabilities
- POST /task
- GET /works/<id>

## Exemplo

curl -s http://127.0.0.1:8787/task -H 'Content-Type: application/json' -d '{"objective":"Responda somente ABS_PROPRIO_OK","capability_id":"codex","approved":true}'

## Atualização automática

Com ABS_AUTO_UPDATE=1, o processo verifica o branch main do repositório remoto periodicamente.

Quando existe um novo commit e a cópia local está limpa, ele faz fast-forward e reinicia o próprio processo.

Se uma atualização falhar, o ABS em execução continua funcionando.

## Princípio

Esta V1 não transforma GitHub no núcleo do ABS. GitHub é apenas uma fonte externa de código/continuidade. O núcleo local recebe e executa tarefas diretamente.
