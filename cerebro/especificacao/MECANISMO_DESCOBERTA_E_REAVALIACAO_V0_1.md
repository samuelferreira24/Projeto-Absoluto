# Mecanismo de Descoberta e Reavaliação V0.1

## Finalidade

O Projeto Absoluto deve ser capaz de descobrir, durante a própria construção, que faltam capacidades, requisitos, evidências, relações ou caminhos que não estavam previstos inicialmente.

O planejamento é uma representação provisória do conhecimento atual. A execução pode revelar lacunas novas. Essas lacunas devem retroalimentar o Cérebro, o Tabuleiro, o Estado, o Método e a arquitetura.

## Princípio central

> Descobertas podem alterar a percepção do progresso. Reavaliar não é retroceder; é atualizar o mapa com evidência melhor.

## Ciclo de descoberta

```text
PLANEJAMENTO → EXECUÇÃO → OBSERVAÇÃO → DESCOBERTA
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

## O que deve ser reavaliado

- estado real;
- evidências disponíveis;
- requisitos conhecidos e descobertos;
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

Progresso deve refletir aquilo que está efetivamente demonstrado, não apenas o que foi implementado ou planejado.

Uma frente pode estar planejada, implementada, testada, verificada, validada, operacional ou observada em uso. Cada estágio pode revelar novas exigências. Portanto, nenhuma porcentagem deve ser tratada como definitiva.

## Tipos de descoberta

- **Lacuna:** algo necessário não estava representado.
- **Dependência oculta:** uma capacidade depende de outra ainda não identificada.
- **Requisito emergente:** a experiência revela uma necessidade nova.
- **Evidência insuficiente:** o resultado parece válido, mas a evidência não é suficiente.
- **Contradição:** nova evidência entra em conflito com hipótese ou decisão anterior.
- **Oportunidade:** uma capacidade habilita outros caminhos.
- **Novo caminho:** a execução revela uma rota não prevista.
- **Reavaliação de escopo:** a compreensão do problema mudou.

## Registro da descoberta

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

## Relação com o Cérebro e o Tabuleiro

O Cérebro deve preservar não apenas a conclusão, mas como ela foi descoberta, com origem, contexto, temporalidade e relações.

Uma descoberta pode criar um nó, criar uma relação, alterar o estado de uma capacidade, abrir ou bloquear um caminho, revelar uma dependência, questionar uma decisão, substituir uma hipótese ou gerar nova pesquisa.

## Regra contra falsa conclusão

Não considerar uma frente concluída somente porque o código existe, um teste unitário passou, uma execução funcionou uma vez ou uma IA afirmou que está pronta. A conclusão deve considerar o nível de evidência exigido pelo objetivo e pelo risco.

## Princípio evolutivo

> O Projeto deve ser capaz de descobrir o que ainda não sabe que precisa construir.

Essa é uma capacidade permanente do Projeto, aberta a novas formas de descoberta, pesquisa, validação e evolução.