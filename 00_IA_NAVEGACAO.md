# 00 — NAVEGAÇÃO PARA IA

## Objetivo
Este arquivo é a porta de entrada para qualquer IA, agente ou ferramenta que precise compreender e navegar este repositório.

## Regra de navegação
1. Leia este arquivo.
2. Leia `README.md`.
3. Leia `00_ESTRUTURA_REPOSITORIO.md`.
4. Para o estado atual do cérebro, consulte `cerebro/00_estado/`.
5. Para mapas, consulte `cerebro/mapas/`.
6. Para especificações, consulte `cerebro/especificacao/00_INDICE_ESPECIFICACOES.md`.
7. Para dados/conhecimento, consulte `cerebro/data/00_INDICE_DADOS.md`.
8. Para continuidade, consulte `continuidade/00_LEIA_PRIMEIRO.md`.
9. Para operação do ABS, consulte `docs/01_operacao/`.
10. Para arquitetura e integrações, consulte `docs/02_arquitetura/`.
11. Para planejamento, consulte `docs/03_planejamento/`.
12. Para cooperação ABS/Mini-Cérebro, consulte `docs/04_referencia/MANUAL_CEREBRO_MINI_CEREBRO_COOPERACAO_V1.md`.
13. Para o Mini-Cérebro histórico/auxiliar, consulte `mini-cerebro/README.md` e `mini-cerebro/00_INDICE.md`.

## Camadas do repositório
| Caminho | Função | Estado |
|---|---|---|
| `abs_core/` | núcleo operacional ABS V1 | ATIVO |
| `cerebro/` | cérebro, estado, mapas, especificações e testes | ATIVO/EM EVOLUÇÃO |
| `mini-cerebro/` | cérebro auxiliar/histórico e investigação | AUXILIAR/HISTÓRICO |
| `continuidade/` | continuidade operacional e ponto de retomada | ATIVO |
| `docs/` | documentação organizada | ATIVO |
| `scripts/` | automação e operação Termux | ATIVO |
| `tests/` | testes do ABS | ATIVO |
| `tools/` | ferramentas documentais | AUXILIAR |
| `20_interface/` | camada de interface | ATIVO |
| `50_frentes/` | frentes de expansão | ESTRUTURAL |
| `99_arquivo/` | material preservado/histórico | NÃO TRATAR COMO FONTE OPERACIONAL |

## Prioridade das fontes
Para saber o que o sistema faz hoje, priorize código e testes atuais.
Para entender por que algo existe, consulte continuidade, especificações e histórico.
Arquivos em `99_arquivo/` são preservados e não devem ser tratados como estado operacional atual sem validação.

## Navegação por intenção
- **Estado atual:** `cerebro/00_estado/`, `continuidade/`
- **Arquitetura:** `docs/02_arquitetura/`, `cerebro/especificacao/`
- **Planejamento:** `docs/03_planejamento/`, `cerebro/mapas/`
- **Operação:** `docs/01_operacao/`, `scripts/`, `abs_core/`
- **Histórico/evidências:** `docs/90_fontes/`, `cerebro/especificacao/07_historico/`, `99_arquivo/`
- **Mini-Cérebro:** `mini-cerebro/`
- **Testes:** `tests/`, `cerebro/tests/`, `mini-cerebro/tests/`

## Regra de segurança documental
Não alterar, mover ou excluir um arquivo apenas por inferência sem verificar dependências e função. Organização documental não significa mudança de comportamento.
