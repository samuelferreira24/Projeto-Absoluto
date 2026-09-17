# PROTOCOLO DE OTIMIZAÇÃO CONTÍNUA — V0.1

## Objetivo

Estabelecer como o Projeto Absoluto deve trabalhar para que boas ideias não sejam apenas executadas: elas devem ser pesquisadas, comparadas, testadas, otimizadas e incorporadas quando houver evidência de melhoria.

## Princípio

> Toda ideia relevante é uma hipótese de melhoria até ser confrontada com conhecimento externo, experiência interna, alternativas e evidências.

Pesquisa não é uma etapa isolada. Pode ocorrer antes, durante e depois da execução.

## Ciclo

```text
IDEIA / PROBLEMA
      ↓
PESQUISA INICIAL
      ↓
ALTERNATIVAS
      ↓
ANÁLISE DE TRADE-OFFS
      ↓
DECISÃO DE IMPLEMENTAÇÃO
      ↓
EXECUÇÃO
      ↓
PESQUISA DURANTE A EXECUÇÃO
      ↓
TESTE / EVIDÊNCIA
      ↓
RESULTADO
      ↓
AUDITORIA
      ↓
PESQUISA PÓS-RESULTADO
      ↓
OTIMIZAÇÃO
      ↓
NOVA VALIDAÇÃO
      ↓
APRENDIZADO
      ↓
REGISTRO
      ↺
```

## Quando pesquisar

### Antes
Pesquisar para:

- verificar se a ideia já existe;
- encontrar abordagens mais maduras;
- identificar padrões e arquiteturas relevantes;
- descobrir riscos conhecidos;
- comparar alternativas;
- evitar construir novamente algo inferior;
- identificar critérios de avaliação;
- estimar custos e complexidade.

### Durante
Pesquisar para:

- resolver bloqueios;
- validar decisões de implementação;
- comparar soluções descobertas no caminho;
- acompanhar mudanças tecnológicas;
- encontrar evidências melhores;
- detectar que a estratégia escolhida deixou de ser a melhor disponível para aquele objetivo;
- corrigir o rumo antes de acumular trabalho desnecessário.

### Depois
Pesquisar para:

- comparar o resultado com práticas externas;
- procurar explicações para falhas e desvios;
- identificar melhorias;
- verificar se a solução continua atual;
- descobrir usos que não foram considerados;
- transformar a experiência em lição e, quando sustentada, sabedoria aplicada.

## Regra de eficiência

Pesquisar não significa pesquisar tudo indiscriminadamente. A profundidade deve ser proporcional ao impacto da decisão.

### Baixo impacto

Pesquisa rápida + implementação + teste.

### Médio impacto

Múltiplas fontes + alternativas + trade-offs + teste.

### Alto impacto

Pesquisa aprofundada + fontes primárias quando disponíveis + alternativas + riscos + validação independente + evidência operacional + revisão posterior.

## Critério de otimização

Uma otimização deve melhorar pelo menos um dos seguintes fatores sem degradar de forma inaceitável os demais:

- qualidade;
- confiabilidade;
- segurança;
- rastreabilidade;
- continuidade;
- portabilidade;
- desempenho;
- custo;
- simplicidade;
- manutenção;
- capacidade de evolução;
- capacidade de aprendizado.

## Evitar otimização local

Uma melhoria em um componente não deve ser considerada automaticamente uma melhoria do Projeto.

Sempre que relevante, avaliar:

```text
MELHORIA LOCAL
      ↓
IMPACTO NO COMPONENTE
      ↓
IMPACTO NAS INTERFACES
      ↓
IMPACTO NO SISTEMA
      ↓
IMPACTO NO PROJETO
```

Uma solução mais rápida, por exemplo, pode reduzir rastreabilidade ou aumentar dependência de fornecedor. O trade-off deve ser registrado.

## Comparação de alternativas

Quando existirem alternativas plausíveis, registrar:

- objetivo;
- alternativas consideradas;
- critérios;
- evidências;
- riscos;
- custos;
- dependências;
- reversibilidade;
- decisão;
- motivo da decisão;
- condições que fariam a decisão ser revista.

## Validação

Nenhuma melhoria relevante deve ser considerada incorporada apenas porque parece melhor.

O mínimo esperado é:

1. implementação;
2. teste;
3. evidência;
4. comparação com o estado anterior ou critério definido;
5. registro do resultado.

Para mudanças de maior impacto, acrescentar revisão independente, experimento controlado ou validação por múltiplos métodos quando viável.

## Aprendizado

Cada ciclo deve produzir, quando aplicável:

- resultado;
- erro;
- experiência;
- lição aprendida;
- hipótese de melhoria;
- sabedoria aplicada.

A experiência permanece ligada às evidências e ao contexto que a produziu.

## Pesquisa como capacidade permanente

O Projeto deve poder pesquisar continuamente:

- novas tecnologias;
- novos métodos;
- novas arquiteturas;
- novas ferramentas;
- novos riscos;
- novas evidências;
- mudanças nas plataformas externas;
- resultados obtidos pelo próprio Projeto.

A pesquisa externa complementa, mas não substitui, a experiência interna.

## Independência de fornecedor

Uma pesquisa pode descobrir uma tecnologia superior. Isso não significa que o Projeto deva se tornar dependente dela imediatamente.

Antes de incorporar uma tecnologia externa, avaliar:

- portabilidade;
- custo de troca;
- lock-in;
- disponibilidade;
- estabilidade;
- segurança;
- capacidade de exportação;
- impacto sobre a identidade do Projeto.

## Registro mínimo de uma otimização

```text
OTIMIZACAO
- id
- problema_ou_oportunidade
- ideia_original
- pesquisa_realizada
- alternativas
- criterios
- decisao
- implementacao
- evidencias
- resultado
- tradeoffs
- riscos
- aprendizado
- condicao_de_revisao
```

## Regra final

> Não basta ter uma boa ideia. O Projeto deve tentar descobrir se existe uma ideia melhor, testar a escolhida, observar o resultado e aprender com o processo.

Esse protocolo transforma pesquisa em parte do mecanismo de evolução do Projeto, e não em uma atividade separada.