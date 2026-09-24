# AUDITORIA — FONTES, HISTÓRICO, MINI-CÉREBRO E ARQUIVO

## Objetivo

Auditar a fronteira entre fontes de origem, conhecimento histórico, Mini-Cérebro e patrimônio arquivado antes de qualquer nova migração física.

## Resultado

A separação física atual é funcional e não justifica uma migração ampla nesta etapa.

| Área | Classificação | Ação |
|---|---|---|
| docs/90_fontes/ | fontes de origem e materiais preservados | KEEP |
| cerebro/especificacao/07_historico/ | conhecimento histórico derivado | KEEP / HISTÓRICO |
| cerebro/especificacao/legado_reintegrado/ | especificações recuperadas do legado | KEEP / LEGADO |
| mini-cerebro/ | ferramenta de investigação histórica | KEEP / INVESTIGAÇÃO |
| mini-cerebro/investigacoes/ | reconstruções e análises históricas | KEEP |
| 99_arquivo/ | patrimônio histórico/legado | KEEP / ARQUIVO |

## Fonte-base

As três fontes-base documentais versionadas permanecem em docs/90_fontes/. Elas são fontes de origem da visão/conhecimento e não devem ser reescritas como documentação técnica do ABS.

O material histórico localizado anteriormente em branches/Library continua distinguido da fonte versionada até haver importação controlada.

## Histórico do Sistema

cerebro/especificacao/07_historico/ contém reconstruções causais, semânticas e operacionais do Sistema anterior. Esse material pode informar aprendizagem, mas não representa automaticamente a arquitetura operacional atual.

cerebro/especificacao/legado_reintegrado/ contém contratos e especificações recuperados do legado. O nome já sinaliza a condição correta: legado recuperado, não autoridade atual.

## Mini-Cérebro

O Mini-Cérebro é definido pelo próprio README como sistema histórico de recuperação e investigação do antigo Sistema Absoluto. Sua fonte original é somente leitura; fatos, inferências e hipóteses devem permanecer separados; informação derivada deve apontar para a fonte.

Ele não é o Cérebro atual e não é o ABS.

## Arquivo

99_arquivo/ é patrimônio histórico/legado sem participação automática na operação atual. O pacote O-IMPERIO-COMPLETO-claude possui separação interna por projeto, sistema, cliente, migração, histórico e material superado.

Não migrar conteúdo do arquivo para áreas operacionais apenas por relevância temática.

## Regra de promoção histórica

Material histórico só deve influenciar uma capacidade atual quando houver:

1. fonte identificada;
2. interpretação explícita;
3. decisão/autorização quando necessária;
4. implementação atual;
5. teste ou evidência correspondente.

## Conclusão

O principal risco desta zona não é a localização física dos arquivos. É a promoção indevida de material histórico para autoridade atual.

Portanto, nesta etapa:

- nenhum arquivo histórico foi apagado;
- nenhum código foi movido;
- nenhuma fonte-base foi reescrita;
- nenhuma área histórica foi fundida com a operação atual.

## Próxima frente

Auditar referências e órfãos documentais: localizar caminhos antigos como docs/architecture/, continuidade/06_interface/, continuidade/02_estado/ e continuidade/04_construcao/ que ainda apareçam em documentos atuais. Corrigir apenas referências comprovadamente quebradas.
