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
