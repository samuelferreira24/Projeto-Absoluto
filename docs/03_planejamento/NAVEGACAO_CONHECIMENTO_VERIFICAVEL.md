# Navegação de Conhecimento Verificável

A antiga Navegação V2 passa a ser tratada como uma capacidade independente: Navegação de Conhecimento Verificável.

## Propósito

A camada existe em dois estados igualmente válidos:

1. Pré-ABS: uma IA ou operador pode usá-la diretamente, sem depender do runtime, Cérebro ou Orquestrador do ABS.
2. ABS: o ABS pode incorporá-la como capacidade de aquisição, localização, expansão e verificação de conhecimento.

Ela não é o cérebro e não produz uma resposta por conta própria. Ela fornece evidência navegável para que uma IA possa responder com base em fontes reais.

## Contrato para IA

Entrada: pergunta/objetivo, fonte opcional e limites de exploração.

Saída: documentos candidatos, símbolos, relações, conteúdo inspecionado, SHA-256 e último commit conhecido.

CLI independente:

    python -m tools.navegacao.ai --db .abs-navigation/index.sqlite "como a proveniência é verificada?"

Também aceita JSON via stdin:

    echo '{"question":"onde fica o orquestrador?","source":"projeto-absoluto"}' | python -m tools.navegacao.ai --db .abs-navigation/index.sqlite

Nenhuma chamada importa abs_core. A capacidade continua operacional mesmo que o ABS esteja indisponível.

## Camadas

- Aquisição: indexação local de múltiplos repositórios, atualização incremental e remoções.
- Localização: FTS5/BM25, símbolos, filtros por fonte/caminho/extensão e relações/importações.
- Expansão: investigação por múltiplos termos, inspeção e relações.
- Verificação: SHA-256, integridade FTS e cobertura explícita.
- Memória temporal: último commit/data e histórico Git pela ferramenta existente.

## Limite

A camada não afirma compreensão semântica onde não existe. A investigação amplia a consulta por termos e estrutura; a resposta final deve ser construída pela IA a partir das evidências.

Embeddings, ranking híbrido, grafo semântico profundo e conectores externos são extensões futuras, não pré-requisitos do núcleo.

## Compatibilidade

A classe Navigator e o pacote tools.navegacao permanecem para compatibilidade. A nomenclatura conceitual nova é Navegação de Conhecimento Verificável.
