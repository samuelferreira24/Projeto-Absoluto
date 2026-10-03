# INVENTÁRIO E MODELO DE OBJETOS — PROJETO ABSOLUTO

## Princípio

**Projeto Absoluto não é uma lista de capacidades.**

As capacidades são uma dimensão de um sistema muito maior. O inventário completo distingue pelo menos:

**visão → princípios → decisões → pesquisa → evidência → conhecimento → capacidades → componentes → agentes → modelos → ferramentas → recursos → nós → ambientes → interfaces → artefatos → planos → mapas → estado → eventos → testes → fontes → continuidade → histórico → infraestrutura → serviços → sistemas externos.**

## Zonas canônicas

| Zona | Função | Estado |
|---|---|---|
| raiz / governança | identidade, navegação, estrutura | canônica |
| abs_core/ | implementação operacional atual do ABS em construção | canônica |
| cerebro/ | especificações, mapas, estado e conhecimento relacionado ao Cérebro | referência ativa |
| continuidade/ | decisões, continuidade, estado e conhecimento observável | canônica |
| docs/ | documentação funcional | canônica |
| 20_interface/ | interface | canônica |
| 50_frentes/ | frentes futuras/abertas | aberta |
| tests/ + cerebro/tests/ | prova automatizada | canônica |
| .github/ | CI/automação | canônica |
| 99_arquivo/ | patrimônio histórico | histórico |
| mini-cerebro/ | investigação histórica | referência histórica |
| scripts/ | operação auxiliar | suporte |
| tools/ | utilitários | suporte |

O inventário quantitativo está em continuidade/07_conhecimento/project_registry.json.

## Distinções obrigatórias

### Visão ≠ decisão
Visão define direção. Decisão registra uma escolha concreta feita sob essa direção.

### Pesquisa ≠ evidência
Pesquisa produz conhecimento/investigação. Evidência sustenta uma afirmação ou resultado específico.

### Capacidade ≠ componente
Uma capacidade é o que o sistema consegue fazer. Um componente é uma parte que implementa, suporta, integra ou observa isso.

### Ferramenta ≠ recurso
Ferramenta é um meio operacional. Recurso é algo que pode ser utilizado pelo sistema.

### Modelo ≠ agente
Modelo é mecanismo de inferência. Agente é uma entidade operacional com contexto, política, loop, ferramentas, estado e responsabilidade definidos.

### Agente ≠ orquestrador
Agente pode executar uma função. Orquestrador coordena execução, composição e rotas.

### Estado ≠ histórico
Estado responde “onde estamos”. Histórico responde “como chegamos aqui”.

### Handoff ≠ memória
Handoff é ponte de transferência. Memória é o conjunto persistente de conhecimento, estado e histórico recuperável.

### Interface ≠ ABS
Interface é um canal de acesso. O ABS em construção existe além de uma interface específica.

### Arquivo histórico ≠ estado atual
Material antigo é preservado como patrimônio, mas não deve ser confundido com a verdade operacional atual.

## Registries ativos

- capability_registry.json — capacidades.
- decision_registry.json — decisões explícitas.
- trajectory_registry.json — trajetória/proveniência.
- project_knowledge.json — estado derivado observável.
- project_registry.json — inventário estrutural do próprio projeto.
- closure_registry.json — fechamento controlado das lacunas restantes.

## O que foi fechado nesta organização

1. Estrutura física principal.
2. Zonas canônicas.
3. Separação atual/histórico/referência.
4. Catálogo das 72 capacidades.
5. Inventário físico do abs_core.
6. Registro das decisões explícitas já documentadas.
7. Registro da trajetória.
8. Registro estrutural dos principais tipos de objeto.
9. Relação entre os registros e o Project Knowledge.

## Estado final da organização

A camada de **inventário e organização** está fechada: as lacunas que não podem ser marcadas como resolvidas foram individualmente registradas em `closure_registry.json`, com critério de fechamento e evidência exigida. Isso encerra a classificação estrutural sem fingir que capacidades ainda não comprovadas já funcionam.

## O que permanece como fechamento semântico

Esses itens não serão falsamente marcados como resolvidos:

- decisão específica → evidência específica;
- evidência → implementação;
- implementação → resultado;
- resultado → decisão que a substituiu;
- pesquisa → evidência;
- artefato → decisão/capacidade/componente;
- agente → modelo/política/ferramentas/responsabilidade;
- recurso externo → ambiente/nó/serviço;
- estado real de ambientes externos;
- fechamento end-to-end das capacidades parciais.

Essas são relações que ainda precisam de evidência, não novas categorias de arquivos.

## Regra de fechamento

O projeto só é considerado organizado quando qualquer objeto relevante puder responder:

**o que é → onde está → a que pertence → quem o autorizou → de onde veio → em que estado está → que evidência o sustenta → o que produziu → o que depende dele → o que o substituiu → como recuperá-lo.**

Quando uma resposta não puder ser dada, o correto é registrar a lacuna — não inventá-la.
