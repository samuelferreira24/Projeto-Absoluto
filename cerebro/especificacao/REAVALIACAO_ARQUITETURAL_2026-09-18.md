# Reavaliação Arquitetural — Ciclo 2026-09-18

## Objetivo

Reavaliar o estado real do Projeto Absoluto antes de continuar a construção, sem assumir que o plano anterior continua sendo a melhor rota.

## Estado observado

A branch de desenvolvimento `base-cerebro-v0.1` já contém uma base muito mais ampla do que o mapa mestre V0.2 registra. Existem componentes funcionais iniciais para:

- ingestão e coleta;
- memória e recuperação;
- proveniência e rastreabilidade;
- histórico temporal;
- identidade e eventos;
- continuidade;
- aprendizagem e consolidação;
- grafo de tarefas;
- scheduler adaptativo;
- seleção de executores;
- orçamento de combustível;
- simulação de planos;
- replanejamento;
- retries, fallbacks e cancelamento;
- claims/leases para evitar dispatch duplicado;
- executor autorizado;
- política de autonomia;
- telemetria;
- persistência da orquestração;
- detecção inicial de sinergias;
- runtime contínuo;
- workflows de despertar, validação e coleta.

Portanto, o próximo avanço não deve ser simplesmente adicionar outro componente isolado.

## Descobertas arquiteturais

### 1. A orquestração já ultrapassou o planejamento inicial

Há uma cadeia real:

`objetivo → tarefas → grafo → scheduler → plano → controle → executor → resultado → aprendizado → replanejamento`

Isso muda a prioridade: agora o valor maior está em integrar, validar e endurecer essa cadeia.

### 2. Existem superfícies de orquestração que precisam de contratos mais claros

A base contém:

- `Orquestrador`: missão/ciclo persistente;
- `AgendadorAdaptativo`: seleção de tarefas;
- `OrquestradorAdaptativo`: fachada do scheduler;
- `ExecutorPlano`: execução de um plano;
- `RuntimeContinuo`: ciclos contínuos;
- `ControleExecucao`: claims e leases.

Eles podem representar camadas diferentes, mas a fronteira entre missão, plano, tarefa, ciclo e execução ainda precisa ser consolidada em contratos únicos. A duplicação de especificações V0.1/V0.2 sobre agendamento confirma essa necessidade.

### 3. Existem dois modelos de recursos que ainda não estão unificados

`cerebro/recursos.py` representa estoque de recursos/capacidade com origem, quantidade, validade, consumo e valor gerado.

O scheduler usa `OrcamentoCombustivel` e `PerfilExecutor` como modelo próprio.

Ambos são úteis, mas ainda não existe uma ligação canônica entre:

`estoque de recurso → capacidade/motor → custo → combustível → consumo → resultado`

Essa integração deve ser feita antes de uma economia de capacidade mais avançada.

### 4. O paralelismo não deve ser maximizado por padrão

Pesquisa recente de 2026 mostra que planejamento multiagente deve ser avaliado sob dependências, perturbações e coordenação, e que paralelismo tem trade-offs de comunicação e recuperação. O REALM-Bench avalia explicitamente dependências, threads paralelas e perturbações dinâmicas. citeturn0search0

A arquitetura já calcula makespan e comunicação, mas ainda usa heurísticas simples. O próximo passo é medir o ganho real do paralelismo, não aumentar o número de tarefas simultâneas.

### 5. Durabilidade exige semântica explícita de replay

Pesquisas atuais de execução durável destacam determinismo, checkpointing, idempotência, retries e separação entre orquestração e efeitos colaterais. Operações com efeitos externos precisam de chaves de idempotência ou semântica de execução adequada. citeturn2search0turn2search1turn2search3

O Projeto já possui idempotency keys, claims e recuperação. A lacuna restante é transformar essas ideias em um contrato uniforme de execução de efeitos externos.

### 6. Segurança deve acompanhar a autonomia, não vir depois

A pesquisa atual trata identidade, ferramentas, harness/orquestração e ambiente como camadas de segurança distintas. Least privilege, allowlists de ferramentas, aprovação humana e auditoria devem estar na fronteira de execução. citeturn0search4turn1search6turn1search26

O Projeto já possui níveis de autonomia, aprovação, identidade, telemetria e controle. Nesta rodada, a allowlist de executáveis foi endurecida para comparar caminhos resolvidos, evitando que apenas o nome do executável determine autorização.

### 7. Memória e orquestração precisam de avaliação contínua

Benchmarks atuais de memória avaliam aprendizagem online, retenção, transferência e esquecimento, enquanto trabalhos recentes mostram que estruturas de memória mais complexas não são automaticamente superiores a baselines mais simples. citeturn0search1turn0search8

Conclusão: não devemos aumentar a complexidade da memória ou dos grafos sem medir se a recuperação e a aplicação realmente melhoram.

## Correções implementadas neste ciclo

### Correção A — Semântica de recursos

Antes, `GrafoTarefas.prontas(None)` tratava ausência de filtro como conjunto vazio, bloqueando qualquer tarefa que declarasse recurso.

Agora:

- `None` = nenhum filtro externo de disponibilidade foi imposto;
- `set()` = nenhum recurso externo está disponível.

Foram adicionados testes para os dois comportamentos.

### Correção B — Claim duplicado

Antes, `Cerebro.iniciar_plano()` adquiria o claim e `ExecutorPlano.executar()` tentava adquiri-lo novamente.

Agora o claim pertence ao `ExecutorPlano`, que controla o ciclo completo de execução.

`iniciar_plano()` apenas registra o início operacional do plano.

Foi adicionado teste de integração da fachada.

### Correção C — Allowlist técnica

A autorização de executáveis deixou de comparar apenas o basename.

Agora os caminhos são resolvidos antes da comparação com a allowlist.

Foi adicionado teste que demonstra que um caminho diferente não é aceito apenas por possuir o mesmo nome.

## Pesquisa externa considerada

- REALM-Bench: avaliação de planejamento/agendamento multiagente sob dependências e perturbações. citeturn0search0
- AgentMemoryBench: avaliação de memória online, replay, transferência e esquecimento. citeturn0search1
- AWS Durable Execution: determinismo, checkpoint/replay, idempotência, retries e operações duráveis. citeturn2search0turn2search1turn2search3
- Microsoft: identidade, RBAC, escopo e binding seguro de ferramentas para agentes. citeturn0search4
- OpenAI: sandbox, guardrails, aprovação, observabilidade e limites de ferramentas. citeturn1search0turn1search6turn1search9
- Anthropic/NIST RFI: segurança como propriedade do sistema inteiro, incluindo modelo, ferramentas, harness e ambiente. citeturn1search26

## Estado do Git

`main` permanece em:

`958476848b5111cdac02efa6206f2fb32f550624`

A branch de desenvolvimento está separada de `main`. O compare atual mostra divergência histórica entre as linhas: a branch está à frente em centenas de commits e também está atrás de alguns commits de `main`. Isso não foi alterado neste ciclo, porque sincronizar essas linhas sem uma operação de integração/revisão explícita pode introduzir mudanças não relacionadas.

Nenhuma alteração foi feita em `main`.

## Próxima etapa identificada automaticamente

A próxima etapa de maior valor não é criar mais uma camada isolada.

É construir uma **camada de contratos e integração do núcleo de execução**, unificando:

`Missão → Plano → Tarefa → Claim → Autorização → Execução → Resultado → Evento → Aprendizado`

e ligando o modelo de recursos ao combustível do scheduler.

Depois disso, a prioridade passa a ser um **harness de avaliação**, capaz de executar cenários controlados de falha, retry, paralelismo, custo, risco, autorização e recuperação, comparando o resultado observado com o planejado.

Essa etapa desbloqueia evolução segura do scheduler, do runtime, da memória e da futura multi-IA sem transformar cada novo componente em mais uma superfície isolada.
