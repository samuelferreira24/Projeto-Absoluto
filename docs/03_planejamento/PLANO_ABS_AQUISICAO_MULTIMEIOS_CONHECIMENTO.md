# PLANO ABS — AQUISIÇÃO MULTIMEIOS DE CONHECIMENTO

## 1. Objetivo
Dar ao ABS capacidade progressiva de descobrir, acessar, coletar, preservar, organizar, atualizar e recuperar informações de diferentes meios. O objetivo não é baixar a Internet inteira, mas permitir que o Imperador determine fontes, assuntos, consultas ou monitoramentos e o ABS escolha o melhor meio disponível.

## 2. Princípio central
A aquisição é uma capacidade do ABS, não de uma interface.

IMPERADOR → INTERFACE/API/AUTOMAÇÃO → AQUISIÇÃO ABS → ADAPTADOR → DADO ORIGINAL → PROVENIÊNCIA → BIBLIOTECA → BUSCA/RECUPERAÇÃO → IAs/AGENTES/INTERFACES

Terceiros entram como motores auxiliares. O ABS controla contratos, armazenamento, proveniência e substituição.

## 3. Meios de aquisição
- Motores de busca e metabusca.
- Busca de notícias, imagens e vídeos.
- APIs REST/GraphQL e APIs oficiais.
- HTTP/HTTPS e páginas HTML.
- RSS/Atom e sitemaps.
- Crawling e scraping.
- Browser automation.
- PDFs, documentos, planilhas, CSV, JSON e XML.
- Bases acadêmicas, governamentais e datasets.
- Repositórios de código e documentação.
- OCR, áudio, vídeo e transcrição.
- Fontes autenticadas autorizadas.
- Dados do Android, sensores e outros nós no futuro.

## 4. Camada de aquisição ABS
Criar uma abstração única para: search, fetch, extract, crawl, subscribe, download, query_api, monitor e discover.

Cada fornecedor entra por adaptador. Exemplos: search/brave, search/searxng, crawl/apify, crawl/scrapy, query_api/openalex, query_api/crossref, query_api/github.

A troca de fornecedor não deve exigir alteração do núcleo.

## 5. Biblioteca de conhecimento
Preservar conteúdo original, fonte/URL ou identificador, autor/organização, datas, método de aquisição, hash, versão, relações e histórico de processamento.

Primeira implementação: arquivos + SQLite. Depois: busca textual, indexação, embeddings, busca semântica, relações/grafo quando justificadas e sincronização entre nós.

## 6. Peças de terceiros para V1
Brave Search API: descoberta Web, notícias, imagens, vídeos e resultados estruturados.
SearXNG: metabusca open source, self-hosted e agregação de múltiplos mecanismos.
Tavily: busca, extração e crawling orientados a pesquisa.
Apify: scraping, crawling e browser automation.
OpenAlex: trabalhos, autores, instituições e tópicos acadêmicos.
Crossref: DOI e metadados bibliográficos.
Common Crawl: grandes conjuntos históricos da Web.
GitHub API: repositórios, código, issues, documentação e releases.

## 7. Estratégia de custo
Começar com recursos gratuitos e capacidades que já existem no ABS. Prioridade: HTTP/RSS/APIs públicas, SearXNG quando houver ambiente adequado, franquias gratuitas e só depois uso pago ou infraestrutura adicional.

Não contratar vários serviços pagos simultaneamente.

## 8. Evolução
Fase 0 — fundação: contrato, proveniência, armazenamento, deduplicação, logs, limites, erros e autorização.
Fase 1 — pequeno: HTTP, APIs, RSS, arquivos, uma busca Web, uma extração Web e biblioteca local.
Fase 2 — ampliação: múltiplos motores, crawling, sitemap, monitoramento, notícias, acadêmico, GitHub e datasets.
Fase 3 — automação: fontes monitoradas, coleta periódica, detecção de novidade, atualização incremental, classificação e indexação.
Fase 4 — inteligência: pesquisa multi-etapas, cruzamento de fontes, verificação, síntese com citações e recuperação para qualquer IA.
Fase 5 — independência: SearXNG próprio, crawlers e extratores próprios, conectores próprios, múltiplos provedores, redundância e nós distribuídos.

## 9. Interfaces
Interfaces não são a camada de aquisição. Open WebUI, LibreChat, AnythingLLM, Dify e a interface própria apenas utilizam a capacidade do ABS.

## 10. Distribuição
Não instalar todos os componentes no telefone. O telefone é inicialmente ponto de comando, ABS Core, armazenamento inicial, IA local e ambiente de testes. Componentes pesados podem posteriormente ir para VPS, servidor próprio, outro Android ou outros nós.

## 11. Aplicativos/componentes
Já existentes e manter: Termux, Git, Python, llama.cpp, Qwen local, navegador Android e ABS Core/Gateway.

Não instalar agora: Jan, Dify completo no telefone, LibreChat completo no telefone, AnythingLLM completo no telefone e múltiplos crawlers simultaneamente.

Open WebUI continua candidato para teste, mas em ambiente Python isolado: a documentação atual suporta Python 3.11/3.12, enquanto o ABS usa Python 3.14.6.

Brave Search API, Tavily, OpenAlex, Crossref e GitHub API são serviços/conectores, não aplicativos obrigatórios do Android.

## 12. Primeiro conjunto operacional
1. ABS HTTP existente.
2. RSS.
3. APIs públicas.
4. Brave Search API ou SearXNG.
5. Tavily para extração/crawl.
6. Biblioteca local ABS.
7. Proveniência.
8. Recuperação para Qwen e demais IAs.

Adicionar um meio por vez.

## 13. Critério de sucesso
O Imperador fornece uma pergunta ou fonte e o ABS consegue descobrir/acessar o conteúdo, extrair o dado, preservar o original, registrar a origem, armazenar no celular, recuperar depois e entregar o conhecimento para uma IA com sua proveniência.

## 14. Regra permanente
CAPACIDADE ABS → CONTRATO ABS → ADAPTADORES → TERCEIROS/PRÓPRIOS.

A capacidade permanece mesmo quando um fornecedor é removido.

## 15. Estado
Planejamento técnico inicial concluído.
Complementa PLANO_ABS_V1_CURTO_MEDIO_LONGO_PRAZO.md, ARQUITETURA_MULTIPLAS_INTERFACES_ABS.md e AUDITORIA_INTERFACES_ABS.md.
Próxima implementação: construir o contrato e o primeiro pipeline mínimo de aquisição sem alterar o núcleo já operacional.