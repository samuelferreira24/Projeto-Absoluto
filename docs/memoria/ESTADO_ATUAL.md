# Estado Atual — Projeto Absoluto

Memória operacional versionada. Atualizar após mudanças relevantes.

## 2026-10-08

### VPS
- Host: abs-vps-01
- Ubuntu 24.04 / x86_64
- 3 vCPU / ~5.7 GiB RAM / 2 GiB swap
- ~46 GiB livres no último teste
- usuário operacional: absadmin

### ABS
- Serviço systemd: abs.service
- Endpoint local: 127.0.0.1:8787
- Health: PASS
- Ciclo V1 objetivo → work → capability → execução → verificação → proveniência → persistência → resultado: PASS
- Inicialização automática: ativa

### Ponte operacional
- GitHub Actions → self-hosted runner → VPS: PASS
- Runner: abs-vps-01
- Canal atual: Issue #121 com comandos allowlisted

### OpenClaw
- Versão instalada: 2026.9.8
- Binário: /usr/bin/openclaw
- Serviço: openclaw-gateway.service
- Gateway: 127.0.0.1:18789
- Serviço: ativo e habilitado
- Memória observada: ~740 MB
- Autenticação de modelo: ainda não configurada

## Arquitetura provisória
Imperador → ABS → OpenClaw (operador 24/7) → ambientes/capacidades.
ChatGPT e outras IAs são inteligências externas.

## Próximo bloqueio
Autenticar uma inteligência no OpenClaw. Preferência inicial: OpenAI Codex/ChatGPT OAuth por device code, se elegível.
