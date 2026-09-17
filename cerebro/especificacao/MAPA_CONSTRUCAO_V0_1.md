# Mapa da Construção — V0.1

## Finalidade

O Mapa da Construção registra o estado necessário para que a construção do Projeto Absoluto possa continuar por diferentes IAs, pessoas e ferramentas sem depender da memória de uma conversa específica.

## Princípio

> O conhecimento de como construir o Projeto pertence ao Projeto.

Uma IA pode executar uma etapa, mas não deve ser a única portadora das informações necessárias para continuar a construção.

## Unidade de construção

Cada componente, capacidade ou unidade de trabalho relevante deve possuir, quando aplicável:

```text
ID
NOME
OBJETIVO
REQUISITOS
CAPACIDADE ATENDIDA
DEPENDÊNCIAS
INTERFACES / CONTRATOS
ESTADO
IMPLEMENTAÇÃO
TESTES
EVIDÊNCIAS
PROBLEMAS
DECISÕES RELACIONADAS
ÚLTIMA VALIDAÇÃO
PRÓXIMA AÇÃO
CRITÉRIO DE CONCLUSÃO
VERSÃO
```

## Estados de construção

```text
NÃO_INICIADO
EM_PLANEJAMENTO
EM_CONSTRUÇÃO
EM_TESTE
EM_VALIDAÇÃO
VALIDADO
BLOQUEADO
SUPERADO
ARQUIVADO
```

Estado de construção não significa certeza sobre o funcionamento. A validação deve possuir evidência própria.

## Relações estruturais

O mapa deve distinguir relações de construção de relações de conhecimento.

Relações estruturais iniciais:

- `ATENDE_REQUISITO`
- `IMPLEMENTA_CAPACIDADE`
- `DEPENDE_DE`
- `PARTE_DE`
- `INTEGRA_COM`
- `SUBSTITUI`
- `BLOQUEIA`
- `VALIDA`
- `GERA_EVIDENCIA`

## Continuidade entre agentes

Antes de assumir uma tarefa, o agente deve conseguir consultar:

```text
VISÃO
  ↓
ARQUITETURA
  ↓
MAPA
  ↓
ESTADO
  ↓
DECISÕES
  ↓
CONTRATOS
  ↓
CÓDIGO / ARTEFATOS
  ↓
TESTES
  ↓
PROBLEMAS
  ↓
EVIDÊNCIAS
```

Ao terminar, deve produzir um estado de transferência:

```text
O QUE FOI FEITO
O QUE FOI TESTADO
O QUE FUNCIONOU
O QUE NÃO FUNCIONOU
O QUE FOI DESCOBERTO
DECISÕES TOMADAS
PROBLEMAS ENCONTRADOS
HIPÓTESES ABERTAS
DEPENDÊNCIAS
RISCOS
O QUE NÃO DEVE SER ALTERADO
PRÓXIMA AÇÃO
EVIDÊNCIAS
```

## Regra contra perda de contexto

Nenhuma informação essencial para continuar a construção deve existir somente em uma conversa, conta ou memória privada de uma IA.

Quando uma decisão, descoberta, problema ou aprendizado alterar o estado de construção, ele deve ser registrado nos artefatos apropriados do Projeto.

## Relação com o Cérebro

O Mapa da Construção não substitui o Cérebro.

- O Mapa responde principalmente **como a construção está organizada e em que estado ela se encontra**.
- O Cérebro preserva **fontes, conhecimento, experiência, evidências, decisões e aprendizados**.
- O repositório preserva os artefatos versionados de implementação e documentação.
- O controle operacional acompanha execução e trabalho.

Essas camadas devem se relacionar sem se tornarem uma única estrutura rígida.

## Ciclo

```text
MAPA
  ↓
PRÓXIMA AÇÃO
  ↓
EXECUÇÃO
  ↓
TESTE
  ↓
VALIDAÇÃO
  ↓
EVIDÊNCIA
  ↓
ATUALIZAÇÃO DO ESTADO
  ↓
ATUALIZAÇÃO DO MAPA
  ↓
NOVA AÇÃO
```

## Integridade

O mapa não deve declarar um componente como validado apenas porque código foi criado ou um teste superficial passou.

A validação deve considerar a necessidade que o componente deveria atender e evidência suficiente para o contexto.

## Evolução

O mapa é versionado. Alterações relevantes devem preservar histórico e motivo.

O objetivo não é produzir um desenho perfeito antecipadamente, mas manter um modelo suficientemente fiel para orientar a próxima etapa e permitir reconstrução da trajetória.
