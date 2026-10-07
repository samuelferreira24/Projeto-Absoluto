# Navegação de Conhecimento Verificável

Camada independente do ABS para aquisição, localização, expansão e verificação de conhecimento em múltiplas fontes. Pode ser usada diretamente por uma IA/operador antes do ABS e, depois, como capacidade nativa do ABS.

## Capacidades

- busca lexical SQLite FTS5 + BM25;
- símbolos e relações/importações;
- inspeção com conteúdo, hash e estado temporal;
- investigação orientada a evidências;
- cobertura mensurável, incluindo arquivos ignorados e não indexados;
- verificação de proveniência e integridade;
- múltiplos repositórios no mesmo índice;
- indexação incremental e remoções;
- histórico Git;
- interface Python estável e CLI JSON para IA.

## Indexar os dois repositórios

    python -m tools.navegacao.index --db .abs-navigation/index.sqlite \
      --repo projeto-absoluto=/caminho/Projeto-Absoluto \
      --repo sistema=/caminho/Sistema

## Usar diretamente por uma IA

    python -m tools.navegacao.ai --db .abs-navigation/index.sqlite "como a proveniência é verificada?"

Ou por JSON:

    echo '{"question":"onde fica o orquestrador?","source":"projeto-absoluto"}' | python -m tools.navegacao.ai --db .abs-navigation/index.sqlite

A CLI não importa abs_core. Se o ABS estiver parado, esta camada continua utilizável.

## API

    from tools.navegacao.navigator import KnowledgeNavigator
    nav = KnowledgeNavigator(".abs-navigation/index.sqlite")
    nav.search("memória temporal")
    nav.symbols("executor")
    nav.inspect("projeto-absoluto", "docs/00_MODELO_PROJETO_ABSOLUTO.md")
    nav.investigate("como a proveniência é verificada?")
    nav.coverage()

Navigator continua disponível como alias compatível.

## Validação real

    python -m tools.navegacao.validate_real --db /tmp/navigation.sqlite \
      --repo projeto-absoluto=/caminho/Projeto-Absoluto \
      --repo sistema=/caminho/Sistema \
      --report /tmp/navigation-report.json

A validação registra cobertura, indexação incremental/remoções, proveniência e uma matriz de consultas. Ela mede a capacidade sem confundir quantidade de registros com cobertura completa.

## Princípios

- não modifica as fontes;
- preserva origem e proveniência;
- é idempotente;
- pode ser apagada e reconstruída;
- não confunde índice com verdade;
- não depende de uma IA, modelo, banco vetorial ou fornecedor;
- respostas finais devem ser construídas a partir das evidências, não inventadas pelo navegador.

## Limites

A camada não finge compreensão semântica. Expansão por termos e estrutura é deliberadamente verificável. Embeddings, ranking híbrido, grafo semântico profundo e conectores externos podem ser adicionados depois, mas não são dependências do núcleo.
