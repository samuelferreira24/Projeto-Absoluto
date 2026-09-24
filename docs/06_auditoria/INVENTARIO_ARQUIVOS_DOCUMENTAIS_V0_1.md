
# INVENTÁRIO DOCUMENTAL — BASE HISTÓRICA V0.1

> **Status:** inventário de referência produzido no início da reorganização documental. As linhas abaixo registram o universo e a classificação daquela etapa; caminhos posteriormente migrados ou removidos podem aparecer aqui deliberadamente como histórico. **Não use este arquivo para afirmar que um caminho ainda existe.** Para a árvore atual, consulte `00_ESTRUTURA_REPOSITORIO.md`, `00_IA_NAVEGACAO.md` e os índices canônicos de cada área.

## Finalidade

Preservar a rastreabilidade da auditoria inicial sem transformar um snapshot documental em estado vivo.

## Autoridade atual

- árvore física do `main` → existência atual de arquivos/caminhos;
- índices canônicos → navegação por área;
- código/testes/CI/evidência → capacidade operacional;
- Project Knowledge → estado estruturado derivado;
- este inventário → histórico da classificação documental inicial.

## Zonas auditadas

- `docs/02_arquitetura/` — arquitetura canônica atual;
- `docs/03_planejamento/` — entrada documental do planejamento;
- `docs/06_auditoria/` — auditorias;
- `docs/90_fontes/` — fontes preservadas;
- `cerebro/00_estado/` — estado/snapshots;
- `cerebro/mapas/` — mapas;
- `cerebro/especificacao/` — especificações e conhecimento histórico;
- `continuidade/` — continuidade/handoffs;
- `mini-cerebro/` — investigação histórica;
- `99_arquivo/` — patrimônio histórico.

## Resultado das fases posteriores

As referências físicas antigas identificadas no inventário foram auditadas e, quando comprovadamente redundantes ou obsoletas, foram migradas, removidas ou corrigidas nos PRs #72 e #74–#80. Em particular, não existem mais na árvore atual as antigas áreas `docs/architecture/`, `continuidade/02_estado/`, `continuidade/04_construcao/` e `continuidade/06_interface/`.

O conteúdo original deste inventário foi reclassificado como snapshot para evitar que uma fotografia histórica continue sendo interpretada como inventário vivo.

## Regra

**Inventário histórico não é estado atual.**

Antes de citar um caminho como existente, verificar a árvore atual e o índice da área correspondente.
