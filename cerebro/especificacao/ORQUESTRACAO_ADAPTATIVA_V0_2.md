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
