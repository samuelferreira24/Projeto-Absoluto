# Scheduler / Orquestrador Adaptativo V0.1

## Objetivo

Transformar o grafo de tarefas do Cérebro em um sistema de planejamento adaptativo que decide o que executar, quando executar, em paralelo ou em sequência, com quais recursos/executores e sob quais restrições, reavaliando o plano conforme novos resultados aparecem.

## Princípios

1. Dependências duras bloqueiam execução.
2. Recursos compartilhados limitam concorrência.
3. Combustível é um orçamento explícito e separado do valor lógico da tarefa.
4. Prioridade não é suficiente: valor esperado, custo, tempo, risco, incerteza, prazo e comunicação entram na decisão.
5. Paralelização é uma decisão contextual, não uma regra fixa.
6. Resultado real atualiza perfis de confiabilidade e tempo.
7. Falhas podem acionar retry ou fallback sem apagar o histórico da falha.
8. Cancelamentos são eventos históricos e podem propagar para dependentes.
9. Mudanças de cenário provocam replanejamento.
10. A seleção de executor é dinâmica e pode considerar capacidades, ferramentas e modelos.
11. Decisões de planejamento e motivos de mudança permanecem persistidos.
12. Experiências de orquestração alimentam o Cérebro para reutilização futura.

## Modelo de decisão

A pontuação inicial de uma tarefa considera:

valor_esperado = (valor + oportunidade) × (1 - risco) × (1 - incerteza) × confiabilidade

A pontuação também considera custo, tempo observado/estimado, urgência derivada do prazo e comunicação.

Não existe uma função universalmente ótima. O Scheduler pode gerar planos sob diferentes estratégias e preservar as alternativas.

## Paralelo versus sequencial

O Scheduler escolhe PARALELO quando as tarefas selecionadas são independentes e os recursos suportam a concorrência.

Escolhe SEQUENCIAL quando há dependência entre tarefas selecionadas, quando a execução é explicitamente forçada ou quando a comunicação estimada torna a coordenação paralela pouco atraente.

O tempo de um lote paralelo é aproximado pelo maior tempo de seus componentes; o tempo sequencial é a soma.

## Recursos e combustível

Recursos são capacidades operacionais, por exemplo CPU, GPU ou uma ferramenta exclusiva.

Combustível representa recursos consumíveis, por exemplo créditos, tokens, orçamento de execução ou capacidade computacional contratada.

A separação permite otimizar capacidade e consumo de forma independente.

## Seleção dinâmica de executor

PerfilExecutor registra:
- capacidades;
- ferramentas;
- modelos;
- confiabilidade;
- fator de tempo;
- multiplicador de custo;
- consumo de combustível;
- concorrência suportada.

A escolha é feita no momento do planejamento. O histórico de execução pode alterar a confiabilidade e o fator de tempo percebidos.

## Replanejamento

Fluxo:

Grafo → candidatos → seleção → execução → resultado → atualização de experiência → replanejamento

Novas informações podem ser registradas no cenário e usadas na próxima decisão.

## Retry, fallback e cancelamento

Retry reabre uma tarefa falha sem apagar o registro da falha.

Fallback ativa uma tarefa alternativa previamente declarada quando a principal falha.

Cancelamento marca a tarefa como CANCELADA e pode propagar o cancelamento aos dependentes quando solicitado.

## Aprendizado

Cada resultado relevante pode gerar histórico operacional, atualização do perfil da tarefa, aprendizado persistente, evidência e contexto.

Isso cria a ponte:

execução → experiência → aprendizado → próxima decisão

## Meta-orquestração

O Scheduler preserva estratégias e padrões de execução. A próxima evolução deve permitir que o Meta-Cérebro compare sistematicamente estratégia, contexto, recursos, executor, custo, tempo, risco, resultado, qualidade e sinergias.

A partir daí, poderá aprender como escolher melhor o próprio método de orquestração, em vez de apenas escolher tarefas.

## Limites do V0.1

Ainda não há:
- solver matemático global;
- otimização multiobjetivo exata;
- execução assíncrona real de ferramentas;
- observabilidade distribuída;
- comunicação entre agentes em tempo real;
- aprendizado estatístico de políticas;
- detecção causal de sinergia.

Esses pontos ficam como camadas posteriores. O V0.1 estabelece interfaces e histórico necessários para evoluir sem reescrever o núcleo.
