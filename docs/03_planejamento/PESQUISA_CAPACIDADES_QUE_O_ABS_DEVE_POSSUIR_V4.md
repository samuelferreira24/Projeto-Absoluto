# Pesquisa de capacidades que o ABS deve possuir — base para V4

**Estado:** pesquisa de arquitetura; não comprova implementação.  
**Escopo:** capacidades necessárias ao ABS como sistema de execução, inteligência, integração, memória, construção e evolução sob autoridade do Imperador.  
**Regra:** preservar o tabuleiro histórico de 72 capacidades. Esta pesquisa amplia a análise; não substitui o inventário canônico sem reconciliação.

## 1. Conclusão executiva

As 72 capacidades atuais são uma base importante, mas não provam, por si só, que todo o universo de capacidades necessárias ao ABS V4 foi pesquisado. O NIST recomenda classificar ferramentas de agentes por função, padrões de acesso, permissões, risco, confiabilidade e modalidade. Uma taxonomia útil inclui percepção, planejamento/análise/gestão de recursos e ações como uso de computador, execução de código, extensões de software, interação humana e interação entre agentes.

A proposta é um ABS único e evolutivo, com capacidades catalogadas e combináveis, em vez de uma ferramenta por capacidade ou uma nova versão por etapa. Algumas capacidades serão nativas; outras podem vir de adaptadores, modelos, serviços externos, dispositivos ou sistemas derivados. O ABS deve registrar qual mecanismo executou cada ação e como o resultado foi comprovado.

## 2. Critério de inclusão

Cada capacidade deve ter definição observável, entradas/saídas, critérios de sucesso, dependências, classe de execução, permissões, risco, reversibilidade, evidência, estado atual, estratégia de falha/recuperação e proveniência de modelo/ferramenta/serviço/nó/versão.

**Não confundir:** capacidade ≠ componente ≠ ferramenta ≠ modelo ≠ recurso ≠ objetivo ≠ evidência. Uma ferramenta pode servir a várias capacidades; uma capacidade pode ter vários provedores. A troca de provedor não deve redefinir a capacidade.

## 3. Taxonomia de capacidades-alvo

A lista é ampla e serve à reconciliação. Não significa que tudo deva ser construído imediatamente, instalado no VPS ou ativado sem autorização.

### A. Autoridade, identidade e direção
- Preservar autoridade final do Imperador, hierarquia de instruções, propósito, princípios, objetivos e preferências.
- Diferenciar ordem, sugestão, hipótese, requisito e decisão aprovada.
- Autorizar por ação, recurso, contexto, risco, duração e escopo; pedir aprovação para ações de alto impacto, irreversíveis, externas ou com custo material.
- Suspender, cancelar, limitar, revogar e encerrar execuções; registrar quem autorizou, o escopo e o resultado.
- Resolver conflitos entre instruções, políticas, estado observado e permissões.

### B. Interface e interação
- Conversa textual com continuidade; voz com interrupção; entrada multimodal de imagem, documento, áudio e vídeo quando suportada.
- Receber objetivos de alto nível e refiná-los sem exigir que o usuário desenhe workflows.
- Mostrar estado real, progresso, bloqueios, decisões pendentes, evidências e resultados.
- Aprovar, negar, editar, pausar, retomar e cancelar ações pelo celular ou navegador.
- Produzir texto, arquivos, código, relatórios, tabelas e outros artefatos; distinguir proposta, simulação, execução real e resultado comprovado.

### C. Compreensão, raciocínio e planejamento
- Interpretar objetivos, restrições, contexto e critérios de sucesso; detectar ambiguidades, pressupostos, desconhecidos e contradições.
- Perguntar somente quando a informação ausente muda materialmente a decisão ou segurança.
- Decompor objetivos em tarefas, dependências, marcos e condições de conclusão.
- Selecionar o modo mínimo suficiente: direto, workflow, agente ou multiagente.
- Comparar alternativas por evidência, custo, tempo, risco, reversibilidade e valor; gerar hipóteses, contraexemplos e simulações.
- Replanejar diante de falhas ou informações novas; detectar ciclos, duplicação e progresso ilusório; comunicar incerteza.

### D. Modelos e motores de inteligência
- Catalogar modelos locais, APIs e motores especializados; rotear por capacidade, qualidade, latência, custo, privacidade, contexto e disponibilidade.
- Alternar entre nuvem, local e modo offline conforme política e conectividade.
- Fazer fallback, retry e degradação controlada; gerir quotas, rate limits, timeouts, concorrência e orçamento.
- Avaliar modelos em tarefas reais do ABS; registrar modelo, versão, configuração, entrada e saída.
- Encadear modelos especializados quando isso acrescenta valor verificável.
- Não confundir seleção de modelo com autorização para agir; substituir fornecedor sem perder estado e memória.

### E. Agentes, equipes e delegação
- Registrar identidade operacional, missão, responsabilidade, capacidades, permissões e estado de cada agente.
- Delegar com escopo, prazo, orçamento, formato de saída e critério de aceitação.
- Coordenar paralelismo com limites de concorrência; compartilhar contexto seletivamente.
- Detectar duplicação, dependências e conflitos; consolidar resultados divergentes sem esconder dissenso não resolvido.
- Supervisionar, auditar por caminho independente, escalar supervisão e medir contribuição real.
- Pausar, encerrar ou substituir agentes sem perder estado; impedir autoatribuição ilimitada de permissões.

### F. Ferramentas, conectores e interoperabilidade
- Catálogo de ferramentas, APIs, serviços, dispositivos, conectores e recursos; descoberta de capacidades e validação de contratos.
- Adaptadores padronizados com autenticação, timeout, rate limit, tratamento de erros e observabilidade.
- Suporte a API, CLI, MCP e protocolos apropriados, sem depender de um protocolo único.
- Separar leitura, escrita e ações privilegiadas; descoberta não significa confiança nem autorização.
- Controlar escopo, segredos, expiração e revogação; testar contratos e integrações.
- Registrar origem, versão, permissões e efeitos colaterais; permitir substituição e desativação segura.

### G. Internet, pesquisa e conhecimento externo
- Pesquisa exploratória e direcionada, navegação por páginas, links e documentos, extração de texto/tabelas/metadados/arquivos.
- Pesquisa aprofundada com plano, fontes múltiplas, comparação e síntese.
- Verificar data, autoria, autoridade, atualidade e independência; rastrear afirmações até evidências específicas.
- Detectar contradições, lacunas, desatualização e conteúdo promocional; monitorar fontes autorizadas.
- Separar conteúdo externo não confiável de instruções legítimas; transformar pesquisa em conhecimento, decisão, experimento ou oportunidade registrada.

### H. Navegador e uso de computador
- Navegador automatizado isolado do navegador pessoal; navegar, clicar, preencher campos, selecionar, baixar e enviar arquivos dentro das permissões.
- Interagir com aplicações web e interfaces gráficas quando não houver API adequada.
- Manter sessões/cookies seguros e com escopo; capturar screenshot, estado da página e evidências.
- Lidar com carregamento assíncrono, modais, redirecionamentos e mudanças de layout.
- Confirmar o efeito real após a ação; interromper diante de CAPTCHA, MFA, compra ou confirmação sensível que exija intervenção.
- Detectar prompt injection, proteger tokens/cookies e manter logs auditáveis sem expor segredos.

### I. Arquivos, documentos e artefatos
- Criar, ler, pesquisar, editar, versionar, comparar, organizar e entregar arquivos autorizados.
- Processar PDF, DOCX, XLSX, CSV, apresentações, imagens, áudio e formatos técnicos.
- Indexar conteúdo com permissões e proveniência; gerir versões, metadados, relações e retenção.
- Verificar integridade, formato, tamanho e conteúdo não confiável; fazer backup e testar restauração.
- Evitar sobrescrita destrutiva; pesquisar em repositórios, armazenamento local e nuvem; tratar arquivos como dados, não como instruções com autoridade.

### J. Engenharia de software e execução de código
- Entender repositórios, arquitetura, dependências, testes, documentação, histórico, licenças e vulnerabilidades.
- Especificar mudanças e critérios de aceitação; editar código, criar branches/commits/PRs dentro do escopo autorizado.
- Executar testes unitários, integração, end-to-end, regressão, lint e análise estática; construir e validar artefatos isoladamente.
- Diagnosticar com logs/evidências; revisar de forma independente; detectar regressões.
- Implantar com aprovação, health checks e rollback testado; separar desenvolvimento, teste, staging e produção.
- Executar comandos em workspaces isolados com limites de rede, CPU, memória, tempo, arquivos e credenciais; capturar saídas e limpar recursos.
- Não promover código gerado automaticamente a produção e não afirmar execução/implantação sem evidência.

### K. Memória, conhecimento e experiência
- Memória de sessão, missão, longo prazo e operação com propósitos distintos.
- Distinguir decisões, preferências, fatos, hipóteses, fontes, experiências e resultados.
- Recuperar por relevância, tempo, entidade, projeto e relações; preservar proveniência, confiança, validade temporal e conflitos.
- Corrigir, superseder, expirar e esquecer segundo política; não tratar todo histórico como verdade atual.
- Aprender com resultados sem alterar permissões silenciosamente; evitar contaminar memória com prompt injection ou inferências apresentadas como fatos.
- Exportar/importar memória e retomar estado após falhas, troca de modelo, interface ou agente.

### L. Execução durável, filas e continuidade
- Persistir estado por missão, tarefa, etapa, tentativa e resultado.
- Retomar após queda, reinício, perda de rede e troca de worker; suportar filas, agendamento, prioridades, concorrência e backpressure.
- Usar idempotência/deduplicação, retries por classe de erro, backoff, timeout e circuit breaker.
- Pausar à espera de aprovação, credencial, evento ou recurso; cancelar e compensar ações parciais quando possível.
- Distinguir falha transitória, permanente, cancelamento, bloqueio e sucesso parcial; reconstruir estado a partir de eventos.
- Operar continuamente com limites de orçamento, carga e segurança.

### M. Verificação, avaliação e qualidade
- Definir critérios de sucesso antes da execução; verificar contratos, invariantes, pós-condições e resultado end-to-end.
- Comparar afirmações com evidências e citar fontes.
- Avaliar qualidade, sucesso, latência, custo, robustez e intervenção humana com conjuntos de testes versionados.
- Auditar por caminho independente e executar red-team de prompt injection, abuso de ferramentas, vazamento e escalada de privilégio.
- Detectar resultados incompletos e falsos positivos de sucesso; registrar falhas, causa, impacto, correção e reteste.
- Não usar nota agregada para ocultar riscos críticos.

### N. Segurança, privacidade e confiança
- Autenticação forte para Imperador, serviços, agentes e nós; autorização de menor privilégio por recurso e ação.
- Gestão de segredos, rotação, expiração, revogação e isolamento de rede/serviços/workspaces.
- Defesa contra prompt injection, exfiltração, abuso de ferramentas, SSRF, command injection, path traversal e comprometimento da cadeia de suprimentos.
- Classificação de dados, minimização, retenção, exclusão e auditoria de ações sensíveis.
- Gestão de vulnerabilidades, atualização, imagens confiáveis e resposta a incidentes.
- Fail-closed para ações privilegiadas; avaliar risco por capacidade, permissão, ambiente, reversibilidade e impacto.
- Segurança não pode depender apenas da instrução do modelo.

### O. Observabilidade, operação e infraestrutura
- Estado consultável de serviços, nós, modelos, ferramentas, filas e missões; logs estruturados, métricas, traces e correlação por missão.
- Medir latência, erro, consumo, custo, disponibilidade e backlog; alertar e escalar por severidade.
- Health checks, readiness, liveness, verificação funcional e recuperação automática limitada por política.
- Inventariar CPU, RAM, armazenamento, rede, GPU/NPU, quotas e serviços; orçar por missão e proteger contra exaustão.
- Backup independente do volume principal, restauração testada, manutenção, migração e recuperação de desastre.
- Distinguir redundância de processo, máquina, rede e provedor; dois processos no mesmo VPS não são redundância física.
- Suportar modo degradado/offline para capacidades selecionadas e escalar local/nuvem/VPS/dispositivo conforme política.

### P. Integração de plataformas e dispositivos
- Conectar GitHub, APIs, bancos, armazenamento, ferramentas de desenvolvimento e serviços autorizados.
- Integrar Android e outros dispositivos com permissões claras e revogáveis.
- Descobrir e administrar nós remotos sem confundir disponibilidade com confiança; sincronizar estado e resolver conflitos.
- Suportar padrões abertos, APIs estáveis e conectores isolados/substituíveis.
- Registrar limitações, custos, quotas e dependências; distinguir credencial configurada de integração validada.

### Q. Pesquisa de oportunidades e expansão de capacidade
- Detectar lacunas entre objetivos e capacidades; descobrir ferramentas, modelos, serviços e técnicas úteis.
- Comparar alternativas antes de adotar tecnologia; estimar benefício, custo, risco e dependências.
- Propor experimentos isolados e reversíveis; validar antes de marcar como operacional.
- Criar novas ferramentas/sistemas derivados com identidade, escopo e proveniência próprios.
- Descobrir capacidades desconhecidas, preservar caminhos rejeitados e atualizar o mapa sem inflá-lo com sinônimos.
- Nunca usar autodesenvolvimento como autorização para remover controles ou ampliar privilégios.

### R. Colaboração humana, multimodalidade e agendamento
- Pedir intervenção humana diante de política, risco ou incerteza material; vincular aprovação ao escopo exato.
- Apresentar opções e consequências, preservar progresso enquanto aguarda e permitir que o Imperador assuma o controle.
- Analisar imagens/documentos visuais; transcrever, compreender e produzir áudio; interpretar vídeo e gerar/editar mídia quando motores adequados existirem.
- Validar formato, qualidade e integridade de artefatos multimodais e declarar indisponibilidade quando aplicável.
- Executar por horário, intervalo ou evento; monitorar condições; evitar disparos duplicados/loops e registrar condição, regra e ação.

### S. Economia, valor e capacidades condicionais
- Estimar custos diretos/indiretos; comparar execução manual, modelo, ferramenta, serviço e automação.
- Priorizar conforme metas do Imperador e valor esperado; medir resultado útil após implantação.
- Não realizar compras, transações ou compromissos financeiros sem autorização apropriada.
- Manter como domínios condicionais — não requisitos imediatos — robótica/hardware físico, sensores do mundo real, telefonia ativa, operações financeiras, sistemas regulados e ambientes de alta criticidade. Exigem objetivo explícito, permissões, análise de risco, recursos e avaliação legal.

## 4. Capacidades transversais obrigatórias

Estas devem atravessar todos os domínios: autorização; proveniência; evidência; tratamento de falha; recuperação; observabilidade; interoperabilidade; privacidade; custo; reversibilidade; controle humano; atualidade; isolamento; portabilidade. Cada execução deve responder: está autorizada? quem a realizou? com quais entradas e versões? qual evidência prova o resultado? como falha e recuperação são tratadas? qual custo e impacto ocorreram?

## 5. Reconciliação com as 72 capacidades existentes

Não renumerar nem substituir o tabuleiro original automaticamente. Criar uma matriz com uma linha por capacidade proposta e estes campos:
- research_id: identificador estável;
- canonical_capability_id: ID atual das 72, se houver correspondência;
- domínio e definição da capacidade;
- relação: mesma, subcapacidade, transversal, ausente, fora de escopo ou duplicada;
- justificativa da correspondência/lacuna;
- classe de implementação: nativa, adaptador, serviço, humana, futura ou desconhecida;
- evidência atual: código, teste, integração, execução real e limitações;
- comportamento-alvo e teste de aceitação;
- riscos, permissões, dependências e estado.

A matriz deve impedir que “navegador” esconda subcapacidades independentes e evitar inflação por sinônimos. Desmembrar apenas quando muda contrato, dependência, permissão, evidência ou critério de sucesso.

## 6. Fontes públicas e implicações

1. **NIST — taxonomia de ferramentas de agentes:** categorias funcionais e dimensões de acesso, confiança do ambiente, permissões e risco. Sustenta descrever capacidades por função e condições de uso, não apenas por nome de ferramenta.  
https://www.nist.gov/news-events/news/2025/08/lessons-learned-consortium-tool-use-agent-systems

2. **Model Context Protocol — especificação:** recursos, prompts, ferramentas, ciclo de vida, negociação de capacidades e autorização para transportes HTTP. É opção de interoperabilidade, não arquitetura total nem substituto da autoridade própria do ABS.  
https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/specification/2025-11-25/basic/index.mdx

3. **OpenAI Agents SDK:** ferramentas, handoffs, guardrails, sessões, participação humana, sandboxing e tracing; são capacidades separáveis, sem obrigar o ABS a adotar esse SDK.  
https://openai.github.io/openai-agents-python/

4. **Temporal — execução durável:** workflows retomáveis após falhas, indisponibilidade de rede e interrupções. Execução retomável é distinta de um processo simplesmente ativo.  
https://docs.temporal.io/

5. **NIST AI RMF e perfil de GenAI:** referências para governar, mapear, medir e gerir riscos durante o ciclo de vida.  
https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10  
https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

6. **LangGraph — persistência:** checkpoints para estado de execução e stores para memória de longo prazo, incluindo retomada, interrupção e recuperação. A distinção entre estado de missão e conhecimento persistente deve existir independentemente da ferramenta escolhida.  
https://docs.langchain.com/oss/python/langgraph/persistence

## 7. Regras para não converter pesquisa em lista de instalações

- Não instalar uma ferramenta por capacidade nem adotar SDK/framework/protocolo como autoridade central do ABS.
- Não escolher tecnologia apenas por popularidade; comparar com o que já existe e medir benefício, custo, manutenção, segurança, recursos e lock-in.
- Não exigir que todas as capacidades residam simultaneamente no VPS.
- Manter capacidades desejadas no catálogo mesmo se recursos ainda não existirem, usando estado correto.
- Não marcar como operacional apenas porque existe código, credencial ou teste unitário.
- Não marcar como ausente sem auditar código, documentação, runtime e evidências.
- Preferir contratos e adaptadores substituíveis, preservando controle, memória e proveniência próprios.

## 8. Próxima saída obrigatória antes de fechar a arquitetura V4

Produzir a **Matriz de Reconciliação das Capacidades ABS V4** cruzando: as 72 capacidades canônicas; os registros de capacidades e fechamento; código, testes, adaptadores e endpoints; evidência operacional; lacunas, duplicatas e capacidades transversais; requisitos centrais versus condicionais.

A matriz deve mostrar o que o ABS precisa ter, o que já tem, o que está parcial, o que falta e como comprovar cada capacidade. Só depois devem ser fixadas arquitetura final, ordem de execução e adoção de tecnologias.

## Limite desta pesquisa

Esta taxonomia ampla e síntese de fontes públicas não é uma prova matemática de completude universal. A completude prática deve ser testada contra os objetivos reais do Projeto Absoluto, o inventário canônico e a descoberta contínua de capacidades desconhecidas. Este documento não afirma que V4 foi implementada nem que todos os domínios são adequados para operar no hardware atual.
