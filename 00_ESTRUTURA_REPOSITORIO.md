# Estrutura do repositório — Projeto Absoluto

## Regra

A estrutura física separa **código atual**, **cérebro**, **continuidade**, **documentação**, **frentes**, **ferramentas**, **testes** e **patrimônio histórico**.

A numeração é classificatória. Ela não cria uma fila de execução.

## Camadas principais

| Caminho | Função | Autoridade |
|---|---|---|
| `abs_core/` | implementação operacional do ABS V1 | código atual |
| `cerebro/` | estado, dados, mapas, especificações e testes do Cérebro | estado/conhecimento |
| `mini-cerebro/` | componente histórico e investigação do patrimônio antigo | histórico/pesquisa |
| `continuidade/` | continuidade entre sessões e IAs | transferência operacional |
| `docs/01_operacao/` | documentação para operar o sistema atual | operacional |
| `docs/02_arquitetura/` | contratos e fundamentos arquiteturais | arquitetura |
| `docs/03_planejamento/` | entrada e organização do planejamento | planejamento |
| `docs/04_referencia/` | referências técnicas e de integração | referência |
| `docs/90_fontes/` | fontes, relatórios e materiais de origem | fonte |
| `scripts/` | automação e operação Termux | operação |
| `tests/` | testes do ABS V1 | verificação |
| `50_frentes/` | frentes futuras/experimentais | frentes |
| `20_interface/` | interface preservada como camada separada | interface |
| `tools/` | ferramentas auxiliares | ferramenta |
| `99_arquivo/` | patrimônio histórico/legado | arquivo |

## Regras de separação

### Estado atual
A referência para saber o que realmente existe é, nesta ordem prática:

1. código atual;
2. testes;
3. CI;
4. resultados verificáveis;
5. documentação operacional correspondente.

### Cérebro
`cerebro/` organiza estado, dados, mapas, especificações, recuperação histórica e testes do próprio Cérebro.

**Mapa não é implementação.**

### Histórico
`mini-cerebro/`, `docs/90_fontes/` e `99_arquivo/` preservam patrimônio.

Material histórico não vira capacidade atual apenas por existir.

### Continuidade
`continuidade/` registra o contexto necessário para retomada por outra sessão ou IA. Snapshots antigos continuam identificados como snapshots.

## Regra contra duplicação

Quando documentos parecem tratar do mesmo assunto, identificar primeiro a função:

- **mapa** → navegação/estrutura;
- **especificação** → definição;
- **planejamento** → direção e possibilidades;
- **estado** → situação observada;
- **histórico** → evidência do passado;
- **código** → implementação;
- **teste** → verificação.

Não fundir documentos apenas por semelhança de tema.

## Regra contra quebra

Código operacional não deve ser movido apenas por estética.

Antes de mover código:

1. verificar imports;
2. verificar scripts;
3. verificar CI;
4. verificar entrypoints;
5. verificar documentação dependente do caminho;
6. executar testes.

Por isso, componentes como `abs_core/`, `cerebro/` e `mini-cerebro/` permanecem em seus caminhos próprios enquanto sua identidade operacional estiver vinculada a eles.

## Princípio

**Organizar não é apagar, reescrever ou misturar.**

É tornar explícito:

`onde está` → `o que é` → `qual autoridade possui` → `como verificar`.
