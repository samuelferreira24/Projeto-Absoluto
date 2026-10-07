# Fechamento — Navegação de Conhecimento Verificável

Data da validação: 2026-10-07

## Estado

A Navegação de Conhecimento Verificável foi validada como capacidade independente e foi integrada à main do Projeto-Absoluto pelo PR #107.

Commit de merge: b26b350cc7171bba24a3259dd2119698ea1e9918.

Ela continua independente do runtime ABS e pode ser usada diretamente por uma IA através da API Python, CLI e protocolo JSONL/STDIO.

## Evidência final

- 157 testes automatizados passaram no ABS Core.
- Workflow de testes do conhecimento passou.
- Validação real dos dois repositórios: **PASS**.
- Repositórios auditados: projeto-absoluto e sistema.
- Documentos indexados: Projeto-Absoluto 387; Sistema 38; total 425.
- Candidatos textuais descobertos: 425.
- Candidatos textuais não indexados: 0.
- Entradas obsoletas no índice: 0.
- Cobertura: 1.0 / 100% dos candidatos textuais definidos pelo indexador.
- Proveniência verificada: 425 documentos; inválidos: 0.
- Projeto-Absoluto: 1.004 símbolos e 934 relações.
- Sistema: 158 símbolos e 84 relações.
- Matriz de consultas: arquivo, conceito, estrutura, implementação, verificação, agente, cross-repo e documentação — todas com evidência.
- Testes adversariais: termos em português/inglês, nomes de símbolos, arquivo, conceitos e JSONL — todos com hit.
- Lifecycle: atualização incremental, mutação externa detectada por hash e deleção — **PASS**.
- Protocolo de agente no índice real: **PASS**; investigação retornou evidências e cobertura retornou as fontes.

## Defeito encontrado e corrigido durante o fechamento

Os testes de lifecycle revelaram um problema real na manutenção do FTS5 externo durante atualização/deleção: a estratégia anterior podia produzir "database disk image is malformed".

A implementação foi corrigida para tratar documents_fts como índice FTS5 de conteúdo externo e reconstruí-lo após as mutações da tabela de documentos. A correção foi então coberta por testes de atualização, deleção e integridade.

## O que foi efetivamente provado

1. localizar documentos;
2. localizar símbolos;
3. navegar por relações;
4. inspecionar conteúdo;
5. preservar fonte, caminho, hash e metadados Git;
6. investigar perguntas como bundle de evidências;
7. detectar alterações externas;
8. atualizar incrementalmente;
9. remover documentos apagados;
10. medir cobertura;
11. operar sobre múltiplas fontes;
12. ser usada por uma IA sem o ABS estar funcionando;
13. executar pelo protocolo de agente JSONL/STDIO;
14. validar o comportamento contra os dois repositórios reais.

## Limites explícitos

Este fechamento não declara compreensão semântica perfeita nem recuperação de qualquer conceito que não possua representação recuperável na fonte/indexador.

O núcleo continua deliberadamente verificável e independente de modelo, fornecedor, embeddings ou banco vetorial. Ranking híbrido, embeddings, grafo semântico profundo e conectores externos continuam sendo extensões futuras, não dependências do núcleo.

## Decisão

**Navegação de Conhecimento Verificável — V1 standalone: FECHADA.**

A próxima etapa pode ser a integração nativa dessa capacidade ao ABS.
