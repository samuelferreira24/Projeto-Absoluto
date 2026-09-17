# Ciclo Permanente de Aprendizado — V0.1

## Objetivo

O Cérebro deve preservar e utilizar dois fluxos complementares:

1. **aprendizado acumulado** — conhecimento já consolidado durante a evolução do Projeto;
2. **aprendizado novo** — eventos, descobertas, entendimentos, correções e demais aprendizados produzidos durante a construção atual.

Nenhum dos dois substitui silenciosamente o outro.

## Princípio de preservação

As fontes de aprendizado permanecem intactas. A consolidação produz uma **camada derivada**, permitindo reconstrução, auditoria e reprocessamento.

```text
APRENDIZADO ACUMULADO ─┐
                       ├→ CONSOLIDAÇÃO → VISÃO UNIFICADA → RECUPERAÇÃO/APLICAÇÃO
APRENDIZADO NOVO ──────┘                              ↓
                                               NOVA EXPERIÊNCIA
                                                      ↓
                                                  APRENDIZADO
                                                      ↓
                                              ACUMULAÇÃO CONTÍNUA
```

## Entradas

- `cerebro/memoria/aprendizados_fundamentais_v0_1.json`
- `cerebro/memoria/aprendizados.jsonl`
- futuros registros de aprendizado que adotem o mesmo contrato.

## Saída derivada

- `cerebro/memoria/aprendizados_consolidados_v0_1.json`

A saída não é a fonte de verdade. Ela pode ser reconstruída a partir das fontes preservadas.

## Regras

- Não apagar aprendizado acumulado ao registrar aprendizado novo.
- Não descartar aprendizado novo apenas porque existe conhecimento anterior.
- Deduplicar somente registros semanticamente idênticos segundo a chave definida pelo consolidator.
- Preservar camada e status de cada origem.
- Manter proveniência e contexto sempre que disponíveis.
- Permitir evolução futura do modelo sem obrigar a arquitetura atual a reproduzir protótipos antigos.
- O processo de construção também é uma fonte de aprendizado e deve alimentar o Cérebro.
- Histórico informa decisões atuais, mas não possui autoridade automática sobre a arquitetura futura.

## Integração

A fachada `Cerebro` expõe `consolidar_aprendizados()`, tornando a consolidação parte da capacidade operacional do Cérebro sem acoplar o núcleo a um único formato de armazenamento.

A integração deve evoluir posteriormente para um ciclo automático disparado por eventos relevantes, mantendo a operação explícita e auditável.
