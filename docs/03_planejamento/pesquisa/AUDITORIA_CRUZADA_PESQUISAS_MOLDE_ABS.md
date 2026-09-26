# AUDITORIA CRUZADA — PESQUISAS DO MOLDE ABS

**Status:** CONCLUÍDA  
**Escopo:** comparar as duas pesquisas somente depois da auditoria individual.

## 1. Convergências

As duas pesquisas convergem independentemente no núcleo conceitual:

- autoridade separada da execução;
- objetivo separado da estratégia;
- estado persistente externo ao modelo;
- modelos substituíveis;
- ferramentas/capacidades substituíveis;
- contexto gerenciado;
- observação;
- verificação;
- recuperação;
- orçamento/limites;
- workflows como mecanismos condicionais;
- agentes como mecanismos condicionais;
- multiagente como estratégia condicional;
- complexidade elástica;
- possibilidade de mudar estratégia durante a execução.

As duas também rejeitam, como molde absoluto:
- agente universal monolítico;
- multimodo rígido;
- multiagente como núcleo obrigatório;
- workflow rígido;
- planner permanente;
- descentralização absoluta.

## 2. Divergências

As divergências são menores que as convergências.

A Pesquisa 01 enfatiza mais:
- requisitos;
- control plane;
- tool/model brokers;
- evidence ledger;
- provenance;
- recovery policy;
- autonomia e autorização;
- architecture selector.

A Pesquisa 02 enfatiza mais:
- redução ao núcleo;
- elasticidade da complexidade;
- objetivo × estratégia × ação;
- identidade da execução;
- evolução V0→V3;
- substituição de componentes;
- escala e mutação.

Isso é complementar, não contraditório.

## 3. Ponto metodológico crítico

A convergência entre os estudos é significativa, mas não deve ser tratada como dois experimentos independentes confirmando empiricamente o mesmo resultado.

Eles são estudos conceituais produzidos em contexto relacionado e compartilham o mesmo problema, linguagem e objetivo geral.

Portanto:

**CONVERGÊNCIA CONCEITUAL: FORTE**

**CONFIRMAÇÃO EMPÍRICA INDEPENDENTE: NÃO EXISTE**

## 4. Evidência externa

As fontes atuais verificadas independentemente sustentam a existência de mecanismos semelhantes:

- OpenAI Agents SDK: agentes, ferramentas, handoffs, guardrails, sessões e runtime de turnos. https://openai.github.io/openai-agents-python/
- OpenAI tool guardrails: validação antes/depois de ferramentas e possibilidade de bloquear execução. https://openai.github.io/openai-agents-python/guardrails/
- Anthropic: contexto como recurso finito e necessidade de curadoria dinâmica do contexto em loops longos. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic: ferramentas precisam ser projetadas como contratos entre sistemas determinísticos e agentes não determinísticos. https://www.anthropic.com/engineering/writing-tools-for-agents
- Microsoft Agent Framework: agentes em workflows, workflows como agentes, checkpoints, retomada, observabilidade e multiagente. citeturn0search1turn0search9
- Microsoft Agent Framework: HITL e aprovação de ferramentas antes da execução. https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop

Essas fontes sustentam mecanismos, não o molde ABS como superior.

## 5. Resultado cruzado

A melhor síntese não é escolher Pesquisa 01 ou Pesquisa 02.

É combinar os mecanismos que sobreviveram às duas:

**CONTROLE + OBJETIVO + ESTADO + ESTRATÉGIA + CONTEXTO + CAPACIDADES + EXECUÇÃO + OBSERVAÇÃO + VERIFICAÇÃO + RECUPERAÇÃO + AUTORIDADE**

com execução adaptável:

**DIRETO | WORKFLOW | AGENTE | MULTIAGENTE**

selecionada conforme a tarefa.

## 6. Resultado epistemológico

O que podemos afirmar:

### Forte
Esses mecanismos existem em sistemas reais/documentados e são recorrentes em arquiteturas contemporâneas.

### Moderado
A combinação parece uma hipótese arquitetural coerente para o ABS.

### Ainda não demonstrado
Que essa combinação seja mais eficiente, confiável ou simples que alternativas em implementação real.

## 7. Veredito da auditoria cruzada

As pesquisas não precisam ser descartadas.

Também não devem ser tratadas como prova definitiva.

Elas produziram uma **hipótese arquitetural suficientemente forte para passar à fase de construção experimental mínima**.

Não é autorização automática para implementar toda a arquitetura.
