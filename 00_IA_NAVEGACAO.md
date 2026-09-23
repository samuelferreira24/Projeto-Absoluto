# 00 — NAVEGAÇÃO PARA IA

## Porta de entrada
Este arquivo é a navegação rápida para qualquer IA, agente ou ferramenta.

**Governança da informação:** leia primeiro `AGENTS.md`, depois este arquivo e `docs/00_GOVERNANCA_INFORMACAO.md`.

## Ordem canônica de leitura
1. `AGENTS.md` — regras permanentes.
2. `README.md` — visão resumida.
3. `docs/00_GOVERNANCA_INFORMACAO.md` — autoridade, classificação e continuidade.
4. `docs/00_MODELO_PROJETO_ABSOLUTO.md` — relação entre Projeto Absoluto, Sistema e projetos.
5. `00_ESTRUTURA_REPOSITORIO.md` — estrutura física.
6. Estado vivo: `continuidade/07_conhecimento/project_knowledge.json` e `MAPA_AUTO_ESTADO_PROJETO.md`.
7. `cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md` — navegação estratégica.
8. Fonte específica conforme a pergunta.


## Regra de autoridade
Para afirmar o que existe hoje:
**código + testes + CI + evidência operacional > documentação antiga/handoff.**

Para decisões e princípios:
**registro autorizado de decisão do Imperador.**

Para histórico:
**fonte histórica preservada, sem tratá-la como estado atual.**

## Navegação por intenção
- **Projeto Absoluto / visão:** `docs/00_MODELO_PROJETO_ABSOLUTO.md` + arquivos-base catalogados na auditoria.
- **Estado atual:** `continuidade/07_conhecimento/`, código e testes.
- **Conhecimento:** `cerebro/` e Project Knowledge.
- **Decisões:** `continuidade/03_decisoes/`.
- **Arquitetura:** `docs/02_arquitetura/`, `docs/architecture/`, especificações do Cérebro.
- **Planejamento/mapas:** `docs/03_planejamento/`, `cerebro/mapas/`.
- **Operação:** `docs/01_operacao/`, `scripts/`, `abs_core/`.
- **Evidências/testes:** `tests/`, CI e Project Knowledge.
- **Sessão/retomada:** `continuidade/05_handoffs/` e `continuidade/07_conhecimento/SESSAO_ATUAL.md`.
- **Histórico/fontes:** `docs/90_fontes/`, `mini-cerebro/`, `99_arquivo/`.
- **Interface:** `20_interface/`.

## Camadas principais
| Caminho | Função | Estado |
|---|---|---|
| `abs_core/` | núcleo operacional ABS V1 | ATIVO |
| `cerebro/` | conhecimento, mapas, especificações e estado do Cérebro | ATIVO/EVOLUÇÃO |
| `mini-cerebro/` | investigação/patrimônio histórico auxiliar | AUXILIAR/HISTÓRICO |
| `continuidade/` | transferência entre sessões/IAs | ATIVO |
| `docs/` | documentação técnica | ATIVO |
| `scripts/` | automação/operação | ATIVO |
| `tests/` | verificação | ATIVO |
| `20_interface/` | interface | ATIVO |
| `50_frentes/` | frentes futuras/experimentais | ESTRUTURAL |
| `99_arquivo/` | patrimônio preservado | HISTÓRICO |

## Regra de segurança
Não alterar, mover ou excluir arquivo apenas por inferência. Antes de reorganizar, verificar função, referências, dependências e testes.
