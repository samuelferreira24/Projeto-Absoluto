# ABS V2 — FECHAMENTO PRÉ-CONSTRUÇÃO

**Estado:** arquitetura preparada para engenharia; construção V2 ainda não iniciada  
**Branch:** `arquitetura/abs-v2-pre-construcao`  
**Baseline:** `main @ dee0b582249b22b0549e3994e982a36298c15e2a`  
**Regra:** preservar a V1 operacional e evoluir por contratos verificáveis.

## 1. Decisão arquitetural

O ABS não será reconstruído como um "superagente".

> **ABS é o sistema soberano que transforma objetivos autorizados em capacidades coordenadas, selecionando e governando os meios necessários para realizá-los.**

O ABS pode usar agentes, modelos, ferramentas, workflows, nós, protocolos e serviços externos, mas nenhum desses meios define a identidade ou autoridade do ABS.

## 2. Núcleo soberano

Permanecem sob responsabilidade própria do ABS:

- autoridade do Imperador;
- políticas e limites;
- Work e ciclo de vida;
- estado e transições;
- seleção de modo;
- seleção/roteamento de capacidades e recursos;
- admission control e orçamento;
- evidência, proveniência e auditoria;
- verificação e estado UNKNOWN;
- recovery/replanning;
- memória/estado soberano;
- contratos entre componentes;
- identidade do ABS;
- decisão sobre adoção/substituição de executores.

Nenhum modelo, agente, ferramenta ou executor poderá aumentar sua própria autoridade.

## 3. Modos de execução

O ABS escolhe o menor mecanismo suficiente:

`DIRETO → WORKFLOW → AGENTE → MULTIAGENTE`

- **DIRETO:** operação simples, determinística ou de baixo risco.
- **WORKFLOW:** ordem/etapas explícitas.
- **AGENTE:** raciocínio adaptativo necessário.
- **MULTIAGENTE:** somente quando divisão/delegação realmente agregar valor.

Multiagente não será o padrão.

## 4. Work como unidade soberana

Toda operação relevante deve estar vinculada a um Work.

Campos mínimos:

- work_id;
- objective + objective_version;
- autoridade/origem;
- constraints;
- risco;
- orçamento;
- estado;
- modo selecionado;
- capacidades/recursos escolhidos;
- executor(es);
- attempts;
- checkpoints;
- eventos;
- observações;
- evidências;
- proveniência;
- verificação;
- resultado;
- falha/recovery;
- parent/child work quando houver.

Estados necessários:

`CREATED, PLANNING, WAITING_APPROVAL, READY, RUNNING, PAUSED, WAITING_RESOURCE, RECOVERING, REPLANNING, UNKNOWN, FAILED, COMPLETED, VERIFIED, CANCELLED`

## 5. Separação epistemológica

O ABS não tratará a saída de uma IA ou executor como prova.

Fluxo:

`CLAIM → OBSERVATION → EVIDENCE → VERIFICATION → CONCLUSION`

Se não houver evidência suficiente:

`UNKNOWN`

Exemplo: "OpenClaw instalou X" é uma afirmação. Exit code, existência do binário e execução bem-sucedida são observações/evidências. Só depois vem a conclusão verificada.

## 6. Memória e estado

Precedência operacional:

1. estado atual verificado;
2. observação atual;
3. evidência verificada;
4. estado recente;
5. memória;
6. hipótese do modelo.

Conflito entre memória e estado atual dispara revalidação.

Memória de executor externo não substitui memória soberana do ABS.

## 7. Recovery

Recovery deve trabalhar sobre o último estado verificável, não sobre a última afirmação de um executor.

Obrigatórios:

- checkpoint;
- retry controlado;
- idempotência;
- detecção de duplicação;
- substituição de executor;
- replanejamento;
- tratamento de sucesso parcial;
- tratamento de conflito;
- rollback quando aplicável;
- estado UNKNOWN quando não for possível concluir.

## 8. Autoridade, risco e autonomia

Autonomia não será um booleano global.

A decisão depende de:

- tipo de ação;
- risco;
- impacto;
- reversibilidade;
- autorização;
- contexto;
- política;
- orçamento.

Operações de alto impacto ou irreversíveis exigem controle/approval conforme política.

## 9. Executores externos

### OpenClaw — ADOTAR COMO EXECUTOR DE AGENTE/OPERAÇÃO

OpenClaw não será incorporado como "ABS". Será um executor atrás de contrato.

Uso previsto:

`ABS → Executor Router → OpenClaw → ferramentas/nó/host`

Peças aproveitáveis:

- gateway/controle de sessão;
- execução de ferramentas;
- shell/arquivo/browser;
- sessões;
- plugins/integrações;
- nodes;
- mecanismos de aprovação;
- sandbox/política de ferramentas.

O ABS continuará responsável por Work, autoridade, política soberana, evidência e conclusão.

### MCP — ADOTAR COMO PROTOCOLO DE FERRAMENTAS/RECURSOS

MCP será uma fronteira de interoperabilidade, não um núcleo do ABS.

`ABS policy → MCP adapter → server/tool/resource`

Ferramenta MCP nunca recebe autoridade implícita.

### A2A — ADOTAR COMO PROTOCOLO DE AGENTES EXTERNOS

A2A será utilizado quando houver necessidade real de conversar com agentes independentes.

Um task externo pode ser associado a um Work do ABS.

A2A não substitui Work nem governa o ABS.

### OpenAI Agents SDK — ADOTAR COMO EXECUTOR OPCIONAL

Será uma opção de executor para tarefas agentic quando suas primitivas forem vantajosas.

Não será dependência obrigatória do ABS.

### Microsoft Agent Framework — ADOTAR COMO EXECUTOR/WORKFLOW OPCIONAL

Será avaliado para workflows, agentes, human-in-loop e checkpoints.

Não será o controlador do ABS.

### Temporal — RESERVAR PARA DURABILIDADE REAL

Temporal é forte candidato para execução durável em escala. Não deve ser introduzido apenas por prestígio tecnológico.

Primeiro o ABS define o contrato de Work/durabilidade. Depois Temporal pode implementar essa responsabilidade se demonstrar vantagem suficiente.

### LangGraph — NÃO ADOTAR COMO DEPENDÊNCIA BASE

Pode ser executor/adaptador futuro. Não há motivo para adicionar outro runtime de grafo enquanto o contrato do ABS ainda puder ser implementado sem ele.

### Codex — MANTER COMO EXECUTOR ESPECIALIZADO

Codex permanece capacidade/executor de engenharia, atrás do contrato de execução do ABS.

## 10. Regra de composição

Um componente externo só entra se:

1. resolver uma responsabilidade real;
2. tiver contrato compatível;
3. reduzir complexidade ou aumentar confiabilidade;
4. permanecer substituível;
5. não tomar autoridade do ABS;
6. puder ser verificado;
7. não criar dependência desnecessária.

Não haverá "coleção de frameworks".

## 11. Componentes próprios a consolidar

A V2 deverá consolidar, sem presumir uma nova árvore de diretórios específica:

- Authority/Policy;
- Work/State;
- Context;
- Strategy;
- Mode/Architecture Selector;
- Budget/Risk Governor;
- Capability Registry;
- Resource Manager/Router/Dispatcher;
- Intelligence/Executor Registry;
- Execution adapters;
- Observation;
- Evidence;
- Verification;
- Provenance;
- Recovery;
- Replanning;
- Memory/Knowledge;
- Idempotency;
- Conflict management;
- Protocol adapters;
- Interface/Gateway.

A organização física será determinada pelo código existente e pelos contratos, não por uma árvore imposta antecipadamente.

## 12. Invariantes obrigatórios

1. Autoridade do Imperador não pode ser escalada por IA/ferramenta/executor.
2. Nenhuma conclusão de sucesso sem verificação exigida pelo risco.
3. UNKNOWN nunca equivale a sucesso.
4. Toda execução relevante possui Work, tentativa e proveniência.
5. Executor externo é substituível.
6. Tarefa simples não entra desnecessariamente em loop de agente.
7. Ações de alto risco passam por política/approval.
8. Retry não duplica efeitos não idempotentes.
9. Conflitos entre Works são detectados.
10. Memória não vence estado atual verificado.
11. Falha do executor não corrompe o estado soberano.
12. ABS continua funcional em modo degradado.
13. Executor externo não pode redefinir o núcleo.
14. Transições importantes são auditáveis.
15. Seleção de arquitetura é limitada por política e orçamento.
16. Claims de ferramentas não são confiança automática.
17. Fronteiras externas são autenticadas/autorizadas.
18. Recovery parte do último estado verificável.

## 13. Critérios de prontidão para iniciar construção

A construção V2 só começa depois de:

- baseline V1 registrado;
- inventário do ABS atual confrontado com o molde V2;
- responsabilidades duplicadas identificadas;
- contratos definidos;
- fronteiras de autoridade definidas;
- executores externos classificados;
- plano de migração V1→V2 definido;
- invariantes convertidos em testes;
- estratégia de compatibilidade definida;
- estratégia de rollback definida;
- critérios de aceite definidos;
- riscos de migração classificados.

## 14. Estratégia de migração

Não haverá big-bang rewrite.

Sequência:

1. proteger baseline V1;
2. criar contratos;
3. adicionar testes de invariantes;
4. colocar adapters atrás dos contratos;
5. migrar uma responsabilidade por vez;
6. manter V1 funcional durante a transição;
7. executar testes unitários + integração + adversariais;
8. validar no VPS;
9. só então retirar duplicações antigas.

## 15. Estado de conclusão desta etapa

A etapa de desenho está fechada.

O que falta antes da primeira alteração estrutural de código é a **matriz de convergência peça-a-peça** e sua transformação em plano de migração executável.

Nenhum componente será removido apenas porque parece redundante. A remoção exige evidência de substituição e cobertura de testes.
