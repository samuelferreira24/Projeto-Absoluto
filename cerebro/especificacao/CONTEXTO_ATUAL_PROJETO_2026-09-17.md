# CONTEXTO ATUAL — PROJETO ABSOLUTO

Data: 2026-09-17
Branch de construção: `base-cerebro-v0.1`

## Ponto de parada

A prioridade atual mudou: antes de avançar a orquestração, a continuidade entre chats passou a ser prioridade.

Objetivo do próximo ciclo:

> Guardar o contexto de trabalho, a memória, o que foi aprendido e o ponto exato de parada, permitindo continuar em outro chat sem recomeçar do zero.

## Contexto que precisa sobreviver

- visão e princípios do Projeto Absoluto;
- estado atual da arquitetura;
- decisões já tomadas e seus motivos;
- aprendizados acumulados;
- descobertas;
- erros e correções;
- progresso de construção;
- tarefas abertas e dependências;
- pesquisas e conclusões relevantes;
- histórico necessário para interpretar decisões;
- objetivo atual e próximo passo;
- estado do código e branch de trabalho.

## Estado técnico conhecido

O Cérebro já possui armazenamento persistente de registros, aprendizado, consolidação, reconstrução histórica, rede evolutiva, runtime, orquestração e grafo de tarefas.

Existe `cerebro/continuidade.py`, que já validava um manifesto operacional. Ela foi ampliada para fornecer:

- `criar_snapshot(...)`;
- `salvar_snapshot(...)`;
- `carregar_snapshot(...)`;
- `gerar_prompt_retoma(...)`;
- `salvar_prompt_retoma(...)`.

O `Cerebro` foi ampliado com:

- `checkpoint(...)`;
- `preparar_retoma(...)`;
- `carregar_continuidade(...)`;
- `prompt_de_retoma(...)`.

O diagnóstico passou a indicar se existe um arquivo de continuidade persistido.

## Artefatos de continuidade

`cerebro/data/continuidade.json` será o snapshot estruturado da sessão.

`cerebro/data/RETOMAR_OUTRO_CHAT.md` será o pacote textual portátil para colar em outro chat.

`cerebro/especificacao/CONTINUIDADE_ENTRE_CHATS_V0_2.md` define o contrato conceitual.

## Limite importante

A memória externa deve registrar explicitamente o conhecimento que precisa sobreviver. Não se deve presumir que estados internos ocultos de um modelo sejam exportáveis ou permanentes.

A continuidade deve ser reconstruível por outra instância de IA a partir de dados persistidos e verificáveis.

## Regra de operação

O chat é uma interface. O Cérebro é a memória persistente.

Trocar de conversa não deve apagar o trabalho.

Antes de continuar em uma nova sessão:

1. carregar o snapshot;
2. ler o contexto atual;
3. ler os aprendizados relevantes;
4. verificar o estado do repositório;
5. verificar o que mudou desde o snapshot;
6. continuar do ponto válido mais recente;
7. registrar o novo progresso.

## Segurança da construção

Não escrever em `main` durante esta fase. A construção continua em `base-cerebro-v0.1`.

O PR #2 continua aberto e não deve ser mesclado automaticamente.

## Próxima evolução

Depois do mecanismo básico estar consolidado, evoluir para:

- checkpoints automáticos;
- snapshots incrementais;
- cadeia de sessões;
- comparação de snapshots;
- recuperação seletiva por objetivo;
- resolução de conflitos entre sessões;
- sincronização entre chats, contas e plataformas;
- compactação com preservação semântica;
- recuperação automática por agente.
