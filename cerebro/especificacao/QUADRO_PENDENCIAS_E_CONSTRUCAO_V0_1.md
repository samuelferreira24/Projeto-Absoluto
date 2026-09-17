# QUADRO DE PENDÊNCIAS E ESTRATÉGIA DE CONSTRUÇÃO — PROJETO ABSOLUTO V0.1

## 1. Natureza

Este quadro é um instrumento de planejamento e execução evolutiva. Não é uma arquitetura definitiva nem uma lista fechada de tudo que o Projeto será.

O Projeto está sendo planejado e construído ao mesmo tempo. Cada ciclo pode alterar prioridades, arquitetura, tecnologias e até hipóteses anteriores quando novas evidências surgirem.

## 2. Regra de organização

As pendências devem ser organizadas por **capacidade**, não apenas por arquivo ou tecnologia.

Para cada capacidade:

1. entender a necessidade;
2. inspecionar o que já existe;
3. pesquisar alternativas e evidências;
4. definir hipótese de solução;
5. construir o menor incremento útil;
6. testar;
7. validar no contexto real;
8. registrar experiência, decisão e evidência;
9. atualizar o Cérebro;
10. revisar o planejamento;
11. só então ampliar a capacidade.

## 3. Quadro maior

| Bloco | Capacidade | Situação | Próxima direção |
|---|---|---|---|
| A | Visão e princípios | estabelecidos | manter vivos e revisáveis |
| B | Método de trabalho | em consolidação | usar como método operacional real |
| C | Arquitetura global | hipótese evolutiva | consolidar relações entre capacidades sem congelá-las |
| D | Fundação técnica | construída em boa parte | validar integração e eliminar lacunas |
| E | Cérebro | construção inicial | transformar módulos isolados em fluxo integrado |
| F | Memória e registros | implementados | ampliar qualidade, versionamento e consulta |
| G | Proveniência | implementada inicialmente | aprofundar rastreabilidade ponta a ponta |
| H | Eventos e histórico | implementados inicialmente | ligar trajetória, estado e decisões |
| I | Identidade | implementada inicialmente | ampliar identidade de agentes, sessões e recursos |
| J | Ingestão | piloto validado | preparar ingestão controlada dos materiais reais |
| K | Semântica | primeira camada implementada | validar com casos reais e ambíguos |
| L | Recuperação | funcional e em evolução | combinar texto, relações, contexto e tempo |
| M | Temporalidade | primeira camada implementada | construir histórico temporal mais completo |
| N | Experiência/aprendizado | modelos iniciais | integrar ao ciclo real de construção |
| O | Sabedoria operacional | modelo inicial | validar condições, limites, evidências e aplicação |
| P | Pesquisa contínua | método ativo | registrar pesquisa antes/durante/depois |
| Q | Autoaprendizado da construção | iniciado | fazer o Cérebro registrar o próprio desenvolvimento |
| R | Consolidação assistida | planejada | ativar somente após validação semântica/recuperação |
| S | Interface operacional | CLI inicial | evoluir sem acoplar o núcleo a uma interface |
| T | GitHub/controle | integração inicial validada | ampliar controle, evidência e observabilidade |
| U | Execução integrada | futura | conectar intenção, ação, resultado e evidência |
| V | Integrações externas | futura | criar camada de integração substituível |
| W | Automação | futura | automatizar somente processos já compreendidos |
| X | Agentes de IA | planejamento | testar papéis sem fixar arquitetura final |
| Y | Multi-IA | hipótese | experimentar interoperabilidade e substituição de provedores |
| Z | Orquestração | hipótese | experimentar delegação, coordenação e retorno |
| AA | Supervisão/auditoria | parcialmente iniciada | separar execução, verificação e autoridade |
| AB | Segurança/governança | futura | construir antes de ampliar autonomia real |
| AC | Observabilidade | inicial | ampliar visão de estado, eventos e falhas |
| AD | Operação contínua | futura | somente após controle, segurança e recuperação suficientes |
| AE | Portabilidade/continuidade | em construção | garantir transferência entre IAs, contas e plataformas |
| AF | Memória organizacional | futura | consolidar conhecimento coletivo e histórico |
| AG | Grafo/knowledge graph | planejamento | crescer a partir de relações já existentes |
| AH | Expansão | aberta | adquirir capacidades conforme necessidade real |
| AI | Capacidades desconhecidas | aberta | preservar espaço para soluções ainda não imaginadas |

## 4. O que deve ser construído agora

A próxima prioridade não é construir imediatamente toda a visão futura. É transformar a base atual em uma **capacidade coerente de Cérebro vivo**.

### Frente 1 — Consolidar a base existente

- auditar todos os módulos atuais;
- verificar contratos entre módulos;
- eliminar duplicações e inconsistências;
- confirmar testes e cobertura das capacidades críticas;
- verificar se documentação e implementação continuam sincronizadas;
- separar claramente capacidade validada de capacidade apenas proposta.

### Frente 2 — Integrar o Cérebro

Unificar progressivamente:

`ingestão → registro → proveniência → semântica → relações → temporalidade → recuperação → auditoria → aprendizado`

A integração deve preservar a possibilidade de utilizar cada camada separadamente.

### Frente 3 — Construir memória temporal de verdade

Não guardar apenas o estado atual. Preservar a trajetória:

`evento → contexto → decisão → ação → resultado → evidência → mudança → aprendizado`

Permitir distinguir:

- quando algo aconteceu;
- quando foi conhecido;
- quando foi registrado;
- quando deixou de ser válido;
- por que foi alterado.

### Frente 4 — Tornar o Cérebro participante da construção

Registrar no próprio Cérebro:

- pesquisas;
- fontes;
- decisões;
- hipóteses;
- interpretações;
- correções;
- erros;
- testes;
- resultados;
- aprendizados;
- mudanças de planejamento;
- experiências da construção.

Isso cria a primeira forma de memória do próprio Projeto.

### Frente 5 — Preparar a ingestão do planejamento real

Antes de importar o grande acervo:

1. preservar os arquivos originais;
2. registrar origem e contexto;
3. identificar versões;
4. ingerir primeiro um lote controlado;
5. comparar preservação estrutural e semântica;
6. detectar conflitos entre materiais;
7. registrar proveniência;
8. só ampliar após evidência suficiente.

### Frente 6 — Preparar continuidade entre IAs

Criar um pacote mínimo que permita a uma nova IA reconstruir o contexto sem depender da conversa atual:

`visão + princípios + método + arquitetura atual + estado + histórico + decisões + evidências + problemas + aprendizados + próximo objetivo`

### Frente 7 — Preparar execução futura

Sem ativar autonomia ampla ainda, definir contratos para:

- tarefas;
- permissões;
- resultados;
- evidências;
- erros;
- escalonamento;
- auditoria;
- reversão.

## 5. Ordem de construção

A ordem não é rígida. Ela pode mudar quando pesquisa ou experiência mostrarem uma dependência diferente.

```text
                 VISÃO
                   ↓
             MÉTODO VIVO
                   ↓
          AUDITORIA DA BASE
                   ↓
        INTEGRAÇÃO DO CÉREBRO
                   ↓
       MEMÓRIA + PROVENIÊNCIA
                   ↓
       HISTÓRICO + TEMPORALIDADE
                   ↓
       SEMÂNTICA + RECUPERAÇÃO
                   ↓
       EXPERIÊNCIA + APRENDIZADO
                   ↓
        SABEDORIA OPERACIONAL
                   ↓
       CÉREBRO USADO NA PRÁTICA
                   ↓
       INGESTÃO DO PLANEJAMENTO
                   ↓
       CONTINUIDADE ENTRE IAs
                   ↓
       EXECUÇÃO E INTEGRAÇÕES
                   ↓
      AUTOMAÇÃO / AGENTES / MULTI-IA
                   ↓
      SUPERVISÃO / GOVERNANÇA / 24H
                   ↓
                 EVOLUÇÃO
                   ↺
```

Esta ordem representa uma estratégia atual, não uma obrigação permanente.

## 6. Critério para cada incremento

Nenhum incremento deve ser considerado concluído apenas porque o código funciona.

Deve existir:

`necessidade → implementação → teste → evidência → validação → registro → aprendizado`

Quando uma capacidade tiver impacto sistêmico, também verificar:

- interfaces;
- dependências;
- segurança;
- portabilidade;
- continuidade;
- efeitos sobre o restante do Projeto.

## 7. Como lidar com ideias futuras

Ideias como múltiplas IAs, hierarquias, supervisão em cadeia, operação 24h, MCP, automações e novas formas de inteligência permanecem classificadas como **hipóteses ou possibilidades** até serem pesquisadas e experimentadas.

O Cérebro deve registrar o estado epistemológico de cada informação:

`fonte | observação | interpretação | hipótese | experimento | resultado | conhecimento validado | decisão | princípio operacional`

Isso evita que uma ideia de planejamento seja confundida com uma característica definitiva do Projeto.

## 8. Ciclo de trabalho permanente

```text
PESQUISAR
   ↓
PLANEJAR
   ↓
CONSTRUIR
   ↓
TESTAR
   ↓
VALIDAR
   ↓
USAR
   ↓
OBSERVAR
   ↓
APRENDER
   ↓
REGISTRAR NO CÉREBRO
   ↓
REVISAR O PLANEJAMENTO
   ↓
OTIMIZAR
   ↺
```

Pesquisa pode ocorrer antes, durante e depois da construção.

## 9. Princípio de não congelamento

O Projeto deve preservar duas coisas simultaneamente:

1. **continuidade**, para não perder o que já foi construído e aprendido;
2. **liberdade de evolução**, para poder mudar aquilo que novas evidências demonstrarem ser melhor substituir.

Portanto, preservar o passado não significa ficar preso ao passado.

## 10. Resultado esperado desta estratégia

A meta imediata é chegar a um Cérebro que não seja apenas um conjunto de módulos, mas uma capacidade integrada capaz de:

- receber informação;
- preservar a fonte;
- compreender contexto;
- registrar relações;
- acompanhar mudanças no tempo;
- recuperar conhecimento;
- distinguir níveis de certeza;
- registrar decisões;
- aprender com experiências;
- transformar aprendizado em orientação contextual;
- registrar sua própria construção;
- entregar contexto completo para outra IA continuar o trabalho.

A partir dessa capacidade, o Projeto poderá testar de maneira mais segura as camadas futuras de execução, integração, automação, agentes e múltiplas IAs.
