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
- interface Python estável;
- CLI JSON para uma investigação;
- protocolo JSONL persistente para uma IA operar search/symbols/inspect/related/investigate/coverage/verify.

## Indexar os dois repositórios

    python -m tools.navegacao.index --db .abs-navigation/index.sqlite \
      --repo projeto-absoluto=/caminho/Projeto-Absoluto \
      --repo sistema=/caminho/Sistema

## Usar diretamente por uma IA

Investigação única:

    python -m tools.navegacao.ai --db .abs-navigation/index.sqlite "como a proveniência é verificada?"

Protocolo de agente persistente:

    python -m tools.navegacao.agent --db .abs-navigation/index.sqlite

Cada linha de entrada é um JSON, por exemplo:

    {"action":"search","query":"orquestrador","source":"projeto-absoluto","limit":10}
    {"action":"investigate","question":"como a proveniência é verificada?","limit":8}
    {"action":"inspect","source":"projeto-absoluto","path":"tools/navegacao/navigator.py"}

Cada resposta é JSONL com ok=true/false. A interface não importa abs_core. Se o ABS estiver parado, a navegação continua utilizável.

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

A validação registra cobertura, indexação, remoções, proveniência e uma matriz de consultas. Ela mede a capacidade sem confundir quantidade de registros com cobertura completa.

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
