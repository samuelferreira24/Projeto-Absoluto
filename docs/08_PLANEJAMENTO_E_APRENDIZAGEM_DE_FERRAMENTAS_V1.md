# Planejamento e aprendizagem de ferramentas — ABS V1

A camada de recursos agora evolui de catálogo/roteamento para planejamento baseado em conhecimento.

Fluxo:

OBJETIVO → CAPACIDADES → CONHECIMENTO DE FERRAMENTAS → ROTAS → PLANO → AUTORIZAÇÃO → EXECUÇÃO → EVIDÊNCIA → APRENDIZADO

O `ToolPlanner` não executa uma ferramenta e não concede autorização. Ele produz opções de uso fundamentadas no conhecimento disponível e nas rotas atualmente acessíveis.

O `ToolLearningEngine` registra resultados observados como evidência explícita. Uma ferramenta só muda para `validated` quando um resultado bem-sucedido é informado junto com evidência.

Isso cria a separação necessária entre:

- ferramenta conhecida;
- ferramenta descoberta;
- ferramenta catalogada;
- ferramenta validada;
- caminho operacional;
- ferramenta em degradação.

O conhecimento também pode acumular lições e padrões de uso. Assim, o ABS pode melhorar a forma como utiliza uma ferramenta sem depender de uma única IA ou de um único fornecedor.

A descoberta continua aberta: novas ferramentas podem ser encontradas por pesquisa, documentação, conectores, dispositivos, redes ou necessidades descobertas durante a execução.
