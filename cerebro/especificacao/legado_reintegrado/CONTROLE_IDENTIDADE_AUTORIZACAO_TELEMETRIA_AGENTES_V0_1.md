# Controle de Identidade, Autorização e Telemetria de Agentes — V0.1

## Descoberta

A arquitetura já separava identidade, política de autonomia, execução, eventos e runtime, mas não possuía um plano de controle único para verificar cada ação antes da execução.

Pesquisa atual reforça a necessidade de identidade e autorização próprias para agentes, least privilege, allowlists de ferramentas, limites de custo e cadeia, separação entre decisão e execução e auditoria estruturada. NIST trata identidade, autenticação, autorização, delegação e auditoria de agentes como problemas arquiteturais específicos; OWASP recomenda controles equivalentes. OpenTelemetry fornece convenções para correlacionar agentes, ferramentas, resultados e recuperação, sem obrigar o núcleo a depender de um fornecedor.

## Estrutura

IDENTIDADE → AUTORIZAÇÃO → ESCOPO → AÇÃO → TELEMETRIA → RESULTADO → LEDGER/AUDITORIA

## Implementação V0.1

- identidade portável do agente;
- allowlist explícita de ferramentas;
- allowlist opcional de recursos;
- limite de autonomia;
- limite de custo;
- limite de profundidade de cadeia;
- aprovação explícita quando exigida;
- telemetria append-only local;
- correlação e parentização de eventos;
- integração opcional com o ledger existente.

## Limites

Esta versão não implementa sandbox de sistema operacional, identidade criptográfica, autenticação remota, rotação de credenciais, política de rede, quotas de CPU/memória ou não repúdio criptográfico.

## Próxima etapa

A camada já foi conectada ao ExecutorCerebro e possui um caminho controlado no RuntimeContinuo. O próximo endurecimento é tornar esse caminho obrigatório para operações de maior impacto, sem quebrar operações locais de baixo risco. Em paralelo, avaliar um adaptador OpenTelemetry e testes de falha/recuperação.
