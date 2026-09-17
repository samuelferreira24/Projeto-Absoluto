# Runtime Contínuo V0.1

O runtime é a camada que mantém o ciclo de execução vivo independentemente da interface conversacional.

## Estados

`PARADO → EXECUTANDO → AGUARDANDO_PROXIMO_CICLO`

Em falha transitória:

`EXECUTANDO → ERRO_RECUPERAVEL`

Após uma interrupção detectada na inicialização:

`EXECUTANDO → RECUPERADO`

## Garantias iniciais

- estado do runtime persistido em disco;
- contador de ciclos persistido;
- último ciclo persistido;
- falha registrada como recuperável;
- interrupção anterior detectada na inicialização;
- parada explícita disponível;
- seleção de trabalho permanece contextual, sem fila fixa.

## Limite

Este runtime é uma fundação de execução persistente local. Ainda não fornece sozinho disponibilidade 24/7, processo supervisionado pelo sistema operacional, distribuição, leases, heartbeat, filas, escalonamento, múltiplos workers ou execução cloud.

Essas capacidades devem ser incorporadas conforme a experiência e os requisitos reais revelarem necessidade.
