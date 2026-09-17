# Contexto Compartilhado entre Chats V0.1

## Objetivo

Qualquer chat, agente ou sessão que participe do Projeto Absoluto deve conseguir reconstruir o estado operacional antes de executar uma ação.

Não basta transferir o histórico da conversa. O sucessor precisa saber:

- o que está sendo feito;
- como está sendo feito;
- por que está sendo feito;
- objetivo atual e objetivo maior;
- o que já foi feito;
- decisões e motivos;
- ações, ferramentas e resultados;
- tarefas pendentes;
- plano e próximo passo;
- bloqueios, riscos e restrições;
- evidências relevantes;
- aprendizados e mudanças de entendimento;
- agentes ativos e ferramentas disponíveis.

## Princípio

> **O contexto operacional é uma camada compartilhada de coordenação. O chat não deve depender da memória implícita de uma conversa para saber o estado do trabalho.**

A pesquisa realizada para esta implementação converge em três padrões: handoff estruturado entre agentes, memória compartilhada/blackboard e artefatos persistentes para continuidade entre sessões. A documentação atual da OpenAI descreve handoffs que transferem o estado recente entre agentes e tracing/observabilidade para depuração e otimização; trabalhos sobre blackboard recomendam estado estruturado, persistência e tratamento explícito de conflitos; e pesquisas de agentes de longa duração destacam artefatos persistentes para a próxima sessão.

## Contrato mínimo

```text
IDENTIDADE DO PROJETO
OBJETIVO
ESTADO ATUAL
O QUE ESTÁ SENDO FEITO
COMO ESTÁ SENDO FEITO
POR QUE ESTÁ SENDO FEITO
PLANO ATUAL
PRÓXIMO PASSO
DECISÕES
AÇÕES RECENTES
TAREFAS PENDENTES
BLOQUEIOS
RISCOS
RESTRIÇÕES
EVIDÊNCIAS
APRENDIZADOS
MUDANÇAS DESDE A ÚLTIMA SESSÃO
AGENTES ATIVOS
FERRAMENTAS DISPONÍVEIS
PROVENIÊNCIA / ATUALIZAÇÃO
```

## Fluxo

```text
CHAT / AGENTE ENTRA
        ↓
LER CONTEXTO OPERACIONAL
        ↓
VALIDAR ESTADO REAL
        ↓
ENTENDER O QUÊ / COMO / POR QUÊ
        ↓
EXECUTAR
        ↓
REGISTRAR AÇÃO + FERRAMENTA + MOTIVO + RESULTADO + EVIDÊNCIA
        ↓
ATUALIZAR CONTEXTO
        ↓
GERAR HANDOFF / CHECKPOINT
        ↓
PRÓXIMO CHAT CONTINUA
```

## Blackboard + memória

O contexto operacional não substitui a memória.

```text
                 CONTEXTO OPERACIONAL
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
     TAREFAS          ESTADO          DECISÕES
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                    CÉREBRO
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
   EVIDÊNCIAS       APRENDIZADOS       HISTÓRICO
```

O contexto é a visão operacional atual. A memória preserva a história e as evidências.

## Regra de atualização

Nenhuma sessão deve alterar silenciosamente o contexto. Quando houver conflito:

1. preservar os estados anteriores;
2. registrar a nova afirmação;
3. registrar a evidência;
4. marcar a divergência;
5. resolver explicitamente ou manter a incerteza.

## Implementação V0.1

- `cerebro/contexto_operacional.py` — contrato e construção do contexto;
- `cerebro/interface_chat.py` — contexto inicial para qualquer chat;
- `cerebro/continuidade.py` — contexto no snapshot/handoff;
- `cerebro/servico.py` — consulta, persistência e checkpoint;
- `cerebro/tests/test_contexto_operacional.py` — testes.

Artefatos portáteis gerados pelo Cérebro:

- `cerebro/data/contexto_operacional.json`;
- `cerebro/data/CONTEXTO_PARA_QUALQUER_CHAT.md`;
- `cerebro/data/continuidade.json`;
- `cerebro/data/RETOMAR_OUTRO_CHAT.md`.

## Limite atual

Esta implementação cria o contrato e o mecanismo de geração/retomada. Ela não consegue, sozinha, obrigar uma interface externa a consultar o contexto. Cada integração de chat deve consumir `contexto_inicial()`/`prompt_inicial()` ou o snapshot/handoff antes de executar.

A evolução natural é transformar esse contrato em um plano de contexto compartilhado persistente, com controle de versão, conflitos, permissões, atualização incremental, observabilidade e integração com cada conector de chat.
