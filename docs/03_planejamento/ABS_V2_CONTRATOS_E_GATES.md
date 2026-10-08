# ABS V2 — CONTRATOS E GATES DE ACEITE

## 1. Contrato Work

Um Work representa intenção autorizada e seu ciclo de realização.

Campos obrigatórios:

`id, objective, objective_version, origin, authority, constraints, risk, budget, state, mode, capabilities, resources, executor, attempts, events, checkpoints, evidence, provenance, verification, result`

Regras:

- Work não pode ser criado sem objetivo.
- Mudança material do objetivo cria nova versão.
- Executor não pode alterar autoridade.
- Resultado sem verificação não vira conclusão verificada.

## 2. Contrato Capability

Uma capability declara:

- identidade;
- responsabilidade;
- entradas;
- saídas;
- pré-condições;
- permissões;
- risco;
- recursos necessários;
- executor/adapters disponíveis;
- mecanismo de verificação;
- evidência produzida.

Registrar capability não concede autorização de execução.

## 3. Contrato Resource

Um recurso é um meio disponível para uma capability.

Exemplos:

- modelo;
- agente;
- serviço;
- API;
- máquina;
- node;
- ferramenta;
- credencial/conexão;
- executor.

Resource Router seleciona. Policy decide se pode usar. Executor executa.

## 4. Contrato Executor

Todo executor externo deve poder responder de forma normalizada:

`prepare → execute → observe → result → status`

O contrato não deve depender da implementação interna do executor.

Exemplos:

- OpenClaw;
- Codex;
- Agents SDK;
- Agent Framework;
- execução direta;
- futuro executor próprio.

## 5. Contrato Observation

Observation deve separar:

- fonte;
- timestamp;
- operação;
- estado observado;
- saída bruta quando necessária;
- contexto;
- relação com Work/attempt.

Observation não é automaticamente Evidence.

## 6. Contrato Evidence

Evidence deve indicar:

- o que prova;
- fonte;
- método de obtenção;
- integridade/proveniência;
- Work/attempt relacionado;
- nível de confiança;
- validade temporal.

## 7. Contrato Verification

Verification recebe resultado + evidências relevantes e produz:

- accepted/rejected/unknown;
- checks;
- evidências utilizadas;
- razão;
- verifier;
- timestamp.

A verificação deve ser proporcional ao risco.

## 8. Contrato Policy

Policy deve poder responder:

- esta ação é permitida?
- requer aprovação?
- qual executor pode realizá-la?
- quais ferramentas podem ser usadas?
- qual orçamento?
- qual nível de autonomia?
- qual evidência é obrigatória?
- qual risco máximo é aceitável?

Policy deve ser aplicada antes da execução e, quando necessário, durante o ciclo.

## 9. Contrato Mode Selector

Entrada:

- objetivo;
- contexto;
- risco;
- restrições;
- recursos;
- orçamento;
- necessidade de adaptação.

Saída:

- DIRECT;
- WORKFLOW;
- AGENT;
- MULTIAGENT;
- razão;
- requisitos;
- limites.

O selector não pode aumentar a própria autoridade.

## 10. Contrato Executor Router

Entrada:

- Work;
- capability;
- recursos necessários;
- políticas;
- disponibilidade.

Saída:

- executor selecionado;
- adapter;
- plano de fallback;
- justificativa;
- limites.

A seleção não significa execução autorizada.

## 11. Máquina de estados

Fluxo nominal:

`CREATED → PLANNING → READY → RUNNING → COMPLETED → VERIFIED`

Possíveis desvios:

`WAITING_APPROVAL`

`RUNNING → PAUSED → READY`

`RUNNING → WAITING_RESOURCE`

`RUNNING → RECOVERING → REPLANNING`

`RUNNING → UNKNOWN`

`RUNNING → FAILED`

Cancelamento:

`qualquer estado executável → CANCELLED`

Nenhum estado não verificável deve ser promovido diretamente para VERIFIED.

## 12. Gates de segurança

### Gate 1 — Authority
Quem autorizou?

### Gate 2 — Policy
A ação é permitida?

### Gate 3 — Capability
Existe capacidade adequada?

### Gate 4 — Resource
Existe recurso utilizável?

### Gate 5 — Executor
Existe executor compatível?

### Gate 6 — Execution
A execução ocorreu?

### Gate 7 — Observation
O que realmente aconteceu?

### Gate 8 — Verification
Foi provado?

### Gate 9 — State
O estado do Work foi atualizado corretamente?

### Gate 10 — Provenance
O caminho pode ser reconstruído?

## 13. Gates de migração

A migração V1→V2 só pode avançar quando:

- testes V1 continuam verdes;
- contrato novo está coberto;
- adapter substituto funciona;
- rollback foi demonstrado;
- evidência operacional foi registrada;
- nenhum comportamento V1 essencial foi perdido.

## 14. Testes de invariantes

### Autoridade
Tentar fazer modelo/executor aumentar privilégio → REJECT.

### Verificação
Executor afirma sucesso sem prova → UNKNOWN/FAIL conforme risco.

### Substituição
Executor A indisponível → executor B compatível.

### Idempotência
Mesma operação duas vezes → segundo intento não duplica efeito quando a operação é protegida.

### Recovery
Falha após checkpoint → retomar do último estado verificável.

### Concorrência
Dois Works alterando o mesmo recurso incompatível → conflito detectado.

### Memória
Memória antiga contradiz observação atual → revalidar; observação atual vence quando confirmada.

### Budget
Orçamento excedido → parar/replanejar/solicitar autorização.

### Multiagent
Tentativa de criar agentes recursivamente sem orçamento/admission → bloquear.

### Segurança
Prompt/tool injection tenta contornar policy → bloquear e registrar.

### Degradação
Executor principal desaparece → selecionar fallback ou entrar em WAITING_RESOURCE/UNKNOWN.

## 15. Testes adversariais

O conjunto V2 deverá incluir:

- prompt injection;
- tool poisoning;
- executor malicioso;
- verifier comprometido;
- claims falsos;
- metadata de capability desatualizada;
- race condition;
- duplicate execution;
- replay;
- partial success;
- schema drift;
- protocolo incompatível;
- checkpoint corrompido;
- segredo exfiltrado;
- escalada de autoridade;
- loop infinito;
- explosão de subagentes;
- budget exhaustion;
- network partition;
- memória obsoleta;
- conflito entre agentes;
- falha em cascata.

## 16. Aceite da primeira vertical slice V2

A primeira vertical slice não precisa conter todas as capacidades.

Ela precisa provar o contrato completo:

`objetivo → Work → policy → mode → capability → resource → executor → observation → verification → evidence → state`

Com pelo menos:

- DIRECT;
- um executor externo;
- um fallback;
- uma verificação real;
- uma falha recuperável;
- uma evidência persistida;
- uma execução repetida protegida por idempotência.

Somente depois dessa prova começa a expansão para os demais modos.

## 17. Regra final

A arquitetura pode evoluir.

Os contratos fundamentais e invariantes só mudam mediante nova evidência, teste e decisão arquitetural registrada.

Nenhum framework externo pode virar requisito estrutural do ABS apenas por conveniência local.
