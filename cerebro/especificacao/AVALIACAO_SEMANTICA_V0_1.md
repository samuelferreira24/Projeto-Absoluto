# Avaliação semântica V0.1

## Objetivo

Medir a capacidade da camada semântica de preservar distinções importantes antes de ativar inferência automática em escala.

A avaliação separa quatro propriedades:

1. classificação semântica;
2. proveniência e origem;
3. relações e contradições;
4. contexto temporal.

## Casos mínimos

### Caso 1 — Fato explícito
Uma fonte afirma diretamente uma informação.

Esperado: `FATO`, origem na fonte, proveniência explícita e confiança não inventada.

### Caso 2 — Hipótese explícita
A fonte apresenta uma possibilidade ainda não comprovada.

Esperado: `HIPOTESE`; não promover para `FATO`.

### Caso 3 — Interpretação
Uma conclusão é produzida a partir de uma ou mais unidades da fonte.

Esperado: `INTERPRETACAO`, `derived_from` preenchido e origem inferencial identificável.

### Caso 4 — Decisão
Uma escolha do projeto é registrada com justificativa e contexto.

Esperado: `DECISAO`, sem confundir decisão com fato externo.

### Caso 5 — Ambiguidade
O texto não permite determinar com segurança se uma afirmação é fato, hipótese ou interpretação.

Esperado: `OUTRO` ou tratamento explícito como incerto; nunca uma classificação inventada.

### Caso 6 — Contradição
Duas fontes apresentam afirmações incompatíveis.

Esperado: preservar ambas as fontes, representar a relação `CONTRADIZ` quando houver base para isso e não apagar uma afirmação para produzir uma falsa concordância.

### Caso 7 — Tempo do fato diferente do tempo do registro
Um fato valeu em uma data anterior, mas a evidência só foi registrada posteriormente.

Esperado: manter `valid_from`/`valid_until` separados de `recorded_at`.

### Caso 8 — Referência externa
Uma unidade derivada aponta para uma fonte ou registro fora do lote atual.

Esperado: aceitar a referência como dependência externa; não tratá-la como corrupção apenas por não estar no lote auditado.

## Critérios de aprovação

A camada passa quando:

- nenhuma fonte original é alterada;
- cada unidade relevante possui origem rastreável;
- inferência não é armazenada como fato sem marcação;
- contradições são preservadas;
- referências inválidas são detectadas sem rejeitar referências externas legítimas;
- consultas temporais distinguem validade e registro;
- resultados podem ser revisados sem destruir versões anteriores.

## Métricas futuras

Quando houver conjunto anotado maior, medir precisão, recall e F1 por tipo semântico; cobertura de proveniência; precisão de relações; taxa de contradições detectadas; precisão de recuperação no top-k; recall no top-k; MRR/nDCG quando houver ranking; e acurácia de consultas temporais.

Não existe um limiar universal nesta versão. Os limiares devem ser definidos por capacidade, risco e custo de erro do uso real.
