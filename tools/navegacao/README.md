# Navegação e Pesquisa V1

Camada independente do ABS em construção. Pode ser usada diretamente por uma IA/operador e posteriormente pelo ABS.

## Capacidades atuais

- **Busca lexical:** SQLite FTS5 + BM25, snippets e filtros por fonte, caminho e extensão.
- **Busca estrutural:** símbolos de Python/JS/TS/TSX/JSX e imports/dependências.
- **Navegação de objeto:** conteúdo, hash, estado temporal, símbolos e relações.
- **Navegação relacional:** encontrar documentos que importam/referenciam um alvo, com filtro de tipo.
- **Navegação temporal:** SHA/data do último commit e pesquisa Git por alteração.
- **Múltiplas fontes:** qualquer quantidade de repositórios no mesmo índice, preservando source_id.
- **Indexação incremental:** arquivos inalterados não são reprocessados.
- **Metadados Git eficiente:** o histórico é obtido por repositório, evitando uma chamada Git por arquivo.

## Comandos

Indexar ambos:

~~~bash
python -m tools.navegacao.index --db .abs-navigation/index.sqlite \
  --repo projeto-absoluto=/caminho/Projeto-Absoluto \
  --repo sistema=/caminho/Sistema
~~~

Busca geral:

~~~bash
python -m tools.navegacao.search --db .abs-navigation/index.sqlite "memória temporal"
~~~

Busca com filtros:

~~~bash
python -m tools.navegacao.search --db .abs-navigation/index.sqlite \
  --source projeto-absoluto --path-prefix docs/ --extension md "governança"
~~~

Busca de símbolos:

~~~bash
python -m tools.navegacao.search --db .abs-navigation/index.sqlite \
  --symbols --kind function "executor"
~~~

Relações:

~~~bash
python -m tools.navegacao.related --db .abs-navigation/index.sqlite \
  --type imports "abs_core"
~~~

Histórico:

~~~bash
python -m tools.navegacao.history --repo /caminho/Projeto-Absoluto "memória"
python -m tools.navegacao.history --repo /caminho/Projeto-Absoluto --regex "memory|memória"
~~~

Inspeção:

~~~bash
python -m tools.navegacao.inspect --db .abs-navigation/index.sqlite \
  --source projeto-absoluto --path docs/00_MODELO_PROJETO_ABSOLUTO.md
~~~

## Princípios

- não modifica as fontes;
- preserva origem e proveniência;
- é idempotente;
- pode ser apagada e reconstruída;
- não confunde índice com verdade;
- mantém camadas avançadas opcionais;
- não depende de uma IA, modelo, banco vetorial ou fornecedor.

## Limites deliberados

A V1 não finge ter compreensão semântica. Embeddings, grafo semântico mais profundo, pesquisa web/conectores e ranking híbrido podem ser adicionados posteriormente e precisam ser validados contra casos reais.