# Catálogo ampliado de componentes, serviços e ferramentas candidatas — ABS V4

**Finalidade:** complementar a Lista Operacional Completa com um inventário abrangente de componentes que podem ser necessários durante a construção do ABS. Este documento não manda instalar tudo simultaneamente e não substitui a auditoria do estado real.

**Regra:** todos os grupos permanecem no inventário. A decisão de não instalar agora define apenas a fase/gatilho de ativação; não remove o item da lista. Já existir não significa estar integrado, e estar integrado não significa estar validado. Não instalar duplicatas se a solução existente cumprir os mesmos critérios comprovadamente.

## 1. Infraestrutura e execução
- Sistema operacional Linux/Ubuntu, Python, Node.js e runtimes específicos.
- Docker Engine, Compose, imagens OCI, redes, volumes, Coolify e systemd.
- Containers isolados, sandboxes, workspaces descartáveis, limites de CPU/RAM/disco/PIDs/rede/tempo.
- Nós remotos, gateway de nós, health checks e comunicação autenticada entre nós.
- Acesso administrativo privado: Tailscale ou WireGuard; SSH por chave.
- Gestão pelo navegador móvel: painel ABS, Code Server e interfaces de administração.

## 2. Dados, memória e recuperação
- Bancos relacionais: PostgreSQL e SQLite; outros motores somente se houver requisito específico.
- Cache e locks: Redis/Valkey ou mecanismo embutido.
- Filas e mensageria: fila própria persistente, fila apoiada em PostgreSQL, Redis/Valkey, RabbitMQ, NATS e, se a escala justificar, Kafka/Redpanda.
- Armazenamento de objetos: S3 compatível, MinIO ou serviço gerenciado; volumes e workspace por missão.
- Pesquisa textual: full-text PostgreSQL, Meilisearch, OpenSearch/Elasticsearch.
- Pesquisa vetorial/RAG: pgvector, Qdrant, Weaviate, Milvus; embeddings e reranking locais ou por API.
- Backup independente, snapshots, exportação/importação, checksums, cópia externa e testes de restauração; política RPO/RTO.

## 3. IA e orquestração
- Runtime local: Ollama, llama.cpp/llama-server e alternativas compatíveis.
- Adaptadores nativos e API compatível com OpenAI; catálogo de modelos e contratos uniformes.
- Os seis modelos locais já registrados e candidatos futuros, com avaliação individual de licença, quantização, RAM, latência e qualidade.
- Gateway multi-provedor: LiteLLM ou alternativa, mantendo o roteador e a autoridade no ABS.
- Orquestração: runtime próprio do ABS; Microsoft Agent Framework, LangGraph, AutoGen ou outros como executores subordinados, após comparação.
- Provedores de IA em nuvem autorizados; embeddings/rerankers; STT/TTS, OCR, visão, transcrição e processamento de áudio/vídeo.
- Harness de avaliação comparativa, conjunto de missões de referência, custo/latência/qualidade e testes de fallback.

## 4. Navegador, web e documentos
- Playwright + Chromium como primeira opção de navegador; Selenium ou equivalente como alternativa.
- Container e perfis isolados, sessões temporárias, políticas de saída de rede e handoff humano para MFA/CAPTCHA.
- APIs/provedores de busca, crawler controlado, parsers HTML, Readability, BeautifulSoup/lxml, extração de tabelas e páginas dinâmicas.
- Parsers e ferramentas para PDF, DOCX, XLSX, CSV, apresentações, imagens, áudio e vídeo.
- Bloqueio de SSRF, loopback, metadata e redes privadas; downloads validados e uploads explicitamente autorizados.

## 5. Conectores e automação
- Git/GitHub API, webhooks, CI, PRs, terminal controlado, clientes HTTP, OpenAPI, OAuth2 e chaves de API.
- MCP e conectores de terceiros, cada qual avaliado individualmente e com allowlist de ferramentas.
- Automação de workflows: n8n, Temporal, Prefect, Dagster, cron/systemd timers ou agendador próprio.
- APIs autorizadas de e-mail, chat, notificações, armazenamento e outros serviços que venham a integrar missões.
- Android: web responsiva/PWA, futura APK e APIs do dispositivo com consentimento e permissões explícitas.

## 6. Observabilidade, auditoria e qualidade
- Logs estruturados, métricas, OpenTelemetry, tracing, correlação por missão/Work/tentativa.
- Prometheus/exporters, Grafana ou painel próprio, Uptime Kuma ou equivalente, alertas.
- Langfuse ou alternativa de tracing/eval de LLM; tracing próprio se cumprir os critérios com menos risco/custo.
- Auditoria append-only, trilha de autorização/ação/resultado, gestão de bugs e regressões.
- Testes unitários, de contrato, integração, E2E, carga, falha, recuperação e red team.

## 7. Identidade, segredos e segurança
- Autenticação de painel, OAuth/OIDC quando adequado, política de autorização por missão/capacidade/recurso.
- Segredos: variáveis protegidas, Docker secrets, SOPS/age, Vault ou equivalente; rotação e revogação.
- TLS, proxy reverso, firewall, rede privada, rate limits, quotas e orçamento por missão.
- Imagens versionadas, análise de dependências, SBOM quando apropriado, isolamento, filesystem restrito e usuário sem privilégios.
- Redação de logs, retenção, criptografia quando aplicável e procedimento de resposta a incidentes.

## 8. Deploy e ciclo de vida
- Git branches/tags/releases, GitHub Actions ou CI equivalente, Coolify/Compose ou CD equivalente.
- Configuração por ambiente, migrações de banco, health/readiness, smoke test pós-deploy e rollback.
- Inventário de serviços, versões, portas, volumes, dependências, custos, backups e responsáveis.

## 9. Interface e operação pelo Imperador
- Painel responsivo, chat, anexos e multimodalidade conforme motores disponíveis.
- Estado de missões, aprovações, pausa/cancelamento/retomada, notificações e evidências.
- Gestão segura de arquivos, continuidade entre sessões/dispositivos e histórico de decisões.

## 10. Registro obrigatório por item
Para cada componente, registrar: finalidade; capacidades habilitadas; estado observado (ausente, instalado, configurado, integrado, testado, validado ou obsoleto); evidência; dependências/conflitos; alternativas e motivo da escolha; fase e gatilho; custo e recursos; risco e permissões; testes de aceitação; rollback; próximo passo e data da revisão.

## 11. Regra de completude
- Este catálogo complementa a matriz das 72 capacidades, a lista operacional e a especificação explícita do navegador.
- Não excluir itens porque não serão instalados agora. Registrar o motivo e o gatilho de reavaliação.
- A lista é ampla e evolutiva, não uma promessa de prever toda ferramenta futura. Novos requisitos descobertos durante auditorias e testes devem ser adicionados.
- A abrangência do inventário não significa execução simultânea: a instalação é faseada, testada, reversível e limitada pelos recursos reais da VPS.
