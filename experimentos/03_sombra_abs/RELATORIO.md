# Experimento 03 — Baseline do ABS atual

## Resultado

O ABS atual possui seleção explícita de capability, mas CapabilityRegistry.choose() sem identificador não é um seletor de estratégia: ele retorna o primeiro registro.

Isso não é tratado como bug isolado. É evidência arquitetural de que a nova camada deve ficar acima de capability/resource selection.

## Consequência

A sequência correta continua sendo:

OBJETIVO → CONTEXTO/ESTADO → ESTRATÉGIA → MODO → CAPACIDADE → RECURSO → EXECUTOR

e não:

OBJETIVO → CAPACIDADE → primeiro recurso disponível

## Decisão experimental

Não modificar CapabilityRegistry para fazê-lo virar o "cérebro" da estratégia. O experimento reforça a separação entre estratégia e capacidade.

## Próximo teste

Conectar uma camada de planejamento em sombra aos registries atuais sem executar trabalho real.
