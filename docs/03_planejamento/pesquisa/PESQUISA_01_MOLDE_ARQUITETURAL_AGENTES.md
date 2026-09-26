# Título

PESQUISA 01 — MOLDE ARQUITETURAL DE AGENTES

**Identificação da pesquisa:** PESQUISA_01_MOLDE_ARQUITETURAL_AGENTES  
**Data:** 2026-09-26  
**Objetivo:** descobrir, por investigação documental, exploração arquitetural, simulações conceituais, testes adversariais e análise de convergência, os mecanismos e o molde arquitetural mais robusto para a construção futura do agente do ABS, sem escolher framework como arquitetura e sem transformar o resultado desta pesquisa em decisão oficial de implementação.  
**Status:** PESQUISA CONCLUÍDA — AGUARDANDO AUDITORIA CRUZADA  
**Observação:** este estudo ainda NÃO representa uma decisão arquitetural oficial do ABS.

---

# 1. NATUREZA E ESCOPO DO ESTUDO

Esta pesquisa foi conduzida como um experimento de engenharia arquitetural.

O objetivo não foi descobrir “qual framework é melhor”, “qual agente é melhor” ou escolher uma implementação pronta. O objetivo foi descobrir mecanismos arquiteturais que apareçam de forma recorrente quando se tenta construir um sistema capaz de executar tarefas simples e complexas com:

- capacidade;
- confiabilidade;
- autonomia controlada;
- verificabilidade;
- recuperação;
- eficiência;
- modularidade;
- persistência;
- continuidade;
- independência de modelos;
- independência de ferramentas;
- capacidade de utilizar múltiplas IAs;
- capacidade de utilizar diferentes classes de ferramentas;
- capacidade de alternar estratégias conforme a tarefa;
- controle humano;
- auditabilidade;
- substituibilidade de componentes.

O estudo investigou famílias arquiteturais e mecanismos documentados em sistemas e pesquisas contemporâneos, e depois utilizou simulações conceituais e ataques adversariais para tentar descobrir onde cada abordagem funciona, onde falha e quais mecanismos sobrevivem quando a arquitetura é submetida a condições difíceis.

A pesquisa foi explicitamente separada de implementação.

Não houve, como parte desta pesquisa:

- alteração da arquitetura oficial do ABS;
- implementação das conclusões no código;
- escolha definitiva de framework;
- escolha definitiva de fornecedor;
- merge de código;
- declaração de que o molde encontrado é a arquitetura oficial do ABS.

---

# 2. DISTINÇÕES METODOLÓGICAS

Durante o estudo, foram mantidas as seguintes distinções.

## 2.1 Evidência documental

Informação obtida em documentação, artigos técnicos, documentação oficial, descrições de arquiteturas ou literatura técnica.

Uma evidência documental mostra que determinado mecanismo foi documentado, implementado, proposto ou estudado por uma fonte.

Ela não prova automaticamente que o mecanismo é universalmente superior.

## 2.2 Experimento real

Execução efetiva de um sistema, software, agente ou arquitetura em condições controladas, com resultados observáveis.

As simulações desta pesquisa NÃO devem ser confundidas com experimentos reais.

## 2.3 Benchmark

Medição experimental comparável, com tarefas, métricas, condições e resultados definidos.

Esta pesquisa NÃO constitui um benchmark real entre frameworks ou arquiteturas.

## 2.4 Simulação conceitual

Raciocínio estruturado sobre como determinada arquitetura provavelmente se comportaria diante de determinado cenário, considerando seus mecanismos, estado, ferramentas, contexto, falhas e políticas.

As simulações são úteis para exploração e falsificação de hipóteses, mas não equivalem a resultados empíricos.

## 2.5 Hipótese

Proposição ainda não estabelecida.

## 2.6 Inferência

Conclusão intermediária obtida a partir da combinação de evidências e resultados de simulação.

## 2.7 Conclusão arquitetural da pesquisa

Padrão que permaneceu após exploração, comparação e tentativa de refutação suficientes para ser considerado candidato a mecanismo do molde.

Uma conclusão arquitetural desta pesquisa NÃO é uma decisão de implementação do ABS.

---

# 3. METODOLOGIA

A metodologia evoluiu durante a pesquisa.

A investigação começou com estudo de arquiteturas e mecanismos contemporâneos e depois passou para exploração por cenários e simulações.

Foram investigadas famílias como:

- agente monolítico;
- agente único com loop;
- workflow determinístico;
- planner/executor;
- router;
- arquitetura multimodo;
- manager + especialistas;
- hierarquia de agentes;
- multiagente;
- agentes como ferramentas;
- handoffs;
- agentes especializados;
- execução paralela;
- execução sequencial;
- loops iterativos;
- evaluator/optimizer;
- arquiteturas baseadas em estado;
- arquiteturas baseadas em eventos;
- arquiteturas híbridas;
- arquiteturas com memória;
- arquiteturas com contexto dinâmico;
- arquiteturas com seleção de modelos;
- arquiteturas com seleção dinâmica de ferramentas;
- arquiteturas com recuperação;
- arquiteturas com human-in-the-loop;
- arquiteturas com sandbox/execution environment;
- arquiteturas com checkpoints e persistência.

A investigação inicial envolveu pelo menos 1.000 cenários conceituais e 200 cenários adversariais, conforme registrado durante o estudo.

A exploração posterior foi ampliada por famílias e combinações arquiteturais, chegando a milhares de combinações conceituais — registrada no estudo como aproximadamente 3.000 combinações. Também foi registrado que foram analisados mais de 200 modelos/arquiteturas durante a exploração.

Essas quantidades representam cobertura de exploração conceitual. Não representam milhares de benchmarks independentes nem milhares de experimentos reais.

O critério final deixou de ser “quantidade de simulações” e passou a ser CONVERGÊNCIA.

---

# 4. CRITÉRIO DE CONVERGÊNCIA

A pesquisa foi considerada madura quando novas simulações começaram a apresentar principalmente:

- mecanismos já descobertos;
- variações de mecanismos já conhecidos;
- falhas já observadas;
- trade-offs já identificados;
- confirmações de padrões recorrentes;
- pequenas mudanças nas fronteiras de aplicabilidade.

O estudo verificou:

1. Se novas simulações descobriam mecanismos realmente novos.
2. Se novas simulações mudavam conclusões anteriores.
3. Se novas arquiteturas apresentavam vantagens relevantes e generalizáveis.
4. Quais mecanismos reapareciam em diferentes famílias.
5. Quais mecanismos funcionavam apenas em determinados cenários.
6. Quais mecanismos falhavam sob adversarial.
7. Se as últimas simulações estavam produzindo informação nova ou apenas redundância.
8. Se os problemas restantes eram de arquitetura ou de capacidade/modelo/dados/ambiente.
9. Se determinada característica deveria ser obrigatória, condicional ou opcional.
10. Se a arquitetura deveria ser fixa ou capaz de mudar sua própria forma operacional conforme a tarefa.

O resultado foi uma convergência considerada ALTA, MAS NÃO FINAL.

---

# 5. FONTES E EVIDÊNCIAS DOCUMENTAIS INVESTIGADAS

## 5.1 OpenAI / Codex / Agent Harness

### Unrolling the Codex agent loop — OpenAI

A descrição do loop do Codex foi utilizada para investigar o padrão:

modelo → chamada de ferramenta → resultado → novo contexto → nova inferência.

O mecanismo relevante para a pesquisa não é o produto em si, mas a existência de um loop de agente/harness em que:

- o modelo decide;
- ferramentas executam;
- resultados retornam;
- o estado/contexto é atualizado;
- o modelo continua;
- gerenciamento de contexto torna-se necessário;
- sandbox e aprovação podem limitar ações.

Também foi relevante a existência de compactação automática de contexto e a separação entre o modelo e responsabilidades do harness.

### Introducing the Agents API — OpenAI

Foram observados mecanismos relacionados a:

- harness gerenciado;
- compactação de contexto;
- descoberta de ferramentas;
- chamadas programáticas de ferramentas;
- subagentes;
- tarefas de longa duração;
- ambientes de execução.

A evidência foi usada para investigar quais responsabilidades pertencem ao runtime/harness e quais pertencem ao modelo.

### How agents are transforming work — OpenAI

Foi utilizada como evidência de sistemas agentivos executando tarefas de horizonte longo através de ambientes e chamadas de ferramentas.

### WebSockets / bug-fix loop — OpenAI

Foi relevante como exemplo de ciclos iterativos de:

- observar;
- ler;
- modificar;
- testar;
- verificar;
- repetir.

A importância arquitetural está no loop verificável, não no produto específico.

### Agents SDK — OpenAI

Foram observados mecanismos de:

- harness orientado ao modelo;
- arquivos;
- comandos;
- edição de código;
- sandbox;
- separação entre harness e compute.

---

## 5.2 Anthropic

### Effective context engineering for AI agents

Foi utilizada para investigar contexto como algo maior que “janela de tokens”.

A evidência enfatiza:

- instruções;
- ferramentas;
- MCP;
- dados externos;
- histórico;
- seleção contextual;
- just-in-time context;
- compactação;
- notas estruturadas;
- arquiteturas multiagente;
- problemas de tarefas de horizonte longo.

A consequência para o estudo foi separar:

- memória;
- histórico;
- contexto vivo;
- artefatos;
- estado;
- notas;
- evidência.

### How we built our multi-agent research system

Foi utilizada para investigar:

- orchestrator-worker;
- subagentes especializados;
- paralelização;
- decomposição de pesquisa;
- custo de coordenação.

A fonte também foi usada para reconhecer que multiagente aumenta consumo de tokens/custo e não é adequado para todas as tarefas, especialmente quando existem dependências fortes entre etapas.

### Writing effective tools for AI agents

Foi utilizada para investigar:

- ergonomia de ferramentas;
- namespaces;
- propósito distinto;
- descrição clara;
- quantidade de contexto retornado;
- eficiência de tokens;
- avaliação de ferramentas.

### Code execution with MCP

Foi utilizada para investigar execução de código como camada intermediária para orquestrar ferramentas e reduzir overhead de contexto.

### Agent Skills

Foi utilizada para investigar Skills como unidades de conhecimento procedural contendo:

- instruções;
- scripts;
- recursos;
- carregamento dinâmico.

### Advanced tool use

Foi utilizada para investigar:

- descoberta dinâmica de ferramentas;
- carregamento de ferramentas;
- chamadas programáticas;
- redução de sobrecarga de contexto.

---

# 6. GOOGLE ADK

Foram investigados mecanismos documentados no Google ADK.

## 6.1 Runtime e execução

Foram observados:

- sandbox persistente;
- persistência de sessão;
- execução isolada;
- execução multi-etapa;
- análise de dados;
- execução de código.

## 6.2 Padrões de agentes

Foram observados:

- SequentialAgent;
- ParallelAgent;
- LoopAgent;
- estado;
- contexto;
- workflows.

## 6.3 Avaliação

A documentação de avaliação foi usada para investigar:

- uso de ferramentas;
- trajetória multi-turn;
- sucesso da tarefa;
- recuperação;
- geração de casos;
- ciclo avaliação → correção → nova avaliação.

## 6.4 Skills e orquestração

Foram investigados:

- skills;
- callbacks;
- state;
- workflows;
- avaliação;
- deploy;
- observabilidade.

## 6.5 A2A e sistemas distribuídos

Foram observados cenários de:

- feedback intermediário;
- RAG;
- integração de ferramentas;
- incident response;
- especialistas;
- migração distribuída.

---

# 7. LANGGRAPH / DEEP AGENTS E PADRÕES RELACIONADOS

A documentação e os padrões investigados incluíram:

- subagents;
- handoffs;
- router;
- skills;
- memory;
- context engineering;
- graph/function APIs;
- workflows;
- estado;
- execução durável;
- interrupções;
- retomada;
- decomposição de tarefas.

A investigação não tratou LangGraph como molde obrigatório.

Seu valor para a pesquisa foi servir como evidência de mecanismos recorrentes de:

- estado explícito;
- grafo;
- persistência;
- execução durável;
- workflows;
- subagentes;
- interrupção;
- retomada;
- controle de fluxo.

---

# 8. OUTRAS EVIDÊNCIAS ACADÊMICAS INVESTIGADAS

## Agentic Context Engineering

Foi investigada a ideia de contexto evolutivo e playbooks estruturados que podem ser atualizados durante a execução.

A pesquisa registrou resultados experimentais publicados que relatam melhorias em determinados benchmarks. Esses resultados foram tratados como evidência específica da fonte, não como prova universal de superioridade.

## VerifyLLM

Foi investigada a ideia de verificação do plano antes da execução, inclusive utilizando especificações formais em determinados domínios.

O mecanismo extraído foi:

VERIFICAR O PLANO ANTES DA EXECUÇÃO quando o risco justificar.

## Architecting Resilient LLM Agents

Foram investigados mecanismos como:

- plan-then-execute;
- ferramentas limitadas por tarefa;
- sandbox;
- replanejamento;
- DAG;
- human-in-the-loop.

## A-MEM

Foi investigada memória agentiva com:

- organização dinâmica;
- ligação entre memórias;
- evolução da memória.

A pesquisa considerou essa área relevante, mas ainda com convergência menor que os mecanismos fundamentais de estado, contexto e recuperação.

---

# 9. FAMÍLIAS ARQUITETURAIS INVESTIGADAS

A exploração comparou, combinou e atacou diferentes famílias.

## 9.1 Agente único / monolítico

Características:

- um modelo principal;
- loop;
- ferramentas;
- contexto;
- memória opcional.

Vantagens observadas:

- baixa coordenação;
- simplicidade;
- menor overhead;
- bom desempenho conceitual em tarefas simples;
- menor superfície de coordenação.

Fraquezas:

- concentração de decisões;
- dificuldade de especialização;
- maior dependência de um único contexto/modelo;
- risco de decisões erradas propagarem-se pelo loop;
- maior dificuldade em tarefas muito complexas.

Conclusão:

Não foi descartado como mecanismo operacional. Foi descartado como molde universal.

---

# 10. WORKFLOW DETERMINÍSTICO

Características:

- etapas definidas;
- sequência conhecida;
- controle explícito.

Vantagens:

- previsibilidade;
- auditabilidade;
- custo controlável;
- facilidade de testar;
- boa adequação a tarefas conhecidas.

Fraquezas:

- pouca adaptação;
- baixa capacidade de lidar com objetivos ambíguos;
- dificuldade de lidar com ambientes desconhecidos;
- necessidade de conhecer antecipadamente a estrutura da tarefa.

Conclusão:

Workflow é mecanismo importante, mas não pode ser o único modo de execução.

---

# 11. PLANNER / EXECUTOR

Características:

- planejamento explícito;
- execução posterior;
- possibilidade de replanejamento.

Vantagens:

- separação entre intenção e ação;
- melhor tratamento de tarefas longas;
- maior auditabilidade;
- possibilidade de verificar o plano antes da execução.

Fraquezas:

- plano pode estar errado;
- ambiente pode mudar;
- planejamento pode consumir recursos;
- execução pode revelar informação que exige novo plano.

Conclusão:

Planejamento é mecanismo relevante, mas precisa existir dentro de um loop com observação e replanejamento.

---

# 12. ROUTER / MULTIMODO

Características:

- classifica a tarefa;
- escolhe modo operacional.

A exploração mostrou que diferentes tarefas exigem estruturas diferentes.

Foi daí que surgiu um dos mecanismos mais importantes da pesquisa:

## ARCHITECTURE SELECTOR

O sistema não deve ser obrigado a executar todas as tarefas com a mesma arquitetura interna.

Ele deve poder escolher, conforme:

- natureza da tarefa;
- risco;
- complexidade;
- incerteza;
- necessidade de ferramentas;
- dependências;
- orçamento;
- necessidade de paralelização;
- necessidade de especialização;
- necessidade de aprovação humana.

Exemplos de modos:

- fast path;
- workflow;
- planner/executor;
- agente dinâmico;
- manager + especialistas;
- multiagente;
- evaluator/optimizer.

Conclusão:

A capacidade de escolher o molde operacional é mais fundamental que escolher um único molde fixo.

---

# 13. MANAGER + ESPECIALISTAS

Características:

- coordenador;
- especialistas;
- delegação;
- agregação.

Vantagens:

- especialização;
- paralelização;
- isolamento de contexto;
- decomposição.

Fraquezas:

- custo;
- coordenação;
- duplicação de trabalho;
- inconsistências;
- comunicação entre agentes;
- maior superfície de falha.

Conclusão:

Útil quando a tarefa justifica. Não deve ser ativado automaticamente.

---

# 14. MULTIAGENTE

A exploração mostrou repetidamente que multiagente é uma ESTRATÉGIA, não uma capacidade que deva estar sempre ativa.

Pode ajudar quando:

- partes são independentes;
- há necessidade de especialização;
- tarefas podem ser paralelizadas;
- existe ganho de diversidade;
- há necessidade de isolamento.

Pode prejudicar quando:

- etapas dependem fortemente umas das outras;
- coordenação é maior que o trabalho;
- orçamento é pequeno;
- a tarefa é simples;
- agentes repetem informação;
- subagentes geram ruído.

Conclusão:

Multiagente deve ser condicional.

---

# 15. SWARM / ARQUITETURA DESCENTRALIZADA

Foi investigada como alternativa.

Problemas recorrentes:

- dificuldade de autoridade;
- coordenação;
- auditabilidade;
- controle;
- propagação de erro;
- dificuldade de interrupção;
- dificuldade de atribuir responsabilidade;
- dificuldade de aplicar políticas globais.

Conclusão:

Não foi selecionada como fundação do molde ABS.

Pode existir como mecanismo localizado em ambientes específicos, mas não como autoridade arquitetural principal.

---

# 16. AGENTS-AS-TOOLS / AGENT-AS-AGENT

A exploração mostrou utilidade em tratar um agente especializado como recurso controlável.

Isso permite:

- isolamento;
- contrato;
- limite de escopo;
- orçamento;
- entrada definida;
- saída definida;
- possibilidade de substituir o especialista.

O agente especializado não precisa controlar o sistema inteiro.

---

# 17. HANDOFFS

A pesquisa identificou necessidade de handoffs tipados.

Um handoff relevante deve poder transportar:

- objetivo;
- escopo;
- entradas;
- restrições;
- autoridade;
- resultado esperado;
- evidências exigidas;
- prazo;
- orçamento;
- estado;
- incertezas.

A resposta deve poder retornar:

- resultado;
- artefatos;
- evidências;
- falhas;
- incertezas;
- recomendações;
- estado.

Conclusão:

Delegação sem contrato explícito aumenta risco de perda de intenção e autoridade.

---

# 18. LOOPS ITERATIVOS

O loop de agente apareceu como padrão recorrente.

Forma abstrata:

1. entender;
2. planejar;
3. decidir;
4. agir;
5. observar;
6. verificar;
7. decidir novamente;
8. replanejar se necessário;
9. finalizar somente quando houver evidência suficiente.

O loop não deve ser infinito.

Daí surgiu:

## LOOP BUDGET

O sistema deve controlar:

- número de iterações;
- tempo;
- custo;
- chamadas de modelo;
- chamadas de ferramenta;
- subagentes;
- computação.

---

# 19. FAST PATH E DEEP PATH

A exploração mostrou que uma arquitetura que usa toda sua complexidade para toda tarefa desperdiça recursos e aumenta superfície de falha.

Foi descoberto o padrão:

## FAST PATH

Para tarefas:

- simples;
- de baixo risco;
- bem especificadas;
- de alta confiança;
- com pouca necessidade de ferramentas.

## DEEP PATH

Para tarefas:

- complexas;
- longas;
- ambíguas;
- de maior risco;
- com múltiplas dependências;
- que exigem pesquisa;
- que exigem verificação;
- que exigem coordenação.

Conclusão:

Complexidade deve ser elástica.

---

# 20. BUDGET / RESOURCE GOVERNOR

Um mecanismo recorrente identificado foi o controle explícito de recursos.

O governador deve poder controlar:

- tokens;
- tempo;
- dinheiro;
- número de chamadas de modelo;
- número de ferramentas;
- número de subagentes;
- paralelismo;
- computação;
- armazenamento;
- tentativas.

Objetivo:

evitar:

- loops infinitos;
- exploração sem limite;
- subagentes em cascata;
- custos imprevisíveis;
- consumo excessivo;
- tarefas que continuam sem progresso.

---

# 21. CONTROL PLANE

A maior convergência da pesquisa ocorreu em torno de um Control Plane externo ao modelo.

O Control Plane deve ser responsável por:

- receber objetivo;
- aplicar autoridade;
- aplicar políticas;
- analisar tarefa;
- selecionar arquitetura operacional;
- controlar orçamento;
- controlar estado;
- controlar execução;
- controlar autorização;
- controlar recuperação;
- controlar persistência;
- registrar eventos;
- controlar subagentes;
- controlar ferramentas;
- controlar modelos;
- controlar verificação.

O modelo não deve ser a autoridade do sistema.

---

# 22. AUTORIDADE

A pesquisa convergiu para uma regra fundamental:

## A autoridade deve estar fora do modelo.

O modelo pode:

- interpretar;
- planejar;
- sugerir;
- decidir dentro do escopo autorizado;
- selecionar ferramentas permitidas;
- gerar ações.

Mas a autoridade final sobre:

- políticas;
- permissões;
- limites;
- ações de alto impacto;
- aprovação;
- interrupção;
- cancelamento;
- override;

deve estar em uma camada externa.

No contexto do ABS, essa autoridade pertence ao Imperador.

---

# 23. AUTONOMIA GRADUAL

A pesquisa rejeitou o binário:

AUTÔNOMO / NÃO AUTÔNOMO.

Foi proposto um modelo de níveis conceituais:

- L0 — somente resposta;
- L1 — sugestão;
- L2 — ações reversíveis;
- L3 — tarefas delimitadas;
- L4 — autonomia dentro de política;
- L5 — ações de alto impacto dependem de autorização do Imperador.

Esses níveis são um mecanismo de pesquisa, não uma decisão oficial de implementação.

---

# 24. AUTORIZAÇÃO DINÂMICA

Foi identificado que autorização não deve depender apenas do nome da ferramenta.

A autorização deve considerar:

- ação;
- alvo;
- contexto;
- efeitos;
- risco;
- política;
- estado;
- nível de autonomia;
- reversibilidade.

Uma mesma ferramenta pode ser:

- permitida em um contexto;
- proibida em outro;
- permitida com aprovação em outro.

---

# 25. CONTEXTO

A pesquisa concluiu que contexto não deve ser tratado como simples histórico integral.

O Context Engine deve ser capaz de:

- selecionar;
- priorizar;
- filtrar;
- comprimir;
- recuperar;
- injetar;
- retirar;
- atualizar.

Uma classificação conceitual investigada:

- crítico;
- importante;
- útil;
- opcional;
- ruído.

---

# 26. MEMÓRIA

Foi estabelecida uma distinção importante:

## MEMÓRIA ≠ CONTEXTO

Memória é armazenamento recuperável.

Contexto é o conjunto de informações selecionadas para uma inferência específica.

Também foi rejeitada a ideia:

## MEMÓRIA = VERDADE

Memória deve carregar metadados como:

- origem;
- confiança;
- timestamp;
- validade;
- estado de revalidação;
- relacionamento com outras informações.

Memória antiga pode estar errada.

Memória não deve ser autoridade absoluta.

---

# 27. COMPACTION

A compactação foi considerada mecanismo útil para tarefas longas.

Porém:

## COMPACTION ≠ MEMORY

Compactação reduz ou reorganiza contexto ativo.

Não substitui:

- memória;
- estado;
- eventos;
- artefatos;
- evidência;
- histórico persistente.

---

# 28. ESTADO EXTERNO

Uma das maiores convergências foi a necessidade de estado fora do modelo.

O estado deve sobreviver:

- mudança de modelo;
- mudança de contexto;
- reinício;
- falha;
- interrupção;
- troca de ferramenta;
- retomada.

O modelo não deve ser o único local onde existe o estado da tarefa.

---

# 29. PERSISTÊNCIA E RESUME

Tarefas longas exigem capacidade de:

- pausar;
- persistir;
- reiniciar;
- retomar;
- continuar de um checkpoint.

Isso implica:

- estado;
- eventos;
- checkpoints;
- artefatos;
- identificação da tarefa;
- status;
- progresso.

---

# 30. EVENT LOG

A pesquisa identificou o registro de eventos como componente estrutural.

O sistema deve poder registrar, conceitualmente:

- objetivo;
- plano;
- decisão;
- chamada de modelo;
- chamada de ferramenta;
- resultado;
- observação;
- erro;
- verificação;
- recuperação;
- aprovação;
- alteração de estado.

Isso aumenta:

- auditabilidade;
- observabilidade;
- recuperação;
- diagnóstico;
- reconstrução da trajetória.

---

# 31. ESTADOS EXPLÍCITOS

Foi identificado que somente SUCCESS / FAILURE é insuficiente.

Estados importantes incluem:

- RUNNING;
- PAUSED;
- BLOCKED;
- WAITING_APPROVAL;
- WAITING_RESOURCE;
- FAILED;
- STOPPED;
- UNKNOWN.

## UNKNOWN

Foi particularmente importante.

Se o sistema não consegue confirmar se a ação ocorreu ou qual foi seu resultado, não deve afirmar automaticamente sucesso nem falha.

UNKNOWN deve ser estado de primeira classe.

---

# 32. FERRAMENTAS

A pesquisa rejeitou a ideia de disponibilizar todas as ferramentas ao modelo em todo momento.

Foi identificada uma arquitetura de:

TASK → CAPABILITY SEARCH → CANDIDATE TOOLS → SELECTION → LOAD → EXECUTE → VERIFY.

Isso exige:

## Capability Registry

Registro de capacidades disponíveis.

Pode incluir:

- capacidade;
- ferramenta;
- versão;
- permissões;
- pré-condições;
- efeitos;
- side effects;
- custo;
- latência;
- confiabilidade;
- verificabilidade;
- reversibilidade;
- idempotência;
- restrições.

---

# 33. TOOL BROKER

O Tool Broker deve intermediar:

- descoberta;
- seleção;
- carregamento;
- autorização;
- execução;
- observação;
- verificação;
- troca de ferramenta.

Isso ajuda a manter o núcleo independente da ferramenta específica.

---

# 34. MODELOS

O modelo deve ser tratado como recurso substituível.

A pesquisa rejeitou:

## MODELO = ARQUITETURA

A arquitetura deve poder trabalhar com:

- modelos diferentes;
- modelos locais;
- modelos externos;
- modelos especializados;
- modelos de capacidades diferentes.

Foi identificado um:

## MODEL BROKER

Responsável por:

- selecionar;
- rotear;
- substituir;
- adaptar;
- controlar custo;
- controlar capacidade.

---

# 35. MODEL ROUTING

Model routing pode depender de:

- tarefa;
- complexidade;
- risco;
- contexto;
- custo;
- latência;
- disponibilidade;
- capacidade;
- necessidade de especialização.

Porém routing autônomo total continua com convergência menor que os fundamentos.

---

# 36. VERIFICAÇÃO

A verificação apareceu como um dos mecanismos mais fortes.

Ela deve existir depois de ações relevantes.

Mas a pesquisa também descobriu:

## PRE-EXECUTION VERIFICATION

Antes de ações críticas, verificar:

- plano;
- permissões;
- pré-condições;
- alvo;
- efeitos;
- risco;
- orçamento;
- coerência.

Depois:

## POST-EXECUTION VERIFICATION

Verificar:

- resultado;
- pós-condição;
- evidência;
- efeitos;
- integridade.

---

# 37. VERIFICADOR NÃO PRECISA SER OUTRO LLM

Foi rejeitada a ideia de que toda verificação deve ser feita por outro modelo.

Dependendo do caso, o verificador pode ser:

- teste determinístico;
- regra;
- invariável;
- comparação;
- evidência externa;
- ferramenta independente;
- modelo independente;
- mesmo modelo;
- humano.

Quando o risco é alto, depender do mesmo mecanismo que produziu a decisão pode reproduzir o mesmo erro.

---

# 38. EVIDENCE LEDGER

Foi descoberto um mecanismo adicional:

## EVIDENCE LEDGER

Resultados e afirmações importantes devem poder apontar para:

- evidência;
- fonte;
- operação;
- timestamp;
- ferramenta;
- documento;
- modelo;
- estado da verificação.

Isso evita que uma afirmação sobreviva separada de sua origem.

---

# 39. PROVENIÊNCIA

Foi identificada como propriedade estrutural:

RESULTADO → OPERAÇÃO → FERRAMENTA → API/DOCUMENTO → MODELO/MEMÓRIA.

Proveniência permite saber:

- de onde veio;
- quando veio;
- como foi transformado;
- quem/qual componente produziu;
- se foi verificado.

---

# 40. RECOVERY

A pesquisa rejeitou:

## RETRY INFINITO

Recuperação deve depender do tipo de falha.

Possibilidades:

- retry;
- fallback;
- trocar ferramenta;
- trocar modelo;
- replanejar;
- rollback;
- compensar;
- pedir autorização;
- intervenção humana;
- abortar.

---

# 41. ACTION SEMANTICS

Foi descoberto que ações precisam ter semântica explícita.

Metadados relevantes:

- é idempotente?
- é reversível?
- é transacional?
- possui side effects?
- pode ser compensada?
- pode ser repetida com segurança?
- como verificar seu resultado?

Isso influencia diretamente recovery.

---

# 42. RECOVERY POLICY ENGINE

A recuperação não deve ser simplesmente:

ERRO → TENTE NOVAMENTE.

Deve considerar:

- tipo de erro;
- estado;
- risco;
- custo;
- orçamento;
- alternativas;
- semântica da ação;
- possibilidade de rollback;
- possibilidade de compensação;
- necessidade de humano.

---

# 43. EXECUTION ENVIRONMENT

A execução deve ser separada do modelo.

Pode existir:

- sandbox;
- ambiente isolado;
- shell;
- execução de código;
- filesystem;
- browser;
- APIs;
- servidores;
- dispositivos.

A arquitetura deve controlar o ambiente, não entregar autoridade total ao modelo.

---

# 44. SUBAGENTS COMO RECURSOS CONTROLADOS

A pesquisa identificou:

## AGENT ADMISSION CONTROL

Subagentes não devem nascer sem controle.

Antes de criar um subagente, considerar:

- necessidade;
- escopo;
- orçamento;
- autoridade;
- contexto;
- permissões;
- prazo;
- resultado esperado.

O subagente deve poder ser:

- criado;
- monitorado;
- limitado;
- interrompido;
- encerrado.

---

# 45. CONTRATOS DE SUBAGENTES

Cada subagente deve receber um contrato tipado.

Entrada conceitual:

- objetivo;
- escopo;
- contexto;
- restrições;
- permissões;
- orçamento;
- prazo;
- formato de saída;
- requisitos de evidência.

Saída conceitual:

- resultado;
- artefatos;
- evidências;
- falhas;
- incertezas;
- estado;
- recomendação.

---

# 46. WORKFLOW + AGENT

A exploração mostrou que workflow e agente não precisam competir.

Um molde híbrido pode usar:

- workflow para partes previsíveis;
- agente para partes incertas;
- ferramenta para operações;
- especialista para domínio;
- verificador para validação;
- humano para decisões de alto impacto.

---

# 47. ARQUITETURA HÍBRIDA

A convergência favoreceu uma arquitetura híbrida.

Não:

“tudo é workflow”.

Não:

“tudo é agente”.

Não:

“tudo é multiagente”.

Mas:

## usar a menor estrutura suficiente para a tarefa.

Esse princípio apareceu como uma das consequências mais importantes da exploração.

---

# 48. ARQUITETURE SELECTOR

O mecanismo de seleção arquitetural foi considerado uma descoberta relevante.

Fluxo conceitual:

TASK ANALYZER  
↓  
ARCHITECTURE SELECTOR  
↓  
FAST PATH / WORKFLOW / AGENT / MULTI-AGENT / HYBRID  
↓  
EXECUTION

A escolha deve considerar:

- complexidade;
- risco;
- incerteza;
- dependências;
- paralelismo;
- especialização;
- orçamento;
- necessidade de verificação;
- autorização.

---

# 49. META-CONTROLE

A arquitetura não deve somente executar.

Ela deve poder controlar:

- como executa;
- quanto pode executar;
- quando deve parar;
- quando deve mudar de estratégia;
- quando deve pedir ajuda;
- quando deve verificar;
- quando deve replanejar.

Isso caracteriza uma camada de meta-controle.

---

# 50. TESTES ADVERSARIAIS

As arquiteturas foram atacadas conceitualmente com:

- loops;
- decisões erradas;
- alucinações;
- uso incorreto de ferramentas;
- excesso de ferramentas;
- poucas ferramentas;
- perda de contexto;
- memória incorreta;
- estado perdido;
- APIs indisponíveis;
- modelos indisponíveis;
- resultados incompletos;
- resultados contraditórios;
- falhas de execução;
- subagentes fora de controle;
- excesso de autonomia;
- pouca autonomia;
- impossibilidade de verificar;
- impossibilidade de recuperar;
- impossibilidade de retomar;
- dependência de fornecedor;
- dependência de modelo;
- single points of failure;
- custo excessivo;
- latência excessiva;
- falso sucesso;
- planejamento incorreto;
- objetivo ambíguo;
- objetivo mutável;
- contexto excessivo;
- contexto insuficiente.

---

# 51. RESULTADOS RECORRENTES DOS ATAQUES

## 51.1 Loop sem limite

Falha.

Resposta arquitetural:

- loop budget;
- budget governor;
- stop conditions;
- estado;
- recovery policy.

## 51.2 Modelo errado

Falha possível.

Resposta:

- model broker;
- modelo substituível;
- verificação;
- fallback;
- replanejamento.

## 51.3 Ferramenta errada

Falha possível.

Resposta:

- capability registry;
- tool broker;
- contratos;
- verificação;
- fallback;
- troca de ferramenta.

## 51.4 Contexto excessivo

Falha possível.

Resposta:

- context engine;
- ranking;
- filtering;
- compaction;
- just-in-time context.

## 51.5 Contexto insuficiente

Falha possível.

Resposta:

- retrieval;
- memória;
- estado;
- evidência;
- contexto sob demanda.

## 51.6 Memória errada

Falha possível.

Resposta:

- origem;
- timestamp;
- confiança;
- validade;
- revalidação.

## 51.7 Subagente fora de controle

Falha possível.

Resposta:

- admission control;
- scope;
- permissions;
- budget;
- typed handoff;
- termination.

## 51.8 Falso sucesso

Falha crítica.

Resposta:

- post-verification;
- evidence;
- postcondition;
- UNKNOWN.

## 51.9 Falha durante execução

Resposta:

- checkpoint;
- event log;
- state;
- recovery;
- resume.

---

# 52. ARQUITETURAS / MECANISMOS DESCARTADOS COMO FUNDAÇÃO

A pesquisa não afirma que estes mecanismos nunca têm utilidade. Eles foram descartados como fundação universal do molde.

- swarm descentralizado como autoridade;
- multiagente sempre ativo;
- contexto completo sempre carregado;
- memória tratada como verdade;
- uma IA para tudo;
- uma ferramenta por capacidade sem broker;
- framework como núcleo da arquitetura;
- interface como núcleo da arquitetura;
- modelo como autoridade;
- verificador exclusivamente baseado em LLM;
- retry infinito;
- subagentes sem orçamento;
- autonomia irrestrita;
- aprovação humana para absolutamente tudo;
- memória vetorial como memória única;
- auto-modificação irrestrita;
- workflow determinístico como única forma;
- agente puro como única forma.

---

# 53. MECANISMOS CONTROVERSOS OU DE CONVERGÊNCIA MÉDIA

## Memória agentiva

Promissora, mas ainda não tão consolidada quanto estado externo, contexto, persistência e recuperação.

## Self-improvement

Relevante, mas com riscos de:

- drift;
- alteração indesejada;
- auto-referência;
- dificuldade de auditoria;
- perda de controle.

## Model routing autônomo

Útil, mas precisa de política e avaliação.

## Multi-agent adaptativo

Promissor, porém sensível a custo e coordenação.

---

# 54. ÁREAS INSUFICIENTEMENTE TESTADAS

Permaneceram como questões abertas:

- memória completamente auto-organizada;
- prompts permanentemente auto-modificáveis;
- Control Plane que se reescreve autonomamente;
- arquitetura totalmente descentralizada;
- governança sem Imperador;
- autoavaliação sem mecanismos externos;
- seleção arquitetural automática universal;
- aprendizagem online permanente sem autorização;
- auto-organização total de agentes;
- autogoverno completo.

---

# 55. PROBLEMAS NÃO RESOLVIDOS

A pesquisa não eliminou:

- raciocínio incorreto;
- verificador incorreto;
- informação externa incorreta;
- objetivos mal especificados;
- ambiguidade de autoridade;
- custo de coordenação;
- instruções maliciosas;
- memória incorreta;
- erro compartilhado entre modelo e verificador;
- segurança de ferramentas;
- mudanças de ambiente;
- conflitos entre objetivos;
- conflitos entre políticas;
- impossibilidade de observar determinados efeitos externos.

---

# 56. MATRIZ DE CONVERGÊNCIA

| Categoria | Resultado |
|---|---|
| Agent loop | Convergência muito alta |
| Estado externo | Convergência muito alta |
| Persistência/checkpoints | Convergência alta |
| Event log | Convergência alta |
| Context engineering | Convergência muito alta |
| Memória separada de contexto | Convergência alta |
| Tool abstraction | Convergência alta |
| Tool discovery | Convergência alta |
| Capability registry | Convergência alta |
| Model abstraction | Convergência alta |
| Model routing | Convergência média/alta |
| Verification | Convergência muito alta |
| Recovery | Convergência muito alta |
| Human authorization | Convergência muito alta |
| Policy engine | Convergência alta |
| Budget governor | Convergência alta |
| Pre-execution verification | Convergência alta |
| Post-execution verification | Convergência muito alta |
| Evidence/provenance | Convergência alta |
| Fast path | Convergência alta |
| Deep path | Convergência alta |
| Workflow | Convergência alta como modo |
| Planner/executor | Convergência alta como modo |
| Multi-agent | Convergência condicional |
| Handoffs | Convergência alta quando há delegação |
| Agent-as-tool | Convergência condicional |
| Agent admission control | Convergência alta |
| Dynamic architecture selection | Convergência alta como hipótese arquitetural |
| Agentic memory | Convergência média |
| Self-improvement | Convergência média/baixa |
| Fully decentralized architecture | Convergência baixa |
| Autonomous self-rewriting | Convergência baixa |

---

# 57. ARQUITETURAS CANDIDATAS QUE PERMANECERAM RELEVANTES

As famílias abaixo permaneceram relevantes, mas não como vencedoras exclusivas:

## OpenAI / Codex-like harness

Relevante para:

- agent loop;
- ferramentas;
- sandbox;
- contexto;
- compactação;
- execução longa.

## Anthropic-like context engineering

Relevante para:

- contexto;
- just-in-time retrieval;
- ferramentas;
- subagentes;
- skills;
- compactação.

## LangGraph-like stateful orchestration

Relevante para:

- estado;
- grafos;
- execução durável;
- interrupção;
- retomada;
- subagentes;
- workflows.

## Google ADK-like workflow/agent runtime

Relevante para:

- sequential;
- parallel;
- loops;
- state;
- sessions;
- sandbox;
- evaluation;
- observability;
- A2A.

Nenhuma dessas referências foi considerada arquitetura oficial do ABS.

---

# 58. MOLDE RESULTANTE DA EXPLORAÇÃO

A convergência não ocorreu em torno de um framework.

O padrão recorrente foi:

## CONTROL + STATE + CONTEXT + MODELS + TOOLS + EXECUTION + OBSERVATION + VERIFICATION + RECOVERY + AUTHORITY

A pesquisa concluiu que o molde mais consistente não é:

“um agente com muitas ferramentas”.

É:

## um sistema de controle capaz de montar, operar, verificar, interromper, recuperar e substituir diferentes configurações de execução conforme a tarefa.

Isso implica:

- autoridade externa;
- Control Plane;
- seleção arquitetural;
- loop;
- estado;
- contexto;
- memória;
- modelos substituíveis;
- ferramentas substituíveis;
- execução isolada;
- observação;
- verificação;
- recuperação;
- orçamento;
- auditoria;
- controle humano.

---

# 59. DIAGRAMA CONCEITUAL RESULTANTE

```
                         IMPERADOR
                             │
                    ┌────────▼────────┐
                    │ AUTHORITY       │
                    │ + POLICY        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ CONTROL PLANE   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        TASK ANALYZER   ARCHITECTURE    BUDGET
                         SELECTOR        GOVERNOR
              │              │              │
              └──────────────┼──────────────┘
                             ▼
                      EXECUTION PLAN
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
             FAST PATH              DEEP PATH
                  │                     │
                  │          ┌──────────┼─────────┐
                  │          ▼          ▼         ▼
                  │       Workflow    Agent    Multi-Agent
                  │                     │
                  └──────────┬──────────┘
                             ▼
                       AGENT RUNTIME
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 CONTEXT ENGINE        MODEL BROKER         TOOL BROKER
        │                    │                    │
        ▼                    ▼                    ▼
    MEMORY               MODELS              CAPABILITIES
        │                                         │
        └────────────────────┬────────────────────┘
                             ▼
                     EXECUTION ENVIRONMENT
                             │
                             ▼
                          OBSERVE
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
               PRE-VERIFY          EXECUTE
                                      │
                                      ▼
                                  POST-VERIFY
                                      │
                           ┌──────────┼──────────┐
                           ▼          ▼          ▼
                         PASS       FAIL       UNKNOWN
                           │          │          │
                           ▼          ▼          ▼
                        COMMIT     RECOVERY   INVESTIGATE
                                      │
                       ┌──────────────┼──────────────┐
                       ▼              ▼              ▼
                     RETRY         REPLAN        HUMAN
                                      │
                                      └──────→ LOOP

              ─────────────────────────────────────
                STATE + EVENTS + EVIDENCE + AUDIT
              ─────────────────────────────────────
```

Este diagrama é o resultado conceitual da pesquisa, não uma arquitetura oficial implementada.

---

# 60. REQUISITOS DO MOLDE ABS

Os seguintes requisitos sobreviveram à exploração e foram registrados como requisitos candidatos do molde.

## R1 — Autoridade externa ao modelo

A autoridade não pode depender do modelo.

## R2 — Control Plane independente

Deve existir uma camada de controle independente da implementação específica do agente/modelo.

## R3 — Agent Loop explícito

Deve existir capacidade de entender, planejar, decidir, agir, observar, verificar e replanejar.

## R4 — Estado externo

O estado da tarefa deve existir fora do modelo.

## R5 — Persistência e retomada

Tarefas devem poder ser pausadas, persistidas e retomadas.

## R6 — Event Log

Eventos importantes devem ser registrados.

## R7 — Context Engine

Contexto deve ser selecionado, organizado e controlado.

## R8 — Memória separada de contexto

Memória e contexto devem ser conceitos distintos.

## R9 — Memória não é verdade absoluta

Memória precisa de confiança, origem, validade e possibilidade de revalidação.

## R10 — Abstração de modelo

O núcleo não pode depender de um único modelo.

## R11 — Model routing

O sistema deve poder selecionar modelos conforme tarefa e política.

## R12 — Abstração de ferramenta

O núcleo não deve depender de uma ferramenta específica.

## R13 — Descoberta de ferramentas

Ferramentas devem poder ser descobertas conforme capacidade necessária.

## R14 — Capability Registry

Capacidades disponíveis devem ser registradas e consultáveis.

## R15 — Execution Isolation

Execução deve possuir isolamento e limites apropriados.

## R16 — Pré-verificação

Ações críticas devem poder ser verificadas antes da execução.

## R17 — Pós-verificação

Resultados devem ser verificados após a execução.

## R18 — Evidence

Resultados relevantes devem possuir evidência.

## R19 — Provenance

Resultados devem possuir proveniência.

## R20 — Recovery

O sistema deve suportar retry, fallback, troca, rollback, compensação, replanejamento, humano e abortamento conforme contexto.

## R21 — Budget

Deve existir orçamento para tempo, tokens, custo, ferramentas, subagentes e computação.

## R22 — Loop Budget

Loops devem possuir limites.

## R23 — Fast Path

Tarefas simples devem poder usar caminho simplificado.

## R24 — Deep Path

Tarefas complexas devem poder receber estrutura adicional.

## R25 — Multi-agent condicional

Multiagente deve ser ativado somente quando justificado.

## R26 — Subagentes limitados

Subagentes devem possuir escopo, permissões, orçamento, contexto e contrato de saída.

## R27 — Typed Handoffs

Delegação deve possuir contrato tipado.

## R28 — Workflows e agents

O sistema deve suportar ambos.

## R29 — Arquitetura híbrida

O sistema deve combinar diferentes mecanismos.

## R30 — Autonomia gradual

Autonomia deve ser controlável por níveis.

## R31 — Human-in-the-loop

Deve existir aprovação, rejeição, pausa, retomada, cancelamento e override.

## R32 — Autorização baseada em ação/contexto/efeitos

Permissão não deve depender apenas da identidade da ferramenta.

## R33 — UNKNOWN

Incerteza operacional deve ser estado de primeira classe.

## R34 — Verificação independente quando possível

O mecanismo de verificação deve poder ser diferente do mecanismo produtor.

## R35 — Substituibilidade

Modelos, ferramentas, agentes e outros componentes devem poder ser substituídos.

## R36 — Interface desacoplada

A interface não deve definir o núcleo da arquitetura.

## R37 — Framework/fornecedor não é arquitetura

Frameworks devem ser componentes substituíveis.

## R38 — Auditabilidade

A trajetória deve poder ser auditada.

## R39 — Observabilidade

O sistema deve expor estado, eventos, execução e falhas.

## R40 — Capability switching durante execução

O sistema deve poder mudar de modelo, ferramenta, estratégia ou arquitetura operacional quando necessário e autorizado.

---

# 61. CONCLUSÕES DA PESQUISA

## Conclusão 1

Não existe uma topologia única que seja ideal para todas as tarefas.

## Conclusão 2

O molde deve ser adaptativo.

## Conclusão 3

A arquitetura deve controlar agentes, e não depender de um agente como controlador absoluto.

## Conclusão 4

Estado externo, persistência e recuperação são fundamentos, não acessórios.

## Conclusão 5

Context engineering é estrutural para tarefas longas.

## Conclusão 6

Memória e contexto devem ser separados.

## Conclusão 7

Ferramentas precisam ser tratadas como capacidades descobríveis e controláveis.

## Conclusão 8

Modelos devem ser recursos substituíveis.

## Conclusão 9

Multiagente é estratégia condicional.

## Conclusão 10

Verificação precisa existir tanto antes quanto depois de ações de maior importância.

## Conclusão 11

Recovery precisa ser uma política arquitetural, não um retry genérico.

## Conclusão 12

UNKNOWN precisa ser representado explicitamente.

## Conclusão 13

Orçamento é mecanismo de segurança e eficiência.

## Conclusão 14

Autonomia precisa ser graduada.

## Conclusão 15

A autoridade deve permanecer fora do modelo.

## Conclusão 16

O molde deve permitir workflows e agentes dentro do mesmo sistema.

## Conclusão 17

A complexidade deve aumentar conforme a tarefa exige.

## Conclusão 18

O núcleo deve ser independente de framework, fornecedor, modelo, ferramenta e interface.

## Conclusão 19

A principal convergência foi para um sistema de controle adaptativo, não para um agente monolítico.

## Conclusão 20

A descoberta mais importante foi a mudança de pergunta:

não “qual agente devemos construir?”,

mas:

“qual sistema deve controlar diferentes formas de execução agentiva de maneira verificável, recuperável, substituível e sob autoridade humana?”

---

# 62. LIMITAÇÕES

1. As simulações são conceituais.
2. Não foram realizadas milhares de execuções reais de cada arquitetura.
3. Quantidade de simulações não equivale a quantidade de evidências independentes.
4. Resultados de simulação dependem das premissas usadas.
5. Diferentes modelos reais podem alterar resultados.
6. Ferramentas reais possuem diferenças de confiabilidade, latência e segurança.
7. Custos reais podem divergir.
8. Ambientes reais introduzem falhas que uma simulação conceitual pode não reproduzir.
9. Algumas arquiteturas foram investigadas em nível documental e conceitual, não por implementação equivalente.
10. Não existe garantia de que o molde identificado seja ótimo em todos os domínios.
11. Alguns mecanismos permanecem insuficientemente testados.
12. A pesquisa não substitui validação experimental futura.
13. A matriz de convergência é uma avaliação arquitetural, não uma métrica científica universal.
14. As fontes documentais possuem escopos e objetivos diferentes.
15. Resultados publicados em benchmarks específicos não devem ser generalizados automaticamente.

---

# 63. INCERTEZAS

Continuam incertos:

- até onde architecture selection pode ser automatizado com segurança;
- qual nível de complexidade é economicamente justificável;
- quanto multiagente deve ser usado em tarefas reais;
- como medir corretamente o valor de memória agentiva;
- como evitar erros correlacionados entre produtor e verificador;
- como construir verificação independente em todos os domínios;
- como tratar instruções maliciosas em ferramentas;
- como resolver conflitos de objetivos;
- como fazer aprendizagem online sem perda de controle;
- como permitir evolução arquitetural sem autoalteração perigosa;
- como determinar automaticamente quando uma tarefa precisa de humano;
- como construir políticas universais de recuperação;
- como medir autonomia de forma objetiva entre domínios diferentes.

---

# 64. QUESTÕES ABERTAS

1. O Control Plane deve ser completamente determinístico, híbrido ou parcialmente agentivo?
2. Até que ponto o Architecture Selector pode decidir sua própria estrutura?
3. Qual é o limite seguro de autonomia?
4. Como representar políticas complexas?
5. Como verificar decisões quando não existe teste determinístico?
6. Como separar erro de modelo de erro de ferramenta?
7. Como medir confiança real?
8. Como detectar que memória ficou inválida?
9. Como detectar que uma tarefa mudou de natureza no meio da execução?
10. Como decidir quando replanejar?
11. Como decidir quando abandonar?
12. Como tratar UNKNOWN em ações externas com efeitos irreversíveis?
13. Como coordenar múltiplos modelos sem criar dependência excessiva?
14. Como garantir que um subagente não expanda seu próprio escopo?
15. Como impedir crescimento exponencial de subagentes?
16. Como auditar decisões distribuídas?
17. Como verificar agentes que verificam outros agentes?
18. Como combinar evidência contraditória?
19. Como fazer seleção dinâmica de ferramentas sem sobrecarregar contexto?
20. Como manter substituibilidade real, e não apenas nominal?

---

# 65. GRAU DE CONVERGÊNCIA

## ALTO / MUITO ALTO

- autoridade externa;
- Control Plane;
- loop;
- estado;
- persistência;
- checkpoints;
- eventos;
- contexto;
- memória separada;
- ferramentas controláveis;
- modelos substituíveis;
- verificação;
- recovery;
- human authorization;
- observabilidade;
- auditabilidade.

## ALTO / CONDICIONAL

- workflows;
- planner/executor;
- multiagente;
- handoffs;
- agent-as-tool;
- parallelização;
- architecture selection;
- fast/deep paths.

## MÉDIO

- memória agentiva;
- model routing autônomo;
- self-improvement;
- adaptação multiagente.

## BAIXO / INSUFICIENTE

- descentralização total;
- auto-organização total;
- auto-reescrita permanente;
- governança sem autoridade humana;
- aprendizagem permanente sem aprovação.

Resultado geral:

# CONVERGÊNCIA ALTA, MAS NÃO FINAL.

A convergência é forte sobre os fundamentos, mas não sobre todas as formas de adaptação e autoevolução.

---

# 66. CANDIDATO A MOLDE ARQUITETURAL

A pesquisa produziu como candidato conceitual:

## SISTEMA DE CONTROLE ADAPTATIVO PARA EXECUÇÃO ORIENTADA A OBJETIVOS

Características:

- autoridade externa;
- políticas;
- estado;
- objetivos;
- continuidade;
- recuperação;
- meta-controle;
- seleção arquitetural;
- agentes substituíveis;
- workflows substituíveis;
- modelos substituíveis;
- ferramentas substituíveis;
- verificação;
- evidência;
- orçamento;
- controle humano.

O molde não exige que a execução seja sempre:

- agente;
- multiagente;
- workflow;
- planner;
- modelo único.

Ele permite selecionar a estrutura mínima suficiente.

---

# 67. FORMULAÇÃO ALTERNATIVA ENCONTRADA DURANTE A PESQUISA

Também foi registrada a formulação:

## “Molde de Execução sob Autoridade”

e, em inglês:

## “Goal-Oriented Adaptive Execution Runtime”

Essas formulações são nomes conceituais usados durante a exploração. Não são nomes oficiais de componentes do ABS.

---

# 68. CUIDADOS CONTRA INTERPRETAÇÃO INCORRETA

O estudo NÃO conclui que:

- OpenAI seja a arquitetura do ABS;
- Anthropic seja a arquitetura do ABS;
- LangGraph seja a arquitetura do ABS;
- Google ADK seja a arquitetura do ABS;
- multiagente seja obrigatório;
- um determinado modelo seja obrigatório;
- um framework específico seja obrigatório;
- o diagrama apresentado seja implementação;
- os 40 requisitos já sejam especificação oficial;
- o candidato de molde já esteja aprovado;
- o ABS deva ser implementado agora.

O estudo conclui somente que determinados mecanismos sobreviveram à exploração conceitual e devem ser considerados na futura auditoria cruzada.

---

# 69. REGRA DE PRESERVAÇÃO DA PESQUISA

Este documento deve permanecer separado de outras pesquisas arquiteturais.

A Pesquisa 01 deve ser tratada como uma unidade documental independente.

Uma futura auditoria cruzada deve:

- comparar esta pesquisa com a Pesquisa 02;
- preservar divergências;
- preservar contradições;
- identificar convergências independentes;
- identificar resultados exclusivos;
- verificar quais conclusões realmente sobrevivem quando as pesquisas são comparadas.

Nenhuma divergência deve ser apagada para produzir falsa convergência.

---

# 70. ESTADO FINAL DA PESQUISA

**Pesquisa:** PESQUISA 01 — MOLDE ARQUITETURAL DE AGENTES  
**Natureza:** investigação arquitetural documental + simulação conceitual + análise adversarial  
**Benchmark real:** não realizado  
**Implementação do resultado:** não realizada  
**Código ABS alterado pela pesquisa:** não  
**Arquitetura oficial do ABS definida:** não  
**Convergência:** alta, mas não final  
**Próxima etapa prevista:** auditoria cruzada com pesquisa independente  
**Estado:** PESQUISA CONCLUÍDA — AGUARDANDO AUDITORIA CRUZADA

---

# 71. REGISTRO DE INTEGRIDADE INTERPRETATIVA

As afirmações deste estudo devem continuar classificadas segundo sua natureza original:

- **EVIDÊNCIA:** documentação ou literatura investigada;
- **EXPERIMENTO:** execução real, quando houver;
- **BENCHMARK:** medição experimental comparável, quando houver;
- **SIMULAÇÃO:** análise conceitual de comportamento;
- **HIPÓTESE:** proposição ainda não estabelecida;
- **INFERÊNCIA:** conclusão derivada da combinação de evidências e simulações;
- **CONCLUSÃO ARQUITETURAL:** padrão que sobreviveu à exploração;
- **DECISÃO DE IMPLEMENTAÇÃO:** não produzida por esta pesquisa.

A ausência de experimento real não deve ser escondida.

A ausência de benchmark real não deve ser convertida em benchmark implícito.

Uma simulação não deve ser citada posteriormente como prova experimental.

Uma hipótese não deve ser citada posteriormente como fato.

Uma conclusão desta pesquisa não deve ser citada posteriormente como decisão oficial do ABS sem passar pela auditoria cruzada e pela autorização correspondente.

---

# 72. FIM DA PESQUISA 01

Este documento preserva o resultado recuperável da pesquisa arquitetural realizada nesta linha de investigação.

A pesquisa permanece independente e aguardando auditoria cruzada.

Nenhuma implementação é autorizada por este documento.
