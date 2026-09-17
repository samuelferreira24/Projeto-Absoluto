# Ingestão do Cérebro — V0.1

## Objetivo

Este diretório contém a primeira camada executável de ingestão do Cérebro do Projeto Absoluto.

A ingestão não transforma o arquivo original em conhecimento automaticamente. Ela deve preservar a fonte, registrar sua identidade e produzir uma representação intermediária que possa ser analisada posteriormente.

## Fluxo

```text
FONTE
  ↓
IDENTIFICAÇÃO
  ↓
REPRESENTAÇÃO INTERMEDIÁRIA
  ↓
METADADOS + INTEGRIDADE
  ↓
PROVENIÊNCIA
  ↓
REGISTRO DA FONTE
  ↓
ANÁLISE / EXTRAÇÃO DE CONHECIMENTO
```

## Princípios

- O original nunca é substituído pela representação extraída.
- Cada formato deve entrar por um adaptador substituível.
- A representação intermediária deve preservar estrutura sempre que possível.
- A origem de cada informação derivada deve ser rastreável.
- Falhas de ingestão devem ser registradas sem destruir a fonte.
- Ferramentas externas são componentes substituíveis, não o Cérebro.

## V0.1

A primeira implementação executável será deliberadamente pequena: validar a presença da camada de ingestão e estabelecer o contrato para futuros adaptadores. A implementação completa de DOCX/PDF/MHT e demais formatos será adicionada depois da validação do contrato com fontes reais.
