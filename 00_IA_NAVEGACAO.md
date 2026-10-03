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
7. Retomada detalhada e contexto consolidado: `continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md`.
8. `continuidade/05_handoffs/04_HANDOFF_ARQUITETURA_PROJETO_ABSOLUTO_2026-09-23.md` é histórico; handoffs `01–03` são snapshots históricos. Não substituem o estado vivo.
9. `cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md` — navegação estratégica.
10. Fonte específica conforme a pergunta.


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
- **Arquitetura:** `docs/02_arquitetura/` e especificações do Cérebro.
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


## Referência de preservação de contexto — 2026-10-03
A pesquisa profissional sobre continuidade concluiu que **handoff não é memória inteira**. A preservação deve usar camadas relacionadas: conhecimento, decisões, pesquisas, evidências, estado, memória de experiências, histórico, artefatos, checkpoints, handoff, mapas e proveniência.

Referência canônica: `docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md`.

Regra de recuperação: nova IA → mapa → estado → decisões → evidências → fontes profundas → trabalho. O handoff é ponte de entrada e não substitui as fontes originais.

## Trajetória e proveniência — referência arquitetural
A pesquisa de trajetória bidirecional concluiu que o repositório deve preservar relações explícitas entre eventos, commits, fontes, evidências e estados, permitindo navegação origem → presente e presente → origem.

Referência: `docs/00_governanca/PESQUISA_TRAJETORIA_PROVENIENCIA_BIDIRECIONAL_V1.md`.

O inventário estrutural de todo o Projeto está em `continuidade/07_conhecimento/project_registry.json` e o modelo de objetos em `docs/00_GOVERNANCA_INVENTARIO_PROJETO_V1.md`. O inventário de decisões explícitas está em `continuidade/07_conhecimento/decision_registry.json`.

O inventário operacional das 72 capacidades está em `continuidade/07_conhecimento/capability_registry.json`, com índice humano em `docs/02_arquitetura/INVENTARIO_CAPACIDADES_ABS_V1.md`.

O Project Knowledge agora projeta relações de trajetória observáveis. Isso não substitui Git, decisões, evidências ou fontes primárias.
A implementação operacional está em `abs_core/trajectory.py`, com relações semânticas explícitas em `continuidade/07_conhecimento/trajectory_registry.json`; a travessia pode ser feita para frente ou para trás e é validada antes da projeção.
