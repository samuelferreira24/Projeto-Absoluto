# Representação semântica intermediária V0.1

## Objetivo

Criar uma camada entre a fonte extraída e o conhecimento derivado. A camada semântica não altera a fonte original e não transforma inferência em fato.

## Princípio central

```text
FONTE → EXTRAÇÃO ESTRUTURAL → UNIDADES SEMÂNTICAS → RELAÇÕES → CONHECIMENTO DERIVADO
```

A representação semântica deve manter explícita a diferença entre o que veio da fonte e o que foi inferido posteriormente.

## Unidades semânticas

Cada unidade deve possuir, no mínimo:

- `id`: identificador estável;
- `source_id`: identificação da fonte de origem;
- `kind`: `FATO`, `HIPOTESE`, `INTERPRETACAO`, `DECISAO`, `PERGUNTA` ou `OUTRO`;
- `content`: conteúdo da unidade;
- `confidence`: `ALTA`, `MEDIA`, `BAIXA` ou `DESCONHECIDA`;
- `provenance`: localização e mecanismo de origem;
- `derived_from`: referências às unidades ou fontes que sustentam a unidade;
- `state`: estado da unidade.

## Fato, hipótese, interpretação e decisão

**FATO** representa uma afirmação tratada como informação da fonte ou evidência explicitamente registrada. Não significa que o sistema tenha provado a verdade externa da afirmação.

**HIPOTESE** representa uma explicação ou proposição ainda sujeita a teste.

**INTERPRETACAO** representa uma leitura, síntese ou inferência derivada do material.

**DECISAO** representa uma escolha adotada no contexto do projeto, incluindo sua justificativa quando conhecida.

Quando a classificação não puder ser determinada com segurança, usar `OUTRO` ou `DESCONHECIDA`; não inventar classificação.

## Proveniência

A proveniência deve permitir responder:

1. De qual fonte veio?
2. Qual trecho ou unidade estrutural sustenta a representação?
3. Foi extraída ou inferida?
4. Qual processo produziu a representação?
5. Quando foi produzida?

## Relações

Relações são explícitas e direcionadas. Exemplos:

- `DERIVA_DE`
- `SUSTENTA`
- `TESTA`
- `CONTRADIZ`
- `INFLUENCIA`
- `DEPENDE_DE`
- `SUBSTITUI`
- `PARTE_DE`

Uma relação não deve ser criada apenas porque duas unidades parecem relacionadas; deve existir evidência ou uma inferência registrada.

## Separação de camadas

```text
CAMADA 1 — FONTE
bytes/documento original

CAMADA 2 — REPRESENTAÇÃO ESTRUTURAL
texto, parágrafos, tabelas, metadados, posições

CAMADA 3 — REPRESENTAÇÃO SEMÂNTICA
unidades, classificação, relações, confiança, proveniência

CAMADA 4 — CONHECIMENTO DERIVADO
sínteses, modelos, conclusões, decisões e aprendizados
```

As camadas superiores podem apontar para as inferiores, mas não devem sobrescrevê-las.

## Regra de segurança semântica

Automação pode propor classificação ou relação. A camada de armazenamento deve preservar a distinção entre `proposto` e `validado` quando a origem for inferencial.

## Critério de validação

A representação será considerada adequada quando conseguir, em um conjunto real:

- apontar a origem de cada unidade;
- separar conteúdo extraído de conteúdo derivado;
- representar fato, hipótese, interpretação e decisão sem colapsá-los;
- preservar confiança e estado;
- representar relações sem perder proveniência;
- permitir revisão posterior sem destruir o registro anterior.

## Limite deliberado desta versão

Esta especificação define o contrato conceitual. A classificação automática por IA e a indexação semântica só devem ser adicionadas depois que o contrato for testado com exemplos reais e casos ambíguos.
