# Controle de Execução Persistente — V0.1

## Função

Separar a autoridade de dispatch e recuperação do scheduler e do executor.

Fluxo:

PLANO → CLAIM → EXECUÇÃO → RESULTADO → CONCLUIR / RETRY / LIBERAR
                         ↓
                    LEASE / RECONCILIAÇÃO

## Estado persistido

Cada tarefa pode possuir:
- claim_id;
- tentativa;
- estado;
- aquisição;
- expiração do lease;
- retry agendado;
- último erro.

## Princípios

1. Uma tarefa não deve ser despachada duas vezes enquanto possui claim ativo.
2. Claim expirado pode ser recuperado com nova tentativa.
3. Falha pode gerar retry explícito.
4. O controle não substitui o histórico de aprendizagem.
5. O scheduler continua responsável por escolher o plano.
6. O executor continua responsável por executar.
7. O controle apenas governa a posse operacional e a recuperação.

## Limite

Ainda falta uma fila distribuída real e uma garantia de coordenação multi-host. A implementação atual é um controle persistente local, adequado como camada arquitetural mínima antes de escolher infraestrutura distribuída.
