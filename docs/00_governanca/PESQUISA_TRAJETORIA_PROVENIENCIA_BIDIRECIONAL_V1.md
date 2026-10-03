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

## 20. Simulações comparativas com o uso real do repositório

A hipótese foi testada contra situações que já aparecem no trabalho do Projeto, em vez de comparar arquiteturas apenas em abstrato.

### Modelos comparados

M1 — Linha do tempo documental: um documento cronológico como fonte principal.

M2 — Event Sourcing: eventos como fonte primária e estado reconstruído a partir deles.

M3 — Knowledge Graph: nós e relações sem uma disciplina específica de proveniência.

M4 — Grafo de Proveniência: entidades, atividades, agentes, derivação, tempo e origem.

M5 — Grafo de Proveniência Temporal Nativo do Git:
- Git como histórico durável de alterações;
- eventos observáveis do repositório;
- relações semânticas explícitas em registro separado;
- temporalidade e autoridade nas relações;
- estado/checkpoints como projeções;
- índices/mapas derivados;
- travessia para frente e para trás;
- validação das relações;
- sem banco de grafo obrigatório.

### Simulação 01 — Nova IA entra no projeto

Situação: uma IA nova recebe somente o repositório e precisa descobrir estado atual, decisões, pesquisas, evidências e ponto de retomada.

M1 consegue localizar uma narrativa, mas depende de manutenção manual e pode perder fontes.

M2 consegue reconstruir eventos, mas não possui naturalmente a separação entre decisão humana, pesquisa, evidência e documentação.

M3 recupera relações se elas estiverem completas, mas não define por si só autoridade, proveniência nem validade temporal.

M4 recupera origem e relações com boa precisão, mas precisa de integração específica com Git e com a estrutura documental.

M5 utiliza os mapas e estado já existentes, segue relações explícitas e pode voltar às fontes originais.

Resultado: M5 PASS.

### Simulação 02 — Começar pelo estado atual e voltar à origem

Situação: o estado atual indica uma capacidade ou decisão. Pergunta: “como chegamos aqui?”

O caminho desejado é:

estado → artefato/arquivo → alteração → commit → evento/decisão/fonte relacionada → origem

Git já fornece uma linhagem forte para commits e arquivos. git log permite seguir histórico, inclusive por caminho e além de renome em casos suportados. citeturn2search1

Resultado: M5 PASS.

### Simulação 03 — Começar por uma decisão e avançar até o presente

Situação: uma decisão antiga precisa ser seguida para descobrir quais mudanças e resultados ela originou.

Uma simples timeline exige leitura sequencial. Um grafo permite seguir relações de consequência, mas somente se essas relações forem explícitas e não inventadas.

Resultado: M5 PASS.

### Simulação 04 — Decisão substituída

Situação: uma decisão antiga deixa de ser vigente.

O modelo precisa preservar decisão original, período de validade, sucessora e estado atual.

ADRs são uma referência importante porque registram contexto, decisão, consequências e ciclo de vida; a coleção forma um log de decisões. citeturn1search4turn1search6

Resultado: M5 PASS.

### Simulação 05 — Pesquisa → evidência → decisão → implementação → teste

Situação: uma pesquisa influencia uma decisão, que gera implementação, que produz teste.

PROV fornece justamente um vocabulário para entidades, atividades, agentes, derivação e tempo. citeturn0search0turn0search1

Resultado: M4 e M5 PASS; M5 é mais adequado ao repositório porque mantém as fontes originais e Git como infraestrutura de histórico.

### Simulação 06 — Branch, merge e evolução de arquivos

Situação: trabalho ocorre em branches e depois é integrado.

O histórico do Git já é um grafo, não uma lista linear. O modelo não deve tentar copiar esse histórico para outro banco como nova fonte de verdade.

Resultado: M5 PASS.

### Simulação 07 — IA produz hipótese

Situação: uma IA sugere uma relação causal que não está explicitamente comprovada.

O sistema não pode promover automaticamente “IA inferiu X” para “Projeto sabe X”.

A proveniência deve registrar a origem da afirmação e manter sua autoridade distinta. PROV trata proveniência como informação sobre entidades, atividades e agentes envolvidos na produção de algo. citeturn0search0

Resultado: M5 PASS quando a relação possui origem/autoridade explícitas.

### Simulação 08 — Falha e recuperação

Situação: uma execução falha e é necessário recuperar o último estado válido.

Checkpoints são adequados para preservar estado operacional recuperável; Microsoft Agent Framework documenta captura e retomada de checkpoints para workflows longos e recuperação após interrupções. citeturn0search2turn0search3

Resultado: M5 PASS, tratando checkpoint como estado operacional e não como substituto do histórico.

### Simulação 09 — Encontrar informação sem ler todo o repositório

Situação: “Por que estamos usando esta estrutura?”

A resposta deve começar em um nó atual, seguir relações e recuperar apenas as fontes relevantes.

A organização documental também deve preservar a distinção entre referência, how-to e explicação; Diátaxis recomenda que cada forma atenda uma necessidade diferente e que a referência descreva o sistema de forma precisa. citeturn1search1turn1search2

Resultado: M5 PASS.

### Simulação 10 — Relação incorreta ou cíclica

Situação: uma relação de precedência/derivação cria um ciclo impossível.

A especificação de constraints do W3C PROV trata explicitamente de ordenação e validação de provenance e recomenda detectar ciclos inconsistentes. citeturn2search5turn2search2

Resultado: M5 PASS porque a implementação inclui validação de relações de ordem estrita.

## 21. Resultado das simulações

As simulações eliminaram progressivamente:
- timeline puro;
- event sourcing puro;
- knowledge graph puro;
- grafo de proveniência isolado.

O modelo que melhor se ajustou ao uso real foi:

Grafo de Proveniência Temporal Nativo do Git + relações semânticas explícitas + estado/checkpoints + projeções derivadas.

Ele não é um banco de dados de grafo obrigatório. É uma camada lógica sobre as fontes existentes.

## 22. Modelo selecionado

Fonte primária: Git + arquivos/fontes persistentes do Projeto.

Git continua sendo a fonte do histórico de alterações do código e dos arquivos versionados.

A camada de trajetória representa:
- nós;
- relações;
- autoridade;
- origem da relação;
- temporalidade;
- validade;
- status;
- proveniência.

Relações automáticas/observadas:
- commit → precedes → commit;
- commit → changed → arquivo;
- evento → generated → evidência;
- commit → observed_by → evento.

Relações semânticas explícitas:
- pesquisa → informs → decisão;
- decisão → supersedes → decisão;
- handoff → points_to → estado;
- resultado → derived_from → evidência;
- objetivo → led_to → proposta.

A segunda classe nunca deve ser inventada silenciosamente por uma IA.

## 23. Forma de armazenamento escolhida

Não foi adotado um banco de grafo externo.

A primeira implementação usa:
continuidade/07_conhecimento/trajectory_registry.json

para relações semânticas explícitas, enquanto:
project_knowledge.json

continua sendo uma projeção derivada do estado observável.

Isso mantém o repositório portátil, versionável e utilizável offline.

A implementação de travessia está em:
abs_core/trajectory.py

Ela permite:
- forward;
- backward;
- ancestors;
- descendants;
- filtragem por tipos de relação;
- validação de relações;
- detecção de ciclos em relações de ordem estrita.

## 24. Invariantes do modelo

1. Git continua sendo fonte do histórico Git.
2. Estado atual não substitui histórico.
3. Handoff não substitui fontes.
4. Relação inferida não vira fato automaticamente.
5. Decisão humana não pode ser promovida ou alterada pela projeção automática.
6. Relações de ordem estrita não podem formar ciclos.
7. Uma relação deve possuir origem identificável.
8. Temporalidade deve poder distinguir presente de histórico.
9. Projeções podem ser regeneradas.
10. O modelo deve funcionar sem banco de grafo externo.
11. O modelo deve permanecer portátil no repositório.
12. A nova camada deve complementar, não duplicar, Git, decisões, evidências e documentos.

## 25. Resultado arquitetural

A ideia inicial — “guardar uma linha do começo ao fim” — foi refinada para:

“preservar uma estrutura de proveniência temporal navegável, capaz de reconstruir trajetórias em ambas as direções a partir das fontes duráveis do repositório.”

Portanto, origem → presente e presente → origem não são dois históricos diferentes. São duas consultas sobre a mesma estrutura de trajetória.

## 26. Limites atuais

A implementação inicial ainda não tenta inferir automaticamente toda a história semântica do Projeto.

Isso é deliberado.

Git permite observar com alta confiabilidade commits, parentesco, alterações, arquivos e revisões.

Mas Git não sabe, por si só, que “esta pesquisa foi a causa daquela decisão” ou que “esta conversa foi a origem daquela arquitetura”.

Essas relações precisam de registro explícito, evidência ou uma inferência marcada como tal.

A camada atual fornece a infraestrutura para registrar e navegar essas relações sem falsificar causalidade.

## 27. Próxima evolução

O próximo teste relevante é alimentar a camada com casos reais adicionais do Projeto e verificar se uma IA consegue responder, de forma rastreável:
1. Como chegamos neste estado?
2. O que originou esta decisão?
3. O que esta decisão produziu?
4. Qual decisão substituiu esta?
5. Qual evidência sustenta esta afirmação?
6. O que mudou desde este ponto?
7. Qual era o estado imediatamente anterior?
8. Qual é a fonte primária?

A resposta deve conter caminhos de recuperação e não apenas uma narrativa gerada.

## 28. Estado da pesquisa

Conclusão: modelo selecionado após simulações comparativas.

Implementação inicial: realizada na branch trajectory-provenance-v1.

Validação: testes específicos adicionados para travessia bidirecional, ciclos, integração com Git, registro semântico e projeção.

Status epistemológico: arquitetura selecionada e implementada; a validação empírica deve continuar com casos reais do Projeto antes de considerar a camada definitiva.
