# Adendo ao Tabuleiro — Execução Persistente V0.1

Este adendo incorpora a nova meta de execução persistente ao tabuleiro sem substituir o quadro mestre.

## Nova capacidade transversal

**EXECUÇÃO PERSISTENTE INDEPENDENTE DA INTERFACE**

Ela atravessa várias frentes existentes:

```text
CÉREBRO
  ↕
ESTADO
  ↕
ORQUESTRADOR
  ↕
DESPERTADOR
  ↕
WORKER
  ↕
AGENTES / EXECUTORES
  ↕
COLETA / EVENTOS
  ↕
RESULTADOS
  ↘
   APRENDIZADO → PLANEJAMENTO → NOVOS CAMINHOS
```

## Efeito multiplicador

A capacidade de execução persistente deve aumentar o valor de outras capacidades porque permite:

- coleta contínua;
- análise incremental;
- organização automática;
- experimentos sem presença constante do usuário;
- recuperação após interrupções;
- execução por múltiplas IAs;
- supervisão contínua;
- atualização do Cérebro;
- retroalimentação do planejamento.

## Caminhos simultâneos

A implementação deve poder avançar em paralelo em:

1. runtime persistente;
2. coleta universal;
3. organização do Cérebro;
4. análise dos repositórios;
5. continuidade entre IAs;
6. observabilidade e auditoria;
7. integração externa;
8. validação real.

Nenhum desses caminhos deve bloquear os demais quando houver trabalho independente e seguro disponível.

## Regra operacional

A cada ciclo, o sistema deve perguntar:

- o que mudou?
- o que está pendente?
- o que pode ser executado agora?
- o que precisa de pesquisa?
- qual caminho pode desbloquear outros?
- qual resultado pode multiplicar valor?
- o que foi aprendido?
- o que mudou no planejamento?

As respostas são sinais para decisão contextual, não uma fila fixa.

## Meta de validação

A capacidade será progressivamente validada por evidências, incluindo execução fora da interface, persistência, recuperação, idempotência, registro de resultados e continuidade após reinício.

## Relação com o quadro maior

Esta capacidade não é o destino do Projeto. É uma engrenagem que aumenta a capacidade do quadro inteiro e pode revelar arquiteturas e caminhos melhores durante a própria execução.
