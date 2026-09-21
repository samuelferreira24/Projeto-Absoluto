# Mecanismo de Descoberta e Reavaliação V0.1

## Finalidade

O Projeto Absoluto deve ser capaz de descobrir, durante a própria construção, que faltam capacidades, requisitos, evidências, relações ou caminhos que não estavam previstos inicialmente.

O planejamento é uma representação provisória do conhecimento atual. A execução pode revelar lacunas novas. Essas lacunas devem retroalimentar o Cérebro, o Tabuleiro, o Estado, o Método e a arquitetura.

## Princípio central

> Descobertas podem alterar a percepção do progresso. Reavaliar não é retroceder; é atualizar o mapa com evidência melhor.

## O ciclo

```text
PLANEJAMENTO
    ↓
EXECUÇÃO
    ↓
OBSERVAÇÃO
    ↓
DESCOBERTA
    ↓
┌───────────────────────────────┐
│ algo está faltando?           │
│ algo foi superestimado?       │
│ surgiu nova dependência?      │
│ apareceu novo risco?          │
│ existe nova oportunidade?     │
│ a validação ainda é suficiente?│
└───────────────┬───────────────┘
                ↓
             PESQUISA
                ↓
           REAVALIAÇÃO
                ↓
      CÉREBRO + TABULEIRO
                ↓
        NOVO PLANEJAMENTO
                ↺
```

## Dimensões que devem ser reavaliadas

- estado real;
- evidências disponíveis;
- requisitos conhecidos;
- requisitos descobertos;
- dependências;
- riscos;
- lacunas;
- qualidade da validação;
- cobertura de testes;
- integração;
- portabilidade;
- segurança;
- continuidade;
- valor multiplicador;
- caminhos alternativos;
- aprendizados e sabedoria operacional.

## Progresso revisável

O progresso deve ser calculado a partir do que está efetivamente demonstrado, não apenas do que foi implementado ou planejado.

Uma frente pode estar:

- planejada;
- implementada;
- testada;
- verificada;
- validada;
- operacional;
- observada em uso;
- aprendida com a experiência;
- reavaliada após novas evidências.

Cada estágio pode revelar novas exigências. Portanto, nenhuma porcentagem deve ser tratada como definitiva.

## Tipos de descoberta

### Lacuna
Algo necessário não estava representado.

### Dependência oculta
Uma capacidade depende de outra que ainda não foi identificada.

### Requisito emergente
A experiência revela uma necessidade nova.

### Evidência insuficiente
O resultado parecia válido, mas não há evidência suficiente para sustentá-lo.

### Contradição
Uma descoberta entra em conflito com uma hipótese ou decisão anterior.

### Oportunidade
Uma capacidade criada para um objetivo habilita outros caminhos.

### Novo caminho
A execução revela uma rota que não estava no planejamento.

### Reavaliação de escopo
A compreensão do problema mudou e o planejamento precisa acompanhar.

## Registro obrigatório da descoberta

```text
DESCOBERTA:
CONTEXTO:
COMO FOI REVELADA:
EVIDÊNCIA:
IMPACTO:
CAPACIDADES AFETADAS:
CAMINHOS AFETADOS:
DECISÕES AFETADAS:
AÇÃO DE REAVALIAÇÃO:
NOVO CONHECIMENTO:
APRENDIZADO:
SABEDORIA DERIVADA:
```

## Relação com o Cérebro

Toda descoberta relevante deve poder ser preservada com origem, contexto, temporalidade e relações. O Cérebro não deve guardar apenas a conclusão; deve preservar como ela foi descoberta.

## Relação com o Tabuleiro

Uma descoberta pode:

- criar um nó;
- criar uma relação;
- alterar o estado de uma capacidade;
- abrir um caminho;
- bloquear temporariamente um caminho;
- revelar uma dependência;
- multiplicar o valor de outra frente;
- questionar uma decisão;
- substituir uma hipótese;
- gerar nova pesquisa.

## Relação com a arquitetura

Descobertas não devem ser corrigidas automaticamente apenas no nível local. Quando uma descoberta afeta interfaces, contratos, segurança, continuidade, dados ou outras capacidades, o impacto sistêmico deve ser reavaliado.

## Regra contra falsa conclusão

Não considerar uma frente concluída somente porque:

- o código existe;
- um teste unitário passou;
- uma execução funcionou uma vez;
- uma IA afirmou que está pronta;
- uma documentação foi escrita.

A conclusão deve considerar o nível de evidência exigido pelo risco e pelo objetivo.

## Princípio evolutivo

> O Projeto deve ser capaz de descobrir o que ainda não sabe que precisa construir.

Esse mecanismo é uma capacidade permanente do Projeto, e não uma etapa única. Deve permanecer aberto a novas formas de descoberta, pesquisa, validação e evolução.