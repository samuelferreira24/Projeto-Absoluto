# Estrutura Atual do Cérebro — BASE V0.1

**Finalidade:** fotografia técnica da estrutura do Cérebro no momento de conclusão da fundação V0.1. Este arquivo é material de consulta, calibração e futura melhoria. Não substitui as especificações nem os materiais de origem.

## 1. Princípio

O Cérebro é uma camada evolutiva para preservar fontes, memória, conhecimento, experiências, decisões, aprendizados, relações, proveniência e histórico, independente de GitHub, banco de dados específico ou fornecedor de IA.

## 2. Camadas

```text
FONTES
  ↓
INGESTÃO
  ↓
REPRESENTAÇÃO ESTRUTURADA
  ↓
REGISTROS / MEMÓRIA
  ↓
ANÁLISE E CLASSIFICAÇÃO
  ↓
CONHECIMENTO
  ↓
RELAÇÕES + PROVENIÊNCIA
  ↓
EXPERIÊNCIA / APRENDIZADO
  ↓
EXECUÇÃO
```

## 3. Estrutura lógica atual

```text
cerebro/
├── README.md
├── especificacao/
│   ├── BASE_V0_1.md
│   ├── SCHEMA_REGISTRO_V0_1.json
│   ├── ARQUITETURA_INGESTAO_V0_1.md
│   └── ROADMAP_V0_1.md
├── esquemas/
├── ingestao/
├── registros/
├── relacoes/
└── historico/
```

## 4. Contrato fundamental

Cada registro possui identidade própria e pode evoluir sem depender da identidade do arquivo, do GitHub ou da plataforma que o originou.

Campos fundamentais:

- `id`
- `kind`
- `title`
- `created_at`
- `updated_at`
- `source`
- `content`
- `state`
- `relations`
- `provenance`
- `version`

O contrato permite propriedades adicionais para evolução controlada.

## 5. Tipos previstos na base

FONTE, DOCUMENTO, IDEIA, PESQUISA, CONHECIMENTO, HIPOTESE, EVIDENCIA, DECISAO, PLANEJAMENTO, EXPERIMENTO, PROBLEMA, ERRO, RESULTADO, EXPERIENCIA, APRENDIZADO, QUESTAO_ABERTA e METODO.

## 6. Relações fundamentais

`deriva_de`, `baseia_se_em`, `contem`, `relaciona_se_com`, `gera`, `testa`, `produz`, `causa`, `corrige`, `aprende_de`, `influencia`, `substitui`, `contradiz`, `depende_de`, `faz_parte_de`.

## 7. Proveniência

Informações derivadas devem apontar para sua origem. O original não é substituído pela interpretação extraída dele.

A proveniência deverá permitir reconstruir, conforme a capacidade disponível, de onde veio uma informação, quando foi obtida, por qual processo foi produzida e qual versão da fonte/processamento participou.

## 8. Histórico

Mudanças importantes devem preservar versões anteriores. O estado atual não deve apagar a trajetória que levou até ele.

## 9. Ingestão

A entrada de informação é tratada como capacidade permanente. A arquitetura utiliza adaptadores por formato e uma representação intermediária comum, evitando acoplamento do Cérebro a um único formato.

Formatos previstos para a evolução da ingestão incluem DOCX, PDF, MHT/MHTML, HTML, TXT, Markdown, JSON e CSV, com possibilidade de novos adaptadores posteriormente.

## 10. Estado atual da maturidade

A V0.1 é uma fundação. Ela define identidade, contrato, relações, proveniência, histórico e arquitetura de ingestão. Não pretende ser ainda o Cérebro completo.

Ainda não fazem parte da fundação consolidada:

- migração integral do arquivo histórico;
- classificação automática sem revisão;
- grafo de conhecimento completo;
- automação inteligente total;
- arquitetura final de armazenamento;
- dependência obrigatória de uma IA, fornecedor ou plataforma.

## 11. Material de calibração

Os três materiais atuais considerados referência para a evolução são:

1. `Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx`
2. `Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx`
3. `Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx`

Eles devem permanecer preservados. A fotografia desta estrutura não os substitui.

## 12. Função deste arquivo

Este documento registra **como o Cérebro está estruturado neste ponto da evolução**. Ele poderá ser usado no futuro para:

- comparar versões da arquitetura;
- entender por que determinados componentes existem;
- identificar lacunas;
- orientar novas IAs e colaboradores;
- evitar perda de decisões anteriores;
- avaliar melhorias sem perder a base histórica.

Quando a estrutura mudar de maneira relevante, uma nova fotografia poderá ser criada/versionada em vez de apagar esta referência.
