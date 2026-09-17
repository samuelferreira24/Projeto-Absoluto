# BASE V0.1 — Cérebro do Projeto Absoluto

## 1. Objetivo

Estabelecer uma fundação pequena, portátil e evolutiva para transformar materiais dispersos em memória e conhecimento rastreáveis, sem prender o projeto a GitHub, banco de dados, formato de arquivo ou fornecedor de IA.

## 2. O que a base precisa resolver

1. Identificar cada objeto do Cérebro com identidade própria.
2. Preservar a fonte original.
3. Registrar de onde uma informação veio.
4. Diferenciar fonte, memória, conhecimento, hipótese e interpretação.
5. Preservar versões e mudanças relevantes.
6. Representar relações entre objetos.
7. Permitir ingestão de vários formatos.
8. Permitir recuperação por texto e, futuramente, por semântica e relações.
9. Permitir que a estrutura evolua sem quebrar registros anteriores.

## 3. Princípios

### 3.1 Fonte não é conhecimento
Um documento é uma fonte. Uma conclusão extraída dele é outro objeto.

### 3.2 Original é preservado
Processamento, classificação ou resumo nunca substituem a fonte.

### 3.3 Identidade é independente da plataforma
IDs do Cérebro não dependem de IDs do GitHub, caminhos locais ou nomes de arquivos.

### 3.4 Proveniência é obrigatória para informação derivada
Uma afirmação importante deve poder apontar para sua origem.

### 3.5 Histórico não deve ser apagado
Alterações relevantes geram versões ou eventos históricos.

### 3.6 Relações são informação
O sistema deve saber não apenas o que existe, mas como os objetos se relacionam.

### 3.7 Automação deve ser auditável
Quando uma IA classificar ou derivar informação, o resultado deve registrar que foi produzido por processamento automático e manter a fonte usada.

### 3.8 Incerteza deve ser explícita
O sistema não deve transformar hipótese em fato apenas porque uma IA a classificou.

## 4. Tipos iniciais

- `FONTE`
- `DOCUMENTO`
- `IDEIA`
- `PESQUISA`
- `CONHECIMENTO`
- `HIPOTESE`
- `EVIDENCIA`
- `DECISAO`
- `PLANEJAMENTO`
- `EXPERIMENTO`
- `PROBLEMA`
- `ERRO`
- `RESULTADO`
- `EXPERIENCIA`
- `APRENDIZADO`
- `QUESTAO_ABERTA`
- `METODO`

A lista é extensível. Não deve ser tratada como enumeração definitiva do futuro sistema.

## 5. Contrato mínimo de registro

Todo registro deve poder representar, no mínimo:

```text
id
kind
title
created_at
updated_at
source
content
state
relations
provenance
version
```

Campos específicos podem ser adicionados conforme o tipo.

## 6. Estados iniciais

- `NOVO`
- `EM_ANALISE`
- `EM_TESTE`
- `VALIDADO`
- `REFUTADO`
- `SUPERADO`
- `ARQUIVADO`

Estado representa o estado do objeto, não a certeza absoluta sobre seu conteúdo.

## 7. Relações iniciais

- `deriva_de`
- `baseia_se_em`
- `contem`
- `relaciona_se_com`
- `gera`
- `testa`
- `produz`
- `causa`
- `corrige`
- `aprende_de`
- `influencia`
- `substitui`
- `contradiz`
- `depende_de`
- `faz_parte_de`

Novas relações podem ser adicionadas sem alterar a identidade dos objetos existentes.

## 8. Proveniência

A proveniência deve permitir responder:

- qual foi a fonte;
- qual versão da fonte;
- quando foi obtida;
- qual trecho, página, seção ou unidade originou o dado, quando disponível;
- quem ou qual processo produziu a derivação;
- se o conteúdo foi observado diretamente ou inferido;
- qual transformação foi aplicada.

## 9. Ingestão

A ingestão é uma capacidade permanente do Sistema, não um script descartável.

Fluxo:

```text
arquivo/fonte
    ↓
detecção de formato
    ↓
adaptador/conversor
    ↓
representação estruturada
    ↓
metadados + integridade
    ↓
proveniência
    ↓
memória de fonte
```

A camada deve ser preparada para DOCX, PDF, MHT/HTML, TXT, Markdown, CSV, JSON, Office, imagens e formatos futuros, sem exigir que o Cérebro conheça detalhes de cada formato.

## 10. Organização de material bagunçado

A V0.1 não exige reorganização física imediata dos arquivos.

Primeiro:

```text
material existente
    ↓
catálogo
    ↓
identidade
    ↓
extração
    ↓
classificação
    ↓
relações
    ↓
conhecimento derivado
```

O arquivo original permanece onde estava até existir uma decisão explícita de migração.

## 11. Pesquisas existentes

Uma pesquisa existente deve entrar como fonte/documento e depois ser analisada em unidades menores. O sistema deve separar:

- afirmações encontradas;
- evidências;
- interpretações;
- hipóteses;
- decisões derivadas;
- questões ainda abertas;
- aprendizados.

Uma única pesquisa pode originar vários registros relacionados.

## 12. Busca

A ordem evolutiva prevista é:

1. busca textual;
2. busca por metadados;
3. busca semântica;
4. busca por relações;
5. consultas híbridas.

Busca semântica não substitui a busca textual nem a proveniência.

## 13. O que não entra na V0.1

- grafo de conhecimento completo;
- migração automática de todo o acervo histórico;
- classificação automática sem revisão/auditoria;
- dependência obrigatória de um fornecedor de IA;
- dependência obrigatória do GitHub;
- exclusão ou substituição dos documentos atuais;
- arquitetura final do Cérebro.

## 14. Primeiro teste real

Os três materiais atuais indicados pelo usuário são candidatos ao primeiro conjunto de calibração:

1. `Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx`
2. `Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx`
3. `Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx`

Eles devem ser preservados e analisados como fontes. Não devem ser reescritos para se encaixar na estrutura.

## 15. Evolução

```text
BASE
 ↓
INGESTÃO
 ↓
REGISTRO CONTROLADO
 ↓
TESTE
 ↓
BUSCA
 ↓
RELAÇÕES
 ↓
CLASSIFICAÇÃO ASSISTIDA
 ↓
AUTOMAÇÃO AUDITÁVEL
 ↓
APRENDIZADO
 ↓
EVOLUÇÃO DA BASE
```

A V0.1 é uma fundação, não a arquitetura final do Projeto Absoluto.
