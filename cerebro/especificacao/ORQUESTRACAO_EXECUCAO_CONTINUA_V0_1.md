# Orquestração e Execução Contínua — V0.1

## Objetivo

Criar a capacidade de receber uma missão, preservar seu estado e permitir que ciclos de trabalho continuem sem depender de uma conversa aberta como mecanismo de continuidade.

## Princípio

A conversa é uma interface possível. A missão pertence ao Projeto.

O encerramento de uma interface não deve apagar o estado da execução nem obrigar o usuário a enviar "continue" para cada ciclo.

## Arquitetura inicial

```text
INTERFACE
   ↓
MISSÃO PERSISTENTE
   ↓
ORQUESTRADOR
   ↓
CONTEXTO + CÉREBRO + TABULEIRO + ESTADO
   ↓
AGENTE/EXECUTOR
   ↓
AÇÃO
   ↓
RESULTADO
   ↓
REGISTRO
   ↓
ATUALIZAÇÃO DO PROJETO
   ↓
NOVO CICLO
```

## Não é uma fila fixa

O orquestrador não deve transformar o tabuleiro em uma sequência predeterminada. Cada ciclo deve poder pesquisar, questionar, mudar de caminho, abrir novos caminhos ou pausar quando o estado real exigir.

## Persistência

A missão deve sobreviver à interrupção da interface. O estado mínimo inclui objetivo, contexto, estado da missão, resultados e histórico de execução.

## Evolução prevista

1. Persistência local da missão e histórico.
2. Integração com Estado e Cérebro.
3. Seleção contextual de caminhos no Tabuleiro.
4. Executor baseado em ferramentas e agentes.
5. Retomada após interrupção.
6. Supervisão, validação e limites de autonomia.
7. Execução contínua em ambiente persistente.
8. Múltiplos agentes e múltiplas IAs.
9. Operação 24/7 com observabilidade e governança.

Nenhuma dessas etapas constitui uma ordem definitiva do Projeto; são capacidades que podem evoluir e impulsionar umas às outras.
