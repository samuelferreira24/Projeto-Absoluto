# Organização documental — Projeto Absoluto

## Governança
A classificação documental é definida por `docs/00_GOVERNANCA_INFORMACAO.md`.

A documentação é organizada por **função**, não por cronologia. Cada documento deve ter função, autoridade e relação com outras fontes identificáveis.

## Áreas documentais

- `01_operacao/` — como operar o que existe hoje.
- `02_arquitetura/` — arquitetura, contratos, limites e relações entre componentes.
- `03_planejamento/` — planejamento, índices e possibilidades de avanço.
- `04_referencia/` — referências técnicas e manuais estáveis.
- `06_auditoria/` — auditorias, inventários e avaliações temporais.
- `90_fontes/` — fontes de origem e materiais preservados.

Áreas técnicas específicas:
- `api/` — contrato/referência da API.
- `20_interface/` — implementação atual da interface e seus artefatos diretamente associados.
- `cerebro/` — implementação, conhecimento, mapas e histórico do Cérebro.
- `continuidade/` — transferência entre sessões/IAs.
- `99_arquivo/` — patrimônio histórico/legado.

## Consolidação arquitetural

A antiga área `docs/architecture/` foi consolidada em `docs/02_arquitetura/`.

Os documentos migrados mantêm o mesmo conteúdo e blob Git; somente o caminho foi reorganizado para eliminar duas áreas concorrentes para arquitetura.

A arquitetura também deve ser lida em conjunto com:
- código atual;
- testes;
- contratos/API;
- especificações do Cérebro quando forem fonte histórica ou de conhecimento;
- evidências operacionais.

## Relação com o Projeto Absoluto

- Projeto Absoluto = visão, método, princípios e objetivos.
- Sistema = infraestrutura/meio para ampliar capacidade.
- ABS = primeiro projeto em construção.
- futuros projetos podem reutilizar ou substituir capacidades existentes.

Documentação técnica do ABS não deve ser tratada como definição da visão maior.

## Regra

**Classificar antes de mover.**

Migrações documentais devem preservar conteúdo, referências e histórico. Código operacional só é movido após verificação de dependências.
