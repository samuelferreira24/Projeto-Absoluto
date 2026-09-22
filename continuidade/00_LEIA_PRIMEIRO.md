# CONTINUIDADE — PROJETO ABSOLUTO

## Função

Este diretório reúne os documentos usados para transferir contexto entre sessões e IAs.

**Importante:** os documentos de continuidade são registros de contexto, não substituem o estado real do código, testes e evidências operacionais.

## Estado atual

O ABS V1 **está em construção**. Já existe uma fundação operacional significativa, mas a V1 não está concluída.

A continuidade atual deve ser lida sem confundir:
- planejamento original;
- estado atual implementado;
- auditoria;
- histórico;
- handoff de uma sessão para outra.

## Ordem recomendada de leitura

1. `05_handoffs/01_HANDOFF_ATUAL_OPERACIONAL.md` — estado operacional mais recente registrado.
2. `05_handoffs/02_HANDOFF_NOVO_CHAT_ABS_V1_PLANEJAMENTO.md` — continuidade produzida a partir do planejamento original.
3. `02_estado/01_ESTADO_ATUAL_PROJETO.md` — registro de estado da continuidade.
4. `01_contexto/01_MODELO_ABS_E_PRINCIPIOS.md` — modelo e princípios.
5. `03_decisoes/01_DECISOES_CORRECOES_E_REGRAS.md` — decisões e correções registradas.
6. `04_construcao/` — pontos de parada e handoffs ligados à construção.
7. `99_legado/` — snapshots antigos; não tratar como estado atual.

## Regra de interpretação

Quando houver conflito entre um documento antigo e o estado atual:

**código atual + testes + CI + evidência operacional > documentação de continuidade antiga.**

A continuidade serve para preservar contexto e evitar reconstrução desnecessária.

## Regra para continuar a construção

Antes de criar qualquer componente:

1. localizar o que o planejamento original exige;
2. verificar se já existe;
3. verificar se está integrado;
4. verificar testes e evidências;
5. construir somente a lacuna comprovada.

A próxima grande análise da V1 deve cruzar o planejamento original com a implementação atual e produzir uma matriz de completude.

## Organização

- `01_contexto/` — contexto e fundamentos.
- `02_estado/` — registros de estado.
- `03_decisoes/` — decisões, correções e regras.
- `04_construcao/` — pontos de parada e continuidade da construção.
- `05_handoffs/` — handoffs operacionais entre chats/IAs.
- `99_legado/` — snapshots de continuidade antigos.

**Não apagar o histórico apenas para deixar a estrutura limpa.** Organizar significa tornar explícito o papel de cada documento.
