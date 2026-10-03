# Navegação e Pesquisa V1

Camada independente de navegação sobre múltiplas fontes. A V1 foi desenhada para funcionar sem depender do ABS em construção.

## Fontes

Uma instância pode indexar qualquer quantidade de repositórios. Cada documento mantém `source_id`, raiz, caminho e tipo temporal/origem. O caso inicial previsto é:

- `projeto-absoluto`
- `sistema`

## Capacidades V1

- índice local SQLite;
- FTS5 com BM25;
- busca por texto, caminho e fonte;
- snippets/highlights;
- filtros por repositório;
- navegação por caminho;
- atualização incremental por SHA do conteúdo;
- metadados para estado/origem/histórico;
- contrato preparado para adicionar busca semântica, símbolos e grafo sem trocar a interface de pesquisa.

## Uso

```bash
python -m tools.navegacao.index --db .abs-navigation/index.sqlite \
  --repo projeto-absoluto=/caminho/Projeto-Absoluto \
  --repo sistema=/caminho/Sistema

python -m tools.navegacao.search --db .abs-navigation/index.sqlite \
  "memória temporal"
```

Para limitar a uma fonte:

```bash
python -m tools.navegacao.search --db .abs-navigation/index.sqlite \
  --source sistema "memória"
```

A V1 não altera os repositórios-fonte. O índice é derivado e pode ser reconstruído.
