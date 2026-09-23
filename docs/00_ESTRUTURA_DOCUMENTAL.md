# Organização documental — Projeto Absoluto

## Governança
A classificação documental é definida por `docs/00_GOVERNANCA_INFORMACAO.md`.

A documentação não deve virar uma sequência cronológica de arquivos. Cada documento precisa ter função e autoridade identificáveis.

## Áreas
- `01_operacao/` — como operar o que existe.
- `02_arquitetura/` — arquitetura e contratos.
- `03_planejamento/` — planejamento e índices.
- `04_referencia/` — referências técnicas.
- `90_fontes/` — fontes e materiais de origem.
- `06_auditoria/` — auditorias e avaliações.
- `architecture/` — documentação arquitetural existente; sua relação com `02_arquitetura/` deve ser consolidada na fase de classificação, sem mover prematuramente.
- `api/` — referência de API.

## Relação com outras áreas
- `cerebro/mapas/` = mapas estratégicos, não documentação operacional.
- `continuidade/` = transferência entre sessões, não depósito geral de documentos.
- `99_arquivo/` = patrimônio histórico.
- `abs_core/` = código atual.

## Regra
**Classificar antes de mover.** Código operacional só é movido após verificar dependências.
