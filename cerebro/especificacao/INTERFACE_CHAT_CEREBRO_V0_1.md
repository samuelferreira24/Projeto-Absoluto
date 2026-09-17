# Interface Chat ↔ Cérebro — V0.1

## Prioridade
MÁXIMA.

O chat não deve ser tratado como um lugar onde o conhecimento do Projeto Absoluto fica preso. O chat deve funcionar como uma **interface do Cérebro**.

## Princípio central

```text
CHAT / OUTRAS INTERFACES
          ↓
     CAPTURA DE EVENTOS
          ↓
   CÉREBRO / MEMÓRIA CENTRAL
          ↓
   CONHECIMENTO + CONTEXTO
          ↓
 RECUPERAÇÃO PARA A INTERFACE
          ↓
      CONTINUIDADE
```

O Cérebro é a camada persistente. A interface pode mudar; o conhecimento não deve desaparecer com a troca de chat, conta, IA ou plataforma.

## O que deve ser guardado

Cada conversa relevante deve poder gerar registros de:

- mensagem/evento bruto;
- origem da conversa;
- conta/interface/plataforma, quando disponível;
- data e ordem temporal;
- contexto;
- objetivo;
- decisão;
- entendimento;
- descoberta;
- progresso;
- erro;
- correção;
- pesquisa;
- evidência e proveniência;
- experiência;
- aprendizado;
- mudança de entendimento;
- resultado;
- relações com registros anteriores;
- incerteza/confiança;
- supersessão/versionamento;
- próximo estado/progresso.

## Regra de preservação

**Capturar primeiro; interpretar depois.**

O conteúdo bruto não deve ser substituído por um resumo. Resumos, fatos, conceitos e aprendizados são camadas derivadas que devem apontar para a origem.

```text
BRUTO
 ↓
FRAGMENTOS
 ↓
FATOS / CONCEITOS
 ↓
EPISÓDIOS
 ↓
EXPERIÊNCIAS
 ↓
PROCEDIMENTOS / PRINCÍPIOS
```

## Recuperação urgente

Deve existir um processo específico para recuperar o máximo de contexto possível de cada chat antes de qualquer perda, migração ou troca de interface.

Pipeline:

```text
CHAT
 ↓
RECUPERAR TUDO QUE ESTIVER DISPONÍVEL
 ↓
PRESERVAR ORIGINAL
 ↓
INDEXAR
 ↓
SEPARAR POR FASE TEMPORAL
 ↓
IDENTIFICAR ENTENDIMENTOS / DECISÕES / DESCOBERTAS / ERROS
 ↓
RELACIONAR
 ↓
CONSOLIDAR SEM APAGAR A ORIGEM
 ↓
CÉREBRO
```

A recuperação deve procurar não apenas palavras-chave, mas também contexto, relações e mudanças de entendimento.

## Interface como janela do Cérebro

A interface deve conseguir:

1. recuperar contexto relevante antes de responder;
2. registrar automaticamente a conversa como evento;
3. salvar decisões e aprendizados explicitamente identificados;
4. consultar memória histórica;
5. recuperar o estado/progresso do Projeto;
6. continuar trabalho iniciado em outra interface;
7. registrar divergências entre IAs sem apagar nenhuma versão;
8. enviar novos eventos para o Cérebro;
9. receber do Cérebro contexto para orientar a sessão;
10. funcionar como uma camada substituível.

## Identidade e proveniência

Cada evento deve manter sua origem. O Cérebro não deve fingir que uma interpretação de uma IA é um fato absoluto.

```text
ORIGEM → EVENTO → INTERPRETAÇÃO → VALIDAÇÃO → CONHECIMENTO
```

Quando houver divergência:

```text
VERSÃO A ─┐
          ├→ CÉREBRO → COMPARAÇÃO / VALIDAÇÃO
VERSÃO B ─┘
```

Não sobrescrever silenciosamente.

## Continuidade entre chats

A troca de chat não pode significar reinício cognitivo.

```text
CHAT A
  ↓
CÉREBRO
  ↓
CHAT B
  ↓
CÉREBRO
  ↓
CHAT C
```

Cada interface deve poder recuperar:
- o que já foi feito;
- por que foi feito;
- o que foi descoberto;
- o que falhou;
- o que mudou;
- onde o Projeto está;
- quais são as próximas ações;
- quais conhecimentos são relevantes para a tarefa atual.

## Segurança contra perda de contexto

O sistema deve manter:

- evidência bruta;
- registros derivados;
- proveniência;
- histórico temporal;
- versionamento;
- idempotência;
- relações;
- contradições;
- confiança/incerteza.

**Nenhuma consolidação pode apagar silenciosamente a fonte original.**

## Relação com a arquitetura maior

```text
              PROJETO ABSOLUTO
                     │
        ┌────────────┼────────────┐
        │            │            │
    IMPERADOR      SISTEMA      IMPÉRIO
                     │
                   CÉREBRO
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       MEMÓRIA    PESQUISA  ORQUESTRAÇÃO
          │          │          │
          └──────────┼──────────┘
                     ↓
               INTERFACES
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
        CHAT       IA/API    OUTRAS
```

O chat é uma interface. O Cérebro é a memória persistente do Sistema. A arquitetura deve continuar independente de plataforma.

## Estado da implementação

A base do Cérebro já possui captura de eventos, memória persistente, recuperação, continuidade/checkpoint, consolidação, grafo de tarefas e agendamento adaptativo. Esta especificação define a prioridade de transformar a interface conversacional em uma entrada/saída direta dessa infraestrutura.

## Próxima evolução

Implementar um adaptador de conversa que transforme cada mensagem/evento disponível em registros persistentes no Cérebro, mantendo o bruto e gerando camadas derivadas. A implementação deve começar pela preservação e recuperação, antes de automações cognitivas mais sofisticadas.
