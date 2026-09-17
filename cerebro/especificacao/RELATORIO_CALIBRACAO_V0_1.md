# Relatório de calibração — Cérebro V0.1

## Objetivo

Registrar a evidência obtida durante a calibração da base do Cérebro, separando claramente capacidade comprovada, limites atuais e próximos passos.

## Conjunto de calibração

### Materiais estruturados

- `Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx`
- `Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx`
- `Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx`

### Acervo heterogêneo representativo

- `Conversaweb.mht`
- `Transcricao_Conversa.txt`
- `Relatorio_Diagnostico_Completo_da_Conversa.docx`

O lote foi deliberadamente pequeno: seu objetivo é testar o modelo antes de qualquer migração ampla.

## Capacidades comprovadas

1. Detecção e tratamento de formatos distintos por adaptadores específicos.
2. Extração de conteúdo não vazio dos materiais testados.
3. Preservação do arquivo-fonte: os bytes originais permanecem inalterados durante a ingestão.
4. Registro de tamanho e SHA-256 do arquivo de origem.
5. Registro da origem do documento.
6. Representação estrutural inicial para documentos DOCX e conteúdo textual para formatos simples.
7. Identificação do parser utilizado, permitindo rastrear o mecanismo de extração.
8. Armazenamento portátil em JSONL.
9. Busca textual.
10. Busca por metadados e campos básicos do registro.
11. Criação de identificadores incrementais por tipo/ano.
12. Atualização versionada de registros, mantendo histórico das versões anteriores.
13. Recusa explícita de duplicação silenciosa de um mesmo identificador.

## Evidência automatizada

A validação contínua executada pelo GitHub Actions no lote heterogêneo anterior concluiu com `9 passed`.

A execução seguinte incorpora também os testes do núcleo de registros e atualização versionada. O resultado deve ser considerado o critério de aceitação deste ciclo somente após a execução do workflow correspondente ao commit final.

## Limites identificados

A ingestão ainda não faz inferência semântica. Em particular, o extrator não deve ser tratado como responsável por descobrir automaticamente:

- relações entre conceitos e registros;
- distinção entre fato, hipótese, interpretação e decisão;
- significado contextual de uma afirmação;
- entidades e relações de domínio;
- conhecimento derivado de múltiplos documentos.

Esses itens pertencem a uma camada posterior de análise/representação semântica. Manter essa fronteira explícita evita atribuir ao parser uma responsabilidade que ele não consegue validar de forma confiável.

## Decisão arquitetural decorrente

A base de ingestão está suficientemente demonstrada para avançar, mas a migração integral do acervo não deve ser iniciada ainda.

O próximo avanço deve ser a definição e validação da camada semântica sobre a representação intermediária, mantendo três propriedades:

1. a fonte original permanece preservada;
2. toda informação derivada mantém proveniência para a fonte e posição/contexto quando disponível;
3. inferências são separadas de conteúdo originalmente presente na fonte e podem carregar estado/confiança.

## Critério para automação semântica

A automação só deve ser introduzida depois que o contrato semântico estiver definido e puder ser testado. Um classificador ou modelo de IA não deve transformar texto plausível em fato por padrão.

A sequência recomendada é:

```text
FONTE
↓
INGESTÃO PRESERVADA
↓
REPRESENTAÇÃO INTERMEDIÁRIA
↓
ANOTAÇÃO SEMÂNTICA EXPLÍCITA
↓
RELAÇÕES + PROVENIÊNCIA
↓
VALIDAÇÃO
↓
AUTOMAÇÃO ASSISTIDA
↓
APRENDIZADO
```

## Resultado do ciclo

A calibração confirmou que a fundação atual preserva a matéria-prima e fornece uma base portátil para evolução. Também revelou uma fronteira importante: preservar informação não é o mesmo que compreender informação.

Essa fronteira passa a orientar a próxima etapa do Cérebro, sem alterar ou reprocessar destrutivamente os materiais originais.
