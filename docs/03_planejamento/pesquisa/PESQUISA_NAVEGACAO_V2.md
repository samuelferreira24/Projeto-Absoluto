# Pesquisa — Navegação e Pesquisa V2

## Escopo
Pesquisa independente da implementação do ABS em construção. Objetivo: avaliar a evolução da camada de navegação sobre múltiplas fontes, preservando proveniência e reconstruibilidade.

## Estado auditado
A V1 já fornece SQLite FTS5 + BM25, identidade multi-fonte, indexação incremental por SHA-256, símbolos Python/JS/TS/TSX/JSX, imports, inspeção, relações simples e histórico Git. Os PRs #96 e #97 estabeleceram a fundação e otimizaram a coleta de metadados Git e filtros.

## Evidência externa
- SQLite FTS5 oferece MATCH, frases, prefixos, tokenização configurável, BM25, snippets e filtros por coluna. A documentação também descreve riscos de inconsistência em tabelas de conteúdo externo e fornece comandos de integrity-check e rebuild. Fonte: documentação oficial SQLite.
- Tree-sitter é um parser incremental que produz árvores sintáticas concretas e pode ser reutilizado após edições; isso torna a técnica adequada para ampliar análise estrutural de código, mas adiciona dependências/grammars e não é necessária para a camada documental. Fonte: documentação oficial Tree-sitter.
- Git log fornece pesquisa temporal e pickaxe -S/-G; -S procura mudanças na quantidade de ocorrências e -G procura linhas adicionadas/removidas que correspondam a regex. Fonte: documentação oficial Git.
- Sistemas modernos de hybrid search combinam resultados lexicais e semânticos e frequentemente usam RRF ou normalização; a própria documentação do OpenSearch ressalta que a configuração ótima depende fortemente dos dados e comportamento do usuário. Portanto não há justificativa para tornar embeddings obrigatórios sem avaliação específica.

## Experimento arquitetural
Conjunto representativo de consultas:
1. conceito explícito;
2. localização de implementação;
3. localização de símbolo;
4. relação/import;
5. decisão/histórico;
6. consulta multi-repositório;
7. consulta com palavras diferentes;
8. inspeção e proveniência;
9. cadeia documento → relação → documento;
10. recuperação após alteração.

Resultado qualitativo esperado/observado pela natureza das fontes:
- lexical é forte quando os termos aparecem literalmente;
- estrutural é forte para código e símbolos;
- relacional é forte para dependências explícitas;
- temporal é forte para evolução e origem;
- semântico pode recuperar paráfrases, mas exige modelo, versionamento, custo e avaliação de relevância;
- híbrido é uma composição útil, mas só deve ser adicionada quando houver conjunto de julgamentos que demonstre ganho.

## Decisão
1. Manter FTS5/BM25 como base determinística e offline.
2. Fortalecer integridade e reconstrução do índice.
3. Criar uma camada de navegação/trace sobre os mecanismos existentes, em vez de acoplar consumidores às tabelas.
4. Melhorar proveniência e verificação na saída.
5. Ampliar segurança do indexador: symlinks, limites de tamanho, contenção de caminhos e erros explícitos.
6. Adicionar testes adversariais e de recuperação.
7. Não adicionar embeddings, banco vetorial ou Tree-sitter como dependência nesta rodada. Devem permanecer extensões futuras experimentais.
8. Reranking semântico também permanece opcional até existir benchmark/julgamento real.

## Modelo mínimo de objetos
A V2 deve tratar source/repository, document/file, symbol, relation e commit como objetos primários. Decisão, research, evidence, capability, state, artifact, memory e checkpoint não devem ser inferidos automaticamente só porque aparecem em texto; quando houver necessidade, deverão ser fontes/artefatos explicitamente indexados ou adaptadores futuros.

## Arquitetura aprovada para implementação
Sources → Indexes (lexical + structural + relations + temporal metadata) → Navigator/Trace API → provenance verification → consumers.

O índice continua sendo projeção derivada. A fonte original permanece autoridade.

## Limites
Não há evidência suficiente nesta rodada para declarar que embeddings melhoram a navegação real do Projeto Absoluto. Também não há justificativa para trocar SQLite por motor externo ou introduzir Tree-sitter em toda a indexação.

## Referências
- https://www.sqlite.org/fts5.html
- https://tree-sitter.github.io/tree-sitter/
- https://git-scm.com/docs/git-log
- https://docs.opensearch.org/latest/vector-search/ai-search/hybrid-search/
