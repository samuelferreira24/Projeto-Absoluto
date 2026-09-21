# Evolução Assistida do ABS

A primeira interface operacional deve permitir que o Imperador utilize o próprio ABS para construir versões posteriores.

## Ciclo

IMPERADOR
↓
INTERFACE
↓
ABS CORE
↓
CÉREBRO / ORQUESTRAÇÃO
↓
RECURSOS: Codex, Claude, Gemini, IA local, Internet, APIs, GitHub e outros
↓
IMPLEMENTAÇÃO
↓
TESTES
↓
GIT / CONTINUIDADE
↓
UPDATE MANAGER
↓
REINÍCIO CONTROLADO
↓
HEALTH CHECK
↓
NOVA VERSÃO

## Limite importante

O ciclo não significa que o ABS deve alterar a si próprio sem autorização. A autoridade continua com o Imperador.

O objetivo é substituir operações manuais repetitivas por um fluxo controlado e auditável.

## Update

O update_manager já possui verificação, comparação de commits, aplicação, registro de estado, reinício via serviço, health check e rollback.

O ambiente Termux/serviço/boot é infraestrutura de continuidade. A interface deve futuramente comandar esse ciclo sem depender de comandos manuais para cada etapa.

## Critério de evolução

Uma futura capacidade de autoevolução deve preservar: autorização, testes, evidência, persistência, rollback, continuidade e observabilidade.

> O ABS pode usar o ABS para construir o próximo ABS, mas o Imperador continua sendo a autoridade do ciclo.