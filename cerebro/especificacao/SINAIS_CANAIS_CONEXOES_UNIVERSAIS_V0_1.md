# SINAIS, CANAIS E CONEXÕES UNIVERSAIS — V0.1

## Princípio
O Cérebro não deve assumir que uma conexão é sinônimo de internet.
Internet é um meio de transporte/acesso. Sinal é informação, evento, comando, resultado ou mudança que pode chegar ao Cérebro por qualquer meio.
Um mesmo sinal pode chegar por internet, rede local, arquivo, interface, processo local ou outro mecanismo. O transporte fica desacoplado do núcleo.

## Mapa amplo de sinais
- HUMANO: comando, correção, ideia, pergunta, decisão e feedback.
- CHAT: mensagens e conversas.
- INTERFACE: UI, voz, terminal, painel e outras interfaces.
- ARQUIVO: documentos, imagens, áudio, vídeo, bancos exportados e pacotes.
- WEB: páginas, eventos e dados públicos.
- API: REST, GraphQL, webhooks e serviços.
- APP: aplicativos locais ou remotos.
- CODIGO: código, execução, testes, logs e resultados.
- GITHUB: repositórios, commits, issues, PRs, releases e eventos.
- CODEX: tarefas, execução, resultados e sinais de desenvolvimento.
- AGENTE: outro agente ou sistema autônomo.
- PROCESSO: eventos de processos e serviços locais.
- SISTEMA_OPERACIONAL: eventos do ambiente de execução.
- BANCO_DE_DADOS: mudanças, consultas e resultados.
- MENSAGERIA: filas, eventos e mensagens.
- SCHEDULE: despertares, agendas e eventos temporais.
- MONITORAMENTO: métricas, alertas e observabilidade.
- RECURSO: disponibilidade, consumo, quota, combustível e capacidade.
- DISPOSITIVO: sinais de hardware ou dispositivos conectados.
- SENSOR: telemetria e medições, quando aplicável.
- RESULTADO: resultado de ação ou experimento.
- ERRO: falha, exceção, timeout ou incompatibilidade.
- FEEDBACK: avaliação humana ou automática.
- DESCOBERTA: nova informação detectada pelo sistema.
- OUTRO: qualquer fonte futura não prevista.

A lista é extensível e nunca deve ser tratada como catálogo fechado.

## Meio não é origem
Exemplos: HUMANO + internet; HUMANO + presencial; API + internet; ARQUIVO + disco local; CODEX + interface; GITHUB + API; AGENTE + rede; PROCESSO + IPC; SENSOR + conexão local.

Fluxo: ORIGEM → SINAL → CANAL/MEIO → CÉREBRO.
Não: INTERNET → CÉREBRO.

## Entrada e saída
Entradas: receber, validar, preservar bruto, identificar origem e proveniência, relacionar contexto e transformar em conhecimento/evento/tarefa quando apropriado.
Saídas: emitir comandos, enviar resultados, chamar capacidades, acionar portas, comunicar com outros cérebros/agentes, atualizar interfaces e solicitar recursos.

## Segurança e controle
Cada sinal pode carregar identidade, origem, destino, canal, contexto, proveniência, confiança, permissões, timestamp, correlação, idempotência, risco, payload bruto e metadados.
Nenhum canal ganha autoridade apenas por existir. Autorização deve ser separada de transporte.

## Arquitetura futura
MUNDO → HUMANOS / SISTEMAS / OUTROS AIs → SINAIS / EVENTOS → ADAPTADORES → CANAIS/MEIOS → CÉREBRO → MEMÓRIA / ORQUESTRAÇÃO / DECISÃO → CAPACIDADES → PORTAS / APPS / AGENTES → AÇÃO → RESULTADO → SINAL → ciclo contínuo.

## Codex, GitHub, app e interface
Codex, GitHub, aplicativos, interfaces e outros serviços não devem ser incorporados ao núcleo como dependências rígidas.
Eles devem ser portas, capacidades e canais substituíveis. Se uma tecnologia mudar, outra porta pode assumir a mesma capacidade.

## Expansão futura
A camada de sinais deve aceitar novos tipos, canais, meios, fontes e protocolos sem alterar a visão central.
O objetivo não é prever todas as conexões. É construir uma arquitetura capaz de incorporar conexões que ainda nem existem.