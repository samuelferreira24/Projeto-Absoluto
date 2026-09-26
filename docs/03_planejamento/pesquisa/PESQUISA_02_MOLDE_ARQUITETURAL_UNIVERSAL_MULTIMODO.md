---
title: "Pesquisa 02 — Molde Arquitetural: Universal × Multimodo × Híbrido × Multiagente"
identificacao: "PESQUISA_02_MOLDE_ARQUITETURAL_UNIVERSAL_MULTIMODO"
data: "2026-09-26"
objetivo: "Investigar, comparar, simular e atacar diferentes moldes arquiteturais para um sistema capaz de operar o ABS, buscando identificar mecanismos estruturais e limites sem transformar a pesquisa em decisão de implementação."
status: "PESQUISA CONCLUÍDA — AGUARDANDO AUDITORIA CRUZADA"
observacao: "Este estudo ainda NÃO representa uma decisão arquitetural oficial do ABS. A decisão será tomada somente após auditoria cruzada com pesquisa independente."
---

# PESQUISA 02 — MOLDE ARQUITETURAL: UNIVERSAL × MULTIMODO × HÍBRIDO × MULTIAGENTE

## 1. Escopo e natureza do estudo

Esta pesquisa investigou o problema arquitetural central: qual estrutura/moldura pode permitir que o ABS realize objetivos diversos, opere com diferentes modelos, ferramentas, especialistas, workflows, ambientes e interfaces, sobreviva a falhas e mude de estratégia sem ficar preso a um único agente, modelo, ferramenta ou modo.

A pergunta investigada não foi simplesmente “qual é o melhor agente?”, mas:

> Qual é o molde arquitetural que deve conter, organizar, substituir e coordenar agentes, modelos, ferramentas, workflows e outros mecanismos de execução?

O estudo foi tratado como pesquisa arquitetural conceitual. Não houve implementação das conclusões, alteração do código do ABS ou decisão oficial de arquitetura.

### Distinções epistemológicas usadas

Durante a pesquisa foram mantidas as seguintes distinções:

- **Evidência documental:** informação observada em documentação ou fonte externa.
- **Experimento/benchmark:** teste executado em sistema real, com comportamento observado.
- **Simulação conceitual:** execução mental/estrutural de cenários, sem afirmar que o comportamento foi demonstrado em sistema real.
- **Hipótese:** explicação ou arquitetura proposta ainda não demonstrada.
- **Inferência:** conclusão intermediária derivada das evidências e/ou simulações.
- **Conclusão:** resultado da pesquisa dentro das limitações do método.
- **Decisão arquitetural:** escolha oficial para o ABS. Esta pesquisa NÃO produz essa decisão.

Nenhuma simulação conceitual desta pesquisa deve ser interpretada como experimento real ou benchmark.

---

# 2. Metodologia

A metodologia utilizada foi deliberadamente adversarial.

Em vez de selecionar uma arquitetura por preferência, foram investigadas famílias diferentes e depois submetidas a cenários de funcionamento, falha, substituição, mudança de objetivo, mudança de estratégia, múltiplos modelos, múltiplos especialistas, ferramentas desconhecidas, contexto limitado, recuperação e escala.

A pesquisa seguiu aproximadamente esta sequência:

1. inventário das arquiteturas plausíveis;
2. descrição estrutural de cada candidato;
3. identificação dos mecanismos que cada candidato oferece;
4. simulação conceitual de tarefas;
5. testes de falha;
6. testes de substituição;
7. testes de mudança de objetivo;
8. testes de mudança de estratégia;
9. testes de recursos desconhecidos;
10. testes de escala e concorrência;
11. tentativa de destruir a arquitetura sobrevivente;
12. reconstrução a partir dos mecanismos que sobreviveram;
13. nova tentativa de refutação;
14. redução do molde ao menor núcleo possível;
15. identificação das hipóteses ainda não verificadas no mundo real.

O critério não foi produzir uma pontuação simples ou um ranking. O objetivo foi descobrir mecanismos causais e limites.

---

# 3. Famílias arquiteturais investigadas

Foram considerados, entre outros, os seguintes candidatos:

1. Agente Universal / monolítico.
2. Agente Multimodo.
3. Arquitetura Multiagente.
4. Hierarquia Supervisor–Especialistas.
5. Planner → Executor.
6. Workflow-first.
7. Event/State-first.
8. Controle adaptativo / Dynamic Routing.
9. Controle descentralizado.
10. Capability Registry / composição orientada a capacidades.
11. Agent Runtime.
12. Task Control Runtime.
13. Event/State Runtime.
14. Arquiteturas híbridas.
15. Goal-Oriented Adaptive Execution (GAE).
16. Adaptive Goal-State Control Runtime (M-1).
17. Adaptive Goal-State Control Runtime refinado (M-2).

Essas famílias não foram tratadas como mutuamente exclusivas em todos os casos. A pesquisa investigou também a possibilidade de uma arquitetura mais geral conter mecanismos pertencentes a várias dessas famílias.

---

# 4. Candidato 1 — Universal / monolítico

## Estrutura conceitual

Um agente central recebe o objetivo e concentra:

- interpretação;
- planejamento;
- escolha de modelo;
- escolha de ferramenta;
- execução;
- memória;
- verificação;
- recuperação;
- mudança de estratégia.

Forma simplificada:

    objetivo
       ↓
    agente central
       ↓
    modelos / ferramentas
       ↓
    resultado

## Vantagens observadas

- simplicidade aparente;
- baixo overhead conceitual;
- adequado para tarefas simples;
- um modelo forte pode resolver muitos problemas sem grande orquestração.

## Problemas encontrados

O modelo universal se torna vulnerável quando:

- o modelo é fraco;
- o executor falha;
- uma ferramenta desaparece;
- uma estratégia falha;
- é necessário recuperar uma execução longa;
- existem múltiplos objetivos;
- existem especialistas diferentes;
- existe autorização humana;
- existe necessidade de verificação independente;
- a tarefa não pertence a uma categoria conhecida.

O maior risco arquitetural é transformar o agente em um ponto único de decisão e falha.

## Resultado

Como molde universal absoluto, apresentou falhas estruturais nos cenários de modelo fraco, recuperação, ferramenta desconhecida e estratégia incorreta, a menos que mecanismos externos fossem adicionados.

Isso significa que, quando os mecanismos necessários são adicionados, o “agente universal” deixa de ser realmente monolítico e passa a se aproximar de uma arquitetura híbrida/controlada.

---

# 5. Candidato 2 — Multimodo

## Estrutura

Um agente possui modos como:

- pesquisa;
- programação;
- execução;
- planejamento;
- análise;
- recuperação;
- etc.

Cada modo altera:

- instruções;
- ferramentas;
- modelo;
- fluxo;
- comportamento.

## Vantagens

- reutilização de um agente;
- adaptação explícita;
- maior organização que um agente completamente monolítico;
- pode escolher mecanismos diferentes conforme a tarefa.

## Problema fundamental

A taxonomia de modos pode se tornar rígida.

Quando aparece uma tarefa desconhecida:

    tarefa nova
       ↓
    nenhum modo apropriado

Adicionar novos modos indefinidamente também cria crescimento estrutural.

O modo tende a confundir:

- objetivo;
- estratégia;
- executor;
- configuração operacional.

## Resultado

Multimodo sobrevive a muitos cenários, mas sua forma rígida não parece adequada como molde fundamental.

O conceito de “modo” sobreviveu apenas depois de ser reinterpretado como configuração operacional temporária, e não como conjunto fechado de categorias.

---

# 6. Candidato 3 — Multiagente

## Estrutura

Vários agentes especializados cooperam:

    objetivo
       ↓
    coordenador
       ├── pesquisador
       ├── programador
       ├── verificador
       └── executor

## Vantagens

- especialização;
- paralelismo;
- possibilidade de diferentes modelos;
- decomposição de tarefas;
- diferentes ferramentas e políticas.

## Problemas

- coordenação;
- conflitos;
- descoberta de agente adequado;
- tarefa desconhecida;
- agentes que discordam;
- especialistas errados;
- dependência de coordenador;
- aumento de custo;
- aumento de contexto;
- aumento de estados intermediários.

Uma tarefa desconhecida pode não possuir um especialista conhecido.

Se um coordenador central passa a decidir absolutamente tudo, ele se aproxima de um meta-agente.

## Resultado

Multiagente sobreviveu como **mecanismo de composição**, mas não como molde absoluto.

---

# 7. Candidato 4 — Hierárquico / Supervisor–Especialistas

Estrutura:

    supervisor
       ├── especialista A
       ├── especialista B
       ├── especialista C
       └── executor

Vantagens:

- delegação;
- especialização;
- controle;
- separação de responsabilidades.

Problema:

Se o supervisor decide tudo, torna-se gargalo e ponto único de falha.

Se os especialistas decidem tudo, surgem conflitos de autoridade.

A arquitetura hierárquica continua útil localmente, mas não elimina a necessidade de uma separação superior entre autoridade, objetivo e execução.

---

# 8. Candidato 5 — Planner → Executor

Estrutura:

    objetivo
       ↓
    planner
       ↓
    plano
       ↓
    executor
       ↓
    resultado

Funciona muito bem quando o mundo é estável.

Problema:

    plano inicial
       ↓
    mundo mudou
       ↓
    plano inválido

A solução exige:

    plano
      ↓
    execução
      ↓
    observação
      ↓
    diagnóstico
      ↓
    replanning
      ↓
    nova execução

Logo:

> Plano é hipótese operacional, não autoridade permanente.

Planner sobrevive como mecanismo, não como molde universal.

---

# 9. Candidato 6 — Workflow-first

Workflow oferece:

- caminhos explícitos;
- etapas;
- estados;
- eventos;
- branching;
- fan-out/fan-in;
- checkpoints;
- subworkflows;
- agentes dentro do workflow;
- workflows apresentados como agentes.

Fontes documentais atuais do Microsoft Agent Framework descrevem workflows como grafos de executores, edges, eventos e estado, com suporte a fan-out/fan-in, roteamento condicional, checkpoints e executores de agentes. A documentação também descreve agentes dentro de workflows e workflows expostos como agentes.

Fonte documental:
- Microsoft Agent Framework — Workflows: https://learn.microsoft.com/en-us/agent-framework/workflows/
- Microsoft Agent Framework — Workflow concepts/capabilities: https://learn.microsoft.com/en-us/agent-framework/workflows/

## Problema

Workflow rígido falha diante de:

- tarefa desconhecida;
- estratégia inesperada;
- nova capacidade;
- mudança radical de objetivo;
- ambiente não previsto.

Quando o workflow ganha mecanismos dinâmicos suficientes para resolver isso, ele se torna um sistema híbrido/adaptativo.

## Resultado

Workflow é mecanismo de execução estruturada, não o molde universal.

---

# 10. Candidato 7 — Event/State-first

Estrutura:

    evento
       ↓
    estado
       ↓
    transição
       ↓
    ação

É forte em:

- durabilidade;
- recuperação;
- transições;
- concorrência;
- observabilidade;
- continuidade.

Problema:

Event/state sozinho não gera necessariamente estratégias abertas para problemas novos.

Ele precisa de algum mecanismo deliberativo.

## Resultado

Estado e eventos sobreviveram como parte muito importante do substrato do runtime, mas não como solução completa isolada.

---

# 11. Candidato 8 — Controle adaptativo

A pesquisa passou então a considerar uma arquitetura em que o sistema não possui uma única forma fixa de execução.

Princípio:

    objetivo
       ↓
    estado
       ↓
    escolher estratégia
       ↓
    executar
       ↓
    observar
       ↓
    mudar estratégia se necessário

Essa família começou a sobreviver melhor aos cenários porque permite trocar o método sem mudar a identidade do objetivo.

---

# 12. Candidato GAE — Goal-Oriented Adaptive Execution

Hipótese intermediária:

> Um sistema orientado a objetivos que escolhe dinamicamente a forma de execução e muda de estratégia conforme a observação do ambiente.

Mecanismos:

- objetivo;
- estado;
- estratégia;
- executor;
- observação;
- replanning;
- seleção de modelo;
- seleção de ferramentas;
- verificação;
- recuperação.

A hipótese foi então atacada por poder virar um “meta-agente”.

---

# 13. Primeiro grande ataque — GAE como meta-agente

Se uma IA central decidir:

- qual modelo usar;
- qual ferramenta usar;
- qual agente usar;
- qual workflow usar;
- quando verificar;
- quando recuperar;
- quando mudar estratégia;
- quando autorizar;
- quando alterar objetivo;

então o GAE se transforma em um superagente central.

Isso produz:

- gargalo;
- ponto único de falha;
- dependência excessiva de uma IA;
- dificuldade de auditoria;
- concentração de autoridade.

## Correção

Separar:

### Controle

- autoridade;
- políticas;
- limites;
- objetivo;
- estado;
- permissões;
- transições;
- recuperação.

### Deliberação

- estratégia;
- planejamento;
- seleção operacional;
- composição.

### Execução

- ação concreta.

Resultado:

> Controle não precisa ser uma inteligência central.

---

# 14. Segundo ataque — executor controlando tudo

Hipótese:

    executor
       ↓
    decide objetivo
       ↓
    decide política
       ↓
    decide execução
       ↓
    executa

Falha para o ABS porque autonomia operacional não deve significar autoridade absoluta.

Princípio sobrevivente:

> Autonomia é delegada, não absoluta.

---

# 15. Terceiro ataque — descentralização absoluta

Hipótese:

    agente A decide
    agente B decide
    agente C decide

Problema:

    A quer X
    B quer Y
    X e Y são incompatíveis

Se houver votação, alguém precisa definir:

- quem pode votar;
- qual voto pesa;
- qual regra vence;
- quais objetivos são prioritários.

Portanto surge novamente uma autoridade.

Conclusão:

> Descentralização pode ser mecanismo local de execução, mas não elimina autoridade e invariantes globais.

---

# 16. Quarto ataque — workflow resolve tudo

Workflow fixo falha com tarefa desconhecida.

Adicionar adaptação torna o workflow um mecanismo híbrido/adaptativo.

Conclusão:

> Workflow é uma forma de execução, não necessariamente o molde fundamental.

---

# 17. Quinto ataque — multiagente resolve tudo

Multiagente também pode não possuir o especialista necessário para uma tarefa desconhecida.

Precisa de:

- descoberta;
- composição;
- seleção;
- criação de estratégia;
- capacidade de operar sem especialista prévio.

Conclusão:

> Multiagente é mecanismo de composição, não molde fundamental.

---

# 18. Sexto ataque — event/state resolve tudo

Estado e eventos resolvem continuidade e transição, mas não necessariamente produzem estratégias novas.

Conclusão:

> Event/state é substrato de execução/continuidade, não sistema completo de deliberação.

---

# 19. Sétimo ataque — adaptatividade resolve tudo

Mesmo um sistema adaptativo pode exagerar:

    tarefa simples
       ↓
    planejamento complexo
       ↓
    múltiplos agentes
       ↓
    múltiplos verificadores
       ↓
    custo desnecessário

Correção:

> Complexidade deve ser elástica.

O sistema deve utilizar o menor nível de deliberação necessário.

---

# 20. Níveis de execução sobreviventes

A pesquisa identificou três níveis úteis:

### Nível 0 — reação direta

    evento → ação

### Nível 1 — execução estruturada

    objetivo → workflow → resultado

### Nível 2 — execução adaptativa

    objetivo
       ↓
    estratégia
       ↓
    executor
       ↓
    observação
       ↓
    replanning
       ↺

Isso permite que o sistema seja simples quando a tarefa é simples e complexo quando a tarefa exige.

---

# 21. Cenários A–P

Os cenários obrigatórios foram utilizados para atacar os principais candidatos.

## A — tarefa simples

Uma arquitetura muito complexa pode adicionar overhead desnecessário.

Mecanismo sobrevivente:

> execução direta deve ser possível.

---

## B — pesquisa

Pesquisa exige:

- interpretação;
- aquisição de informação;
- avaliação;
- síntese.

Nenhuma estrutura fixa dominou universalmente.

Mecanismo importante:

> capacidade de selecionar a próxima estratégia a partir do estado observado.

---

## C — pesquisa + execução

Descobrir algo não é o mesmo que estar autorizado a executar.

Mecanismo:

> separação entre decisão, execução e autoridade.

---

## D — programação

Plano inicial pode estar errado.

Mecanismo:

    planejar
      ↓
    executar
      ↓
    observar
      ↓
    replanejar

---

## E — tarefa longa

Aquilo que precisa sobreviver não é necessariamente o agente.

É:

- objetivo;
- estado;
- progresso;
- eventos;
- checkpoints;
- identidade da execução.

Mecanismo:

> Executor ≠ execução.

---

## F — falha de ferramenta

Uma estratégia acoplada a uma ferramenta única pode morrer com a ferramenta.

Mecanismo:

> estratégia deve poder selecionar outro recurso quando possível.

---

## G — modelo fraco

Arquitetura não cria inteligência ausente.

Mas decomposição, múltiplos modelos, ferramentas e verificação podem compensar em alguns problemas.

Mecanismo:

> capacidade pode ser composta, mas não criada magicamente.

---

## H — modelo forte

Modelo forte reduz necessidade de orquestração cognitiva.

Ainda permanecem:

- autorização;
- persistência;
- recuperação;
- observabilidade;
- limites;
- substituição.

Mecanismo:

> controle operacional continua útil mesmo com executor cognitivo forte.

---

## I — múltiplos modelos

Melhor abstração encontrada:

> roteamento por capacidade, não por identidade fixa do agente.

Modelo é recurso substituível.

---

## J — múltiplos especialistas

Especialistas podem ajudar.

Mas precisam de:

- seleção;
- composição;
- resolução de conflitos;
- verificação.

Multiagente não é estruturalmente obrigatório.

---

## K — mudança de objetivo

Objetivo não é a mesma coisa que estratégia.

    objetivo
       ≠
    estratégia

Mudança de objetivo deve estar sob autoridade apropriada.

---

## L — autorização

HITL é melhor modelado como transição de runtime:

    EXECUTING
       ↓
    REQUIRES_APPROVAL
       ↓
    PAUSED
       ↓
    HUMAN_DECISION
       ↓
    RESUME / ABORT

A documentação do Microsoft Agent Framework descreve RequestPort, pausa, checkpoints e retomada de workflows para interação humana.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop

---

## M — recuperação

Persistir:

- objetivo;
- estado;
- progresso;
- eventos;
- resultados;
- checkpoints.

Permite substituir executor e continuar.

A documentação atual do Microsoft Agent Framework descreve checkpoints e retomada; também existem mecanismos de agentes duráveis para processos longos.

Fontes:
https://learn.microsoft.com/en-us/agent-framework/workflows/
https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints

---

## N — contexto limitado

Separar:

    estado persistente
       ≠
    contexto do modelo

Contexto é um recurso alocado seletivamente à execução.

A documentação do OpenAI Agents SDK descreve sessões persistentes e controle do histórico recuperado para execuções.

Fonte:
https://openai.github.io/openai-agents-python/sessions/

---

## O — ferramenta desconhecida

Arquiteturas baseadas em categorias fechadas podem falhar.

Mecanismo necessário:

> arquitetura aberta a novas capacidades.

---

## P — estratégia errada

O próprio executor pode avaliar incorretamente seu resultado.

Mecanismo:

    executor
       ↓
    evidência / teste
       ↓
    verificação
       ↓
    avaliação da estratégia
       ↓
    nova estratégia

Nenhuma arquitetura garante verificação perfeita.

---

# 22. Testes extremos

## 1. Recursos demais

Risco:

- excesso de opções;
- custo;
- latência;
- paralisia de escolha.

Mecanismo:

> seleção de capacidade + complexidade elástica.

---

## 2. Recursos de menos

O sistema pode não ter capacidade para atingir o objetivo.

Conclusão:

> arquitetura não cria recursos inexistentes.

---

## 3. Modelo primário desaparece

A arquitetura deve permitir substituir o executor.

Objetivo continua.

---

## 4. Ferramenta crítica desaparece

Pode haver rota alternativa.

Se não houver, a execução pode ficar BLOCKED.

O molde continua.

---

## 5. Especialista está errado

Não deve ser autoridade absoluta.

Mecanismo:

- evidência;
- testes;
- critérios;
- verificação.

---

## 6. Especialistas discordam

Autoridade decide processo/permissão.

Evidência deve decidir o que puder ser resolvido empiricamente.

---

## 7. Planner está errado

Planner é produtor de hipótese de execução.

Pode ser substituído/revisado.

---

## 8. Verificador está errado

Verificação independente, evidência externa, testes e HITL podem reduzir o risco.

Não existe garantia absoluta.

---

## 9. Contexto irrelevante ou conflitante

Exige mecanismos de:

- relevância;
- proveniência;
- confiabilidade;
- recência;
- seleção de contexto.

Este mecanismo continua parcialmente aberto.

---

## 10. Tarefa não se encaixa em nenhum modo

A arquitetura adaptativa deve poder:

    objetivo
       ↓
    explorar
       ↓
    descobrir capacidade
       ↓
    criar estratégia
       ↓
    executar

Sem depender de uma lista fechada de categorias.

---

# 23. Relação estratégia × modo × agente

A pesquisa testou explicitamente:

    estratégia A → estratégia B → estratégia C

versus:

    modo A → modo B → modo C

versus:

    agente A → agente B → agente C

Resultado conceitual:

> Estratégia é a abstração mais geral.

Uma estratégia pode utilizar:

- modo;
- workflow;
- agente;
- múltiplos agentes;
- código;
- ferramenta;
- combinação desses.

Forma:

    ESTRATÉGIA
       ├── modo
       ├── workflow
       ├── agente
       ├── multiagente
       ├── código
       └── combinação

Logo, mudança de agente, modelo, ferramenta ou modo pode ser consequência de mudança de estratégia, mas não é equivalente a estratégia em si.

---

# 24. Primeira arquitetura composta — M-1

A primeira composição sobrevivente recebeu o nome:

# Adaptive Goal-State Control Runtime — M-1

Também:

# Molde de Controle Adaptativo Orientado a Objetivos, com Execução Dirigida por Eventos

Estrutura conceitual:

    IMPERADOR
        │
        ▼
    AUTHORITY
        │
        ├── intenção
        ├── autorização
        ├── limites
        └── políticas
        │
        ▼
    GOAL / STATE CONTROL
        │
        ├── goals
        ├── state
        ├── priorities
        ├── constraints
        ├── transitions
        └── continuity
        │
        ├───────────────┐
        ▼               ▼
      EVENTS          STRATEGY
                         │
                  ┌──────┼──────┐
                  ▼      ▼      ▼
                direct workflow agent
                  │      │      │
                  └──────┼──────┘
                         ▼
                     EXECUTOR
                         │
                 ┌───────┼────────┐
                 ▼       ▼        ▼
               model    tool   environment
                         │
                         ▼
                      result
                         │
                         ▼
                    observation
                         │
                    ┌────┴────┐
                    ▼         ▼
                 success    failure
                              │
                         diagnosis
                              │
                         verification
                              │
                        next decision
                              │
                              └──↺

M-1 ainda foi considerado hipótese, não decisão.

---

# 25. Ataque de complexidade e escala

A pesquisa foi então estendida para testar se M-1 permaneceria simples em escala.

## Caso 1 — 1 objetivo / 1 executor

    objetivo
       ↓
    estado
       ↓
    estratégia simples
       ↓
    executor
       ↓
    resultado

Sobrevive.

---

## Caso 2 — 10 objetivos / 10 execuções / 5 modelos / 30 ferramentas

Um controlador que decidisse cada microação se tornaria gargalo.

Correção:

    controle global
       ↓
    controles locais
       ↓
    execuções

O controle global resolve:

- autoridade;
- prioridades;
- conflitos globais;
- recursos globais.

O controle local resolve:

- estratégia;
- execução;
- detalhes operacionais.

---

# 26. Caso 3 — 100 objetivos

Problemas:

- concorrência;
- recursos compartilhados;
- conflitos;
- falhas independentes;
- mudanças de prioridade;
- recuperação.

Foi identificada a necessidade de separar:

    estado do sistema
    +
    estado do objetivo
    +
    estado da execução
    +
    estado dos recursos

Falha de um objetivo não deve significar falha do sistema inteiro.

Falha do executor não deve significar necessariamente falha do objetivo.

---

# 27. Concorrência

Se:

    objetivo A → recurso X
    objetivo B → recurso X

existe conflito.

Um controlador central que arbitrasse cada microação seria um gargalo.

Resultado:

> Controle deve possuir escopo.

Estrutura:

                    AUTORIDADE
                        │
                 CONTROLE GLOBAL
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      CONTROLE A    CONTROLE B    CONTROLE C
          │             │             │
       execução      execução      execução

---

# 28. Ataque de 1.000 objetivos

O controlador não pode carregar todos os detalhes.

O controle superior deve operar sobre abstrações:

    objetivo 37
    status: executando
    risco: baixo
    progresso: 64%
    recurso: disponível

em vez de carregar todos os detalhes internos da execução.

Conclusão:

> Controle superior precisa operar sobre estado abstrato; detalhes permanecem em escopos inferiores.

---

# 29. Ataque de mutação

Testes:

- 5 modelos → 20 modelos;
- 30 ferramentas → 500 ferramentas;
- 10 agentes → 100 agentes;
- 1 ambiente → 20 ambientes.

O molde não deve precisar mudar.

Mecanismo:

    MOLDURA
       │
    CAPACIDADES
       ├── modelos
       ├── ferramentas
       ├── agentes
       ├── workflows
       └── ambientes

Novo recurso entra como capacidade, não como alteração do molde.

---

# 30. Capability Registry

Foi investigada uma arquitetura baseada em registry de capacidades:

    CAPABILITY REGISTRY
       ├── modelos
       ├── ferramentas
       ├── agentes
       ├── workflows
       └── ambientes

O registry responde:

> O que existe?

Mas não necessariamente:

> O que devemos fazer?

nem:

> Devemos fazer?

Resultado:

> Capability Registry é mecanismo auxiliar, não molde fundamental.

---

# 31. Ataque de planner central

    objetivo
       ↓
    planner
       ↓
    plano completo
       ↓
    execução

Falha quando o mundo muda.

Resultado:

> Plano é hipótese operacional revisável.

---

# 32. Ataque de verificador absoluto

    executor
       ↓
    verificador
       ↓
    verdade

Falha porque o verificador pode estar errado.

Mecanismos possíveis:

    executor
       ↓
    evidência
       ↓
    teste
       ↓
    verificador
       ↓
    verificação independente
       ↓
    humano quando necessário

Nenhum mecanismo garante verdade absoluta.

---

# 33. Contexto em escala

Não é sustentável:

    todo histórico
       ↓
    modelo

Nem é seguro simplesmente apagar o histórico.

Separação:

    ESTADO PERSISTENTE
       ↓
    seleção
       ↓
    contexto relevante
       ↓
    executor

Conclusão:

> Contexto é recurso alocado à execução.

---

# 34. Ataque de execução infinita

Estratégias podem entrar em ciclo:

    A falha
      ↓
    B
      ↓
    C
      ↓
    A
      ↓
    B
      ↓
    ...

Portanto a execução precisa de estados terminais, como:

- SUCCESS;
- FAILED;
- BLOCKED;
- CANCELLED;
- REQUIRES_HUMAN;
- TIMEOUT;
- RESOURCE_UNAVAILABLE.

Adaptabilidade sem condição de parada pode virar loop infinito.

---

# 35. Ataque de custo

Uma tarefa simples não deve ativar uma estrutura enorme.

Exemplo:

    pergunta simples
       ↓
    múltiplos agentes
       ↓
    múltiplos modelos
       ↓
    verificadores
       ↓
    workflows
       ↓
    custo desnecessário

Princípio:

> Use o menor nível de complexidade suficiente para o objetivo.

---

# 36. Ataque de risco

Tarefas diferentes exigem diferentes níveis de autonomia.

Conceitualmente:

    baixo risco
       → execução simples

    risco maior
       → mais verificação

    risco alto
       → autorização adicional

    risco crítico
       → controle humano obrigatório, conforme política

A taxonomia exata ainda é hipótese de implementação.

O mecanismo arquitetural sobrevivente é:

> Autonomia deve ser proporcional às permissões e ao risco.

---

# 37. Quatro dimensões de execução

A pesquisa identificou quatro dimensões que não precisam ser confundidas com “modos” fixos:

## Complexidade

    direta → estruturada → adaptativa

## Autonomia

    manual → assistida → delegada → altamente autônoma

## Risco

    baixo → médio → alto → crítico

## Persistência

    instantânea → sessão → longa → durável

Essas dimensões podem variar independentemente.

---

# 38. Execução

Uma execução foi conceitualmente definida como uma entidade que possui:

    Execution
    ├── identity
    ├── objective
    ├── authority
    ├── current state
    ├── constraints
    ├── strategy
    ├── progress
    ├── events
    ├── resources
    ├── observations
    ├── evidence
    └── terminal state

Enquanto o executor é:

    Executor
    ├── model
    ├── tools
    ├── environment
    └── local context

Portanto:

> Execution ≠ Executor.

Essa foi uma das distinções mais importantes de toda a pesquisa.

---

# 39. Migração de execução

Teste:

    Execution 37
        ↓
    Executor A
        ↓
      falha
        ↓
    estado preservado
        ↓
    Executor B
        ↓
    continua

Depois:

    Executor B
        ↓
    modelo X
        ↓
    falha
        ↓
    modelo Y

E:

    estratégia A
        ↓
    falha
        ↓
    estratégia B

O objetivo permanece.

Isso permite continuidade sem depender da identidade de um único executor.

---

# 40. Corrupção de estado

Um executor pode produzir resultado errado.

Se o sistema transformar imediatamente essa resposta em estado verdadeiro, o erro pode se propagar.

Separação conceitual:

    OBSERVAÇÃO
       ↓
    EVIDÊNCIA
       ↓
    INTERPRETAÇÃO
       ↓
    DECISÃO
       ↓
    AÇÃO

Resultado:

> Resultado produzido pelo executor não deve ser automaticamente tratado como verdade absoluta do sistema.

---

# 41. Segunda arquitetura composta — M-2

Após o ataque ao M-1, a arquitetura foi refinada.

# Adaptive Goal-State Control Runtime — M-2

ou:

# Molde de Controle Adaptativo Orientado a Objetivos e Estado

Estrutura:

                         IMPERADOR
                             │
                             ▼
                  ┌─────────────────────┐
                  │ AUTHORITY / POLICY  │
                  │ intenção            │
                  │ autorização         │
                  │ limites             │
                  │ prioridades         │
                  └──────────┬──────────┘
                             │
                             ▼
                ┌────────────────────────┐
                │ GOAL / STATE PLANE     │
                │ objetivos              │
                │ identidade             │
                │ estado persistente     │
                │ eventos                │
                │ transições             │
                │ continuidade           │
                └──────────┬─────────────┘
                           │
                ┌──────────┴──────────┐
                │                     │
          controle global       controles locais
                │                     │
                │              ┌──────┼──────┐
                │              ▼      ▼      ▼
                │           OBJ A  OBJ B  OBJ C
                │              │      │      │
                │              ▼      ▼      ▼
                │           estratégia local
                │              │
                │       ┌──────┼───────┐
                │       ▼      ▼       ▼
                │     direto workflow agente
                │       │      │       │
                │       └──────┼───────┘
                │              ▼
                │          EXECUTOR
                │              │
                │       ┌──────┼──────┐
                │       ▼      ▼      ▼
                │     modelo ferramenta ambiente
                │
                └──────────────┐
                               ▼
                          OBSERVAÇÃO
                               │
                      ┌────────┴────────┐
                      ▼                 ▼
                   sucesso            problema
                                         │
                                   diagnóstico
                                         │
                                   verificação
                                         │
                                   nova estratégia
                                         │
                                   ESTADO ATUALIZADO
                                         │
                                         └──────↺

M-2 continua sendo hipótese de pesquisa. Não é arquitetura oficial do ABS.

---

# 42. Ataque de redução — o que pode ser removido?

Partiu-se de:

- Autoridade;
- Objetivo;
- Estado;
- Estratégia;
- Execução;
- Eventos;
- Observação;
- Verificação;
- Recuperação;
- Capacidades.

## Planner

Pode ser removido.

Não é estrutural.

## Workflow

Pode ser removido.

Não é estrutural.

## Agente

Pode ser removido.

Não é estrutural.

## Multiagente

Pode ser removido.

Não é estrutural.

## Modelo específico

Pode ser removido.

É recurso.

## Ferramenta específica

Pode ser removida.

É recurso.

## Interface

Pode ser removida.

É canal.

## Banco específico

Pode ser removido.

É mecanismo de persistência.

## Verificador

Execução básica continua sem ele, mas a robustez adaptativa diminui.

É mecanismo dependente de risco e necessidade.

## Eventos

Execução simples ainda pode existir sem uma infraestrutura explícita de eventos, mas eventos são fundamentais para representar transições e mudanças de estado no runtime robusto.

## Recuperação

Não é necessária para toda tarefa curta, mas é estrutural para continuidade e durabilidade.

---

# 43. Núcleo reduzido

A poda produziu:

    AUTORIDADE
        │
        ▼
      OBJETIVO
        │
        ▼
       ESTADO
        │
        ▼
     TRANSIÇÃO
        │
        ▼
      EXECUÇÃO
        │
        ▼
     OBSERVAÇÃO
        │
        └──────↺

E mecanismos de robustez ao redor:

- eventos;
- recursos;
- verificação;
- recuperação;
- persistência;
- políticas.

---

# 44. Controle × Deliberação × Execução

Foi identificado um problema: se ninguém escolhe a estratégia, como o sistema se adapta?

Separação:

## Controle

Define:

- o que é permitido;
- limites;
- objetivo;
- estado válido;
- quando continuar;
- quando parar;
- quando solicitar autorização.

## Deliberação

Define:

- como tentar;
- qual estratégia;
- qual executor;
- qual ferramenta;
- quando mudar estratégia.

## Execução

Produz efeitos.

Estrutura:

    CONTROLE
        │
        ├── autoriza
        ├── limita
        ├── preserva
        └── supervisiona
               │
               ▼
          DELIBERAÇÃO
               │
          estratégia
               │
               ▼
           EXECUÇÃO

A deliberação pode ser feita por:

- modelo;
- vários modelos;
- código;
- regras;
- workflow;
- humano;
- combinação.

Logo:

> Não existe necessidade arquitetural de uma inteligência única central.

---

# 45. Objetivo × estratégia × ação

A pesquisa encontrou uma hierarquia mais precisa:

    AUTORIDADE
        ↓
      OBJETIVO
        ↓
     ESTRATÉGIA
        ↓
     PLANO/WORKFLOW
        ↓
       AÇÃO
        ↓
      RECURSO

O objetivo não é estratégia.

A estratégia não é executor.

A ação não é recurso.

Isso permite mudança controlada:

- trocar ação sem trocar estratégia;
- trocar ferramenta sem trocar executor;
- trocar executor sem trocar objetivo;
- trocar estratégia sem perder identidade da execução;
- trocar objetivo somente sob autoridade apropriada.

---

# 46. O princípio causal mais importante

Depois de repetidas simulações, surgiu:

> **SEPARAR A IDENTIDADE DA EXECUÇÃO DA ESTRATÉGIA DE EXECUÇÃO.**

De forma mais ampla:

    O QUE ESTÁ SENDO TENTADO
             ≠
    COMO ESTÁ SENDO TENTADO
             ≠
    QUEM ESTÁ TENTANDO
             ≠
    QUAL RECURSO ESTÁ SENDO USADO

Isso permite:

    mesmo objetivo
       ↓
    estratégia A
       ↓
    executor 1
       ↓
    falha
       ↓
    estratégia B
       ↓
    executor 2
       ↓
    modelo 3
       ↓
    ferramenta 7
       ↓
    continuidade

---

# 47. Evolução V0 → V1 → V2 → V3

## V0

    Imperador
       ↓
    objetivo
       ↓
    executor
       ↓
    resultado

## V1

    objetivo
       ↓
    estado
       ↓
    executor
       ↓
    observação
       ↓
    evento

## V2

    objetivo
       ↓
    estado
       ↓
    estratégia
       ↓
    executor
       ↓
    observação
       ↓
    verificação
       ↓
    replanejamento

## V3

    autoridade
       ↓
    objetivos
       ↓
    execuções independentes
       ↓
    controles locais
       ↓
    múltiplos executores
       ↓
    recuperação
       ↓
    concorrência
       ↓
    governança

Essa evolução é conceitual. Não é plano de implementação.

---

# 48. Substituição de componentes

Foi testada a substituição de:

| Elemento | Sobrevive como parte do molde? |
|---|---|
| Modelo | Sim |
| Ferramenta | Sim |
| Agente | Sim |
| Especialista | Sim |
| Workflow | Sim |
| Planner | Sim |
| Verificador | Sim, com ressalvas |
| Memória | Sim, se preservar o estado necessário |
| Banco de dados | Sim |
| Ambiente | Sim |
| Interface | Sim |
| Executor | Sim |
| Estratégia | Sim |

A ressalva central é:

> Substituir um recurso não garante preservar automaticamente a capacidade da tarefa.

Se nenhum executor disponível possuir a capacidade necessária, a arquitetura pode sobreviver enquanto a tarefa permanece sem solução.

---

# 49. Emergência — tarefa nunca vista

Teste:

> Tarefa que não pertence a nenhuma categoria conhecida.

Arquitetura rígida:

    categoria desconhecida
       ↓
    nenhum modo
       ↓
    falha

Arquitetura adaptativa:

    objetivo
       ↓
    estado
       ↓
    capacidades conhecidas
       ↓
    insuficientes
       ↓
    exploração
       ↓
    descoberta
       ↓
    estratégia
       ↓
    execução
       ↓
    observação

Não existe garantia de sucesso.

Existe, porém, capacidade de continuar procurando sem depender de uma taxonomia fechada.

---

# 50. Controle em escala

A arquitetura refinada precisa operar em diferentes escalas.

## Pequena

    1 objetivo
       ↓
    1 execução

## Média

    objetivos
       ↓
    controles locais
       ↓
    múltiplos executores

## Grande

    autoridade
       ↓
    controle global
       ↓
    controles por escopo
       ↓
    muitas execuções
       ↓
    executores distribuídos

O controle global não precisa conhecer cada microação.

---

# 51. O problema de complexidade interna

O maior ataque restante passou a ser:

> O próprio runtime de controle pode se tornar mais complexo que o problema que pretende resolver?

Esse risco é real.

Se cada tarefa exigir:

- planejamento;
- múltiplos modelos;
- múltiplos agentes;
- vários verificadores;
- roteamento complexo;
- recuperação;
- auditoria;
- registry;
- políticas;

então a arquitetura pode gerar mais complexidade do que resolve.

A resposta conceitual encontrada foi:

# Complexidade elástica.

A execução deve começar pelo mecanismo mínimo e escalar somente quando necessário.

---

# 52. Arquitetura mínima possível

A menor expressão do molde:

    OBJETIVO
       ↓
      ESTADO
       ↓
     EXECUTOR
       ↓
    RESULTADO

Depois pode ganhar:

    + observação
    + eventos

Depois:

    + estratégia
    + replanning

Depois:

    + persistência
    + recuperação
    + verificação

Depois:

    + múltiplos executores
    + capacidades
    + concorrência
    + governança

Essa propriedade permite evolução incremental sem exigir que o ABS nasça completo.

---

# 53. O que não é o ABS

A pesquisa reforçou as seguintes distinções:

## Projeto Absoluto

É a visão, método e direção.

## ABS

É o sistema destinado a transformar intenção em capacidade operacional.

## Agente

É uma possível unidade cognitiva de execução.

## Modelo

É um recurso cognitivo.

## Ferramenta

É um recurso operacional.

## Workflow

É uma forma estruturada de execução.

## Planner

É mecanismo de deliberação.

## Verificador

É mecanismo de validação.

## Memória

É mecanismo de persistência/contexto.

## Interface

É canal de interação.

Nenhum desses, isoladamente, é o ABS.

---

# 54. Evidência documental reunida

As fontes documentais consultadas foram usadas para verificar a existência de mecanismos, não para provar a arquitetura proposta.

## Microsoft Agent Framework

A documentação apresenta workflows como estruturas explícitas que coordenam código, agentes, estado, eventos e entrada humana. Há suporte a executores, edges, eventos, estado, fan-out/fan-in, roteamento condicional, checkpoints, subworkflows e agentes dentro de workflows.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/workflows/

A documentação também apresenta workflows e agentes como pontos diferentes de um espectro de orquestração, dependendo de quem decide o próximo passo, e descreve composição por agentes, workflows, handoffs e outros mecanismos.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/workflows/journeys

A documentação de Human-in-the-loop descreve pausas de execução, request/response, checkpoints e retomada após intervenção humana.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop

A documentação de checkpoints descreve preservação de estado e retomada.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints

A documentação de agentes duráveis descreve processos longos, persistência, eventos externos e retomada após falhas/restarts.

Fonte:
https://learn.microsoft.com/en-us/agent-framework/agents/durable-agents

## OpenAI Agents SDK

A documentação do OpenAI Agents SDK apresenta agentes, ferramentas, handoffs, guardrails e execução em loop.

Fonte:
https://openai.github.io/openai-agents-python/

A documentação de sessões descreve persistência e recuperação de histórico para execução.

Fonte:
https://openai.github.io/openai-agents-python/sessions/

A documentação de guardrails descreve mecanismos de validação e controle em torno da execução.

Fonte:
https://openai.github.io/openai-agents-python/guardrails/

Essas fontes documentam mecanismos existentes. Elas não demonstram que o molde M-2 seja a arquitetura ótima ou oficial para o ABS.

---

# 55. Nível epistemológico dos resultados

## Nível 1 — evidência externa

Existem sistemas e frameworks atuais que demonstram mecanismos como:

- agentes em workflows;
- workflows como agentes;
- estado persistente;
- checkpoints;
- retomada;
- eventos;
- execução longa;
- HITL;
- guardrails;
- múltiplos executores;
- composição de agentes.

Isso é evidência de viabilidade dos mecanismos individualmente.

Não é prova da arquitetura proposta.

---

## Nível 2 — indicado pelas simulações

As simulações conceituais repetidamente apontaram para:

- autoridade separada da execução;
- objetivos persistentes;
- estado externo ao executor;
- estratégia mutável;
- executor substituível;
- eventos;
- observação;
- verificação;
- recuperação;
- complexidade elástica;
- abertura a capacidades novas;
- controle por escopo.

Também repetidamente atacaram como moldes fundamentais:

- agente universal;
- agente central;
- multimodo rígido;
- multiagente como núcleo;
- workflow rígido;
- planner permanente;
- event/state isolado;
- descentralização absoluta.

---

## Nível 3 — hipóteses ainda não verificadas

Ainda precisam de validação real:

- se a separação realmente reduz complexidade;
- quanto overhead o runtime produz;
- como a concorrência será governada em grande escala;
- como contratos de capacidade serão definidos;
- como contexto será selecionado;
- como estratégia ruim será detectada;
- como evitar loops de replanejamento;
- como limitar custo;
- como governar centenas/milhares de execuções;
- como preservar auditabilidade;
- como o runtime poderá evoluir sem se tornar o novo gargalo.

---

# 56. Limitações da pesquisa

1. Simulações foram conceituais.
2. Não houve benchmark do ABS.
3. Não houve implementação do molde.
4. Não houve teste real de recuperação.
5. Não houve teste real de concorrência em escala.
6. Não houve medição real de custo.
7. Não houve medição real de latência.
8. Não houve medição real de qualidade.
9. A arquitetura proposta não foi comparada experimentalmente em ambiente controlado.
10. A disponibilidade de mecanismos em frameworks externos não prova superioridade arquitetural.
11. A arquitetura pode apresentar dificuldades que não apareceram na simulação.
12. A pesquisa foi produzida antes da auditoria cruzada com a segunda pesquisa independente.

---

# 57. Incertezas

Permanecem abertas:

- qual deve ser o contrato mínimo entre runtime e executor;
- como representar estado;
- como representar estratégia;
- como registrar capacidades;
- como medir risco;
- como selecionar contexto;
- como detectar conflito de objetivos;
- como resolver conflitos de recursos;
- como impedir loops;
- como medir quando a complexidade adicional vale a pena;
- como garantir substituição sem perda de estado;
- como preservar observabilidade;
- como fazer evolução do próprio runtime;
- como separar controle global e local sem criar inconsistências.

---

# 58. Questões abertas

1. O runtime mínimo pode realmente permanecer simples em implementação?
2. Qual é o menor conjunto de invariantes necessário?
3. Qual é a melhor representação de uma execução?
4. Qual é a melhor representação de estratégia?
5. Qual mecanismo deve controlar recursos concorrentes?
6. Qual nível de estado deve ser global?
7. Qual estado deve ser local?
8. Como detectar estratégia ruim sem criar um verificador igualmente complexo?
9. Quando chamar um agente?
10. Quando chamar um workflow?
11. Quando executar diretamente?
12. Como descobrir novas capacidades?
13. Como validar capacidades desconhecidas?
14. Como impedir que o sistema se torne excessivamente autônomo?
15. Como manter o Imperador como autoridade?
16. Como impedir que controle global vire meta-agente?
17. Como permitir controle distribuído sem perder invariantes?
18. Como testar tudo isso experimentalmente?

---

# 59. Divergências que devem permanecer preservadas

A pesquisa não elimina todas as arquiteturas alternativas.

Existem mecanismos que podem continuar válidos em diferentes contextos:

- workflow pode ser melhor para caminhos previsíveis;
- agente pode ser melhor para deliberação aberta;
- multiagente pode ser melhor para especialização;
- planner pode ser melhor para tarefas estruturadas;
- event/state pode ser melhor para durabilidade;
- controle adaptativo pode ser melhor para ambientes mutáveis.

A conclusão não é que esses mecanismos são inúteis.

A conclusão conceitual é:

> Eles podem ser mecanismos dentro de um molde mais geral.

---

# 60. Convergência

A convergência ocorreu quando novas simulações passaram a produzir principalmente refinamentos dos mesmos mecanismos, em vez de uma nova arquitetura fundamentalmente diferente.

Os mecanismos que sobreviveram repetidamente foram:

- autoridade;
- objetivos;
- estado persistente;
- eventos;
- políticas;
- estratégia mutável;
- executores intercambiáveis;
- contexto seletivo;
- verificação;
- recuperação;
- observabilidade;
- descoberta de capacidades;
- complexidade elástica;
- workflows opcionais;
- agentes opcionais;
- multiagente opcional;
- planner opcional.

---

# 61. Candidatos descartados como moldes fundamentais

Isso não significa que sejam arquiteturas ruins em geral.

Foram descartados como **molde fundamental absoluto**:

- Universal agent como núcleo;
- Multimode rígido;
- Multiagent como núcleo;
- hierarquia rígida como absoluto;
- planner/executor como molde universal;
- workflow-first;
- event/state-only;
- descentralização absoluta;
- meta-agente central.

Os mecanismos úteis desses candidatos permanecem reutilizáveis.

---

# 62. Conclusão conceitual

Depois das rodadas de investigação, simulação, ataque, reconstrução e redução, a hipótese arquitetural que melhor sobreviveu foi:

# Runtime de Controle Adaptativo Orientado a Objetivos e Estado

Nome de pesquisa:

# Adaptive Goal-State Control Runtime — AGSCR

ou:

# Molde ABS de Controle Adaptativo Orientado a Objetivos e Estado

Definição conceitual:

> ABS é, nesta hipótese de pesquisa, um runtime de controle sob autoridade do Imperador, orientado por objetivos e estado persistente, capaz de selecionar, compor, substituir e adaptar mecanismos de execução conforme o contexto, observando resultados e alterando estratégias sem perder a identidade da execução.

Essa definição é **hipótese de pesquisa**, não decisão arquitetural oficial.

---

# 63. Princípios finais identificados

1. Autoridade ≠ execução.
2. Objetivo ≠ estratégia.
3. Estratégia ≠ executor.
4. Executor ≠ modelo.
5. Modelo ≠ ferramenta.
6. Execução ≠ executor.
7. Estado ≠ contexto do modelo.
8. Resultado ≠ evidência.
9. Agente ≠ ABS.
10. Workflow ≠ ABS.
11. Complexidade deve ser elástica.
12. Execuções devem poder sobreviver à troca de executor.
13. Novas capacidades não devem exigir novo molde.
14. Controle global não deve controlar cada microação.
15. Estratégia deve poder mudar.
16. Objetivo só deve mudar sob autoridade apropriada.
17. Autonomia é delegada, não absoluta.
18. Verificação reduz risco, mas não garante verdade absoluta.
19. Recursos são substituíveis quando existe capacidade alternativa.
20. A identidade da execução deve sobreviver à troca de estratégia e executor.

---

# 64. Fórmula arquitetural final da pesquisa

                         AUTORIDADE
                              ↓
                           OBJETIVO
                              ↓
                            ESTADO
                              ↓
                         ESTRATÉGIA
                              ↓
                  ┌───────────┼───────────┐
                  ↓           ↓           ↓
                DIRETO     WORKFLOW     AGENTE
                  │           │           │
                  └───────────┼───────────┘
                              ↓
                           EXECUTOR
                              ↓
                  MODELO / TOOL / AMBIENTE
                              ↓
                            AÇÃO
                              ↓
                         OBSERVAÇÃO
                              ↓
                           EVIDÊNCIA
                              ↓
                         VERIFICAÇÃO
                              ↓
                      ESTADO ATUALIZADO
                              ↓
                     ┌────────┴────────┐
                     ↓                 ↓
                  sucesso            falha
                                       ↓
                                  diagnóstico
                                       ↓
                               nova estratégia
                                       ↓
                                      ↺

Em escala:

                         AUTORIDADE
                              │
                       CONTROLE GLOBAL
                              │
             ┌────────────────┼────────────────┐
             ↓                ↓                ↓
        CONTROLE A       CONTROLE B       CONTROLE C
             │                │                │
         objetivo A       objetivo B       objetivo C
             │                │                │
         estratégia       estratégia       estratégia
             │                │                │
         execução         execução         execução

---

# 65. Resultado final da pesquisa

A pesquisa não terminou com a seleção de um “melhor agente”.

Terminou com uma hipótese de que as categorias:

- agente;
- multimodo;
- multiagente;
- workflow;
- planner;
- especialista;
- modelo;
- ferramenta;

são melhor entendidas como mecanismos diferentes que podem ser selecionados e combinados por um runtime mais geral.

O mecanismo mais profundo identificado foi:

> **não confundir aquilo que está sendo realizado com a estratégia usada para realizá-lo, com quem executa a estratégia ou com o recurso utilizado pelo executor.**

Isso permite que uma mesma execução atravesse:

    estratégia A
       ↓
    falha
       ↓
    estratégia B
       ↓
    executor diferente
       ↓
    modelo diferente
       ↓
    ferramenta diferente
       ↓
    continuidade

sem perder a identidade do objetivo.

---

# 66. Fronteira atual da pesquisa

A pesquisa atingiu um ponto de convergência conceitual suficiente para interromper a busca indiscriminada por novos moldes.

A principal incerteza restante deixou de ser:

> “Existe outra categoria de agente que explique melhor o problema?”

e passou a ser:

> “Quando implementado, o próprio runtime de controle será simples o suficiente para justificar a capacidade que adiciona?”

Essa questão é empírica.

Ela deve ser testada por construção mínima e experimentação real, sem assumir que a hipótese M-2 está correta.

---

# 67. Status para auditoria futura

Esta pesquisa deve ser tratada como um artefato independente para futura comparação com outra pesquisa arquitetural.

Não deve ser:

- fundida com outra pesquisa;
- convertida automaticamente em decisão;
- usada para alterar o código do ABS;
- tratada como arquitetura oficial;
- usada para justificar implementação sem auditoria cruzada.

A decisão arquitetural deverá ocorrer somente depois da comparação independente das pesquisas.

---

# 68. Encerramento

**PESQUISA CONCLUÍDA — AGUARDANDO AUDITORIA CRUZADA**

O estudo preserva as hipóteses investigadas, as simulações conceituais, os ataques, as contradições, os mecanismos sobreviventes, as limitações e as questões abertas.

Nenhuma conclusão deste documento constitui decisão oficial de arquitetura do ABS.
