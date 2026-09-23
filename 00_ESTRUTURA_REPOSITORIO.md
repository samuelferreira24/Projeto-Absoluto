# Estrutura do repositório — Projeto Absoluto

## Regra
A estrutura física separa código atual, cérebro, continuidade, documentação, frentes, ferramentas, testes e patrimônio histórico.

**A numeração é classificatória. Não cria fila de execução.**

A governança completa está em `docs/00_GOVERNANCA_INFORMACAO.md`.

## Camadas principais
| Caminho | Função | Autoridade |
|---|---|---|
| `abs_core/` | implementação operacional ABS V1 | código atual |
| `cerebro/` | conhecimento, estado, mapas, especificações e testes | estado/conhecimento |
| `mini-cerebro/` | investigação/patrimônio histórico auxiliar | histórico/pesquisa |
| `continuidade/` | continuidade entre sessões/IAs | transferência |
| `docs/01_operacao/` | operação | operação atual |
| `docs/02_arquitetura/` | arquitetura/contratos | arquitetura |
| `docs/03_planejamento/` | planejamento | planejamento |
| `docs/04_referencia/` | referência técnica | referência |
| `docs/90_fontes/` | fontes preservadas | origem |
| `docs/06_auditoria/` | auditorias | avaliação documentada |
| `scripts/` | automação/Termux | operação |
| `tests/` | testes | verificação |
| `20_interface/` | interface | camada |
| `50_frentes/` | frentes | expansão |
| `tools/` | ferramentas auxiliares | ferramenta |
| `99_arquivo/` | patrimônio histórico/legado | arquivo |

## Estado vivo
A fonte estruturada de estado deve ser derivada de Project Knowledge e evidências observáveis.

`project_knowledge.json` = estado estruturado.

`MAPA_AUTO_ESTADO_PROJETO.md` = projeção humana.

Handoffs não substituem o estado vivo.

## Regra contra duplicação
Classificar antes de consolidar:
- mapa → navegação/planejamento;
- especificação → definição;
- estado → situação observada;
- decisão → direção autorizada;
- evidência → prova observada;
- operação → como usar;
- referência → descrição técnica;
- histórico → passado preservado.

Não fundir documentos apenas por semelhança de tema.

## Regra contra quebra
Código operacional não deve ser movido por estética. Antes de qualquer movimento, verificar imports, scripts, CI, entrypoints, documentação e testes.

## Princípio
**Organizar não é apagar, reescrever ou misturar.**

É tornar explícito:
**onde está → o que é → qual autoridade possui → como verificar.**
