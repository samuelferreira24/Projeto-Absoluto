# Arquitetura de Ingestão V0.1

## Objetivo

Criar uma capacidade permanente para receber fontes heterogêneas sem acoplar o Cérebro a um formato específico.

## Arquitetura lógica

```text
FONTE
  ↓
DETECTOR
  ↓
ADAPTADOR DE FORMATO
  ↓
REPRESENTAÇÃO INTERMEDIÁRIA
  ↓
NORMALIZAÇÃO
  ↓
METADADOS + INTEGRIDADE
  ↓
PROVENIÊNCIA
  ↓
REGISTRO DE FONTE
  ↓
ANÁLISE / EXTRAÇÃO DE CONHECIMENTO
```

## Regra de extensão

Cada formato novo deve ser adicionado por um adaptador, sem alterar o contrato dos registros do Cérebro.

## Representação intermediária

A representação intermediária deve preservar, quando disponível:

- texto;
- hierarquia;
- títulos/seções;
- tabelas;
- imagens e referências;
- ordem de leitura;
- páginas ou posições;
- metadados;
- origem/proveniência.

A camada de conhecimento não deve depender diretamente da API interna de um extrator.

## Primeiros formatos

Prioridade inicial de validação:

1. DOCX
2. PDF
3. MHT/HTML
4. TXT
5. Markdown
6. JSON
7. CSV

A lista é extensível.

## Ferramentas

A escolha de biblioteca concreta deve ser tratada como implementação substituível. A arquitetura deve permitir usar uma biblioteca especializada de documentos, bibliotecas nativas ou combinações delas sem mudar o modelo do Cérebro.

## Auditoria

Toda ingestão deve registrar:

- fonte original;
- formato detectado;
- ferramenta/adaptador utilizado;
- versão da ferramenta, quando disponível;
- data/hora;
- sucesso ou erro;
- identificador/hash da fonte, quando possível;
- relação entre fonte e representação produzida.

## Segurança de evolução

Falha ao interpretar um formato não pode apagar ou modificar a fonte original. O erro de ingestão deve ser registrado como evento técnico e a fonte permanece disponível para novo processamento.
