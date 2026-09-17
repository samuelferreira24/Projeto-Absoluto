# Plano de Infraestrutura 24/7 — V0.1

## Objetivo

Permitir que uma missão continue sendo processada após o encerramento da interface que a iniciou.

## Componentes necessários

- runtime persistente de execução;
- armazenamento durável do estado e histórico;
- mecanismo de recuperação após falha;
- heartbeat/lease para evitar execução duplicada;
- idempotência de ações;
- observabilidade e alertas;
- política de autonomia;
- executor de ferramentas/agentes;
- integração por eventos e/ou agendamento;
- supervisão e escalonamento humano para ações de alto impacto.

## Papel das tecnologias

GitHub Actions pode executar automações orientadas a eventos e agendamentos. Um runtime persistente pode executar ciclos longos. APIs de agentes podem fornecer capacidades de raciocínio e uso de ferramentas. Nenhuma dessas tecnologias, isoladamente, representa o Sistema.

## Critério de continuidade

Se o navegador, a sessão ou uma IA forem encerrados, a missão deve permanecer recuperável. Outro agente compatível deve conseguir ler o estado e continuar sem depender do contexto privado da conversa anterior.

## Estado da capacidade

A base de software já possui missão persistente, histórico, ciclo contextual e política inicial de autonomia. Ainda falta a infraestrutura hospedada/persistente que execute esses ciclos continuamente.

## Princípio de segurança

24/7 não significa autonomia irrestrita. A continuidade deve operar dentro de permissões, políticas, limites de recursos, observabilidade, validação e escalonamento.
