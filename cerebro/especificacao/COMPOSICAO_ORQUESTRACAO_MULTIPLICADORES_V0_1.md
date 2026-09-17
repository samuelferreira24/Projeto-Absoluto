# COMPOSIÇÃO E ORQUESTRAÇÃO DE MULTIPLICADORES — V0.1

## 1. Objetivo

Definir uma capacidade arquitetural para que o Projeto Absoluto deixe de utilizar capacidades importantes apenas de forma serial e passe a descobrir, planejar, executar, medir e aprender combinações de capacidades em paralelo ou em sequência conforme as dependências do problema.

O objetivo não é simplesmente executar mais coisas ao mesmo tempo. É aprender **quais combinações de fatores produzem melhores resultados**, em quais condições, com quais custos e com quais dependências.

## 2. Problema identificado

O Projeto possui ou pretende possuir múltiplos fatores multiplicadores: pesquisa, memória, experiência, aprendizado, múltiplas IAs, ferramentas, dados, histórico, conhecimento, automação, computação, recursos, planejamento, feedback e outros.

A limitação atual é de composição: possuir vários fatores não significa conseguir utilizá-los conjuntamente.

Modelo limitado:

```text
FATOR A → executa → FATOR B → executa → FATOR C
```

Modelo desejado:

```text
OBJETIVO
   ↓
MAPEAMENTO DE CAPACIDADES
   ↓
DECOMPOSIÇÃO DINÂMICA
   ↓
DEPENDÊNCIAS
   ├── tarefa A ──┐
   ├── tarefa B ──┼── execução paralela quando possível
   ├── tarefa C ──┘
   ↓
SÍNTESE
   ↓
RESULTADO
   ↓
MEDIÇÃO
   ↓
APRENDIZADO
   ↓
NOVA COMBINAÇÃO / NOVA CAPACIDADE
```

## 3. Evidência externa pesquisada

A pesquisa atual converge para arquiteturas com decomposição dinâmica, grafos de tarefas, execução assíncrona/paralela, compartilhamento semântico de contexto, escalonamento e adaptação em tempo de execução.

- DynTaskMAS descreve um grafo dinâmico de tarefas, motor de execução paralela assíncrona, gerenciamento de contexto e workflow adaptativo. A publicação de 2026 reporta redução de 21,3–33,0% no tempo de execução, aumento de utilização de recursos de 65% para 88% e ganho de throughput com múltiplos agentes. Isso não prova que o mesmo ganho ocorrerá no Projeto Absoluto, mas confirma que a composição paralela é uma linha técnica concreta de pesquisa. 
- Para orquestração de agentes e ferramentas, trabalhos de 2026 investigam um orquestrador capaz de tratar agentes e ferramentas como ações componíveis, com decomposição paralela, delegação e execução assíncrona.
- Pesquisas de 2025 sobre planejamento orientado a agentes tratam um meta-agente como camada de decomposição, alocação, avaliação e ajuste das subtarefas.
- Pesquisas de alocação de recursos mostram que capacidades explícitas dos trabalhadores/agentes ajudam o planejador a distribuir tarefas considerando custo, eficiência e desempenho.
- Trabalhos anteriores sobre interação multiagente demonstraram que estratégias e formas de uso de ferramentas podem emergir da interação entre agentes, indicando que combinações não precisam ser todas previamente programadas.

## 4. Princípio arquitetural

> **Os multiplicadores devem ser tratados como capacidades componíveis, e não como módulos isolados.**

Cada capacidade deve possuir, quando aplicável:

- capacidade oferecida;
- requisitos;
- recursos consumidos;
- custo estimado;
- tempo estimado;
- latência;
- confiabilidade histórica;
- dependências;
- incompatibilidades;
- entradas;
- saídas;
- efeitos colaterais;
- contexto necessário;
- nível de autonomia permitido;
- evidências de desempenho;
- combinações conhecidas;
- combinações ainda não testadas.

## 5. Grafo de composição

A unidade de planejamento deve poder ser representada como um grafo:

```text
                  OBJETIVO
                     │
             ┌───────┴───────┐
             ↓               ↓
          PESQUISA         MEMÓRIA
             │               │
             └───────┬───────┘
                     ↓
                  ANÁLISE
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
         IA-A       IA-B     FERRAMENTA
          └──────────┼──────────┘
                     ↓
                  SÍNTESE
                     ↓
                  TESTE
                     ↓
                 RESULTADO
```

As arestas representam dependências, transferência de contexto ou restrições. Os nós representam tarefas/capacidades/recursos.

## 6. Paralelo versus sequência

Uma tarefa pode ser executada em paralelo quando:

1. não depende da saída de outra tarefa;
2. não existe conflito de recurso;
3. o contexto necessário pode ser disponibilizado;
4. a execução simultânea não reduz a qualidade de maneira inaceitável;
5. os efeitos colaterais são controláveis.

Uma tarefa deve permanecer sequencial quando existe dependência causal, necessidade de validação anterior, conflito de recurso, estado compartilhado crítico ou outra restrição que torne a simultaneidade inadequada.

Portanto, o sistema não deve assumir “tudo paralelo” nem “tudo serial”. Deve **descobrir a topologia apropriada**.

## 7. Descoberta de sinergias

O Projeto deve registrar combinações testadas.

```text
COMBINAÇÃO
   ↓
CONTEXTO
   ↓
OBJETIVO
   ↓
RECURSOS
   ↓
EXECUÇÃO
   ↓
RESULTADO
   ↓
CUSTO / TEMPO / QUALIDADE
   ↓
COMPARAÇÃO COM BASELINE
   ↓
APRENDIZADO
```

Uma combinação pode receber estados como:

- NÃO_TESTADA
- TESTADA
- PROMISSORA
- VALIDADA
- INEFICIENTE
- INCOMPATÍVEL
- CONTEXTUAL
- SUPERADA

Esses estados não são verdades permanentes; devem possuir evidência e contexto.

## 8. Descoberta de novos multiplicadores

O sistema deve procurar não apenas melhorar fatores existentes, mas identificar quando uma combinação cria uma capacidade que não existia como unidade independente.

```text
A + B → capacidade C

A + B + C → capacidade D
```

Uma nova capacidade só deve ser promovida como conhecimento consolidado depois de observação, registro, comparação e, quando possível, repetição/validação.

## 9. Meta-orquestração

A camada de orquestração também deve ser objeto de aprendizado.

O Meta-Cérebro deve poder aprender:

- quais decomposições funcionam;
- quais agentes são adequados para cada tipo de tarefa;
- quando paralelizar;
- quando serializar;
- quando adicionar um auditor;
- quando buscar uma segunda opinião;
- quando utilizar memória antes da pesquisa;
- quando pesquisar antes de decidir;
- quando executar experimentos concorrentes;
- quando interromper uma linha;
- quando combinar resultados;
- quanto recurso alocar;
- quando uma combinação merece ser testada novamente.

## 10. Memória de sinergias

O Cérebro deve futuramente possuir uma representação de **experiências de composição** contendo pelo menos:

```text
id
objetivo
capacidades_utilizadas
ordem/topologia
paralelismo
contexto
recursos
restrições
resultado
qualidade
custo
tempo
confiabilidade
evidencias
combinações_relacionadas
aprendizado
status
versao
```

Isso transforma experiências isoladas em conhecimento reutilizável.

## 11. Ciclo permanente

```text
OBJETIVO
  ↓
MAPEAR CAPACIDADES
  ↓
GERAR PLANOS / COMBINAÇÕES
  ↓
AVALIAR DEPENDÊNCIAS E RECURSOS
  ↓
EXECUTAR PARALELO / SEQUENCIAL
  ↓
OBSERVAR
  ↓
MEDIR
  ↓
COMPARAR
  ↓
CONSOLIDAR
  ↓
APRENDER
  ↓
ATUALIZAR MEMÓRIA DE COMPOSIÇÃO
  ↓
GERAR NOVAS COMBINAÇÕES
  ↺
```

## 12. Relação com o Cérebro V0.1

Esta especificação não substitui a memória existente. Ela adiciona uma nova dimensão ao aprendizado: não apenas **o que o sistema sabe**, mas **como capacidades diferentes podem ser combinadas para produzir resultados**.

O histórico, os erros, as descobertas e as mudanças de entendimento continuam sendo preservados. A arquitetura atual também não deve ser limitada por protótipos antigos.

## 13. Próxima etapa de implementação

Não implementar ainda um orquestrador complexo.

Primeiro criar uma representação mínima e observável de:

1. capacidade;
2. tarefa;
3. dependência;
4. recurso;
5. combinação;
6. execução;
7. resultado;
8. evidência;
9. aprendizado de composição.

Depois criar testes pequenos para demonstrar:

- duas tarefas independentes executadas em paralelo;
- duas tarefas dependentes executadas em sequência;
- conflito de recurso impedindo paralelismo;
- falha de uma subtarefa e replanejamento;
- registro do resultado da combinação;
- recuperação posterior da experiência de composição.

Somente depois disso deve-se evoluir para seleção dinâmica de agentes, alocação de recursos e descoberta automática de novas combinações.

## 14. Fontes principais da pesquisa

- DynTaskMAS / ICAPS: https://ojs.aaai.org/index.php/ICAPS/article/view/36130
- DynTaskMAS / arXiv: https://arxiv.org/abs/2503.07675
- ParaManager / Master Orchestrator: https://arxiv.org/abs/2604.17009
- Self-Resource Allocation: https://arxiv.org/abs/2504.02051
- Agent-Oriented Planning: https://proceedings.iclr.cc/paper_files/paper/2025/hash/31610e68fe41a62e460e044216a10766-Abstract-Conference.html
- Multi-Agent Coordination Survey: https://arxiv.org/abs/2502.14743
- Emergent Tool Use: https://openai.com/index/emergent-tool-use/

## 15. Princípio de fechamento

> **O próximo multiplicador do Projeto Absoluto pode não ser uma nova ferramenta. Pode ser a capacidade de combinar inteligentemente as ferramentas e capacidades que já possui.**

Essa capacidade deve aprender com cada combinação executada e transformar os resultados em conhecimento reutilizável.

## 16. Autonomia sob controle do proprietário

> **Autonomia não significa perda de controle. O Projeto Absoluto deve poder operar, pesquisar, planejar, executar, aprender, replanejar e otimizar autonomamente dentro dos limites, permissões e objetivos definidos pelo proprietário.**

A autonomia deve ser governável. O proprietário mantém autoridade sobre:

- objetivos e prioridades fundamentais;
- permissões e limites de atuação;
- recursos e orçamento de combustível;
- capacidades e ferramentas autorizadas;
- níveis de risco aceitáveis;
- ações que exigem aprovação humana;
- critérios de interrupção, suspensão e retomada;
- mudanças estruturais de alto impacto;
- acesso, compartilhamento e retenção de conhecimento;
- auditoria, histórico e rastreabilidade.

O sistema pode decidir **como** executar uma tarefa dentro desses limites, inclusive escolhendo caminhos alternativos, paralelizando tarefas, replanejando após resultados e aprendendo estratégias melhores. Isso não transfere a autoridade sobre **o que é permitido fazer** para o sistema.

O controle deve ser exercido por uma camada explícita de governança, com permissões, políticas, orçamento, observabilidade, registro de decisões e mecanismos de intervenção. Uma decisão autônoma deve permanecer rastreável: objetivo, contexto, capacidades utilizadas, recursos consumidos, decisão tomada, resultado e motivo de eventual replanejamento.

Assim, o modelo desejado é:

```text
PROPRIETÁRIO
     ↓
OBJETIVOS + LIMITES + PERMISSÕES
     ↓
AUTONOMIA OPERACIONAL
     ↓
PLANEJAR → EXECUTAR → OBSERVAR → APRENDER → REPLANEJAR
     ↺
     ↓
PRESTAÇÃO DE CONTAS / AUDITORIA
     ↓
PROPRIETÁRIO
```

A autonomia é, portanto, uma **capacidade de operação**, e não uma transferência de soberania.
