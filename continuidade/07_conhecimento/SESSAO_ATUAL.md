# CHECKPOINT DE SESSÃO — 2026-09-23

## Projeto
Projeto Absoluto.

## Contexto
A continuidade foi construída para que o Projeto Absoluto não dependa do contexto de um único chat. ABS é apenas uma parte do Projeto; ABS V1 é o segundo protótipo do sistema e terá futuras versões.

## Descoberta crítica desta sessão
O problema não é apenas uma nova IA conseguir ler o repositório. O progresso produzido durante uma sessão também precisa ser persistido no repositório. Se a IA trabalhar apenas no chat e não registrar o resultado, esse progresso continua preso ao contexto da conversa.

## Estado técnico verificado
- AGENTS.md já orienta continuidade pelo repositório.
- A camada Project Knowledge já observa código, Git, testes, runtime, paths e evidências.
- O workflow Project Knowledge Sync existe e tenta persistir as projeções.
- Foi encontrado um defeito no workflow: `git diff --quiet` não detecta arquivos novos não rastreados. Por isso `project_knowledge.json` e `MAPA_AUTO_ESTADO_PROJETO.md` podem ser gerados no runner e depois descartados sem commit.
- A correção aplicada nesta sessão troca a verificação por `git status --porcelain -- <arquivos>`, permitindo detectar arquivos novos e modificados.
- As projeções ainda precisam ser confirmadas no main após a execução do workflow.

## Regra de continuidade
Mudança observável → evento → conhecimento estruturado → projeções → próxima IA.

Além disso:
Sessão produz progresso → checkpoint persistido → próximo chat lê o checkpoint.

## Próxima continuação
1. Confirmar que as projeções foram realmente gravadas no main.
2. Construir um mecanismo de checkpoint/handoff de sessão para registrar automaticamente fatos, resultados, pendências e próximo passo.
3. Integrar eventos GitHub/CI/runtime.
4. Evoluir descoberta automática de capacidades, ferramentas e caminhos.
5. Integrar com o daemon de atualização.

## Limite
Não alterar automaticamente visão, princípios ou decisões do Imperador.
