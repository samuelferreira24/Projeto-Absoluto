# Orquestração Adaptativa e Replanejamento V0.2

## Evidências

- TPS-Bench (ACL 2026) mostra que planejamento de ferramentas precisa avaliar conclusão e eficiência; estratégias sequenciais e paralelas têm trade-offs. 
- REALM-Bench (KDD 2026) avalia dependências, linhas paralelas e interrupções dinâmicas que exigem adaptação em tempo real.
- Agent JIT Compilation (ICML 2026) gera múltiplos planos, valida candidatos e explora paralelização antes de selecionar uma execução.
- Pesquisas de alocação dinâmica multiagente tratam tarefas online, incerteza, deadlines e mudanças de recursos.
- Planejamento híbrido LLM + programação por restrições reforça separar interpretação/decomposição semântica de scheduling verificável.

## Decisão

Um plano é uma hipótese operacional. O Cérebro deve gerar alternativas, comparar objetivos e replanejar sem apagar a história.

OBJETIVO → GRAFO → PLANOS CANDIDATOS → VALIDAÇÃO → SELEÇÃO → EXECUÇÃO → OBSERVAÇÃO → DESVIO → REPLANEJAMENTO → APRENDIZADO.

A V0.2 adiciona:
- estratégias de eficiência, conclusão, rapidez e equilíbrio;
- geração de planos candidatos;
- seleção explícita entre alternativas;
- registro das alternativas consideradas;
- motivo e mudanças que provocaram replanejamento.

Próximas camadas:
- orçamento de combustível;
- capacidades e motores como recursos selecionáveis;
- precondições e pós-condições;
- fallback e recuperação;
- estimativas probabilísticas de duração;
- aprendizagem da política de scheduling;
- descoberta de sinergias;
- meta-orquestração.

## 6. Consolidacao arquitetural

A implementacao confirmou que manter dois motores independentes de selecao criaria risco de divergencia. O AgendadorAdaptativo passa a ser o scheduler canonico; o OrquestradorAdaptativo permanece como fachada de compatibilidade e coordenacao.

## 7. Modelo de tarefa ampliado

A tarefa agora pode registrar, alem de dependencia, prioridade, custo, tempo, risco e prazo:

- restricoes;
- oportunidade;
- incerteza;
- custo estimado de comunicacao;
- fallbacks.

Dependencia obrigatoria e resolvida pelo grafo. Preferencia e tratada como sinal suave. Restricoes podem ser validadas por uma funcao externa. Recursos podem possuir capacidade de concorrencia maior que um.

## 8. Valor esperado e experiencia

A pontuacao passou a considerar valor, oportunidade, risco, incerteza, confiabilidade historica, custo, tempo, urgencia e comunicacao. Isso transforma resultados de execucoes anteriores em informacao operacional para o proximo planejamento.

## 9. Falha e recuperacao

Falhas agora podem produzir registros de retry e ativacao de fallback sem apagar a experiencia anterior. O replanejamento registra motivo, mudancas e estrategia escolhida.

## 10. Integracao com aprendizagem

Resultados de execucao e mudancas de estrategia podem ser registrados no sistema de aprendizado existente. A camada episodica permanece preservada; a consolidacao continua sendo uma etapa separada e controlada.

## 11. Pesquisa adicional incorporada

Pesquisas recentes reforcam a necessidade de tratar planejamento como processo adaptativo, nao como ordem fixa. TPS-Bench avalia simultaneamente sucesso e eficiencia de scheduling; trabalhos recentes sobre memoria mostram que experiencias devem alimentar melhoria continua, mas que consolidacao automatica pode degradar conhecimento se substituir evidencia bruta.

## 12. Limitacoes deliberadas

A V0.2 ainda nao executa agentes reais, nao resolve otimizacao global e nao infere causalidade de sinergias. Essas capacidades ficam preparadas para camadas posteriores. O objetivo desta etapa e criar uma base verificavel para planejamento adaptativo sem introduzir complexidade artificial.
