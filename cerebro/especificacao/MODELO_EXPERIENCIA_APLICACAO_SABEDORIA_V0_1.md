# MODELO DE EXPERIÊNCIA, APLICAÇÃO E SABEDORIA — V0.1

## Objetivo

O Cérebro não deve apenas acumular informação ou conhecimento. Deve transformar experiência em aprendizado reutilizável e, quando houver evidência suficiente, em sabedoria aplicada: orientação contextual para melhorar decisões e ações futuras.

## Base conceitual

Pesquisas sobre aprendizagem organizacional distinguem processos de busca, criação, retenção e transferência de conhecimento; a retenção sem transferência não produz toda a capacidade possível. Estudos sobre aprendizagem a partir de experiências também mostram que a forma de codificar e generalizar experiências influencia a qualidade das decisões futuras. citeturn0search12turn0search1

A literatura sobre lições aprendidas converge na necessidade de transformar experiências positivas e negativas em recomendações transferíveis, em vez de apenas arquivar relatos. Revisões sobre After-Action Reviews mostram o valor de registrar o que aconteceu, por que aconteceu e como evitar repetição de erros. citeturn1search15turn1search2

Estudos sobre sabedoria aplicada à decisão destacam compreensão do contexto, reflexão, julgamento, valores e capacidade de agir, e não apenas posse de informação. citeturn0search2turn0search5

Pesquisas recentes sobre memória de agentes também apontam uma evolução de armazenamento para reflexão e abstração de experiências, com o objetivo de produzir aprendizado contínuo e consistência de longo prazo. citeturn0academia48

## Ciclo operacional

```text
INFORMAÇÃO
    ↓
CONHECIMENTO
    ↓
COMPREENSÃO
    ↓
EXPERIÊNCIA
    ↓
RESULTADO
    ↓
REFLEXÃO / AVALIAÇÃO
    ↓
LIÇÃO APRENDIDA
    ↓
GENERALIZAÇÃO CONTROLADA
    ↓
SABEDORIA APLICADA
    ↓
DECISÃO
    ↓
AÇÃO
    ↓
NOVO RESULTADO
    ↺
```

## Princípios

1. Fonte não é sabedoria.
2. Conhecimento não implica aplicação correta.
3. Experiência deve preservar contexto, ação, resultado e evidência.
4. Lição aprendida deve apontar para experiências de origem.
5. Generalização deve ser controlada: uma experiência não vira regra universal automaticamente.
6. Sabedoria deve registrar condições de aplicação e limites.
7. Sabedoria validada exige evidência; não pode ser apenas uma afirmação produzida por uma IA.
8. Contradições e contraexemplos devem ser preservados.
9. Uma regra pode ser válida em determinado contexto e inadequada em outro.
10. Toda aplicação relevante deve poder gerar nova experiência e revisar a sabedoria existente.
11. O Cérebro deve registrar não apenas o que fazer, mas quando fazer, quando evitar e como adaptar.
12. Sabedoria é orientação para ação, não autoridade absoluta.

## Estruturas

### Experiência

Registra um episódio real ou experimento:

- objetivo;
- contexto;
- ação;
- resultado;
- evidências;
- decisões;
- erros;
- estado.

### Lição aprendida

Transforma uma ou mais experiências em uma proposição transferível:

- princípio;
- recomendação;
- experiências de origem;
- contexto de aplicabilidade;
- contraexemplos;
- evidências;
- estado;
- confiança.

### Sabedoria aplicada

Representa uma orientação contextual suficientemente sustentada para apoiar novas decisões:

- princípio;
- quando aplicar;
- quando evitar;
- como adaptar;
- base de origem;
- evidências;
- resultados observados;
- consequências conhecidas;
- limites;
- estado;
- confiança;
- requisitos contextuais.

## Estados de maturidade

```text
EXPERIÊNCIA
REGISTRADA → ANALISADA → APRENDIDA → SUPERADA

LIÇÃO
IDENTIFICADA → VALIDANDO → VALIDADA → REFUTADA/SUPERADA

SABEDORIA
PROPOSTA → VALIDANDO → VALIDADA → LIMITADA/SUPERADA
```

`VALIDADA` não significa universal. Significa que os critérios de validação definidos para aquele contexto foram atendidos.

## Mecanismo de aplicação

Uma sabedoria validada não deve ser simplesmente recuperada por similaridade textual. O sistema deve verificar:

1. compatibilidade do contexto;
2. estado e validade temporal;
3. evidências disponíveis;
4. limites conhecidos;
5. contraexemplos;
6. resultados anteriores;
7. nível de confiança;
8. risco da decisão atual.

Quando houver conflito, baixa evidência ou contexto incompatível, a sabedoria deve ser apresentada como limitada ou hipótese, e não como regra automática.

## After-Action Review interno

Após ações relevantes, o Cérebro deve poder produzir uma revisão estruturada:

- O que pretendíamos fazer?
- O que fizemos?
- O que aconteceu?
- O que esperávamos que acontecesse?
- Por que houve diferença?
- O que funcionou?
- O que falhou?
- Qual evidência sustenta a análise?
- O que deve ser repetido?
- O que deve ser evitado?
- O que deve ser adaptado?
- Que nova experiência ou teste deve ser executado?

A finalidade é converter execução em aprendizado e evitar que o conhecimento permaneça apenas arquivado. A literatura de After-Action Review trata esse processo como mecanismo de aprendizagem organizacional e melhoria operacional. citeturn1search0turn1search13

## Proteção contra falsa sabedoria

O sistema não deve criar uma regra geral apenas porque uma ação funcionou uma vez. A generalização precisa considerar quantidade e diversidade de experiências, contexto, resultados, contraexemplos e evidências. A pesquisa sobre aprendizagem a partir de experiências únicas destaca justamente o problema de determinar o nível adequado de generalização. citeturn0search1

## Relação com a arquitetura atual

Este modelo complementa:

- `nucleo.py` — registros e histórico;
- `semantica.py` — classificação e relações;
- `auditoria.py` — validação;
- `temporal.py` — validade temporal;
- `eventos.py` e `eventos_ledger.py` — causalidade e rastreabilidade;
- `registro.py` — participantes e recursos;
- `politica.py` — autonomia e risco;
- `continuidade.py` — transferência entre agentes;
- `modelos.py` — modelos substituíveis.

O novo `sabedoria.py` fornece uma primeira representação operacional dessas camadas, sem transformar o Cérebro em um sistema fechado ou dependente de uma IA específica.

## Evolução futura

Próximas capacidades, após validação:

1. recuperação de experiências semelhantes;
2. agrupamento de experiências por contexto;
3. comparação entre sucessos e falhas;
4. detecção de padrões recorrentes;
5. testes de generalização;
6. revisão automática de lições antigas quando surgirem contraexemplos;
7. avaliação de eficácia das recomendações;
8. cálculo de confiança baseado em evidências e histórico;
9. recomendações contextuais para execução;
10. aprendizagem entre diferentes agentes, contas e plataformas sem perder proveniência.

## Regra central

> O objetivo não é construir uma biblioteca que lembra tudo. É construir uma capacidade que lembra, compreende, aprende, aplica, verifica os resultados e transforma experiência validada em orientação cada vez mais útil — sem confundir uma hipótese com sabedoria.