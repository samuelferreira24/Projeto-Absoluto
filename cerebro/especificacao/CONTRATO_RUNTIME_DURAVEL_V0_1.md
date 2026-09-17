# Contrato de Runtime Durável V0.1

## Objetivo

Definir o que significa execução contínua recuperável para o Projeto Absoluto sem confundir um mecanismo local de execução com uma operação 24/7 já hospedada.

## Princípios

1. **Estado durável:** o runtime deve conseguir reconstruir seu estado após encerramento ou reinício.
2. **Checkpoint antes de confiar:** progresso confirmado precisa estar persistido.
3. **Lease com expiração:** um worker que desaparece não pode bloquear o trabalho indefinidamente.
4. **Heartbeat:** workers vivos renovam o lease; workers abandonados tornam-se recuperáveis.
5. **At-least-once para efeitos externos:** uma ação pode ser observada novamente depois de uma falha; efeitos externos devem usar idempotência, chaves estáveis, upsert ou outra coordenação adequada.
6. **Histórico rastreável:** missão, ciclo, decisão, caminho, resultado e falha devem permanecer associados.
7. **Separação entre orquestração e execução:** o runtime coordena; agentes e ferramentas executam.
8. **Portabilidade:** o contrato não depende de OpenAI, Claude, GitHub ou qualquer fornecedor específico.
9. **Recuperação não é continuação literal:** depois de uma interrupção, o sistema retoma a partir do último estado confirmado, aplicando uma política explícita.

## Ciclo durável

```text
MISSÃO
  ↓
ESTADO PERSISTIDO
  ↓
CLAIM / LEASE
  ↓
DECISÃO CONTEXTUAL
  ↓
AÇÃO
  ↓
RESULTADO / EVIDÊNCIA
  ↓
CHECKPOINT
  ↓
LIBERAÇÃO DO LEASE
  ↓
PRÓXIMO DESPERTAR
```

## Lease

O lease representa a posse temporária de uma execução por um runtime.

Campos mínimos:

- `lease_id`
- `runtime_id`
- `expira_em`
- `criado_em`
- `heartbeat_em`

A aquisição local utiliza criação exclusiva do arquivo de lease (`O_CREAT | O_EXCL`) para evitar que dois workers adquiram simultaneamente o mesmo lease em condições normais.

Um lease expirado pode ser recuperado. Um lease ainda válido não deve ser tomado por outro worker.

## Heartbeat

Enquanto uma execução longa estiver ativa, o worker deve renovar o lease antes da expiração. A renovação deve confirmar que o lease ainda pertence ao worker e que não expirou.

## Recuperação

Um estado `EXECUTANDO` só deve ser marcado como recuperável automaticamente quando não houver lease válido. Isso evita tratar uma execução legítima como abandonada apenas porque um novo processo iniciou.

## Idempotência

O runtime não promete execução exatamente uma vez de efeitos externos. Uma queda pode ocorrer depois do efeito externo e antes do checkpoint local. Portanto, ações externas importantes devem receber uma identidade lógica estável de execução e ser desenhadas para tolerar repetição.

Exemplos:

- chave de idempotência em APIs;
- upsert por identificador determinístico;
- registro de operação antes/depois do efeito;
- operações naturalmente repetíveis;
- compensação quando repetição não puder ser evitada.

## Limite atual

V0.1 implementa o núcleo local de lease, expiração, recuperação e heartbeat. Isso **não equivale ainda a um serviço 24/7 hospedado**.

Para operação contínua real ainda são necessários, entre outros:

- armazenamento durável compartilhado quando houver múltiplos workers;
- mecanismo de despertar/scheduler;
- fila ou mecanismo equivalente de trabalho;
- observabilidade;
- retries e backoff;
- cancelamento;
- supervisão;
- controle de custos e recursos;
- recuperação de resultados intermediários;
- autenticação/autorização;
- execução em ambiente persistente;
- políticas para efeitos externos;
- testes de falha e recuperação em ambiente real.

## Relação com o GitHub

GitHub Actions pode funcionar como mecanismo de validação, eventos e despertar de ciclos. Workflows agendados têm intervalo mínimo de cinco minutos e workflows também podem ser acionados por eventos externos via `repository_dispatch`. Isso torna o GitHub útil como parte da infraestrutura, mas não transforma o GitHub no runtime definitivo do Projeto.

## Regra arquitetural

> O Projeto deve possuir um mecanismo de execução recuperável independente da interface usada para comandá-lo. A interface pode desaparecer; a missão, o estado, o histórico e a capacidade de retomada devem permanecer.

## Evidência e evolução

Esta especificação deve evoluir conforme testes reais revelarem novas necessidades. O objetivo não é congelar uma tecnologia, mas preservar as propriedades necessárias para execução contínua, recuperação, rastreabilidade e evolução.
