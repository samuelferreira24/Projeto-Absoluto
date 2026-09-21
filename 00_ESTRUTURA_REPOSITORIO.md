# Estrutura do Projeto Absoluto

## Regra de organização

A estrutura física separa componentes por função sem confundir documentação, código atual, histórico ou planejamento.

### Núcleo atual
- `abs_core/` — runtime executável do ABS V1.
- `tests/` — testes do runtime atual.
- `scripts/` — operação, inicialização e integração Termux.
- `.github/` — automação de CI.
- `pyproject.toml` — configuração do pacote Python.

### Cérebro e conhecimento
- `cerebro/` — cérebro atual, estado, dados, especificações, mapas e testes próprios.
- `mini-cerebro/` — componente histórico/arquitetural separado, preservado para integração e aprendizado.
- `continuidade/` — continuidade operacional e pontos de estado.

### Documentação
- `docs/01_operacao/` — operação atual.
- `docs/02_arquitetura/` — arquitetura e integrações.
- `docs/03_planejamento/` — planejamento.
- `docs/04_referencia/` — materiais de referência técnica.
- `docs/90_fontes/` — fontes e registros preservados.

### Interface e expansão
- `20_interface/` — interfaces de acesso ao ABS.
- `50_frentes/` — frentes de expansão/execução.

### Histórico
- `99_arquivo/` — legado, versões históricas e patrimônio preservado.

## Critério

Código operacional não é arquivado apenas por ser antigo; documentos históricos não são tratados como capacidade executável. Movimentações devem preservar conteúdo e verificar dependências antes de alterar caminhos usados pelo runtime.
