# ABS V4 Completa — Plano Mestre de Arquitetura, Integração e Fechamento

**Estado:** PLANEJAMENTO-MESTRE — proposta técnica para revisão; não é prova de implementação nem autorização para alterar produção.  
**Data:** 2026-10-09  
**Base de auditoria:** repositório `samuelferreira24/Projeto-Absoluto`, branch `main`, checkpoint operacional de 2026-10-09.  
**Objetivo:** definir o destino arquitetural completo do ABS em construção, aproveitar o que já existe, escolher componentes de mercado por função e organizar uma única trajetória de implementação com critérios de fechamento.  
**Regra:** fases abaixo são etapas de execução de um único plano V4, não versões provisórias que exijam reconstrução.

---

## 1. Decisão de enquadramento

O Projeto Absoluto é maior que o ABS. O **ABS geral / Sistema Absoluto** é o ecossistema aberto de capacidades e recursos do Imperador. O **ABS em construção** é o sistema operador/orquestrador desse ecossistema. A V4 trata do ABS em construção, sem pretender encerrar ou limitar o ecossistema inteiro.

A V4 não é:
- um chatbot, uma interface, um agente universal ou um modelo de IA;
- a instalação de todos os produtos conhecidos;
- uma reescrita total de V3;
- a promessa de autonomia ilimitada ou ausência de falhas;
- uma versão mínima que depois exija outra arquitetura.

A V4 é a **arquitetura-alvo completa** para o ABS operar capacidades heterogêneas com autoridade humana, contratos estáveis, estado durável, execução recuperável, verificação independente, memória/proveniência, observabilidade, segurança e expansão para múltiplos nós.

**Princípio de implementação:** preservar componentes que passam a auditoria; substituir apenas quando uma lacuna comprovada exigir. O caminho de V3 para V4 é uma migração incremental, compatível e verificável, não um descarte.

## 2. Baseline observado — o que existe e o que não se pode presumir

O handoff mais recente em `continuidade/08_HANDOFF_ESTABILIZACAO_VPS_IA_LOCAL_2026-10-09.md` registra:
- ABS V3 ativo e health check `alive`;
- runner principal e reserva ativos;
- 202 testes aprovados no checkpoint;
- aproximadamente 4,3 GiB de RAM disponível e 16 GiB livres em disco naquele momento;
- limites de recursos e reinício para os runners e Ollama;
- Qwen 0.8B e Qwen 2B validados ponta a ponta no chat do ABS, sequencialmente;
- Qwen 4B, Ministral 3B e Gemma 4 E2B/E4B registrados, mas não validados neste ambiente e não autorizados a rodar em lote;
- bateria automática dos seis modelos bloqueada.

O código contém, entre outros:
- `abs_core/v3.py`: controle adaptativo, política de custo, capacidade, seleção de inteligência, estado/eventos e ciclo de execução;
- `abs_core/runtime.py`: composition root e integração de registros, roteamento, aprendizagem de ferramentas, runtime cognitivo e inteligência operacional;
- `abs_core/operational_intelligence.py`: plano `direct/workflow/agent/multiagent`, critérios, desconhecidos e replanejamento limitado;
- contratos de capacidades e registro em `abs_core/capabilities.py`;
- verificação em `abs_core/verification.py`;
- API/servidor, endpoint `/v3/status`, chat e compatibilidade OpenAI descrita em `docs/03_planejamento/INTEGRACAO_OPENWEBUI_GATEWAY_ABS.md`;
- estado persistente V3 em SQLite, proveniência/eventos, registros de conhecimento, trajetória e inventário das 72 capacidades;
- integração de GitHub, Codex, motores de IA, navegação HTTP/conhecimento, ferramentas, interface web, atualização/rollback e continuidade;
- runners self-hosted principal e reserva no mesmo VPS.

**Não comprovado como fechado só pela existência de código:** ciclo completo Cérebro → missão → Work → capacidade → resultado → Cérebro; fila durável e concorrência distribuída; execução contínua recuperável; multi-IA end-to-end para todos os motores; aprendizado que altere comportamento de modo verificável; memória temporal completa; auditoria independente; isolamento de código/agentes; restauração de backup; operação de navegador autenticado; HA entre nós.

A classificação vigente de fechamento lista 35 capacidades operacionais, 27 parciais, 6 de governança e 4 planejadas. Esse catálogo não é prova de que todas as capacidades parciais estão prontas. O fechamento V4 deve consumir `capability_registry.json` e `closure_registry.json`, atualizando-os apenas com evidência real.

Há um PR diagnóstico aberto `#123` para OpenClaw/VPS bridge com indicação explícita de que não se destina a merge em produção. Ele deve ser avaliado e fechado/arquivado quando o diagnóstico terminar; não deve virar dependência arquitetural por acidente.

## 3. Objetivo funcional da V4

Dada uma missão do Imperador, o ABS deve conseguir:

1. interpretar o objetivo, restrições, contexto, prazo, risco, orçamento e critérios de sucesso;
2. consultar estado, memória, decisões, evidências, recursos e capacidades disponíveis;
3. escolher o modo de execução mínimo suficiente: direto, workflow, agente ou multiagente;
4. decompor o objetivo, declarar premissas e desconhecidos, planejar e solicitar esclarecimento/aprovação quando necessário;
5. selecionar modelo, ferramenta, ambiente e executor com base em competência, política, disponibilidade, custo, privacidade e recursos;
6. persistir missão, plano, autorizações, tentativas, eventos e checkpoints antes de efeitos importantes;
7. executar em adaptadores isolados e substituíveis;
8. observar resultados e coletar evidências;
9. verificar sucesso de forma proporcional ao risco e, quando apropriado, por caminho independente do executor;
10. replanejar, tentar alternativa, pausar ou escalar quando falhar — sem fingir sucesso;
11. registrar o que foi aprendido e atualizar conhecimento apenas com proveniência e validação;
12. devolver ao Imperador resultado, evidências, custos, mudanças, pendências e próximos passos;
13. continuar ou recuperar tarefas após reinício, timeout, falha de modelo, perda de conexão ou substituição de componente;
14. ser operável pelo celular, sem exigir programação manual frequente;
15. permitir trocar ferramentas, provedores, bancos, executores, interfaces e nós sem alterar os contratos centrais.

## 4. Arquitetura-alvo

A arquitetura é dividida por responsabilidade. Os componentes podem ser processos separados ou módulos no mesmo processo, conforme recursos; os contratos não dependem dessa escolha.

### A. Autoridade, identidade e política
Responsável por identidade do Imperador, papéis, permissões, aprovação, limites de risco, orçamentos, escopos e revogação.
- Toda ação tem principal solicitante, política aplicável e escopo explícito.
- Modelos e agentes podem propor, nunca conceder a si próprios autoridade.
- Ações externas irreversíveis, financeiras, destrutivas ou de publicação exigem aprovação explícita conforme política.
- Negação por padrão para capacidades desconhecidas, como já exige a V3.
- Segredos fora de prompts, logs, repositório e proveniência pública.

### B. Interface do Imperador
A interface web atual continua como superfície principal inicial, não como cérebro.
- Chat/missões, projetos, recursos, inteligências, estado, arquivos, aprovações, eventos, evidências e operação.
- Texto, voz, imagem e comandos multimodais entram como tipos de entrada; capacidades ausentes ficam declaradas.
- Modo explorar/editar/operar deve distinguir alteração visual de alteração operacional real.
- Estado de execução e aprovação visíveis; notificação e retomada pelo celular.
- Open WebUI pode continuar como interface de chat alternativa, atrás do contrato ABS, sem assumir autoridade.

### C. API e contratos estáveis
Manter APIs atuais compatíveis e formalizar contratos versionados para:
- Mission/Objective;
- Plan/Step/Dependency;
- Work/Attempt/Checkpoint;
- Capability/Tool/Executor;
- Authorization/Approval;
- Evidence/Provenance/Verification;
- Memory/Knowledge/Experience;
- Model/Provider/Account/Connection;
- Event/Notification;
- Node/Environment/Health;
- Cost/Budget/ResourceSnapshot.

Toda execução precisa de identificador estável, correlação ponta a ponta, estados válidos, erro estruturado e esquema versionado. Mudanças incompatíveis passam por migração e período de compatibilidade; não se espalham chamadas específicas de fornecedores pelo núcleo.

### D. Cérebro e inteligência operacional
Manter a inteligência operacional do ABS como camada de controle e estratégia, ampliando sua integração com o Cérebro existente.
- Loop fechado: observar → contextualizar → planejar → autorizar → executar → verificar → atualizar estado/conhecimento → replanejar.
- Seleção elástica entre execução direta, workflow, agente e multiagente.
- Multiagente apenas quando paralelismo/independência trouxer benefício verificável.
- Supervisão e meta-supervisão têm escopo e poder limitados; o verificador não deve ser o mesmo raciocínio do executor em tarefas de alto risco.
- Planejamento declara sucesso esperado, critérios, premissas, desconhecidos, orçamento, risco e política de parada.
- Falha de planejamento produz UNKNOWN/hold, nunca um executor inventado.
- O aprendizado de ferramenta/modelo usa estatísticas observadas, amostra mínima, janela temporal, incerteza e reversão; não aprende de uma única resposta nem de conteúdo web não confiável.

### E. Registro de capacidades e adaptadores
O registry existente evolui para catálogo operacional verificável:
- ID estável, contrato de entrada/saída, versão, permissões exigidas, custo, latência, saúde, dependências, localização, isolamento, evidência de validação e política de fallback.
- Descoberta não equivale a aprovação; registrada não equivale a testada; testada não equivale a integrada; integrada não equivale a operacionalmente comprovada.
- Cada adaptador implementa contratos do ABS e mapeia erros específicos para uma taxonomia comum.
- Adapters prioritários: local AI, APIs remotas, Codex, GitHub, HTTP/search, navegador, filesystem, shell/container sandbox, notificações e nós remotos.

### F. Gateway e roteamento de inteligências
Não substituir o roteador V3 sem uma comparação controlada. Criar uma fronteira de provider com:
- capacidades declaradas (chat, raciocínio, tool calling, visão, áudio, embeddings, código, contexto);
- limites de tokens/contexto, orçamento, política de privacidade, latência, disponibilidade e qualidade observada;
- fallback entre provedores, cooldown, timeout, circuit breaker, retries idempotentes e telemetria;
- separação entre modelo que planeja, modelo que executa ferramenta e verificador, quando apropriado;
- suporte a APIs pagas, assinaturas e modelos locais, com custos e permissões explícitos.

**Candidato de mercado:** LiteLLM para gateway de provedores, chaves, orçamentos e fallback, apenas se a auditoria provar lacuna na camada atual. Não delegar ao LiteLLM o planejamento estratégico, autoridade, política do ABS nem a escolha de estratégia de execução. Comparar integração direta atual versus gateway externo antes de adotar.

### G. Execução durável e filas
Esta é uma das lacunas centrais a fechar.
- Persistir a intenção e o estado antes de iniciar efeitos.
- Estados explícitos: created, planned, awaiting_approval, queued, running, paused, retryable, verifying, completed, failed, denied, cancelled, needs_human, compensated.
- Tentativas, leases, heartbeat, timeout, deduplicação, idempotency key, backoff, cancelamento e recuperação.
- Work durável é fonte de verdade; fila em memória é apenas otimização.
- Reconciliador detecta trabalhos presos, resultados incertos e efeitos externos parcialmente concluídos.
- Retentativas distinguem falha transitória de erro permanente; ações não idempotentes exigem reconciliação/aprovação antes de repetir.
- Começar com o store e mecanismos existentes; introduzir PostgreSQL/Redis/Temporal somente quando a semântica e os testes demonstrarem necessidade. Temporal é candidato para workflows longos e duráveis, não uma instalação automática na VPS atual.
- A fila não deve ser considerada durável por ter uma classe Queue nem por teste unitário.

### H. Memória, conhecimento e experiência
Manter separadas:
- estado operacional atual;
- memória episódica (missões, tentativas, resultados);
- conhecimento semântico e documentação;
- histórico imutável/eventos;
- experiência reutilizável;
- decisões e autoridade;
- fontes e evidências;
- artefatos e arquivos;
- trajetória de proveniência.

PostgreSQL é candidato para dados operacionais compartilhados quando houver necessidade de múltiplos serviços; pgvector pode ser adicionado ao mesmo PostgreSQL se busca semântica for validada como útil. Não instalar banco vetorial separado sem benchmark e caso concreto. Preservar SQLite para estado local apropriado e migração testada; não fazer migração por moda.

Toda memória deve indicar origem, tempo, escopo, confiança/estado epistemológico, validade, relação com decisão e condições de atualização. Conteúdo de web/documentos é dado não confiável, nunca política ou instrução de autoridade.

### I. Conhecimento e pesquisa web
Criar um roteador de aquisição:
1. fonte/API oficial quando existe;
2. HTTP e extração para páginas simples;
3. pesquisa web (SearXNG é candidato auto-hospedado) quando busca for necessária;
4. Chromium + Playwright para JavaScript/interação;
5. agente de navegador (Browser Use ou Stagehand) quando a tarefa exigir interpretação adaptativa;
6. serviço gerenciado de browser como capacidade externa opcional quando faltar capacidade local.

A camada visual pessoal e a automação do ABS devem ter perfis, cookies, credenciais e permissões separados. Navegador não deve ter acesso à rede interna administrativa, sockets Docker, metadados cloud ou arquivos do núcleo. Bloquear SSRF, downloads executáveis não aprovados e exfiltração de segredos. Navegadores autenticados exigem isolamento por perfil e aprovação para operações sensíveis.

### J. Execução de código e construção autônoma
A capacidade de construir o próprio ABS é estratégica, mas deve ser isolada.
- GitHub e runners existentes são mantidos; não executar workflows pesados concorrentes sobre a mesma árvore de trabalho.
- Ambientes efêmeros de build/teste; checkout isolado, limites de CPU/RAM/disco/tempo e rede mínima.
- Alterações passam por branch, diff, testes, revisão de risco, CI, deploy controlado, health check e rollback.
- O agente de código propõe patches; ABS verifica e controla o merge/deploy conforme autorização.
- Não executar código arbitrário de modelo no host. Usar contêineres com privilégios mínimos; avaliar microVM como Firecracker ou serviço sandbox isolado quando a ameaça e o ambiente justificarem.
- Não tornar uma IA de programação específica obrigatória. Codex é capability substituível.

### K. Ferramentas e integrações (MCP e APIs)
MCP é uma opção de interoperabilidade para ferramentas, não uma fronteira de confiança.
- Gateway ABS controla identidade, scopes, schemas, limites, auditoria e aprovação.
- Cada servidor MCP é catalogado como capacidade externa e validado.
- Credenciais de cada conector têm mínimo privilégio; tools não recebem acesso universal.
- Chamadas são validadas contra schemas, limites de tamanho e política de efeitos.
- Tool discovery nunca executa automaticamente um recurso recém-descoberto.
- Integrações diretas REST continuam permitidas quando forem mais simples/seguras.

### L. Verificação, avaliação e red team
Fechar a diferença entre “a execução retornou completed” e “o objetivo foi alcançado”.
- Verificação estrutural, verificação de contrato, teste funcional, validação semântica por critérios de sucesso e evidência externa quando aplicável.
- Verificador independente em tarefas de maior risco/complexidade.
- Testes de regressão, benchmark de modelos, testes de prompt injection, falhas parciais, concorrência, duplicação, timeout, provider outage, memória cheia e restauração.
- Avaliar qualidade e custo por classe de tarefa; nenhuma pontuação arbitrária substitui evidência.
- Capturar falhas como casos de teste reproduzíveis.

**Candidato:** Langfuse para tracing/avaliações de IA, se o volume e o custo operacional justificarem; OpenTelemetry como padrão de instrumentação. Não enviar prompts sensíveis sem política explícita de retenção e mascaramento.

### M. Observabilidade e operação
Um painel de estado unificado deve mostrar:
- health por componente/nó;
- fila, trabalhos ativos/presos, idade da tarefa, tentativas;
- memória/CPU/disco, swap e limites;
- estado dos modelos e inferências;
- provedores, latência, erros, rate limits e custos;
- backups recentes e última restauração testada;
- versão/commit implantado, testes e resultado de deploy;
- eventos de segurança e aprovações pendentes.

Uptime Kuma pode continuar para disponibilidade simples. OpenTelemetry/Prometheus/Grafana são candidatos para métricas mais completas; Langfuse cobre telemetria específica de IA. Não instalar o stack completo sem verificar RAM/disco e a necessidade real.

### N. Arquivos e armazenamento
- Separar dados operacionais, documentos de conhecimento, artefatos de execução, uploads e backups.
- File Browser pode oferecer acesso pessoal a arquivos; não deve ser o sistema de memória do ABS.
- Usar armazenamento compatível com objetos (por exemplo, MinIO ou serviço externo) somente quando os artefatos e volumes exigirem; no início, volumes persistentes com backup externo verificado podem bastar.
- Hash, metadados, proveniência, retenção e permissões por artefato.
- Backup fora da mesma VPS; restaurar periodicamente em ambiente isolado e provar recuperação.

### O. Interface e acesso remoto pessoal
- Manter interface web do ABS como centro de operação e o celular como dispositivo de controle.
- Disponibilizar navegador visual remoto (Chromium com desktop remoto/noVNC ou Kasm após estudo de recursos) para uso pessoal, incluindo ChatGPT web, com perfil persistente.
- O perfil pessoal não é compartilhado com automação do ABS.
- A sessão persistente não garante sessão de login infinita nem execução contínua de ChatGPT; o trabalho autônomo é gerido pelo runtime do ABS, não por uma aba aberta.
- Code Server, navegador remoto e Coolify devem ser acessados por autenticação forte e rede privada/HTTPS; nunca expor portas administrativas diretamente sem proteção.

### P. Nós, dispositivos e execução distribuída
VPS é o nó persistente inicial, não a arquitetura final.
- Node registry: identidade, capacidades, recursos, saúde, versão, permissões e heartbeat.
- Jobs enviados a um nó só se o nó declarar a capacidade e cumprir a política.
- Canal autenticado, TLS, autorização por tarefa, expiração e revogação.
- Termux/celular pode ser um nó complementar quando online; não pode ser dependência obrigatória de tarefas que devam continuar após desligamento do celular.
- Planejar segundo nó/serviço externo para tarefas críticas antes de prometer alta disponibilidade.
- Dois runners no mesmo VPS não são redundância física: falha do host afeta ambos.

### Q. Segurança, privacidade e supply chain
- Modelo de ameaça documentado: prompt injection, SSRF, fuga de credenciais, tool abuse, execução de código, comprometimento de runner, dependência maliciosa e perda/corrupção de dados.
- Princípio do menor privilégio, segmentação de rede, secrets manager/variáveis protegidas, rotação, logs sem segredos, dependências fixadas e atualizações verificadas.
- SBOM/scan de dependências e imagens quando viável; imagens fixadas por versão/digest em produção.
- Separar plano de controle do plano de execução.
- Kill switch para interromper novas execuções; pausa segura para trabalhos ativos.
- Backups criptografados e teste de restauração.
- Nunca tratar texto de página, modelo ou tool como autorização.

### R. Atualização, deploy e rollback
A infraestrutura atual de atualização automática deve evoluir com gates:
1. gerar artefato/candidato em branch isolada;
2. executar testes e verificações de segurança;
3. validar contratos e migrações;
4. aprovar alterações de risco;
5. implantar canário ou serviço isolado;
6. health + smoke test + prova funcional;
7. confirmar ou rollback;
8. registrar commit, versão, evidências e responsável.

A atualização automática não deve executar migrações irreversíveis nem aplicar mudança de arquitetura sem política explícita. Manter a última versão comprovada recuperável.

## 5. Seleção do mercado — recomendação por papel

| Papel | Candidato inicial | Decisão |
|---|---|---|
| Runtime e orquestração | ABS V3 + Cérebro existente | Preservar e fechar integração; não substituir por framework |
| Gateway multi-provedor | Adaptadores atuais; avaliar LiteLLM | Só adotar após gap analysis e teste de compatibilidade |
| Workflows visuais/integradores | n8n | Serviço opcional, isolado, para integrações convencionais |
| Execução durável | mecanismo próprio primeiro; avaliar Temporal | Adotar se fila/checkpoint/recovery não forem suficientes |
| Banco operacional | SQLite existente; PostgreSQL planejado | PostgreSQL como destino multi-serviço quando necessário; migração com teste |
| Busca semântica | pgvector | Extensão do PostgreSQL após avaliação; não banco separado por padrão |
| Busca web | APIs/HTTP; SearXNG como opção | Selecionar por cobertura, confiabilidade e política de fontes |
| Browser automation | Playwright + Chromium | Capacidade de execução; serviço separado do navegador pessoal |
| Agente web | Browser Use; comparar Stagehand | Experimento controlado após browser base; não autoridade |
| Navegador pessoal remoto | Chromium visual/noVNC; avaliar Kasm | Escolher após teste de consumo; Kasm completo pode ser pesado no VPS atual |
| Tool interoperability | MCP atrás do gateway ABS | Adoção controlada, com permissões e validação de cada servidor |
| IA observability | OpenTelemetry + Langfuse opcional | Começar com tracing essencial; avaliar custo/recursos |
| Infra observability | Uptime Kuma existente/planejado; Prometheus/Grafana depois | Adicionar conforme necessidade de métricas |
| Files | volumes persistentes + backup; File Browser | Acesso pessoal não substitui storage/memória |
| Dev/build | GitHub Actions self-hosted + Code Server | Manter; isolar checkout/jobs e limitar concorrência |
| Code sandbox | contêiner restrito; microVM como evolução | Não executar código de agente no host |
| Remote access | Tailscale ou alternativa WireGuard | Rede privada para administração e serviços internos |
| Backup | backup externo independente + restauração testada | Obrigatório antes de aumentar a complexidade |
| Interface chat | interface ABS + Open WebUI opcional | UI substituível; ABS continua sendo autoridade |

As ferramentas são candidatas de mercado e não decisões de instalação indiscriminada. A escolha final deve ser sustentada por compatibilidade, manutenção, segurança, custo total, consumo real e cobertura de requisitos.

## 6. Topologia de implantação

### Nó VPS atual — perfil conservador
Com 3 vCPU, cerca de 5,7 GiB de RAM e 60 GB SSD, não manter todos os produtos candidatos residentes.
- Permanentes: ABS, runners com limites, Ollama com limites, dados mínimos, health/monitoramento essencial, proxy/acesso privado e backup.
- Sob demanda: navegador automatizado, navegador visual, agentes de código e tarefas de teste.
- Não rodar modelos locais em lote; manter o Qwen 0.8B como fallback e validar outros sequencialmente.
- Não instalar Kasm completo, stack completo de observabilidade, Temporal, Redis, Langfuse e múltiplas plataformas de agente simultaneamente sem medição e justificativa.
- Definir alertas de capacidade e política de admissão por recursos; a segurança não deve depender só de um limite de memória por processo.

### Expansão futura
Quando carga ou isolamento exigirem, separar em nós:
1. control plane (API, autorização, estado, scheduler);
2. data plane (executores efêmeros, browser, código, jobs);
3. data/backup plane (banco, artefatos, backup);
4. AI plane (local AI e gateways/provedores).
A separação é lógica primeiro; física quando a capacidade, segurança ou disponibilidade justificarem.

## 7. Sequência de execução do plano único V4

A sequência minimiza retrabalho; não cria versões novas.

### Etapa 0 — baseline e proteção
- Registrar SHA de main, estado de deploy, testes, endpoints, recursos e serviços.
- Auditar V3, contratos, capacidades registradas, closure registry, runners e PRs abertos.
- Confirmar backups e rollback antes de mudanças.
- Não modificar produção enquanto baseline não estiver documentado.
**Saída:** baseline reproduzível e lista de lacunas confirmadas.

### Etapa 1 — fechamento do ciclo vertical
- Provar Cérebro → missão → Work persistido → capability → resultado → verificação → retorno ao Cérebro → memória/estado.
- Repetir com echo, HTTP e GitHub/Codex.
- Testar falha, timeout, repetição, cancelamento, autorização e resultado incerto.
**Saída:** ciclo vertical demonstrado ponta a ponta com evidências persistidas.

### Etapa 2 — estado durável e recuperação
- Formalizar máquina de estados e invariantes.
- Tornar fila durável ou provar mecanismo equivalente.
- Adicionar idempotência, leases, reconciliação e checkpoint.
- Simular reinício durante execução, resultado externo incerto e falha de banco.
**Saída:** trabalhos não desaparecem silenciosamente e não duplicam efeitos perigosos.

### Etapa 3 — contratos, catálogo e política
- Versionar contratos de capabilities, modelos, tools, executores e nós.
- Consolidar autorização, budgets, scopes, approvals, provenance e errors.
- Integrar registries de capacidade, decisão, trajetória e fechamento.
**Saída:** capacidade descoberta/registrada não pode ser executada sem validação e política.

### Etapa 4 — roteamento multi-IA completo
- Testar cada provider/modelo sequencialmente, com limites de memória/tokens.
- Registrar capacidade real por tarefa (tool calling, visão, contexto, código, latência/custo).
- Provar fallback, indisponibilidade, rate limit e custo.
- Comparar gateway atual com LiteLLM em branch isolada.
- Só declarar um modelo integrado após teste ponta a ponta com proveniência e verificação.
**Saída:** catálogo honesto de IAs e roteamento substituível; sem lote que ameace a VPS.

### Etapa 5 — memória, conhecimento e aprendizado
- Fechar proveniência semântica: decisão → evidência → implementação → execução → resultado → sucessor.
- Unificar busca e recuperação sem apagar diferenças entre estado, memória, histórico e decisão.
- Fechar experiência → hipótese de melhoria → teste offline → aprovação → promoção/rollback.
**Saída:** aprendizado rastreável e reversível, não simples contagem de sucessos.

### Etapa 6 — execução web e ferramentas
- HTTP/pesquisa primeiro; Playwright para páginas dinâmicas; Browser Use/Stagehand somente quando necessário.
- Navegador pessoal visual isolado da automação.
- Integrar MCP e APIs atrás do gateway de política.
- Testar prompt injection, SSRF, autenticação, downloads e permissões.
**Saída:** tarefas web com logs/evidências e isolamento comprovado.

### Etapa 7 — construção autônoma e sandbox
- Jobs de código isolados; runners não compartilham worktree concorrente.
- Branch → patch → testes → CI → revisão → deploy autorizado → health → rollback.
- Provar que código malicioso/bugado não acessa segredos, Docker socket nem arquivos do host.
**Saída:** o ABS pode ajudar a evoluir o ABS com barreiras e recuperação.

### Etapa 8 — observabilidade, backup e segurança operacional
- Dashboard consolidado e alertas.
- Métricas de execução, modelos, custos, capacidade e falhas.
- Backups externos, restauração testada e runbook de desastre.
- Revisão de dependências, segredos, portas e redes.
**Saída:** é possível saber o que ocorreu, diagnosticar e recuperar sem depender de adivinhação.

### Etapa 9 — interface única e acesso pessoal
- Conectar estado real do ABS à interface, evitando controles apenas visuais.
- Oferecer navegador pessoal remoto e Code Server com acesso privado.
- Aprovações, notificações, histórico e retomada funcionam no celular.
**Saída:** operação prática sem exigir Termux para tarefas rotineiras.

### Etapa 10 — expansão distribuída
- Definir protocolo de nó, identidade, heartbeat, capabilities, policy, job lease e revogação.
- Testar segundo executor fora do VPS antes de alegar redundância.
- Roteamento por capacidade e recursos, com fallback entre nós.
**Saída:** o ABS pode usar outros ambientes sem depender de um host único, conforme recursos disponíveis.

## 8. Portões de aceitação V4

A V4 só pode ser chamada de operacionalmente fechada quando todos os portões aplicáveis tiverem evidência verificável.

### G1 — Controle
- Nenhum modelo pode se conceder permissão.
- Capacidades desconhecidas são negadas.
- Aprovação é persistida e vinculada a uma ação concreta.
- Revogação e kill switch funcionam.

### G2 — Ciclo vertical
- Missão identificada e persistida.
- Plano, Work, capability, tentativas e resultado rastreáveis.
- Resultado retorna ao Cérebro e à interface.
- Critérios de sucesso verificados com evidência.

### G3 — Durabilidade
- Reinício não perde trabalho persistido.
- Repetição não duplica efeitos não idempotentes.
- Timeout e resultado incerto são reconciliados.
- Pausa, cancelamento e retomada têm semântica definida.

### G4 — Multi-IA
- Cada motor integrado tem teste ponta a ponta individual.
- Fallback, limites e custo foram testados.
- O roteador explica a seleção por política/capacidade/estado observado.
- Nenhum modelo é declarado operacional só porque aparece no catálogo.

### G5 — Memória e aprendizado
- Proveniência consultável nos dois sentidos.
- Experiência não vira política automaticamente.
- Aprendizado é avaliado, versionado e reversível.
- Decisões e fontes não são sobrescritas silenciosamente.

### G6 — Ferramentas e segurança
- Ferramentas têm scopes mínimos e schemas validados.
- Browser e código são isolados do control plane.
- SSRF, prompt injection e fuga de segredo têm testes.
- Ações sensíveis exigem aprovação conforme política.

### G7 — Operação e recuperação
- Health, logs, métricas, custos e alertas consultáveis.
- Backup fora do host e restauração demonstrada.
- Atualização tem gate, canário/health e rollback.
- Runbook de indisponibilidade testado.

### G8 — Interface
- Estado apresentado vem do runtime real.
- Aprovações e cancelamentos têm efeito real e auditável.
- Uso pelo celular cobre os fluxos operacionais principais.
- A interface pode ser substituída sem mudar o núcleo.

### G9 — Evolução
- Novo provider/capability pode ser adicionado via contrato/adaptador.
- Testes de contrato detectam incompatibilidade.
- Exportação e restauração de dados funcionam.
- Falha de um provedor ou executor não derruba o control plane inteiro quando houver rota alternativa disponível.

**Cada portão requer:** implementação identificável + contrato + integração + teste/evidência operacional + estado de falha + autorização/proveniência quando aplicável. Documentação ou teste unitário isolado não fecha um portão end-to-end.

## 9. Como evitar novas versões e retrabalho

- Um plano V4 e uma arquitetura-alvo; etapas de implementação não são versões.
- Não abrir “V4 mínima”, “V4.1” ou “V5” para preencher lacunas que já pertencem a este escopo.
- Cada lacuna entra no registro de fechamento e é associada a componente, dependências, teste, evidência e critério de aceite.
- Antes de construir: procurar código existente, histórico, testes e integrações.
- Antes de instalar: medir consumo, dependências, superfície de ataque e duplicação funcional.
- Antes de substituir: executar comparação lado a lado, preservar contrato e provar rollback.
- Cada mudança tem um único objetivo verificável e atualiza o inventário de capacidades.
- Manter compatibilidade com V3 até o novo caminho passar pelos testes; remover legado somente depois de provar que não há consumidores.
- Não afirmar “completo” por quantidade de módulos, modelos instalados ou testes unitários.

## 10. Decisões propostas e questões que exigem evidência

1. **Manter ABS V3 como base de migração**, sem reescrita geral.
2. **Manter autoridade/política/orquestração no ABS**, não transferi-las a n8n, Dify, LangGraph, LiteLLM, OpenClaw ou qualquer agente.
3. **Postergar a seleção definitiva de gateway de IA** até comparar o roteador atual com LiteLLM.
4. **Preferir Playwright para browser automation**, mantendo browser visual pessoal separado; avaliar Browser Use/Stagehand como agentes opcionais.
5. **Não instalar stack completo de observabilidade ou workflow durável na VPS pequena sem medição.**
6. **Priorizar fechar o ciclo Cérebro ↔ ABS Core e a durabilidade da execução**, antes de multiplicar integrações.
7. **Manter Qwen 0.8B como fallback local validado**; Qwen 2B foi validado em teste sequencial, mas não deve substituir automaticamente o fallback padrão. Outros modelos permanecem não validados até teste individual.
8. **Tratar os dois runners no mesmo VPS como redundância de processo, não redundância física.**
9. **Manter navegador, modelos, providers e nós substituíveis**, com configuração declarativa e contrato estável.
10. **Não executar mudanças de produção como consequência deste documento.** A implementação exige plano de migração por lacuna, proteção do estado atual e validação.

## 11. Fontes técnicas iniciais para avaliação

As fontes abaixo são referências primárias de projeto; não equivalem a recomendação de instalar tudo:
- ABS V3 e runtime: `abs_core/v3.py`, `abs_core/runtime.py`, `abs_core/operational_intelligence.py`, `abs_core/verification.py`.
- Baseline VPS/IA local: `continuidade/08_HANDOFF_ESTABILIZACAO_VPS_IA_LOCAL_2026-10-09.md`.
- Inventário e critérios de fechamento: `continuidade/07_conhecimento/capability_registry.json`, `closure_registry.json`, `docs/02_arquitetura/INVENTARIO_CAPACIDADES_ABS_V1.md`.
- Gateway de modelos: https://docs.litellm.ai/
- Execução durável: https://docs.temporal.io/
- Automação web: https://playwright.dev/docs/intro
- Interoperabilidade: https://modelcontextprotocol.io/specification/
- Observabilidade de IA: https://langfuse.com/docs/observability/overview
- Instrumentação: https://opentelemetry.io/docs/
- Busca web: https://docs.searxng.org/

## 12. Próxima ação operacional

1. Revisar este plano e registrar decisões autorizadas.
2. Auditar o baseline real de `main`, o estado da VPS e os testes sem alterar produção.
3. Gerar uma matriz **lacuna → código existente → contrato → dependências → teste → evidência → critério de aceite** a partir do closure registry.
4. Executar o primeiro vertical slice de fechamento, preservando o runtime V3.
5. Atualizar os registros de capacidades e conhecimento com resultados reais.
6. Prosseguir pelas etapas na ordem de dependência, sem criar uma nova arquitetura intermediária.

**Definição de sucesso:** o ABS em construção opera o ecossistema de capacidades com autoridade preservada, execução durável, roteamento substituível, memória/proveniência, verificação, segurança, observabilidade, recuperação e uma interface utilizável pelo Imperador — e pode ampliar essas capacidades sem reescrever o núcleo.
