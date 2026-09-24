# Organização documental — Projeto Absoluto

## Governança
A classificação documental é definida por `docs/00_GOVERNANCA_INFORMACAO.md`.

A documentação não deve virar uma sequência cronológica de arquivos. Cada documento precisa ter função e autoridade identificáveis.

## Áreas
- `01_operacao/` — como operar o que existe.
- `02_arquitetura/` — arquitetura e contratos.
- `03_planejamento/` — planejamento e índices documentais.
- `04_referencia/` — referências técnicas.
- `90_fontes/` — fontes e materiais de origem.
- `06_auditoria/` — auditorias e avaliações.
- `api/` — referência de API.

## Relação com outras áreas
- `cerebro/mapas/` = mapas de navegação, capacidades e planejamento do Cérebro.
- `cerebro/00_estado/` = estado observado e snapshots do Cérebro/ABS; não substitui Project Knowledge.
- `continuidade/` = transferência entre sessões, não depósito geral de documentos.
- `99_arquivo/` = patrimônio histórico.
- `abs_core/` = código atual.

## Planejamento × mapas

A auditoria desta zona concluiu que não há necessidade de fundir fisicamente `docs/03_planejamento/` com `cerebro/mapas/`.

As funções são complementares:

- `docs/03_planejamento/` = entrada documental do planejamento e planejamentos específicos que descrevem como avançar;
- `cerebro/mapas/` = mapas de capacidades, dependências, pendências e rede evolutiva usados para navegação e seleção dinâmica;
- `cerebro/00_estado/` = estado/snapshots; não é planejamento;
- `continuidade/` = contexto de retomada; não é planejamento.

Não mover os mapas apenas para eliminar nomes parecidos. O ganho desta etapa é tornar a relação explícita.

## Regra
**Classificar antes de mover.** Código operacional só é movido após verificar dependências.

## Estado da reorganização em 2026-09-23

A documentação temática de interface foi redistribuída por função:
- pesquisa → `docs/90_fontes/`;
- arquitetura → `docs/02_arquitetura/`;
- planejamento → `docs/03_planejamento/`.

A antiga `docs/architecture/` foi eliminada na migração arquitetural anterior; `docs/02_arquitetura/` é a área canônica.

Snapshots antigos de estado e construção foram reclassificados em `continuidade/99_legado/` ou `continuidade/05_handoffs/` conforme sua função temporal.

O quadro `cerebro/mapas/04_QUADRO_MESTRE_STATUS_ABS_V1_2026-09-22.md` foi reclassificado para `cerebro/00_estado/STATUS_ABS_V1_2026-09-22.md`, pois descreve estado consolidado/snapshot da V1, não um mapa de planejamento.

A próxima zona de auditoria é **fontes × histórico × Mini-Cérebro × 99_arquivo**.
