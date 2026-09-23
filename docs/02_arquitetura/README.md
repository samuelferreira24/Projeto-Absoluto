# Arquitetura — Projeto Absoluto

Esta é a área canônica da documentação arquitetural atual.

## O que pertence aqui

- arquitetura do ABS;
- contratos entre componentes;
- integração e transportes;
- roteamento de recursos;
- evolução controlada;
- descoberta/planejamento/aprendizagem de ferramentas quando descrevem capacidades arquiteturais;
- limites e responsabilidades entre componentes.

## O que não pertence aqui

- código-fonte: `abs_core/`;
- testes: `tests/`;
- operação passo a passo: `docs/01_operacao/`;
- planejamento estratégico: `docs/03_planejamento/` e `cerebro/mapas/`;
- histórico bruto: `docs/90_fontes/`, `mini-cerebro/`, `99_arquivo/`;
- continuidade de sessão: `continuidade/`.

## Autoridade

A documentação arquitetural descreve a intenção/contrato da arquitetura. Para saber o que realmente está funcionando, consultar código, testes, CI e evidências.

Quando houver divergência entre arquitetura documentada e implementação comprovada, registrar a divergência e corrigir a documentação ou o sistema conforme decisão autorizada.

## Relação

```
Projeto Absoluto
   ↓
Sistema — capacidade/infraestrutura
   ↓
ABS — primeiro projeto
   ↓
arquitetura
   ↓
código + testes + evidências
```

A arquitetura deve permanecer aberta para futuras versões do ABS e para projetos que reutilizem capacidades do Sistema.
