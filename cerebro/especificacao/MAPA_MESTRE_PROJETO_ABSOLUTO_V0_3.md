# MAPA MESTRE DO PROJETO ABSOLUTO V0.3 — REAVALIAÇÃO 2026-09-18

Este documento deriva do V0.2. O V0.2 permanece preservado como registro histórico. Esta versão corrige estados que ficaram desatualizados pela construção recente.

## Princípio

O mapa descreve o estado conhecido; não limita o futuro. Planejamento e construção continuam simultâneos.

## Estado revisado

| Domínio | Estado revisado | Observação |
|---|:---:|---|
| Visão | 🟢 | estabelecida |
| Princípios | 🟢 | estabelecidos e versionados |
| Método | 🟢 | em uso e refinamento |
| Arquitetura | 🟡 | ampla, ainda evolutiva |
| Fundação | 🟡 | construída em camada inicial |
| Cérebro | 🟡 | funcional em várias camadas, ainda incompleto |
| Estado | 🟡 | versionado e persistente |
| Histórico temporal | 🟡 | eventos, temporalidade e reconstrução inicial |
| Identidade | 🟡 | identidade/eventos já modelados |
| Proveniência | 🟡 | presente na ingestão e memória |
| Continuidade | 🟡 | snapshots e contratos iniciais |
| Portabilidade | 🟡 | artefatos portáveis, runtime final ainda aberto |
| Interfaces | 🟡 | CLI/chat e contratos iniciais |
| Integração | 🟡 | GitHub e dispatch inicial; ecossistema externo ainda limitado |
| Execução | 🟡 | scheduler + executor + controle + telemetria |
| Automação | 🟡 | workflows e runtime de despertar existentes; executor externo ainda pode permanecer ausente |
| Agentes de IA | 🟡 | identidade/controle e perfis iniciais; agentes reais ainda não integrados |
| Multi-IA | 🔴 | hipótese e preparação, sem rede multi-IA operacional |
| Orquestração | 🟡 | scheduler, grafo, missão e replanejamento iniciais |
| Hierarquia dinâmica | 🔴 | ainda não implementada |
| Supervisão | 🔴 | controles existem, supervisão operacional ainda não é uma camada própria |
| Meta-supervisão | 🔴 | não implementada |
| Auditoria independente | 🟡 | auditoria e telemetria iniciais |
| Segurança | 🟡 | política, identidade, aprovação e allowlists iniciais |
| Governança | 🟡 | políticas e limites iniciais |
| Observabilidade | 🟡 | telemetria, ledger e evidências |
| Aprendizado | 🟡 | persistência e consolidação |
| Sabedoria operacional | 🟡 | modelo inicial |
| Pesquisa contínua | 🟡 | método ativo, automação completa ainda ausente |
| Aplicação do conhecimento | 🟡 | recuperação + planejamento + execução inicial |
| Construção auto-referencial | 🟡 | processo registra aprendizados |
| Memória organizacional | 🟡 | base inicial; consolidação e avaliação ainda necessárias |
| Grafo de relações | 🟡 | rede evolutiva e semântica iniciais |
| Conhecimento temporal | 🟡 | camada temporal inicial |
| Digital thread | 🟡 | rastreabilidade inicial, ainda não ponta a ponta |
| Operação contínua | 🟡 | scaffold 24/7; não é runtime autônomo plenamente configurado |
| Recursos externos | 🟡 | estoque/capacidade modelados, integração externa ainda parcial |
| Evolução | 🟡 | mecanismo de reavaliação e aprendizado inicial |
| Expansão | 🔵 | aberto |
| Sistemas derivados | 🔵 | aberto |
| Escala | 🔵 | aberto |
| Realidade externa | 🔵 | aberto |
| Capacidades desconhecidas | 🔵 | aberto |

## Correção conceitual importante

A existência de código de execução, workflows ou scheduler não significa que o Projeto já possua autonomia operacional completa.

O estado correto é:

`infraestrutura de autonomia inicial` ≠ `autonomia operacional plena`

O runtime pode despertar e verificar se existe executor externo configurado. Quando ele não existe, permanece em espera. Isso é comportamento correto de segurança, não falha.

## Próximo bloco

A prioridade passa a ser:

1. contrato unificado Missão → Plano → Tarefa → Claim → Autorização → Execução → Resultado;
2. integração canônica de recursos/combustível;
3. harness de avaliação e falhas;
4. métricas de qualidade do planejamento;
5. avaliação de memória e retenção;
6. somente depois, expansão real para múltiplos agentes/motores.

O objetivo é reduzir fragmentação antes de aumentar complexidade.
