# Modelo de Rastreabilidade — V0.1

## Finalidade

Ligar intenção, construção e evidência. O modelo impede que componentes existam sem contexto e permite descobrir o que é afetado quando uma parte muda.

## Cadeia principal

```text
OBJETIVO
  ↓
REQUISITO
  ↓
CAPACIDADE
  ↓
COMPONENTE
  ↓
IMPLEMENTAÇÃO
  ↓
TESTE
  ↓
EVIDÊNCIA
  ↓
VALIDAÇÃO
```

## Unidade de rastreabilidade

Cada elemento deve possuir identidade estável e, quando aplicável:

- `id`;
- `tipo`;
- `titulo`;
- `estado`;
- `versao`;
- `origem`;
- `relacoes`;
- `proveniencia`;
- `evidencias`;
- `historico`.

## Relações estruturais mínimas

- `ATENDE` — requisito atende objetivo;
- `HABILITA` — capacidade habilita requisito ou outra capacidade;
- `IMPLEMENTADA_POR` — componente implementa capacidade;
- `DEPENDE_DE` — elemento depende de outro;
- `TESTADA_POR` — implementação/componente é coberta por teste;
- `EVIDENCIADA_POR` — resultado possui evidência;
- `VALIDADA_POR` — necessidade ou capacidade foi validada;
- `SUBSTITUI` — versão/componente substitui anterior;
- `AFETA` — mudança afeta elemento relacionado.

## Regra de evidência

Uma relação de atendimento ou validação não deve ser considerada comprovada apenas porque foi declarada por um agente. Quando a natureza da afirmação exigir prova, a evidência correspondente deve ser registrada.

## Dependências

Dependências de construção são diferentes de relações semânticas do conhecimento. O grafo estrutural deve permitir identificar:

- bloqueios;
- impacto de mudança;
- componentes críticos;
- trabalho independente possível;
- dependências circulares;
- lacunas de implementação;
- lacunas de teste.

## Uso por múltiplas IAs

Qualquer agente pode consultar a cadeia para entender por que uma peça existe, o que ela precisa satisfazer, o que depende dela e como sua conclusão deve ser demonstrada.

## Implementação incremental

A V0.1 define o contrato sem exigir um banco de dados de grafo. A primeira implementação pode utilizar os registros e relações portáveis já existentes, evoluindo para estruturas especializadas somente quando a escala justificar.
