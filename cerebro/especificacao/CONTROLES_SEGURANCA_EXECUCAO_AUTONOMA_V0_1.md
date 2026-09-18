# Controles de Segurança da Execução Autônoma V0.1

## Descoberta

A arquitetura de execução já possuía política de autonomia, identidade de agente, allowlist de ferramentas, telemetria, claims e leases. A reavaliação mostrou duas lacunas importantes: aprovação booleana não vinculava autorização à ação exata; claims persistentes sem serialização entre processos podiam permitir dispatch duplicado.

Pesquisas atuais recomendam separar decisão de execução, least privilege, aprovação vinculada à ação e proteção contra replay. citeturn1search1turn1search8

## Regra arquitetural

AGENTE/PLANEJADOR → PROPOSTA → POLÍTICA INDEPENDENTE → APROVAÇÃO VINCULADA → CONTROLE DE EXECUÇÃO → CLAIM SERIALIZADO → EXECUTOR → TELEMETRIA/EVIDÊNCIA

A IA não deve ser a autoridade final sobre sua própria autorização.

## Aprovação vinculada

A aprovação pode ser emitida para uma ação específica e vinculada a nome da ação, nível de autonomia, ferramenta, recurso, custo máximo, profundidade máxima da cadeia, validade e uso único.

A aprovação é consumida após execução bem-sucedida. Não pode ser reutilizada nem transferida para outra ferramenta ou recurso.

## Claims

ControleExecucao agora serializa operações de claim, conclusão, falha, liberação e reconciliação com lock interprocessos e persistência atômica.

## Recuperação

Quando um claim expira, ele é marcado como expirado; a tarefa correspondente é localizada; se estiver EXECUTANDO, volta a PENDENTE; a recuperação é registrada; e o próximo planejamento pode reconsiderar a tarefa.

## Limites

Ainda faltam armazenamento durável compartilhado, identidade/autenticação forte entre workers, assinatura de mensagens entre agentes, sandbox, gestão segura de segredos, proteção contra memory poisoning, red team automatizado, circuit breakers distribuídos e auditoria verificável externamente.

Pesquisas recentes mostram que memória persistente é superfície de ataque e que proveniência simples pode falhar contra técnicas de laundering, reforçando a necessidade futura de autoridade de origem e controles de escrita na memória. citeturn1academia12turn1academia14

## Princípio

> Autonomia não significa ausência de controle. Quanto maior a capacidade de agir, mais independente, explícita, rastreável e limitada deve ser a autoridade que permite a ação.
