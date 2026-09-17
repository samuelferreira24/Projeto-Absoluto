# Meta de Execução Persistente e Evolutiva V0.1

## Objetivo

Transformar o Projeto Absoluto em uma estrutura capaz de planejar e executar continuamente, preservando contexto, estado, histórico, evidências, aprendizados e sabedoria, sem depender da aba, da conversa ou de uma IA específica permanecer aberta.

Esta é uma meta evolutiva, não uma arquitetura definitiva.

## Princípio central

Planejamento e execução devem acontecer simultaneamente e retroalimentar-se. O sistema não deve esperar um planejamento perfeito para agir nem executar cegamente um plano congelado.

```text
VISÃO
  ↓
CONTEXTO + CÉREBRO + ESTADO + TABULEIRO
  ↓
CAMINHOS POSSÍVEIS
  ↓
DECISÃO CONTEXTUAL
  ↓
AÇÃO AUTORIZADA
  ↓
RESULTADO + EVIDÊNCIA
  ↓
CAPTURA
  ↓
ORGANIZAÇÃO
  ↓
ENTENDIMENTO / APRENDIZADO / SABEDORIA
  ↓
REPLANEJAMENTO
  ↺
```

## Independência da interface

Chat, navegador e aplicativo são interfaces. O trabalho contínuo deve pertencer a um runtime persistente.

```text
INTERFACE → COMANDO / CONSULTA
                 ↓
          RUNTIME PERSISTENTE
                 ↓
      ORQUESTRADOR + CÉREBRO
                 ↓
          AGENTES / FERRAMENTAS
                 ↓
             RESULTADO
                 ↓
          CÉREBRO / ESTADO
                 ↺
```

Fechar a interface não deve apagar contexto nem interromper o ciclo de um runtime que já esteja hospedado e executando.

## Qualquer fonte

A entrada deve permanecer aberta para fontes atuais e futuras. Não será criada uma lista fechada de fontes.

```text
QUALQUER FONTE
      ↓
ADAPTADOR / PROTOCOLO COMPATÍVEL
      ↓
ENVELOPE PADRÃO
      ↓
CAPTURA BRUTA
      ↓
PROVENIÊNCIA + IDEMPOTÊNCIA
      ↓
CÉREBRO
```

A fonte não define a estrutura interna do Projeto. O Projeto preserva a origem e organiza o conhecimento posteriormente.

## Preservação total

A automação deve preservar, quando disponível e autorizado:

- informação original;
- contexto;
- fonte e identidade de origem;
- tempo;
- conversa/sessão;
- decisões;
- entendimentos;
- mudanças de entendimento;
- descobertas;
- pesquisas;
- ações;
- resultados;
- erros;
- correções;
- experiências;
- aprendizados;
- sabedoria;
- relações;
- versões;
- evidências;
- motivos de mudança, substituição ou abandono.

Interpretação derivada nunca deve substituir silenciosamente o material original.

## Análise eficiente

A análise deverá evoluir para processamento incremental:

1. mapear fontes e artefatos;
2. identificar o que mudou;
3. analisar primeiro o conteúdo novo ou alterado;
4. reutilizar análises válidas;
5. agrupar informações relacionadas;
6. detectar relações, contradições, duplicações e lacunas;
7. aprofundar onde houver maior valor informacional ou multiplicador;
8. registrar o resultado no Cérebro;
9. permitir reprocessamento verificável.

O objetivo é reduzir trabalho repetido sem perder cobertura.

## Planejamento em rede

O runtime não deve transformar sinais em uma fila fixa. O tabuleiro continua sendo uma rede de caminhos.

Relações relevantes incluem:

`DEPENDE_DE`, `HABILITA`, `IMPULSIONA`, `MULTIPLICA_VALOR`, `CONVERGE_COM`, `ALIMENTA`, `VALIDA`, `QUESTIONA`, `CONTRADIZ`, `SUBSTITUI`, `REUTILIZA`, `REVELA` e `BLOQUEIA`.

Um resultado pode alterar vários caminhos ao mesmo tempo.

## Recuperação

O runtime deve sobreviver a interrupções por meio de estado persistente, identificação da execução, lease, heartbeat, idempotência e recuperação de trabalho incompleto.

```text
EXECUÇÃO
   ↓
INTERRUPÇÃO
   ↓
ESTADO PERSISTENTE
   ↓
RECUPERAÇÃO
   ↓
CONTINUAÇÃO SEGURA
```

Não se deve confundir recuperação técnica com garantia de que toda ação externa seja repetível. Efeitos externos precisam de idempotência ou mecanismos específicos de compensação.

## Autonomia

A autonomia aumenta conforme capacidade e validação aumentam, mas permanece limitada por política, permissões, risco, reversibilidade e evidência.

Ações de baixo risco podem ser automáticas. Ações de maior impacto devem ser escaladas conforme a política de execução.

## Múltiplas IAs

O runtime deve aceitar diferentes provedores e agentes sem transferir a propriedade do conhecimento para nenhum deles.

```text
                 CÉREBRO / SISTEMA
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
       IA A           IA B           IA C
          │             │             │
          └─────────────┼─────────────┘
                        ▼
                    RESULTADO
```

A substituição de uma IA não pode exigir reconstruir a história do Projeto.

## GitHub

GitHub permanece como uma engrenagem importante para código, documentação, versionamento, testes, workflows, evidências e controle de mudanças. O runtime definitivo pode usar infraestrutura persistente própria ou outros recursos compatíveis.

Não é objetivo transformar GitHub na identidade do Projeto nem criar dependência arquitetural desnecessária.

## Construção da própria capacidade

A meta será implementada enquanto é planejada. Cada ciclo de construção deve alimentar o Cérebro e melhorar a capacidade dos ciclos seguintes.

```text
CONSTRUIR O MECANISMO
        ↓
USAR O MECANISMO
        ↓
EXPERIÊNCIA REAL
        ↓
APRENDIZADO
        ↓
MELHORAR O MECANISMO
        ↺
```

## Critérios de maturidade

A meta só será considerada operacional em determinado nível quando houver evidência correspondente. Não basta o código existir.

### Nível 1 — Núcleo

- missão persistente;
- ciclo contextual;
- estado persistente;
- política de autonomia;
- recuperação básica;
- testes.

### Nível 2 — Execução persistente

- runtime hospedável;
- inicialização independente da interface;
- recuperação após interrupção;
- heartbeat/lease funcionando;
- observabilidade;
- reprocessamento idempotente.

### Nível 3 — Cérebro operacional

- captura contínua;
- organização automática;
- relações;
- histórico temporal;
- entendimentos e mudanças de entendimento;
- aprendizado e sabedoria vinculados à evidência.

### Nível 4 — Múltiplas fontes e IAs

- adaptadores independentes;
- entrada de fontes heterogêneas;
- múltiplos agentes/provedores;
- conflitos preservados;
- substituição de agente sem perda de continuidade.

### Nível 5 — Operação contínua evolutiva

- descoberta de novos caminhos;
- planejamento e execução mutuamente adaptativos;
- supervisão e auditoria;
- otimização incremental;
- capacidade de operar continuamente dentro das políticas e recursos disponíveis.

## Regra de não travamento

Nenhum nível acima deve congelar o Projeto. A experiência pode revelar uma arquitetura melhor, uma fonte nova, um mecanismo diferente ou uma necessidade que altere o próprio plano.

> Planejar sem transformar o planejamento em prisão.

## Estado desta meta

**ESTADO:** EM_CONSTRUCAO

**NATUREZA:** meta evolutiva de arquitetura e execução

**NÃO É:** especificação definitiva

**PRÓXIMA APLICAÇÃO:** usar a própria meta para orientar a auditoria, recuperação e consolidação dos repositórios e do Cérebro, enquanto a infraestrutura de execução persistente continua sendo fortalecida.
