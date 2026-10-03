# Navegação e Pesquisa V1

Camada independente do ABS em construção. Pode ser usada diretamente por uma IA/operador e posteriormente pelo ABS.

## O que a V1 já faz

- **Busca lexical:** SQLite FTS5 + BM25, snippets e filtros.
- **Busca estrutural:** símbolos de Python/JS/TS/TSX/JSX e imports/dependências.
- **Navegação de objeto:** inspeção de um arquivo com conteúdo, hash, estado temporal, símbolos e relações.
- **Navegação relacional:** encontrar documentos que importam/referenciam um alvo.
- **Navegação temporal:** SHA/data do último commit e pesquisa Git por alteração.
- **Múltiplas fontes:** qualquer quantidade de repositórios no mesmo índice, preservando `source_id`.

## Fontes iniciais

- `projeto-absoluto`
- `sistema`

## Comandos

```bash
python -m tools.navegacao.index --db .abs-navigation/index.sqlite \
  --repo projeto-absoluto=/caminho/Projeto-Absoluto \
  --repo sistema=/caminho/Sistema

python -m tools.navegacao.search --db .abs-navigation/index.sqlite "memória temporal"
python -m tools.navegacao.search --db .abs-navigation/index.sqlite --source sistema "memória"
python -m tools.navegacao.search --db .abs-navigation/index.sqlite --symbols "executor"

python -m tools.navegacao.inspect --db .abs-navigation/index.sqlite \
  --source projeto-absoluto --path docs/00_MODELO_PROJETO_ABSOLUTO.md

python -m tools.navegacao.related --db .abs-navigation/index.sqlite "abs_core"

python -m tools.navegacao.history --repo /caminho/Projeto-Absoluto "memória"
```

## Princípios

- não modifica as fontes;
- preserva origem;
- é idempotente;
- pode ser apagada e reconstruída;
- não confunde índice com verdade;
- camadas avançadas são opcionais;
- não depende de uma IA, modelo, banco vetorial ou fornecedor.

## Limites deliberados

A V1 **não finge ter compreensão semântica**. Busca por significado/embeddings, grafo semântico mais profundo, pesquisa web/conectores e ranking híbrido podem ser adicionados como camadas posteriores e testadas contra casos reais. Isso preserva qualidade e evita introduzir um modelo/serviço como dependência obrigatória.
