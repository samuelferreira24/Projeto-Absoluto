# ESTRUTURA ATUAL DO CÉREBRO V0.2

Data: 2026-09-17
Branch: `base-cerebro-v0.1`

## Finalidade

Esta é a fotografia estrutural atual do Cérebro. Ela substitui a descrição operacional da V0.1 como referência de estrutura atual, mas **não apaga nem invalida** a fotografia histórica V0.1.

## 1. Estrutura real

```text
cerebro/
├── núcleo e modelos
│   ├── nucleo.py
│   ├── modelos.py
│   ├── estado.py
│   ├── identidade.py
│   └── eventos.py / eventos_ledger.py
│
├── entrada e coleta
│   ├── ingestao.py
│   ├── coleta.py
│   ├── adaptador_dispatch.py
│   ├── processar_captura.py
│   └── analisador_documentos.py
│
├── conhecimento e memória
│   ├── registro.py
│   ├── conhecimento.py
│   ├── recuperacao.py
│   ├── semantica.py
│   ├── temporal.py
│   ├── rastreabilidade.py
│   ├── aprendizado.py
│   ├── consolidar_aprendizados.py
│   ├── sabedoria.py
│   ├── rede_evolutiva.py
│   └── memoria/
│       ├── aprendizados.jsonl
│       ├── aprendizados_fundamentais_v0_1.json
│       └── recuperacao_chat_2026-09-17.json
│
├── contexto e continuidade
│   ├── contexto_operacional.py
│   ├── continuidade.py
│   ├── interface_chat.py
│   └── especificacao/CONTINUIDADE_ENTRE_CHATS_V0_2.md
│
├── execução e operação
│   ├── executor.py
│   ├── politica.py
│   ├── politica_execucao.py
│   ├── runtime.py
│   ├── worker.py
│   ├── despertador.py
│   ├── github_controle.py
│   └── cli.py
│
├── planejamento e orquestração
│   ├── grafo_tarefas.py
│   ├── agendador.py
│   ├── composicao.py
│   ├── sinergia.py
│   ├── orquestrador.py
│   ├── orquestracao_adaptativa.py
│   ├── organizacao.py
│   └── recursos.py
│
├── especificação
│   └── contratos, arquitetura, mapas, método, memória,
│       continuidade, execução, economia, pesquisa e evolução
│
└── tests/
    └── validação unitária e de integração
```

## 2. Regra de separação

- `cerebro/*.py` = implementação da capacidade do Cérebro.
- `cerebro/especificacao/` = contratos, princípios, arquitetura, métodos, mapas e documentação normativa/analítica.
- `cerebro/memoria/` = dados persistidos de aprendizado e recuperação.
- `cerebro/data/conhecimento/` = base canônica persistente de conhecimento, com histórico versionado.
- `cerebro/tests/` = evidência automatizada da implementação.

Materiais históricos brutos do Projeto não devem ser confundidos com especificações atuais.

## 3. Estado de cada camada

### Núcleo
Responsável pela identidade dos registros, versionamento, estado e eventos.

### Entrada
Responsável por capturar e preservar fontes antes da interpretação.

### Memória
Responsável por armazenar conhecimento derivado, relações, temporalidade, experiência, aprendizado e sabedoria.

### Continuidade
Responsável por transportar o contexto de uma sessão para outra sem depender da memória interna de uma IA.

### Execução
Responsável por transformar missões autorizadas em ações observáveis e controladas.

### Planejamento/orquestração
Responsável por decomposição, dependências, seleção de tarefas, recursos, paralelismo, replanejamento, composição e investigação de sinergias.

## 4. Componentes com estado ainda não plenamente persistido

Os seguintes componentes precisam de evolução antes de serem considerados duráveis em toda a arquitetura:

- estado estrutural do `GrafoTarefas`;
- histórico e conhecimento de `DetectorSinergia`;
- integração automática da experiência de agendamento com a memória permanente;
- decisões do `OrquestradorAdaptativo`;
- recursos quantitativos e consumo real de combustível/capacidade;
- seleção de agentes/modelos/ferramentas como objetos persistentes de decisão.

## 5. Histórico versus estado atual

Arquivos V0.1 e versões anteriores permanecem para reconstrução histórica. Uma nova fotografia estrutural deve ser criada quando houver mudança arquitetural relevante, em vez de reescrever silenciosamente a história.

## 6. Fonte de autoridade

A estrutura deste arquivo descreve a organização física atual. A autoridade conceitual continua distribuída entre os documentos canônicos da especificação, os contratos, os registros de memória e as evidências de implementação.

A classificação de autoridade documental é mantida em `cerebro/especificacao/INDICE_ARQUITETURA_E_ACERVO_V0_1.md`.


## 7. Reavaliação sistêmica — ciclo de 2026-09-18

A auditoria desta etapa mostrou que o núcleo de orquestração já ultrapassou o estágio de simples grafo + scheduler. Há agora runtime recuperável, controle de execução, identidade de agentes, política de autonomia, telemetria, simulação, sinergia e persistência.

A lacuna de maior valor encontrada nesta etapa foi a fronteira entre **decisão** e **autoridade de execução**. Foram reforçados:

- aprovação vinculada à ação, ferramenta, recurso, custo, cadeia e validade;
- consumo único da aprovação;
- serialização interprocessos dos claims;
- persistência atômica do controle de execução;
- reconciliação que devolve tarefas com claim expirado ao estado recuperável;
- registro do aprendizado gerado pela descoberta.

A arquitetura atual passa a tratar segurança como uma camada transversal da execução, e não apenas como uma propriedade do agente.

## 8. Próximas lacunas prioritárias

As próximas lacunas identificadas, sem ordem definitiva de implementação, são:

1. autoridade de origem e confiança da memória;
2. proteção contra memory poisoning e conteúdo externo malicioso;
3. assinatura/autenticação de mensagens entre agentes;
4. circuit breakers e limites distribuídos de custo/retry;
5. persistência compartilhada para operação distribuída;
6. avaliação adversarial automatizada;
7. seleção persistente de modelos, ferramentas e agentes;
8. integração entre resultados de pesquisa e planejamento;
9. descoberta automática de novos caminhos a partir de resultados;
10. observabilidade de ponta a ponta.

A prioridade deve continuar sendo recalculada pelo valor, dependências desbloqueadas, risco e capacidade de multiplicação.
