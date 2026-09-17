# Orquestração Adaptativa e Composição V0.1

## Objetivo
Transformar o grafo de tarefas em um sistema que escolhe combinações de trabalho de acordo com valor, custo, risco, prazo, tempo, recursos e resultados observados.

## Princípios
- dependências são restrições reais;
- recursos compartilhados impedem paralelismo quando há conflito;
- orçamento e tempo são limites explícitos;
- o plano é uma decisão contextual, não uma rota permanente;
- resultados alteram o próximo plano;
- falhas são preservadas como experiência e não apagadas;
- combinações devem ser medidas contra resultados individuais;
- sinergias descobertas tornam-se conhecimento reutilizável;
- o histórico registra por que uma decisão foi tomada.

## Ciclo
```text
OBJETIVO
  ↓
DECOMPOSIÇÃO
  ↓
GRAFO DE TAREFAS
  ↓
SELEÇÃO ADAPTATIVA
  ↓
EXECUÇÃO
  ↓
RESULTADO
  ↓
MEDIÇÃO
  ↓
SINERGIA / FALHA / APRENDIZADO
  ↓
REPLANEJAMENTO
  ↺
```

## Evolução futura
O V0.1 é uma base determinística. As próximas camadas podem aprender pesos, estimar incerteza, incorporar disponibilidade real de motores e combustível, considerar custo de comunicação, formar equipes dinamicamente, testar topologias alternativas e permitir que o Meta-Cérebro aprenda políticas de orquestração.
