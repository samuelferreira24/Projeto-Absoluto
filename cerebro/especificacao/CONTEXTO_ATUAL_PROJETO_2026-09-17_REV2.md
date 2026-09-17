# CONTEXTO ATUAL — PROJETO ABSOLUTO — REV2

Data: 2026-09-17
Branch de construção: `base-cerebro-v0.1`
Commit de referência desta revisão: após a auditoria integral do acervo e organização.

## 1. Ponto atual

O Cérebro já possui uma base ampla de memória, ingestão, recuperação, semântica, temporalidade, continuidade, execução, recursos, rede evolutiva, composição, grafo de tarefas, agendamento adaptativo e detecção inicial de sinergias.

Antes de ampliar indiscriminadamente as capacidades, foi realizada uma varredura profissional para verificar se o patrimônio estava preservado e organizado.

## 2. Resultado da auditoria

Foram identificados:

- conteúdo textual indevidamente armazenado em quatro `.gitkeep`;
- duas referências MHT com o mesmo blob;
- uma visão geral histórica que não deve orientar a arquitetura atual;
- uma fotografia estrutural V0.1 que não corresponde mais à árvore real;
- várias especificações de agendamento/orquestração que precisam de classificação de autoridade;
- uma implementação paralela de orquestração adaptativa não integrada à fachada principal;
- sinergias ainda sem persistência;
- grafo de tarefas ainda sem persistência estrutural completa;
- experiência do agendamento ainda sem consolidação automática na memória permanente;
- descoberta de combinações ainda limitada, nesta camada, principalmente a pares.

Nenhum patrimônio foi apagado para realizar essa organização.

## 3. Nova organização documental

O índice `INDICE_ARQUITETURA_E_ACERVO_V0_1.md` passa a registrar a função dos principais documentos e a diferença entre material canônico, ativo, experimental, histórico, fonte bruta, derivado e migração pendente.

`ESTRUTURA_ATUAL_V0_2.md` representa a árvore física atual do Cérebro.

`AUDITORIA_INTEGRAL_ACERVO_E_ORGANIZACAO_V0_1.md` preserva os achados da varredura.

## 4. Regra de preservação

O Projeto deve preservar fontes, decisões, erros, descobertas, progresso, entendimentos e mudanças de entendimento.

Organizar não significa apagar. A evolução deve tornar o patrimônio mais encontrável e contextualizado.

## 5. Próximo trabalho técnico

A próxima evolução de maior valor é tornar a orquestração realmente durável e aprendível:

```text
TAREFAS
  ↓
GRAFO PERSISTENTE
  ↓
AGENDAMENTO
  ↓
EXECUÇÃO
  ↓
RESULTADOS
  ↓
SINERGIAS
  ↓
EXPERIÊNCIA
  ↓
MEMÓRIA PERMANENTE
  ↓
MELHOR ORQUESTRAÇÃO
  ↺
```

Prioridades:

1. persistência/versionamento do grafo de tarefas;
2. persistência da memória de sinergias;
3. unificação das responsabilidades entre `agendador.py` e `orquestracao_adaptativa.py`;
4. integração da experiência de agendamento ao aprendizado permanente;
5. recursos quantitativos e consumo real de combustível/capacidade;
6. caminho crítico, custo de comunicação e otimização multiobjetivo;
7. geração e avaliação de combinações com mais de dois fatores;
8. seleção persistente de agentes, modelos e ferramentas;
9. reconciliação dos materiais históricos ainda não extraídos.

## 6. Continuidade

A construção permanece exclusivamente em `base-cerebro-v0.1`. A `main` não deve ser modificada por esta fase e o PR #2 permanece sem merge automático.

O histórico anterior continua preservado no Git. Esta revisão não substitui as fotografias anteriores; acrescenta uma fotografia mais atual do entendimento do Projeto.
