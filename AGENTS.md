# Projeto Absoluto — entrada para agentes

Antes de construir, descubra o estado atual do Projeto. Não dependa da memória da conversa.

## Ordem mínima

1. `continuidade/07_conhecimento/00_LEIA_PRIMEIRO.md`
2. `continuidade/07_conhecimento/project_knowledge.json` (se presente)
3. `cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`
4. estado atual, código e testes relevantes
5. histórico/decisões somente quando necessário

## Regras

- Projeto Absoluto é maior que ABS.
- ABS é uma parte do Sistema do Projeto.
- Verificar antes de construir.
- Mapa não é implementação.
- Hipótese não é decisão.
- Documentação não prova capacidade.
- Não alterar silenciosamente visão/princípios/decisões do Imperador.
- Preferir integração e reutilização a duplicação.
- Mudanças observáveis devem alimentar a camada de conhecimento.
- Ao criar uma nova capacidade/caminho, registrar evidência e proveniência.

## Continuidade

Se o chat terminar, o próximo agente deve conseguir continuar lendo o repositório. O repositório é o mecanismo de continuidade; a conversa é apenas uma sessão de trabalho.

## Regra de persistência da sessão

O contexto produzido durante uma sessão não pode permanecer somente no chat quando ele altera o estado do Projeto. Antes de encerrar ou transferir uma sessão, o agente deve persistir no repositório os fatos novos, decisões autorizadas, resultados, evidências, pendências e próximo ponto de continuação. O novo agente deve ler esse estado antes de continuar.

A continuidade automática observa o que mudou no repositório; ela não consegue capturar uma conversa que nunca foi persistida. Portanto, trabalho concluído sem registro no repositório continua sendo contexto de chat e não é considerado continuidade do Projeto.
