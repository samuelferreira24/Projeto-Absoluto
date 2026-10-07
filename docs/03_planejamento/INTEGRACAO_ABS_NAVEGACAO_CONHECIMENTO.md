# Integração ABS + Navegação de Conhecimento Verificável

## Objetivo

A Navegação de Conhecimento Verificável é uma capacidade de suporte do ABS. Ela não é o cérebro, o orquestrador nem um sistema que deve ser expandido indefinidamente.

A integração estabelece o contrato:

`Imperador → ABS → capability knowledge-navigation → fontes/evidências → ABS`

## Limites

- A navegação permanece independente do ABS.
- O ABS apenas consome sua capacidade por contrato.
- A navegação não decide objetivos, prioridades ou execução.
- Cobertura, indexação e verificação pertencem à infraestrutura de navegação.
- Evoluções futuras da navegação só devem ocorrer quando exigidas por uma capacidade real do ABS.

## Contrato

A capability `knowledge-navigation` aceita uma operação e contexto e devolve um envelope `knowledge_navigation`, preservando proveniência e evidências.

Operações suportadas na integração:
- `search`
- `symbols`
- `inspect`
- `investigate`
- `coverage`
- `verify`

Endpoint de integração:
`POST /knowledge/navigation`

## Estado de fechamento desta etapa

A integração deve ser considerada concluída quando:
1. a capability estiver registrada no runtime;
2. o endpoint estiver operacional;
3. testes do contrato passarem;
4. a validação real dos dois repositórios continuar passando;
5. o fluxo de orquestração puder selecionar a capability quando conhecimento/evidência for necessário.

Depois disso, o trabalho deve avançar para o próximo gargalo do ABS, em vez de ampliar a navegação por si mesma.
