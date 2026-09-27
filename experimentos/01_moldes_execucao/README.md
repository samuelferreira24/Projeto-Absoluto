# Experimento 01 — Família de Moldes de Execução

## Objetivo

Testar empiricamente uma hipótese arquitetural antes de alterar o núcleo do ABS:

> O ABS deve poder possuir vários moldes de execução, ativá-los por critérios ou por comando explícito do Imperador, combiná-los quando necessário e trocar de molde quando o contexto/resultado exigir.

Este experimento **não define a arquitetura oficial do ABS**.

## Moldes testados

1. DIRECT — execução direta.
2. WORKFLOW — sequência determinística de etapas.
3. AGENT — execução adaptativa para problemas abertos/incertos.
4. MULTIAGENT — decomposição em partes independentes/paralelizáveis.
5. RESEARCH — exploração ampla de possibilidades e evidências.
6. RECOVERY — recuperação, fallback ou mudança de estratégia após falha.

O número seis é apenas o conjunto inicial do experimento.

## Hipótese

Uma arquitetura de família de moldes pode ser mais flexível que um único molde universal se:

- conseguir escolher um molde adequado por critérios;
- aceitar override explícito do Imperador;
- puder combinar moldes;
- puder trocar de molde quando o estado mudar;
- não usar complexidade maior quando uma execução simples basta;
- não confundir recurso disponível com estratégia adequada.

## O que o experimento mede

- seleção automática;
- seleção explícita;
- complexidade mínima suficiente;
- composição;
- troca de molde;
- recuperação;
- independência entre molde e recurso;
- comportamento diante de contexto alterado.

## Limitação

Este é um experimento de controle/seleção. Ele não prova que os seis moldes sejam suficientes para o ABS real nem prova AGI, autonomia geral ou superioridade de um framework externo.

## Critério de avanço

Só considerar a hipótese fortalecida se os casos passarem sem precisar codificar uma regra específica para cada exemplo.

Se o experimento revelar que o seletor precisa conhecer cada missão individualmente, isso será tratado como falha arquitetural e registrado.
