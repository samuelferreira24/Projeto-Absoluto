# ABS V3 — ESPECIFICAÇÃO FECHADA PARA IMPLEMENTAÇÃO

Estado: arquitetura e especificação de implementação fechadas para construção integrada.
Base: ABS V2 operacional no VPS; V2 permanece como compatibilidade/migração, não como molde obrigatório.

## 1. Regra soberana

Imperador → ABS → política/governança → decisão → execução → modelos/ferramentas.

Nenhum modelo, executor, gateway, protocolo ou fornecedor possui autoridade sobre o ABS.

## 2. Objetivo

Interpretar objetivos; escolher a menor forma de execução suficiente; selecionar inteligência/executor/ferramentas; administrar CPU/RAM/I/O/concor­rência/filas; operar em modo gratuito, assinatura ou pago conforme política; verificar; produzir evidência; recuperar; replanejar; aprender; substituir componentes.

## 3. Núcleo próprio ABS

Authority Core; Objective/Context Interpreter; Decision & Strategy Engine; Mode Selector DIRECT/WORKFLOW/AGENT/MULTIAGENT; Efficiency & Capacity Governor; Admission Controller; Priority/Queue Manager; Intelligence Registry; Executor Registry; Capability Registry; Cost Policy Engine; Strategic Fallback/Replanning; Verification; Evidence/Provenance; Global Work State; Recovery/Reconciliation; Completion Criteria; Strategic Learning; health/capability discovery; compatibilidade V2/V1.

## 4. Peças especializadas

- llama.cpp: inferência local e lifecycle de modelos.
- Ollama: adapter opcional.
- vLLM/SGLang: adapter para hardware futuro.
- LiteLLM: gateway opcional para múltiplos provedores, fallback, retry, balanceamento, rate limits e tracking.
- OpenClaw: runtime/executor de agentes.
- LangGraph: workflows duráveis.
- MCP: tools/resources.
- A2A: tasks/agentes.
- PostgreSQL: banco operacional durável.
- pgvector: memória semântica inicial.
- filesystem/object storage: arquivos grandes.
- Redis: somente coordenação/cache/limites distribuídos quando necessário.
- OpenTelemetry + Prometheus/Grafana: observabilidade.
- Docker: isolamento e limites físicos.

## 5. Pool de inteligência

Cada recurso registra identidade, modelo, fornecedor, local/remoto, capacidades, custo, limites, latência, saúde, contexto, ferramentas, multimodalidade, reasoning/tool-calling, disponibilidade e evidência.

Classes: FREE_LOCAL; FREE_EXTERNAL; SUBSCRIPTION; PAID_API.

Políticas: FREE_ONLY; FREE_FIRST; PAID_ALLOWED.

FREE_ONLY: rota paga é estruturalmente inadmissível. Incapacidade gratuita gera fallback, degradação, espera ou declaração de incapacidade; nunca gasto automático.

PAID_ALLOWED: pagamento só dentro do orçamento autorizado.

## 6. Governor

Controla CPU, RAM, I/O, concorrência, filas, prioridade, duração, número de agentes, carga/descarga de modelos, escolha local/remota, velocidade versus preservação.

Objetivo: máximo trabalho útil por tempo/recurso/custo, não 100% de utilização.

Aprende curvas empíricas de capacidade e evita thrashing/swap.

## 7. Ordem obrigatória

CRASH/RECOVERY → IDEMPOTENCY/RECONCILIATION → VERIFICATION → RISK/AUTHORIZATION → RESOURCE PROTECTION → AVAILABILITY → COST POLICY → CAPABILITY → OPTIMIZATION/SPEED.

## 8. Falhas obrigatórias

CPU saturada; RAM pressão/crítica; I/O congestionado; IA local indisponível; gratuitos indisponíveis; assinatura indisponível; API paga indisponível; Internet indisponível; executor indisponível; componente novo/removido; timeout; crash antes/durante/depois; reboot; duplicação; UNKNOWN; verificação falha; demanda acima da capacidade; concorrência; starvation; deadlock; retry loop; limite de custo; alto risco.

## 9. Persistência

Objetivo, versão, plano, política, orçamento, seleção de recursos, execução, checkpoints, observações, evidências, verificação, tentativas, idempotency key, recovery state, custo/uso e aprendizado devem sobreviver ao processo.

## 10. Verificação

Resultado recebido não equivale a resultado comprovado. Estados explícitos: OBSERVED, VERIFIED, FAILED, UNKNOWN.

## 11. Seleção de componentes

Não preservar algo só porque existe no V2. Comparar capacidade, maturidade, confiabilidade, desempenho, consumo, observabilidade, segurança, extensibilidade, independência, integração, custo, adequação ao VPS e escala. Resultado: KEEP / ADAPT / REPLACE / CREATE.

## 12. Estado atual

Reutilizável: autoridade, policy/risk, modes, executores V2, OpenClaw, capabilities, intelligence registry, resource routing, learning básico, evidence/provenance, idempotency, checkpoints, MCP/A2A e testes.

Substituir/adaptar: SQLite como destino operacional; ranking estático; budgets estáticos; verification simplista; workflow/multiagent serial quando paralelismo seguro for possível; fallback limitado; ausência de governor físico, cost policy, telemetry, learned capacity curves, dynamic model lifecycle e admission/queues adaptativos.

Criar: V3 Control Plane; Efficiency/Capacity Governor; Cost Policy Engine; catálogo enriquecido; admission/queue; telemetry; dynamic intelligence selection; model lifecycle; verification forte; durable state abstraction; strategic learning; discovery/replacement contracts.

## 13. Modelos locais

O modelo local atual de 0.5B permanece baseline/emergency. Qwen3/Qwen3.5 GGUF são candidatos reais para evolução local. A quantização/arquivo final será escolhida pelo benchmark do VPS durante a implantação, sem prender o contrato V3 ao nome de um modelo.

## 14. Simulação de fechamento

Matriz: 3 políticas × 4 demandas × 3 CPU × 3 RAM × 3 IA local × 3 gratuitos × 3 assinaturas × 3 APIs pagas × 3 redes × 4 riscos × 3 verificações × 3 fases de crash × 2 duplicações.

Total: 1.889.568 estados.

Resultados: recuperação 1.259.712; reconciliação 314.928; verificar/replanejar 209.952; proteção de recursos 38.880; aprovação/execução restrita 34.992; local 12.960; espera/degradação 11.648; assinatura 2.176; gratuito externo 3.680; pago 640.

Estados em que API paga foi escolhida fora da política que a permite: 0.

Esta é uma validação combinatória da máquina de decisão, não 1.889.568 execuções reais no VPS.

## 15. Critério de construção concluída

Implementar todos os contratos; fazer FREE_ONLY impedir gasto; PAID_ALLOWED respeitar orçamento; Governor reagir a CPU/RAM/I/O reais; recovery sobreviver a crash/reboot; idempotência; evidência/verificação; fallback; memória persistente; observabilidade; testes unitários/integrados/stress/falha; fluxo completo real no VPS.

## 16. Regra contra V4 prematura

Uma necessidade já coberta pelo contrato V3 é lacuna de implementação, não motivo automático para V4. V4 só nasce por capacidade genuinamente fora do contrato V3.
