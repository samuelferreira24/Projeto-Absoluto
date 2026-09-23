# CONTINUIDADE — PROJETO ABSOLUTO

## Função
Este diretório reúne os documentos necessários para transferir contexto entre sessões e IAs.

**Não é o depósito geral de toda a documentação do Projeto.**

A governança está em `docs/00_GOVERNANCA_INFORMACAO.md`.

## Ordem de leitura para retomada
1. `AGENTS.md`
2. `00_IA_NAVEGACAO.md`
3. `docs/00_GOVERNANCA_INFORMACAO.md`
4. `07_conhecimento/project_knowledge.json`
5. `07_conhecimento/MAPA_AUTO_ESTADO_PROJETO.md`
6. `07_conhecimento/SESSAO_ATUAL.md`
7. fonte específica indicada pelo estado/pergunta.

## Regra de interpretação
Quando houver conflito:
**código atual + testes + CI + evidência operacional > continuidade antiga.**

Project Knowledge representa o estado estruturado observável.
O mapa automático é sua projeção humana.
Handoffs e checkpoints preservam contexto de sessão; não substituem estado vivo.

## Organização atual
- `01_contexto/` — contexto necessário à continuidade.
- `02_estado/` — registros de estado históricos/legados da continuidade; não competir com Project Knowledge.
- `03_decisoes/` — decisões e correções registradas.
- `04_construcao/` — pontos de parada e contexto de construção.
- `05_handoffs/` — handoffs/checkpoints.
- `06_interface/` — material temático de interface mantido provisoriamente; será classificado antes de eventual migração documental.
- `07_conhecimento/` — mecanismo atual de conhecimento e projeções.
- `99_legado/` — snapshots antigos.

## Regra para continuar
Antes de criar componente:
1. localizar o requisito;
2. verificar se já existe;
3. verificar integração;
4. verificar testes/evidências;
5. construir somente a lacuna comprovada.

**Não apagar histórico para deixar a árvore limpa.**
