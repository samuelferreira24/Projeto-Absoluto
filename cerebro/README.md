# Cérebro do Projeto Absoluto

## Estado
BASE V0.1 — núcleo operacional em evolução.

A base já possui ingestão preservada, registro versionado, busca, relações, camada semântica, auditoria determinística, fachada operacional e uma interface para modelos de IA substituíveis.

## Lugar do Cérebro no Projeto
O Cérebro é uma capacidade do Projeto Absoluto, não o Projeto inteiro. O quadro maior da construção está em `especificacao/MAPA_MESTRE_PROJETO_ABSOLUTO_V0_1.md`.

## Objetivo
Criar uma camada independente de plataforma para preservar, organizar, relacionar, recuperar e reutilizar memória, conhecimento, experiências, decisões e aprendizados do Projeto Absoluto.

## Princípio central
O Cérebro não é apenas uma pasta de documentos, um banco de dados ou uma memória de chatbot. Ele é uma estrutura de conhecimento evolutiva que mantém:

- fontes e materiais originais;
- memória derivada desses materiais;
- conhecimento e evidências;
- experiências, erros e resultados;
- decisões e planejamentos;
- relações entre informações;
- proveniência e histórico;
- aprendizados aplicáveis à execução.

## Regra de preservação
Nenhum material original deve ser substituído pela interpretação extraída dele. A fonte permanece preservada e o conhecimento derivado aponta de volta para sua origem.

## Fluxo operacional

```text
FONTE
  ↓
INGESTÃO PRESERVADA
  ↓
REPRESENTAÇÃO ESTRUTURADA
  ↓
REGISTRO + HISTÓRICO
  ↓
REPRESENTAÇÃO SEMÂNTICA
  ↓
AUDITORIA
  ↓
RELAÇÕES + PROVENIÊNCIA
  ↓
RECUPERAÇÃO HÍBRIDA
  ↓
MODELOS / VERIFICAÇÃO
  ↓
CONHECIMENTO VALIDADO
  ↓
EXPERIÊNCIA / APRENDIZADO
  ↓
APLICAÇÃO NA EXECUÇÃO
```

## Arquitetura de modelos
O Cérebro não depende de uma IA específica. `cerebro/modelos.py` define um contrato para conectar diferentes modelos por papel, permitindo substituição de fornecedor, comparação e consenso quando isso gerar evidência útil. A IA propõe; a camada de auditoria e os critérios do Cérebro verificam.

## Recuperação
A recuperação atual combina normalização textual, pesos por campo e expansão por relações. A arquitetura foi deixada modular para receber futuramente embeddings, busca vetorial, reranking e contexto temporal sem substituir a camada determinística.

## Avaliação
`especificacao/AVALIACAO_SEMANTICA_V0_1.md` define os casos e critérios para validar distinções semânticas antes de ampliar a automação. `tests/test_avaliacao_semantica.py` cobre fatos, hipóteses, interpretações, decisões, ambiguidade, contradições, contexto temporal e referências externas.

## Estrutura

- `especificacao/` — contratos, arquitetura, método, avaliação e roadmap.
- `ingestao.py` — entrada e preservação de fontes.
- `nucleo.py` — registros, versionamento e histórico.
- `semantica.py` — representação semântica explícita.
- `auditoria.py` — verificações determinísticas.
- `recuperacao.py` — busca e expansão por relações.
- `modelos.py` — interface para múltiplos modelos/provedores.
- `servico.py` — fachada operacional integrada.
- `cli.py` — interface de operação.
- `tests/` — validação automatizada.

## Regra de evolução
A arquitetura deve evoluir sem destruir fontes, histórico, proveniência ou portabilidade. Componentes externos, modelos e interfaces são substituíveis; a identidade lógica do Cérebro permanece do Projeto Absoluto.

## Próximo estágio
Usar a avaliação semântica como base para ampliar a validação com dados reais, medir recuperação e relações, identificar limites de automação e só então avançar para capacidades semânticas mais fortes e consolidação auditável.
