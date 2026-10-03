# HANDOFF ATUAL — PROJETO ABSOLUTO / ABS
## Preservação integral de contexto e retomada da construção
**Data de referência:** 2026-10-03
**Branch:** main
**Finalidade:** ponto de continuidade vigente para outra IA/sessão

> Este documento não substitui código, testes, decisões do Imperador ou pesquisas originais. Ele consolida o **contexto operacional necessário para continuar o trabalho** sem depender desta conversa: entendimento, correções, decisões, pesquisas, estado, infraestrutura, evidências, limites e próximo ponto de construção.

---

# 1. O QUE É O PROJETO

## Projeto Absoluto

Projeto Absoluto é o projeto maior. Ele contém visão, princípios, método, direção e os sistemas/projetos necessários para transformar visão em capacidade de execução.

O Imperador permanece como autoridade humana sobre visão, direção, decisões e autorizações.

O Projeto Absoluto não é sinônimo de:
- ABS;
- uma IA;
- um aplicativo;
- um servidor;
- um repositório;
- uma arquitetura única.

## Sistema Absoluto / ABS geral

**ABS geral** é a abreviação de **Sistema Absoluto** no sentido amplo: o ecossistema aberto de capacidades e recursos que o Imperador pode utilizar, combinar, substituir, ampliar ou criar.

Esse ecossistema pode conter, entre outras coisas:
- IAs;
- agentes;
- modelos;
- ferramentas;
- APIs;
- servidores;
- dispositivos;
- ambientes;
- serviços;
- projetos;
- automações;
- infraestrutura;
- capacidades próprias ou de terceiros.

Nenhum desses elementos, isoladamente, define o ABS geral.

## ABS em construção

Existe também um **ABS específico que está sendo construído**.

Sua finalidade é operar/orquestrar o ecossistema do Sistema Absoluto sob autoridade do Imperador.

Portanto:

```
PROJETO ABSOLUTO
        ↓
SISTEMA ABSOLUTO / ABS GERAL
        ↓
ecossistema aberto de capacidades e recursos
        ↑
        │
ABS EM CONSTRUÇÃO
operador/orquestrador
        ↓
seleção → autorização → execução
        ↓
verificação → evidência → estado
        ↓
memória → continuidade → novo ciclo
```

**ABS geral ≠ ABS em construção.**

Quando a palavra “ABS” aparecer sem qualificador, a fonte deve deixar explícito qual sentido está sendo usado quando houver risco de ambiguidade.

## ABS V1

**ABS V1 é a primeira versão operacional do ABS em construção.**

Não é:
- o Sistema Absoluto inteiro;
- uma definição final do ABS;
- uma arquitetura permanente;
- o conjunto completo de capacidades futuras.

---

# 2. ENTENDIMENTO CENTRAL QUE PRECISA SER PRESERVADO

O objetivo não é construir um “superagente” que contenha tudo.

O objetivo é construir um sistema capaz de **operar um ecossistema aberto de capacidades**, escolhendo e compondo meios adequados para cada objetivo.

Princípios consolidados:

- Imperador mantém autoridade.
- Capacidades são substituíveis.
- Modelos são meios, não autoridade.
- Ferramentas são meios, não autoridade.
- Interfaces não definem o ABS.
- Servidores não definem o ABS.
- Um fornecedor não deve se tornar identidade estrutural do ABS.
- Um componente pode falhar sem que o ecossistema inteiro deva falhar.
- O sistema deve conseguir descobrir, adquirir, combinar, testar, substituir e criar capacidades.
- O sistema deve registrar o que fez e por que fez.
- Resultado não é automaticamente verdade: precisa de evidência/verificação proporcional ao risco.
- Memória não é autoridade absoluta; precisa de proveniência, contexto e validade.
- Autonomia deve permanecer subordinada a políticas, autorização e controle humano apropriados.
- A construção deve evoluir por evidência, não por assumir que a arquitetura futura já é conhecida.

Princípio de construção:

**necessidade → capacidade necessária → verificar o que já existe → integrar → testar → construir apenas o que faltar.**

---

# 3. MÉTODO DE TRABALHO DO PROJETO

O método utilizado pelo Imperador inclui:

### PP — Primeiros Princípios
Perguntar o que realmente precisa ser realizado, removendo premissas desnecessárias.

### BN — Bola de Neve
Explorar possibilidades, caminhos, mecanismos e capacidades sem limitar prematuramente a solução.

### AV — Avalanche
Aplicar filtros, evidências, riscos, custos, autorização e realidade operacional para decidir o que continua.

A construção não deve ser orientada por “qual ferramenta instalar”, mas por:

**objetivo → necessidade → capacidades → caminhos → execução → verificação → aprendizado.**

---

# 4. PESQUISA ARQUITETURAL — MOLDE DO AGENTE

Foi conduzida uma investigação arquitetural independente para descobrir o molde mais adequado para um agente capaz de operar o ABS.

A investigação deliberadamente não deveria:
- depender da implementação atual;
- construir o ABS;
- modificar código do ABS;
- assumir que um framework específico é a solução;
- parar no primeiro molde aparentemente bom.

Foram investigadas famílias como:
- agente universal;
- multimodo;
- núcleo universal + modos;
- multiagente;
- hierárquico;
- adaptativo;
- workflow;
- máquina de estados;
- reativo;
- deliberativo;
- planner/executor;
- orchestrator/worker;
- manager/specialist;
- evaluator/optimizer;
- reflection;
- routing de modelos;
- composição dinâmica;
- execução direta;
- seleção de estratégia;
- controle humano;
- recuperação/checkpoint;
- sandbox;
- MCP;
- arquiteturas e mecanismos presentes em OpenAI/Codex, Anthropic/Claude Code, Google/ADK, LangGraph/LangChain, Deep Agents, Microsoft e trabalhos open source/acadêmicos.

Conceitos tratados separadamente:
- agente;
- modo;
- estratégia;
- política;
- ferramenta;
- modelo;
- ambiente;
- estado;
- memória;
- contexto;
- harness;
- loop;
- planner;
- tools;
- subagentes;
- verificação;
- autorização;
- execução;
- recuperação;
- interface.

Pergunta central:

> **Quem controla quem?**

Conclusão arquitetural atual:

**não há evidência para escolher um único molde universal fixo.**

A direção mais robusta encontrada foi uma **família de moldes de execução com seleção e composição**, em vez de um único formato obrigatório.

A execução pode variar conforme objetivo, contexto, risco e capacidades disponíveis:

```
objetivo
 ↓
contexto
 ↓
PP
 ↓
BN
 ↓
AV
 ↓
seleção de estratégia
 ↓
direto / workflow / agente / multiagente
 ↓
capacidades e recursos
 ↓
execução
 ↓
observação
 ↓
verificação
 ↓
concluído / replanejar / recuperar
```

Isso não significa que todos esses níveis devam ser usados sempre.

A complexidade deve ser **elástica**:
- tarefa simples → caminho direto;
- tarefa estruturada → workflow;
- tarefa incerta/adaptativa → agente;
- tarefa decomponível com benefício real → multiagente.

---

# 5. EXPERIMENTOS E SIMULAÇÕES

Foram realizados experimentos/simulações numerados de **01 a 30**, cobrindo, entre outros:

- conversa;
- pesquisa;
- planejamento;
- execução;
- debugging;
- falhas;
- tarefas longas;
- contexto;
- memória;
- persistência;
- checkpoint;
- recuperação;
- replanning;
- composição;
- paralelismo;
- falhas parciais;
- retomada;
- concorrência;
- idempotência;
- verificação semântica;
- complexidade mínima;
- descoberta de capacidades;
- implementações divergentes;
- testes adversariais;
- mutation testing;
- single agent vs multiagent;
- especialistas e controle.

Os testes chegaram a **CI verde**, mas isso não foi interpretado como prova definitiva da arquitetura.

O resultado importante foi convergente:

> **o candidato não deve ser uma arquitetura monolítica única; deve ser um sistema capaz de selecionar/compor moldes de execução.**

---

# 6. ATAQUE ADVERSARIAL DO MOLDE

O molde candidato foi deliberadamente atacado.

Ataques relevantes incluíram:
- objetivo mal especificado;
- contexto incompleto;
- modelo forte com ferramenta ruim;
- verificador incorreto;
- ferramenta maliciosa;
- memória inválida;
- contexto excessivo;
- contexto insuficiente;
- executor indisponível;
- corrupção de estado;
- concorrência;
- explosão de subagentes;
- autonomia excessiva;
- Control Plane como gargalo;
- seleção errada de arquitetura;
- tarefa nunca vista.

Invariantes reforçados:
1. Control Plane não pode virar autoridade autônoma.
2. Selector opera dentro de política e orçamento.
3. Complexidade deve ser elástica.
4. Estratégias tentadas precisam ser registráveis.
5. Objetivos precisam de identidade/versionamento.
6. Memória não é autoridade absoluta.
7. Verificação deve poder ser independente.
8. Capacidades precisam de limites além de suas descrições.
9. Subagentes precisam de admission control.
10. Autonomia deve ser proporcional ao risco.
11. Estado precisa de integridade e recuperação.
12. UNKNOWN precisa existir explicitamente.

Conclusão do ataque:

> **O ABS deve possuir um núcleo de controle estável e limitado, enquanto a estratégia de execução pode ser adaptativa e variável.**

Adaptabilidade não significa permitir que o sistema redefina livremente suas próprias regras fundamentais.

A pesquisa não demonstrou superioridade universal, benchmark definitivo, custo, latência ou escalabilidade real. Esses pontos permanecem abertos.

Pesquisa específica preservada em:
`docs/03_planejamento/pesquisa/ATAQUE_ADVERSARIAL_FINAL_MOLDE_ABS_V0.md`

---

# 7. ARQUITETURA DO ABS EM CONSTRUÇÃO

A fundação operacional atual é orientada por:

```
Imperador
  ↓
comando / intenção
  ↓
Work persistente
  ↓
orquestração
  ↓
adaptador de capacidade
  ↓
execução
  ↓
eventos / estado
  ↓
memória / proveniência
  ↓
controle
  ↓
interface
```

O ABS deve operar diferentes recursos sem depender estruturalmente de um único:
- Codex;
- Claude;
- Gemini;
- OpenAI;
- modelos locais;
- Internet;
- APIs;
- GitHub;
- ferramentas;
- servidores;
- dispositivos;
- outros nós.

Esses são exemplos de recursos/capacidades atuais ou potenciais, não um catálogo fechado.

---

# 8. ESTADO REAL DO ABS V1

O repositório possui implementação real em `abs_core/`.

Existem, entre outros:
- Work;
- persistência;
- eventos;
- provenance;
- sessões;
- capabilities;
- orquestração;
- API;
- servidor/runtime;
- adapters;
- Codex;
- GitHub bridge;
- continuidade;
- update manager;
- verification;
- resource routing/selection;
- tool discovery/knowledge;
- Project Knowledge;
- interface/runtime.

A classificação deve continuar obedecendo:

**não confundir documentação com prova; código com capacidade comprovada; capacidade com autorização.**

O quadro de status existente permanece fonte importante:
`cerebro/00_estado/STATUS_ABS_V1_2026-09-22.md`

A fundação V1 foi testada e possui CI verde em incrementos recentes.

---

# 9. CÉREBRO

O Cérebro possui implementação e integração com ABS Core.

Existe:
- estado;
- missão;
- runtime;
- temporalidade;
- ciclo contínuo;
- ponte `cerebro/abs_core_executor.py`.

Fluxo operacional consolidado:

**Cérebro → missão → ABS Core → Work → capability → resultado → retorno ao Cérebro**

A existência dessa ponte não deve ser confundida com um sistema cognitivo ilimitado ou completamente autônomo.

A integração deve continuar sendo demonstrada por evidência real.

---

# 10. MINI-CÉREBRO

O Mini-Cérebro é patrimônio/investigação histórica.

Serve para recuperar:
- experimentos;
- decisões;
- erros;
- soluções;
- descobertas;
- relações;
- evidências;
- material histórico.

Não deve ser confundido com:
- ABS;
- Cérebro operacional;
- arquitetura atual.

Código histórico pode preservar conhecimento mesmo quando não representa capacidade operacional atual.

---

# 11. INTERFACE

A interface é uma camada de operação/visualização do ABS, não sua definição.

Existe interface em:
`20_interface/web/`

Princípios:
- interface não deve fingir que uma mudança visual é mudança real do ABS;
- operações reais devem passar pelas camadas operacionais;
- interface deve evoluir para permitir ao Imperador operar o ecossistema sem precisar abrir manualmente cada ferramenta;
- web é a primeira superfície;
- futuramente podem existir APK e múltiplos dispositivos.

Open WebUI é tratado como **canal/interface substituível**, não como cérebro do ABS.

A integração OpenAI-compatible/gateway já existe no projeto; não reconstruir isso sem evidência de necessidade.

---

# 12. INFRAESTRUTURA DE TRABALHO — VPS

A infraestrutura atual inclui VPS:

- hostname: `abs-vps-01`
- Ubuntu 24.04
- 3 vCPU
- aproximadamente 5,7 GiB RAM
- 60 GB SSD
- IPv4: `207.180.3.245`
- usuário operacional: `absadmin`
- Coolify 4.3.23
- UFW ativo
- SSH endurecido
- root SSH desabilitado
- senha SSH desabilitada
- autenticação por chave
- `absadmin` possui sudo necessário para Coolify.

Princípio:

**VPS é um nó persistente do ambiente de trabalho, não o ABS inteiro, não o cérebro definitivo e não a infraestrutura final.**

---

# 13. ESTADO DO COOLIFY / CODE SERVER

Coolify está instalado e validado.

Sequência desejada:
1. Code Server;
2. teste pelo navegador;
3. PostgreSQL;
4. Uptime Kuma;
5. backup;
6. outros serviços somente quando necessários.

O deployment do Code Server encontrou:

`bash: line 2: cd: /data/coolify/services/u30wfx4gmdt3faj7ntucaeeb: Permission denied`

Após correção anterior de permissões, surgiu:

`Unable to create a directory at /var/www/html/storage/app/ssh/keys.`

**Não executar novo chown às cegas.**

Diagnóstico pendente antes de qualquer nova alteração:

```bash
sudo ls -ld /data/coolify /data/coolify/ssh /data/coolify/ssh/keys && sudo docker inspect coolify --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'
```

Não:
- reinstalar VPS;
- reinstalar Coolify;
- habilitar root SSH;
- apagar Coolify;
- executar chown indiscriminado;
- instalar dezenas de serviços;
- instalar Open WebUI como cérebro;
- instalar agente autônomo prematuramente.

---

# 14. AMBIENTE DO IMPERADOR

O Imperador trabalha principalmente pelo telefone Android.

Ambiente conhecido:
- Android;
- Termux;
- GitHub;
- Codex;
- VPS;
- navegador;
- APIs;
- serviços externos.

Termux continua sendo importante para:
- administração;
- recuperação;
- operação local;
- instalação quando necessária.

O objetivo arquitetural é reduzir progressivamente a necessidade de comandos manuais.

O ambiente de trabalho também faz parte do objetivo do ABS: o sistema deve conseguir operar e coordenar seus próprios meios de trabalho.

---

# 15. EVOLUÇÃO E INDEPENDÊNCIA

A evolução planejada é progressiva:

**operar cedo → aprender → consolidar → modularizar → reduzir dependências críticas → possuir capacidades estratégicas → criar redundância → expandir capacidades.**

Não há objetivo de substituir terceiros simplesmente por princípio.

“Próprio” significa controle/substituibilidade estratégica, não necessariamente escrever tudo do zero.

---

# 16. GOVERNANÇA E EVIDÊNCIA

Estados possíveis continuam sendo explicitados:

- NÃO LOCALIZADO
- ESPECIFICADO
- IMPLEMENTADO
- TESTADO
- INTEGRADO
- OPERACIONAL
- OPERACIONALMENTE COMPROVADO
- PARCIAL
- EXPERIMENTAL
- HISTÓRICO
- HIPÓTESE
- NÃO COMPROVADO

Hierarquia de autoridade para estado atual:

**código + testes + CI + evidência operacional > documentação antiga/handoff**

Para visão, princípios e direção:

**registros autorizados do Imperador**

Para estado estruturado observável:

**Project Knowledge**

Para planejamento:

**mapas/documentos de planejamento**

Para passado:

**fontes históricas preservadas**

---

# 17. CONHECIMENTO E CONTINUIDADE

A camada `continuidade/07_conhecimento/` não deve ser apenas um inventário de arquivos.

Ela deve permitir reconstruir:
1. o que é o Projeto Absoluto;
2. o que é ABS geral;
3. o que é ABS em construção;
4. o que é ABS V1;
5. quem possui autoridade;
6. o que existe de fato;
7. o que é decisão;
8. o que é hipótese;
9. o que foi pesquisado;
10. o que foi testado;
11. quais conclusões são provisórias;
12. quais correções foram feitas;
13. quais erros históricos não devem ser repetidos;
14. qual é o estado da infraestrutura;
15. qual é o próximo ponto de construção.

A conversa pode terminar. O entendimento necessário para continuar o Projeto não pode terminar com ela.

Project Knowledge é regenerado automaticamente pelo repositório e deve ser tratado como projeção estruturada do estado observável, não como substituto das fontes primárias.

---

# 18. ORGANIZAÇÃO DO REPOSITÓRIO

A organização existente foi auditada por:
- função;
- autoridade;
- temporalidade;
- origem;
- público;
- relação com código/evidência.

Regra:

**já existe? → verificar; funciona? → testar; necessário? → validar; integrar? → integrar; só construir se faltar.**

Não criar documentos só porque dois assuntos parecem parecidos.

Classificações:
- Estado;
- Conhecimento;
- Decisão;
- Arquitetura;
- Planejamento;
- Operação;
- Evidência;
- Continuidade;
- Histórico;
- Fonte;
- Referência.

---

# 19. CORREÇÕES IMPORTANTES JÁ FEITAS

Entre as correções e aprendizados preservados:
- handoffs antigos foram reclassificados como históricos quando deixaram de representar estado atual;
- referências para áreas documentais antigas foram corrigidas;
- arquitetura documental foi consolidada;
- Project Knowledge foi automatizado;
- bug de detecção de arquivos novos no workflow foi corrigido;
- continuidade foi separada de projeção;
- código histórico foi separado de capacidade atual;
- Cérebro e Mini-Cérebro foram diferenciados;
- mapas foram diferenciados de estado real;
- documentação não é tratada como prova;
- a definição de ABS foi semanticamente corrigida para distinguir ABS geral de ABS em construção;
- o checkpoint passou a registrar explicitamente que o conhecimento operacional necessário deve sobreviver à conversa.

---

# 20. PESQUISAS QUE DEVEM CONTINUAR SENDO TRATADAS COMO PESQUISA

A pesquisa arquitetural não deve ser transformada artificialmente em decisão final.

Ela deve preservar:
- fontes;
- mecanismos;
- hipóteses;
- experimentos;
- resultados;
- ataques;
- limitações;
- inferências;
- conclusões provisórias.

A pesquisa do molde arquitetural continua independente da implementação do ABS.

Não usar a existência do ABS atual como prova de que o molde pesquisado é correto.

Não usar o molde pesquisado como justificativa automática para alterar o código atual.

---

# 21. O QUE NÃO DEVE SER FEITO AGORA

Não:
- reconstruir componentes já existentes sem auditoria;
- transformar hipótese em arquitetura definitiva;
- instalar plataformas de agentes em massa;
- criar dependência de um único modelo/provedor;
- tratar Open WebUI como cérebro;
- instalar Ollama/local AI na VPS sem necessidade;
- modificar infraestrutura sem diagnóstico;
- apagar histórico para “organizar”;
- resumir pesquisas completas e descartar o original;
- substituir documentos históricos por versões reescritas;
- confundir o ABS geral com o ABS em construção;
- confundir ABS V1 com o estado final do Projeto Absoluto.

---

# 22. PONTO EXATO DE RETOMADA

A fase atual de **preservação e consolidação de contexto** está sendo encerrada.

O objetivo dessa fase foi garantir que o Projeto não dependa da memória desta conversa.

A partir daqui, o trabalho deve voltar para:

**CONSTRUÇÃO DO ABS EM CONSTRUÇÃO**

sem reiniciar a auditoria documental.

A próxima ação deve ser escolhida a partir do estado real, especialmente:
- validação do baseline;
- integração vertical;
- operação real;
- infraestrutura de trabalho;
- próximo experimento que reduza uma incerteza concreta.

No ambiente VPS, o bloqueio imediato conhecido é o diagnóstico do Code Server antes de qualquer nova alteração.

No ABS em construção, a direção técnica é continuar fechando capacidades reais por integração e evidência, em vez de adicionar componentes indiscriminadamente.

---

# 23. REGRA FINAL DE CONTINUIDADE

Uma nova IA deve assumir:

> **Não estamos começando o Projeto Absoluto.**
>
> **Não estamos começando o ABS.**
>
> Estamos continuando uma construção que já possui código, arquitetura, pesquisas, experimentos, decisões, infraestrutura e histórico.
>
> O trabalho desta etapa foi preservar o entendimento completo necessário para que a construção continue sem depender da conversa anterior.
>
> O Imperador continua sendo a autoridade.
>
> O ABS geral é o ecossistema.
>
> O ABS em construção é o operador/orquestrador desse ecossistema.
>
> O ABS V1 é a primeira versão operacional desse operador.
>
> O próximo passo é construir, testar e provar capacidades reais.

