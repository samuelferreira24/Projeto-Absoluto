# AUDITORIA DE INTEGRIDADE — PESQUISAS DO MOLDE ARQUITETURAL ABS

**Data:** 2026-09-26  
**Status:** CONCLUÍDA  
**Escopo:** integridade, preservação, versionamento e separação das Pesquisas 01 e 02.  
**Regra:** esta auditoria não altera os estudos originais.

## 1. Artefatos auditados

### Pesquisa 01
- Arquivo: `docs/03_planejamento/pesquisa/PESQUISA_01_MOLDE_ARQUITETURAL_AGENTES.md`
- Branch: `pesquisa-01-molde-arquitetural-agentes`
- Commit de preservação: `b64779c7` (conforme histórico previamente registrado)
- Estado verificado: arquivo presente na branch.
- Tamanho observado: aproximadamente 54,5 KB / 2.466 linhas.

### Pesquisa 02
- Arquivo: `docs/03_planejamento/pesquisa/PESQUISA_02_MOLDE_ARQUITETURAL_UNIVERSAL_MULTIMODO.md`
- Branch: `pesquisa-02-molde-arquitetural`
- Estado verificado: arquivo presente na branch.
- Tamanho observado: aproximadamente 53,7 KB / 2.607 linhas.

## 2. Relação com main

As duas branches foram comparadas com o mesmo `main`:
- base: `6066a8b8dbaf6f0702d40364abb1cfddd413efb2`;
- cada branch está 1 commit à frente;
- nenhuma está atrás de `main`;
- cada comparação mostra somente a adição do respectivo arquivo de pesquisa;
- não foram encontrados arquivos de código alterados nessas branches de pesquisa.

## 3. Separação

Não foi encontrado sinal de que uma pesquisa tenha sido inserida dentro da outra. Cada estudo está em sua própria branch e seu próprio arquivo.

A independência física/versionada está preservada.

**Limite:** independência epistemológica absoluta não pode ser provada apenas pelo Git. O fato de os estudos chegarem a conclusões semelhantes também exige auditoria do processo e das premissas, não apenas do armazenamento.

## 4. Integridade

Não foram encontrados:
- cortes aparentes no final dos documentos;
- arquivo ausente;
- duplicação de arquivo;
- alteração posterior dos estudos depois do commit de preservação;
- mistura de código com os estudos.

Os próprios estudos também registram explicitamente que não representam decisão oficial nem autorização para implementação.

## 5. Anormalidades ou pontos de atenção

### Pesquisa 01
O documento declara investigação de fontes externas, mas o arquivo preservado não mantém URLs das fontes na forma pesquisável encontrada nesta auditoria. Isso reduz a auditabilidade independente de algumas afirmações documentais.

### Pesquisa 02
O documento mantém URLs explícitas para as fontes finais reunidas, o que melhora a auditabilidade. Entretanto, o método não apresenta um registro operacional equivalente a um dataset de todas as simulações, portanto a quantidade de simulações conceituais não pode ser reproduzida como um experimento.

### Quantidade de simulações
A Pesquisa 01 registra números altos de exploração conceitual (1.000+ cenários, 200 adversariais, aproximadamente 3.000 combinações e mais de 200 modelos/arquiteturas). Esses números devem ser tratados como registros de exploração, não como evidência experimental independente.

## 6. Veredito

**INTEGRIDADE DE PRESERVAÇÃO: OK**

**SEPARAÇÃO ENTRE ESTUDOS: OK**

**INDEPENDÊNCIA VERSIONADA: OK**

**AUDITABILIDADE METODOLÓGICA: PARCIAL**

A preservação não precisa ser refeita. Os estudos originais devem permanecer congelados.
