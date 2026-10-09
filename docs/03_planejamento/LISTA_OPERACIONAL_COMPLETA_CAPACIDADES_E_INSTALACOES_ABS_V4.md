# Lista operacional completa de capacidades, integrações e instalações — ABS V4

**Estado:** plano operacional consolidado; ainda não é prova de implementação nem autorização para alterar produção.  
**Branch de trabalho:** `planning/abs-v4-completa`  
**Referências canônicas:** `continuidade/07_conhecimento/capability_registry.json`, `continuidade/07_conhecimento/closure_registry.json` e a Matriz de Reconciliação ABS V4.  
**Regra central:** preservar a autoridade do Imperador, a V3 funcional e os 72 IDs canônicos. Toda mudança de código deve ocorrer em branch/PR, com testes e evidências. Instalações na VPS/Termux só serão feitas quando a inspeção confirmar necessidade, compatibilidade, recursos e caminho de reversão.

## 1. Resultado final pretendido

O ABS deve receber uma missão em linguagem natural, entender objetivo e restrições, escolher o modo mínimo suficiente (execução direta, workflow, agente ou multiagente), planejar, obter autorização para ações sensíveis, executar por capacidades explicitamente identificadas, persistir estado e resultados, verificar o efeito real, aprender com o resultado sem ampliar privilégios e retomar o trabalho após falhas. O Imperador deve conseguir acompanhar, interromper, aprovar, negar e retomar pelo celular/interface.

Não basta existir uma classe, arquivo, credencial, endpoint ou modelo registrado. Uma capacidade só será considerada fechada quando houver contrato, integração real, autorização, evidência verificável e tratamento de falha/recuperação quando aplicável.

## 2. Ordem de trabalho obrigatória

### Fase 0 — Preservação e diagnóstico
- [ ] Confirmar branch/base e estado do repositório; manter alterações isoladas e revisar PRs abertos antes de mudanças sobrepostas.
- [ ] Reexecutar CI na revisão final de cada mudança; não extrapolar resultados de um commit para commits posteriores.
- [ ] Mapear o ciclo atual entre Cérebro, plano, Work, roteador/orquestrador, adaptadores, store, verificação e resposta final.
- [ ] Conferir os runners principal e reserva por caminho de execução real; distinguir processo vivo, acesso à VPS, execução de comando e resultado comprovado.
- [ ] Fazer snapshot lógico/backup antes de alterações de infraestrutura; nunca considerar volume do serviço como backup independente.
- [ ] Não alterar produção, mesclar PR nem reiniciar serviços críticos sem evidência, plano de rollback e autorização necessária.

### Fase 1 — Fechar o ciclo vertical da inteligência
- [ ] Missão recebida e normalizada, com objetivo, restrições, contexto e critério de sucesso.
- [ ] Plano composto por etapas com IDs de capacidade explícitos e validados; rejeitar etapa sem capacidade autorizada (correção proposta no PR #128).
- [ ] Autoridade e permissões verificadas antes de cada efeito externo ou privilegiado.
- [ ] Work persistido antes/durante/depois da execução, com estados distinguíveis: pendente, em execução, concluído, falhou, bloqueado, cancelado e sucesso parcial.
- [ ] Roteamento para executor/adaptador correto, com entrada/saída validadas, timeout, limites e proveniência.
- [ ] Resultado bruto e resultado normalizado persistidos com missão, etapa, tentativa, executor, modelo/ferramenta, versão e timestamps.
- [ ] Verificação independente do resultado e das pós-condições; não aceitar apenas a declaração do executor.
- [ ] Resposta ao Imperador com resultado, evidências, limitações, custos e pendências.
- [ ] Replanejamento a partir de falha, sucesso parcial, conflito ou informação nova; evitar repetição infinita.
- [ ] Teste ponta a ponta de uma missão simples, uma missão com falha, uma retomada e uma ação bloqueada por falta de autorização.

### Fase 2 — Fechar as capacidades canônicas em aberto
Auditar uma a uma as capacidades parciais e planejadas no registro canônico, mantendo IDs e estados históricos. O foco inicial é:
- [ ] Cérebro: integração real entre contexto, planejamento, Work, execução, verificação e resposta.
- [ ] Memória temporal: persistência temporal, recuperação e retomada após reinício.
- [ ] Pesquisa contínua: ciclo agendado/por evento, fontes e resultados registrados; não confundir pesquisa manual com monitoramento contínuo.
- [ ] Experiência: registrar tarefa, contexto, estratégia, resultado, falha e evidência reutilizável.
- [ ] Aprendizado: demonstrar melhoria verificável a partir de experiência, com revisão e rollback; sem alterar permissões automaticamente.
- [ ] Sabedoria operacional: derivar regras verificáveis e rastreáveis de experiências, separando fatos de hipóteses.
- [ ] Validação: comprovar o resultado end-to-end, não apenas estrutura ou teste unitário.
- [ ] Observabilidade: estado consolidado de missões, Work, runners, modelos, ferramentas, filas, erros e recursos.
- [ ] Auditoria: trilha de ordem, autorização, executor, entradas/saídas, efeitos e evidências.
- [ ] Evolução arquitetural: mudança versionada, testada, revisável e reversível.
- [ ] Registro de agentes, Multi-IA, supervisão, meta-supervisão e auditoria independente: contrato, política, integração, estado e testes ponta a ponta.
- [ ] Idempotência, filas, monitoramento e execução contínua: comportamento real em repetição, concorrência, falha e reinício.
- [ ] Integrações externas e padrões interoperáveis: provar contrato e efeito real por integração.
- [ ] Detecção de conflitos e red team: conflitos identificados, decisão registrada, ataques simulados, achados corrigidos e retestados.
- [ ] Novas capacidades/recursos/sistemas derivados/escala: fluxo governado de descoberta, avaliação, autorização, implementação e prova.
- [ ] Capacidades planejadas 47, 49, 71 e 72: detecção de oportunidades, operação 24/7, capacidades desconhecidas e oportunidades encontradas durante a construção; manter abertas até evidência suficiente.

A lista detalhada e o critério de cada ID permanecem na Matriz de Reconciliação. As contagens do registro (35 operacional, 27 parcial, 6 governança, 4 planejada) são o estado catalogado, não uma certificação independente atual.

### Fase 3 — Segurança e controle do Imperador
- [ ] Política de autorização por ação, recurso, contexto, risco, duração e custo.
- [ ] Fail-closed: capacidade desconhecida, não autorizada ou sem contrato não executa por fallback implícito.
- [ ] Aprovação explícita para operações irreversíveis, financeiras, públicas, destrutivas, privilegiadas ou com custo material.
- [ ] Pausar, cancelar, revogar, limitar e retomar missão; cancelar não pode ser confundido com sucesso.
- [ ] Segredos fora de código, logs, artefatos e prompts; rotação/revogação e escopo mínimo.
- [ ] Separação entre instruções do Imperador e conteúdo não confiável vindo da web, documentos, páginas, repositórios ou modelos.
- [ ] Defesas e testes para prompt injection, exfiltração, SSRF, command injection, path traversal, abuso de ferramenta, escalada de privilégio e supply chain.
- [ ] Autenticação forte para painel e serviços; serviços administrativos não expostos à Internet sem necessidade.
- [ ] Registro de decisões e proveniência sem armazenar segredos desnecessários.
- [ ] Testes de permissões negativas, revogação, limites de custo, concorrência e isolamento.

### Fase 4 — Memória, conhecimento e continuidade
- [ ] Separar memória de sessão, missão, longo prazo e operação; cada tipo com política de escrita/retensão.
- [ ] Vincular fatos, decisões, hipóteses, fontes, experiências e resultados a proveniência e validade temporal.
- [ ] Corrigir/superseder informação sem apagar indevidamente o histórico; resolver conflitos explicitamente.
- [ ] Recuperar contexto por projeto, missão, entidade, tempo e relevância.
- [ ] Exportar/importar memória e retomar missão após troca de modelo, interface, agente, runner ou nó.
- [ ] Persistir eventos/estado de forma suficiente para reconstruir a trajetória da missão.
- [ ] Testar restauração real de backup e retomada após reinício, não apenas existência de arquivos.

### Fase 5 — Execução durável e observabilidade
- [ ] Fila persistente ou mecanismo equivalente, se o mecanismo existente não provar durabilidade/retomada.
- [ ] Idempotência/deduplicação, retry por classe de erro, backoff, timeout, circuit breaker e limites de concorrência.
- [ ] Agendador por horário/intervalo/evento, com chave idempotente e proteção contra loops/disparos duplicados.
- [ ] Logs estruturados, métricas, traces e correlação por missão/Work/tentativa.
- [ ] Health, readiness e teste funcional; alertas de indisponibilidade, backlog, erro, RAM, disco, custo e latência.
- [ ] Painel de status legível pelo celular: missão atual, etapa, executor, bloqueio, custo/uso quando disponível, evidência e próximo passo.
- [ ] Política de degradação: quando uma IA/ferramenta cai, usar alternativa autorizada ou informar bloqueio; nunca simular sucesso.
- [ ] Definir RPO/RTO realistas, cópia fora do VPS e ensaio de restauração.
- [ ] Distinguir redundância de processo (dois runners no mesmo VPS) de redundância física/regional.

### Fase 6 — Internet, navegador, arquivos e engenharia
- [ ] Pesquisa web direcionada e aprofundada, extração de páginas/documentos/tabelas, comparação de fontes e citações por afirmação.
- [ ] Navegação automatizada isolada, com sessão separada do navegador pessoal, captura de evidências e confirmação pós-ação.
- [ ] Interromper e pedir intervenção diante de CAPTCHA/MFA, pagamento, compra, publicação ou confirmação sensível.
- [ ] Descobrir APIs antes de recorrer à GUI; manter conectores substituíveis.
- [ ] Leitura, busca, criação, edição, versionamento e comparação de arquivos com prevenção contra sobrescrita destrutiva.
- [ ] Processamento de PDF, DOCX, XLSX, CSV, apresentações, imagens, áudio e vídeo conforme os motores realmente disponíveis.
- [ ] Workspace de código isolado, limites de CPU/RAM/tempo/rede/arquivos, dependências controladas e sem credenciais de produção.
- [ ] Fluxo de software: branch → alteração → testes → revisão independente → PR → CI → aprovação → deploy controlado → health check → rollback.
- [ ] Artefatos com nome, versão, formato e verificação de integridade.

### Fase 7 — Integração das seis IAs locais
O inventário atual registra seis candidatos no Ollama. A meta é integrá-los ao roteador do ABS por adaptador padronizado e provar cada um individualmente. **Não baixar/abrir todos ao mesmo tempo.** Os modelos não são seis processos que devem ficar simultaneamente carregados.

| Modelo registrado | Papel inicial a avaliar | Situação conhecida | Próxima ação |
|---|---|---|---|
| Qwen 3.5 0.8B | fallback leve/rápido e modo degradado | registrado; inventário anterior reporta teste anterior, confirmar no estado atual | smoke test via ABS, descarga e registro de RAM |
| Qwen 3.5 2B | modelo local geral preferencial, se qualidade/recursos confirmarem | teste anterior via ABS reportado como PASS | repetir teste reproduzível e medir qualidade/recursos |
| Qwen 3.5 4B | qualidade local superior, condicionado a RAM/latência | registrado, não validado ponta a ponta no checkpoint conhecido | testar isoladamente; abortar com pressão de memória |
| Ministral 3 3B | alternativa independente para comparação/fallback | registrado, não validado ponta a ponta | testar isoladamente |
| Gemma 4 E2B | alternativa para avaliação, recursos exigentes | registrado, não validado ponta a ponta | testar isoladamente somente se estimativa/medição permitir |
| Gemma 4 E4B | candidato experimental de maior exigência | registrado, não validado; estimativa prévia ~7 GB torna-o incompatível com 5,7 GiB de RAM VPS sem outras condições | não priorizar instalação/execução; primeiro confirmar hardware e formato de quantização; não comprometer serviços essenciais |

Para cada modelo:
- [ ] Confirmar nome/tag, artefato, quantização, licença, origem e espaço em disco.
- [ ] Medir RAM livre, swap, tempo de carga, tokens/s, latência, pico de memória e descarga.
- [ ] Executar testes padronizados via ABS (não apenas diretamente no Ollama): resposta, timeout, erro, concorrência, contexto, limite de tokens e retorno do formato.
- [ ] Confirmar proveniência: modelo solicitado = modelo executado, endpoint real, status de verificação e Work concluído.
- [ ] Testar falha/indisponibilidade e fallback controlado; provar que o modelo alternativo não muda a autorização da tarefa.
- [ ] Descarregar modelo após o teste e verificar recuperação de memória.
- [ ] Comparar qualidade em tarefas representativas e escolher rota por evidência, não apenas tamanho.
- [ ] Manter modelos incompatíveis como registrados/não disponíveis, sem prometer execução.
- [ ] Não executar bateria paralela dos seis no VPS de 6 GB; testar um por vez.
- [ ] Definir política local/nuvem/offline; uso de API externa requer credencial, custo, política de dados e integração testada.

### Fase 8 — Serviços e infraestrutura a instalar ou configurar

A instalação depende da auditoria do estado real da VPS/Coolify. A tabela é o alvo planejado, não afirma que todos estejam instalados nem manda instalar duplicatas.

| Componente/serviço | Ação prevista | Prioridade e condição |
|---|---|---|
| ABS Core/API + runners principal/reserva | verificar, reparar e validar ciclo real | P0 — essencial; preservar o que funciona |
| Ollama + adaptador local ABS | verificar serviço, modelos e roteamento | P0 — essencial à bateria das IAs |
| PostgreSQL | instalar/configurar se não houver armazenamento durável adequado para serviços/estado que o exijam | P1 — avaliar schema, backup e migração antes |
| Backup independente | configurar cópia externa ao volume/VPS e restauração testada | P0 — antes de mudanças arriscadas |
| Uptime Kuma ou monitor equivalente | instalar se não houver monitoramento equivalente validado | P1 — health checks e alertas |
| Code Server via Coolify | corrigir template/permissões e validar acesso pelo navegador do celular | P1 — há erro conhecido criando `/var/www/html/storage/app/ssh/keys`; não declarar resolvido sem deploy e login de teste |
| File Browser | instalar se a interface atual não permite gerir arquivos necessários com segurança | P2 — acesso autenticado, escopo limitado |
| Tailscale | configurar para acesso administrativo privado, se compatível com o modelo de rede escolhido | P1/P2 — não substituir regras de firewall sem teste |
| GitHub ↔ Coolify | conectar deploys por chave/token de escopo mínimo e validar rollback | P1 — depois de CI e backup |
| n8n | instalar apenas se for necessário para integrações/agenda visual que o ABS ainda não fornece | P2 — não deve virar cérebro nem autoridade |
| Redis | instalar somente se uma fila/cache existente e medida justificar | Condicional — não instalar por padrão |
| LiteLLM | avaliar como gateway de provedores se a integração multi-API justificar; ABS mantém a política de roteamento/autoridade | P2 — só depois da matriz de modelos e segredos |
| Langfuse | avaliar para tracing/eval de LLM se logs/observabilidade atuais forem insuficientes | P2 — controlar retenção e dados sensíveis |
| Navegador automatizado isolado | instalar/configurar runtime apropriado após confirmar ausência de equivalente | P1/P2 — sandbox e políticas antes de usar credenciais |
| Sandbox de código | implementar/configurar ambiente descartável com limites de recursos e rede | P1 — antes de execução autônoma de código não confiável |
| Sistema de fila durável | adotar componente externo somente se armazenamento/eventos existentes não satisfizerem testes de retomada | P1/P2 — escolha após benchmark e teste de recuperação |
| APK/controle Android avançado | planejar como etapa posterior; usar APIs/permissões explícitas | Futuro — não bloquear fechamento do ciclo atual |
| Novas máquinas/nós físicos | não adquirir automaticamente | Futuro — exige necessidade demonstrada, orçamento e autorização |

**Restrições da VPS conhecida:** KVM com cerca de 5,7 GiB de RAM e 2 GiB de swap. Priorizar um modelo local por vez, preservar memória para ABS/Coolify/banco/serviços e não tratar swap como RAM equivalente. O Code Server tinha um erro de permissão/template pendente no último handoff; primeiro diagnosticar, sem abrir permissões globais nem executar comandos destrutivos.

### Fase 9 — Integrações externas e ferramentas
- [ ] GitHub: ler repositórios/PRs/CI, editar em branches, criar PRs, consultar status e registrar commits/evidências.
- [ ] APIs externas: adaptadores com contrato, autenticação, limites, timeouts, retries e proveniência.
- [ ] Ferramentas de terminal: execução isolada, comandos permitidos, limite de tempo/saída e captura de status/artefatos.
- [ ] Conectores/MCP quando úteis: validar ferramenta e permissões; descoberta não significa confiança.
- [ ] Provedores de IA em nuvem: cadastrar somente os que forem realmente escolhidos e autorizados, sem inventar disponibilidade de conta/credencial.
- [ ] Android/dispositivo: separar capacidade do ABS de permissão concedida pelo sistema operacional; revogação e limites explícitos.
- [ ] Cada integração precisa de teste de contrato, teste de falha e teste de revogação.

### Fase 10 — Avaliação, aprendizado e red team
- [ ] Montar conjunto versionado de missões representativas do Projeto Absoluto.
- [ ] Medir sucesso real, qualidade, custo, latência, uso de recursos, falhas e intervenção humana.
- [ ] Comparar modelos/adaptadores nas mesmas tarefas e parâmetros.
- [ ] Executar testes adversariais de prompt injection, ferramenta maliciosa, fonte contraditória, segredo no log, capacidade não autorizada, repetição, corrida e queda no meio da missão.
- [ ] Verificar que o verificador pode rejeitar o resultado do executor.
- [ ] Transformar falhas em regressões automatizadas; registrar causa, correção e reteste.
- [ ] Aprendizado não altera política, permissões ou código de produção sem revisão/autoridade.

## 3. Capacidades adicionais a auditar (não presumir ausentes)

Além das 72 canônicas, verificar separadamente se existem contratos/evidências suficientes para:
1. automação de navegador/GUI;
2. sandbox de execução de código;
3. processamento de artefatos multimodais;
4. backup externo e restauração;
5. filas realmente duráveis;
6. observabilidade por missão;
7. avaliação comparativa de modelos;
8. gestão/rotação de segredos;
9. agendador persistente;
10. aprendizado reversível;
11. recuperação de desastre;
12. pesquisa com evidências ligadas a afirmações;
13. orçamento e limites por missão;
14. portabilidade de memória;
15. defesa contra prompt injection;
16. isolamento de navegador e sessões.

Cada item deverá ser classificado como: já coberto com evidência; parcial; duplicado por outro componente; ausente e necessário; condicional; ou não aplicável no momento.

## 4. Critérios de conclusão do trabalho

O ABS V4 não será declarado fechado até que:
- [ ] Uma missão percorra o ciclo completo com estado persistido e proveniência.
- [ ] Um passo sem capacidade explícita ou sem autorização seja bloqueado antes de produzir efeitos.
- [ ] Resultado incorreto/incompleto seja rejeitado pelo verificador.
- [ ] Uma falha simulada permita recuperação/replanejamento sem duplicar efeitos.
- [ ] Estado sobreviva a reinício conforme o contrato de persistência.
- [ ] Runner principal e reserva tenham papéis, limites e testes demonstrados; falha de um seja detectada e o fallback seja comprovado.
- [ ] Os seis modelos tenham status individual honesto: aprovado, reprovado, bloqueado por recursos ou não disponível; nenhum marcado como funcional apenas por registro.
- [ ] A integração Multi-IA tenha roteamento, proveniência, fallback, custo/recursos e testes de falha.
- [ ] Segurança, auditoria, observabilidade, backup e restauração tenham testes/evidências compatíveis com seu risco.
- [ ] CI esteja verde no commit final; testes específicos e, quando possível, execução real estejam ligados à mudança.
- [ ] Documentação, registros canônicos e handoff sejam atualizados sem apagar o histórico.
- [ ] Nenhuma mudança de produção seja inferida a partir de PR aberto ou CI verde.

## 5. O que não será instalado por impulso

Não instalar uma ferramenta por cada capacidade; não adotar um framework como cérebro/autoridade central; não instalar Redis, n8n, LiteLLM, Langfuse, novos bancos ou novos modelos sem lacuna e benefício demonstrados; não tentar manter seis modelos carregados simultaneamente; não abrir serviços administrativos à Internet sem necessidade; não elevar permissões globalmente para contornar erro; não mesclar/deployar código apenas porque os testes passaram; não declarar hardware, API, credencial ou serviço acessível sem prova.

## 6. Relato obrigatório ao fim de cada bloco

Para cada bloco concluído, registrar:
- mudança concreta (arquivo/commit/PR ou serviço);
- teste executado e resultado;
- evidência observável;
- risco/limitação remanescente;
- estado canônico atualizado ou motivo para mantê-lo aberto;
- próximo bloco executável.

**Regra final:** seguir de forma contínua e em lotes, sem pedir confirmação para cada tarefa reversível e segura. Interromper apenas quando houver decisão humana realmente necessária, risco relevante, credencial/conta indisponível, falta de recurso ou impossibilidade técnica. Não afirmar que trabalho na VPS, instalação ou execução real aconteceu sem resultado observado.
