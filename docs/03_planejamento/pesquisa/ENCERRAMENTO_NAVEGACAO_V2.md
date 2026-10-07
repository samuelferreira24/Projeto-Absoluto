# Encerramento da Navegação V2

Esta validação registra o fechamento operacional da Navegação/Pesquisa V2.

Escopo validado:
- busca lexical FTS5/BM25;
- busca estrutural por símbolos;
- relações/importações;
- metadados temporais Git;
- múltiplas fontes;
- indexação incremental e remoção;
- facade Navigator;
- proveniência por SHA-256;
- integridade e reconstrução do FTS5;
- proteção contra symlinks e arquivos acima do limite;
- suíte de testes de navegação integrada ao workflow Project Knowledge Tests.

A V2 permanece deliberadamente sem busca semântica obrigatória, embeddings ou grafo semântico avançado. Essas camadas são futuras e dependem de validação própria.

Este documento é um registro de encerramento da V2, não uma nova implementação.
