# PESQUISA — TRAJETÓRIA, PROVENIÊNCIA E RECUPERAÇÃO BIDIRECIONAL

Projeto Absoluto — Estudo arquitetural V1

Data: 2026-10-03
Status: pesquisa + simulações + modelo implementado em branch
Finalidade: descobrir uma forma robusta de representar a evolução do trabalho no repositório para permitir recuperação do início ao presente, do presente à origem e entre ramos relacionados, sem transformar o repositório em um único histórico textual.

## 1. Pergunta

Como representar a trajetória de um projeto complexo de modo que uma IA consiga responder:
1. Como chegamos ao estado atual?
2. De onde veio esta decisão?
3. Qual evidência ou pesquisa informou esta mudança?
4. O que esta decisão produziu depois?
5. O que uma decisão antiga substituiu?
6. Quais caminhos paralelos convergiram?
7. O que é fato registrado e o que é apenas inferência?
8. Como recuperar um ponto específico sem ler o repositório inteiro?

O objetivo não é criar uma linha do tempo bonita. É criar uma trajetória reconstruível.

## 2. Base no uso real do repositório

A investigação foi confrontada com situações que já ocorrem no Projeto Absoluto:
- handoff inicial e retomada;
- evolução da infraestrutura VPS/Coolify/Code Server;
- incidentes e diagnósticos;
- decisões de não executar alterações às cegas;
- pesquisas independentes;
- implementação posterior de conhecimento pesquisado;
- commits e testes;
- Project Knowledge;
- distinção entre estado atual e histórico;
- substituição de decisões/documentos;
- preservação de fontes históricas;
- recuperação de contexto por uma nova IA;
- relação entre pesquisa, decisão, implementação e evidência.

O repositório já possuía events, evidence, paths, knowledge_sources, estado estruturado e histórico Git. O problema identificado era a ausência de uma camada explícita e navegável de relações de trajetória entre esses objetos.

## 3. Pesquisa externa

### 3.1 Event Sourcing
Event Sourcing registra mudanças como uma sequência de eventos e permite reconstruir estados anteriores. A ideia é especialmente relevante para responder não apenas onde estamos, mas como chegamos aqui. Fonte: Martin Fowler — Event Sourcing.

Limitação: eventos sozinhos não expressam suficientemente proveniência semântica, autoridade, fontes documentais ou relações como informou, substituiu e validou.

### 3.2 W3C PROV
O W3C PROV modela entidades, atividades e agentes, incluindo tempo, derivação, responsabilidade e relações de proveniência. A derivação conecta uma entidade produzida às entidades que influenciaram sua produção.

Isso fornece uma base formal para representar de onde veio e quem/qual atividade esteve envolvido.

### 3.3 Git como histórico estrutural
Git já mantém um grafo de commits com relações de parent/child e permite percorrer ancestralidade, descendência, ramos e caminhos de ancestralidade.

Portanto, o repositório já possui uma parte importante da trajetória: a história das revisões. Não é necessário reinventá-la.

### 3.4 Checkpoints e estado durável
Documentação do Microsoft Agent Framework separa estado, sessões e checkpoints. Checkpoints permitem salvar e restaurar progresso e manter estado necessário para retomar execução.

Isso reforça que trajetória histórica e estado operacional não devem ser confundidos.

### 3.5 Organização de repositórios
GitHub recomenda documentação que facilite navegação e compreensão e também recomenda criar apenas conteúdo necessário, porque conteúdo excessivo dificulta encontrar a informação.

Conclusão prática: não criar uma narrativa gigante paralela ao repositório. A trajetória deve ser uma estrutura de relações e projeções, usando as fontes existentes.

## 4. Modelos simulados

Foram comparadas seis famílias:
1. árvore documental;
2. timeline;
3. Event Sourcing puro;
4. knowledge graph;
5. provenance graph;
6. híbrido: eventos + proveniência/relações + estado/checkpoints + projeções.

### Simulação A — origem → presente
Pergunta: Como o estado atual surgiu a partir do objetivo original?
Resultado: o híbrido foi o único candidato que combinou sequência, relações semânticas e estado operacional sem exigir uma estrutura única para tudo.

### Simulação B — presente → origem
Pergunta: Por que estamos neste estado?
Caminho necessário: estado → alteração → decisão/atividade → evidência/pesquisa → origem.
Resultado: o híbrido.

### Simulação C — decisão substituída
Exemplo: DEC-A → DEC-B, onde B substitui A.
A decisão A não pode ser apagada, mas também não pode continuar parecendo atual.
Relação: DEC-A --superseded_by--> DEC-B, com temporalidade/status.
Resultado: híbrido com relações temporais.

### Simulação D — ramos paralelos
Duas pesquisas podem começar independentemente e convergir para uma implementação.
Modelo: pesquisa A + pesquisa B → decisão → implementação.
Resultado: grafo/híbrido.

### Simulação E — VPS/Code Server
A sequência real pode ser representada como: handoff VPS → erro → decisão de não usar chown às cegas → diagnóstico → novo erro → próxima ação → validação.
Isso exige eventos temporais e relações entre eles.
Resultado: híbrido.

### Simulação F — pesquisa → implementação
Pesquisa de continuidade → decisão → implementação → testes.
Relações: pesquisa --informed--> decisão; decisão --led_to--> implementação; implementação --validated_by--> evidência.
Resultado: híbrido com autoridade/proveniência explícitas.

### Simulação G — inferência
Uma IA pode suspeitar que A causou B. Essa relação não pode ser registrada como fato apenas porque parece plausível.
Relação possível: A --possibly_related_to--> B, status=inferred.
Relações comprovadas permanecem status=asserted.
Resultado: híbrido.

### Simulação H — recuperação de sessão
A trajetória não substitui checkpoint/estado.
Para retomar: checkpoint → estado → fontes necessárias.
Para entender por que aquele estado existe: estado → trajetória → origem.
Resultado: híbrido.

## 5. Ataque ao modelo
O candidato híbrido foi atacado contra histórico linear, múltiplos ramos, decisão substituída, informação histórica superada, inferência incorreta, evidência sem relação explícita, commit sem documentação, pesquisa que depois influencia implementação e estado atual sem reconstrução completa.

O modelo sobreviveu porque não exige que uma única estrutura responda a tudo.

## 6. Modelo escolhido
O modelo adotado é:

Camada de trajetória/proveniência temporal sobre as fontes existentes, usando relações explícitas, com estado e checkpoints como visões operacionais derivadas.

Não será criado um segundo repositório de memória.
Não será criado um documento único contando toda a história.

Estrutura:
fontes / artefatos / eventos / decisões / evidências
→ relações de trajetória
→ estado + checkpoints
→ projeções / mapas / handoff

## 7. Estrutura mínima
Cada relação possui:
- identificador;
- origem;
- tipo da relação;
- destino;
- status;
- momento;
- referência da fonte;
- observação opcional.

Exemplos:
- commit-A --precedes--> commit-B
- commit-B --changed--> file:X
- event-X --generated--> evidence-X
- research-X --informed--> decision-X
- decision-X --led_to--> implementation-X
- implementation-X --validated_by--> evidence-X
- decision-old --superseded_by--> decision-new

## 8. Regras de autoridade
A automação pode registrar relações observáveis, principalmente as derivadas do Git e dos próprios registros estruturados.
Ela não deve transformar inferência de IA em decisão humana.

Distinções:
- asserted — relação registrada/comprovada pela fonte;
- inferred — hipótese ou relação inferida;
- historical — fato do passado;
- current — estado atual;
- human_authority — autoridade do Imperador;
- derived_observation — estado derivado automaticamente.

## 9. Relação com Git
Git continua sendo a fonte primária da história de versões.
A nova camada não copia o Git inteiro como narrativa. Ela projeta relações úteis: parent → child; commit → arquivo alterado; commit → revisão observada.

## 10. Relação com Project Knowledge
Project Knowledge continua sendo a projeção estruturada do estado observável.
A mudança arquitetural é:
- estado;
- evidências;
- eventos;
- fontes;
- paths;
- nós;
- relações de trajetória.

Linhas do tempo e mapas futuros podem ser gerados dessas relações.

## 11. Implementação realizada
Na branch de trabalho desta pesquisa:
- schema do Project Knowledge passou de 1.2 para 1.3;
- adicionada estrutura Relation;
- Project Knowledge passou a armazenar relações;
- histórico Git é observado;
- relações parent → child são registradas;
- commits → arquivos alterados são registrados;
- eventos → evidências são relacionados;
- fontes, eventos e evidências passam a ser nós navegáveis;
- mapa automático passa a projetar relações de trajetória;
- testes protegem a nova estrutura.

A implementação é deliberadamente pequena: cria a infraestrutura de trajetória sem transformar o repositório em um banco de grafo nem reescrever a documentação existente.

## 12. Limite conhecido
A primeira implementação consegue reconstruir proveniência estrutural observável, especialmente a história Git e relações já presentes no estado estruturado.
Ela ainda não consegue inferir automaticamente toda a genealogia semântica histórica de conversas antigas.

Isso é intencional. Relações semânticas como pesquisa → decisão → implementação precisam ser registradas explicitamente ou posteriormente vinculadas com evidência. A IA não deve inventar essa relação.

## 13. Conclusão
A melhor solução encontrada não é uma timeline isolada, um Event Sourcing puro ou um knowledge graph independente.

É uma arquitetura híbrida:
fontes reais + histórico Git + eventos + relações de proveniência + temporalidade + estado/checkpoints + projeções de navegação.

Ela permite três direções:
ORIGEM → PRESENTE
PRESENTE → ORIGEM
PONTO → RAMOS / CONSEQUÊNCIAS

sem sacrificar autoridade, histórico, evidência, estado atual, independência das fontes, recuperação de sessão e simplicidade do repositório.

## 14. Fontes principais
- W3C PROV-DM — https://www.w3.org/TR/prov-dm/
- Martin Fowler — Event Sourcing — https://www.martinfowler.com/eaaDev/EventSourcing.html
- Git git-log — https://git-scm.com/docs/git-log/pt_BR
- Microsoft Agent Framework — Checkpoints — https://learn.microsoft.com/en-us/agent-framework/workflows/checkpoints
- Microsoft Agent Framework — Durable Extension — https://learn.microsoft.com/en-us/agent-framework/integrations/durable-extension
- GitHub Repositories — https://docs.github.com/en/repositories
- GitHub Content Design Principles — https://docs.github.com/en/contributing/writing-for-github-docs/content-design-principles