# Simulação e Avaliação de Planos de Orquestração — V0.1

## Descoberta

A arquitetura já possui grafo, scheduler adaptativo, fuel, perfis de executores, replanejamento e geração de planos candidatos. A lacuna seguinte é avaliar alternativas antes de executar, inclusive sob perturbações, sem alterar o estado real.

Pesquisas recentes reforçam essa separação: OrchBench avalia planos de orquestração em simulação determinística e mede qualidade, makespan e custo; REALM-Bench avalia adaptação a perturbações dinâmicas.

## Modelo mínimo

Cada plano pode ser testado em cenários controlados:
- BASE
- execução mais lenta
- custo maior
- risco maior

A simulação não executa ferramentas nem altera tarefas reais.

## Resultado

Cada cenário produz:
- executabilidade
- makespan
- custo
- risco médio
- valor esperado
- robustez
- bloqueios

## Regra

SIMULAR → COMPARAR → ESCOLHER → EXECUTAR

A simulação é uma camada de decisão. A execução real continua responsável por efeitos externos, idempotência, autorização e histórico.

## Limites

A V0.1 não tenta prever o mundo real. Ela fornece uma avaliação determinística e substituível. A evolução deverá incluir:
1. caminho crítico
2. valor da informação
3. dependências suaves
4. disponibilidade real de executores
5. incerteza correlacionada
6. simulação Monte Carlo quando houver dados suficientes
7. comparação Pareto
8. calibração com resultados reais
