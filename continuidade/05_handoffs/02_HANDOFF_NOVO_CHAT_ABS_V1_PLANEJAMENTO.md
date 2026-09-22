# HANDOFF — CONSTRUÇÃO DO PROJETO ABSOLUTO / ABS V1

## 0. MISSÃO DESTE HANDOFF

Você é a IA que continuará a construção do Projeto Absoluto em um novo chat.

Não comece reinventando o projeto.

Primeiro **aprenda o sistema existente, opere o ABS atual, entenda os mecanismos já construídos e só depois proponha ou execute novas mudanças**.

O objetivo é continuar a evolução do ABS V1 sobre a fundação existente.

---

## 1. O QUE É O PROJETO ABSOLUTO

Projeto Absoluto não é apenas um aplicativo, startup ou empresa.

É a construção de um sistema sob controle do Imperador, capaz de adquirir, combinar, criar, substituir e desenvolver os meios necessários para executar objetivos.

Princípio central:

**ABS = o sistema sob controle do Imperador, criado para realizar aquilo que ele determina, utilizando, adquirindo, combinando, criando, substituindo ou desenvolvendo quaisquer capacidades, estruturas, recursos e meios necessários para isso.**

Invariantes:

- continuidade;
- controle pelo Imperador;
- capacidade de evoluir;
- nenhuma tecnologia específica é o fim do projeto.

---

## 2. MÉTODO DO PROJETO

O método de trabalho do projeto é:

**PP + BN + AV**
- Primeiros Princípios;
- Bola de Neve;
- Avalanche.

O ciclo é iterativo:

**BN → PP → AV → novo BN**

Planejamento não é tratado como fila fixa. O sistema deve descobrir necessidades novas durante a execução.

Mecanismo permanente:

**planejamento → execução → observação → descoberta → pesquisa → reavaliação → cérebro/tabuleiro → novo planejamento.**

---

## 3. ARQUITETURA DE LONGO PRAZO

A cadeia conceitual é:

**Visão → Princípios → Método → Arquitetura → Fundação → Cérebro → Estado → Identidade → Interfaces → Integração → Execução → Automação → Multi-IA → Orquestração → Hierarquia → Inteligência coletiva → Auditoria → Segurança → Governança → Observabilidade → Aprendizado → Evolução → Continuidade → Portabilidade → Operação contínua → Expansão → Novos sistemas → Escala → Realidade externa → Evolução aberta.**

Não interprete isso como uma lista de funcionalidades já implementadas.

---

## 4. REPOSITÓRIO PRINCIPAL

GitHub:

`samuelferreira24/Projeto-Absoluto`

Branch operacional:

`main`

Estrutura importante:

- `abs_core/` — runtime operacional atual do ABS V1;
- `cerebro/` — cérebro atual, mapas, especificações, estado e testes;
- `mini-cerebro/` — componente histórico/arquitetural que deve ser preservado;
- `continuidade/` — continuidade operacional;
- `docs/` — documentação classificada;
- `scripts/` — operação e Termux;
- `tests/` — testes atuais;
- `20_interface/` — interface;
- `50_frentes/` — frentes de execução;
- `99_arquivo/` — patrimônio histórico/legado.

Existe também o repositório histórico:

`samuelferreira24/Sistema`

Não assumir que o histórico é inútil. Ele contém experimentos e origem arquitetural.

---

## 5. ABS V1 ATUAL

O ABS V1 existente em `abs_core/` já possui:

- Work/state/event model;
- SQLite persistence;
- capability registry;
- orchestrator;
- Codex CLI adapter;
- OpenAI/Claude/Gemini adapters;
- Internet HTTP;
- resources/devices;
- connection registry;
- resource routing;
- resource dispatch;
- accounts;
- tool catalog;
- tool discovery;
- tool knowledge;
- tool planner;
- tool learning;
- interface runtime;
- local server/API;
- continuity snapshots;
- update manager;
- bridge;
- testes automatizados.

Ele é **fundação operacional real**, mas ainda não é o ABS completo planejado.

---

## 6. PRIMEIRA REGRA: APRENDA A OPERAR ANTES DE CONSTRUIR

Antes de alterar arquitetura:

1. leia `abs_core/README.md`;
2. leia `continuidade/00_LEIA_PRIMEIRO.md`;
3. leia `continuidade/01_ESTADO_ATUAL_PROJETO.md`;
4. leia `continuidade/02_MODELO_ABS_E_PRINCIPIOS.md`;
5. leia `continuidade/03_HISTORICO_SISTEMA_ANTIGO_E_MINI_CEREBRO.md`;
6. leia `continuidade/04_PONTO_EXATO_DE_PARADA.md`;
7. leia `continuidade/05_DECISOES_CORRECOES_E_REGRAS.md`;
8. leia este handoff;
9. leia `docs/02_arquitetura/`;
10. leia os mapas em `cerebro/mapas/`;
11. leia o planejamento em `cerebro/especificacao/05_planejamento/`;
12. leia `docs/06_ROTEAMENTO_DE_RECURSOS_V1.md`;
13. leia `docs/07_CONHECIMENTO_E_DESCOBERTA_DE_FERRAMENTAS_V1.md`;
14. leia `docs/08_PLANEJAMENTO_E_APRENDIZAGEM_DE_FERRAMENTAS_V1.md`;
15. leia `docs/09_MEMORIA_PERSISTENTE_DE_FERRAMENTAS_V1.md`.

Depois disso, inspecione o código real.

---

## 7. OPERAÇÃO NO ANDROID / TERMUX

O ambiente histórico de operação é Android + Termux.

Projeto local:

`/data/data/com.termux/files/home/Projeto-Absoluto`

O ambiente conhecido inclui:

- Termux;
- Python;
- Node.js;
- Git;
- Ubuntu via proot-distro;
- Codex CLI;
- Termux:Boot;
- termux-services/runit.

Não assuma que uma ferramenta está disponível só porque existe no código.

Primeiro verificar:

`git status`

`git log --oneline -10`

`python --version`

`git --version`

`codex --version`

Depois verificar ABS:

`python -m abs_core.cli --help`

e iniciar/consultar o serviço conforme os scripts/documentação atuais.

Health esperado quando o serviço estiver ativo:

`http://127.0.0.1:8787/health`

O resultado saudável deve indicar ABS vivo e versão V1.

---

## 8. FERRAMENTAS E MECANISMOS QUE JÁ EXISTEM

### Execução
`Orchestrator`

### Capacidades
`CapabilityRegistry`

### Memória operacional
`WorkStore`

### Recursos
`ResourceManager`

### Conexões
`ConnectionRegistry`

### Roteamento
`ResourceRouter`

### Dispatch
`ResourceDispatcher`

### Conhecimento de ferramentas
`ToolKnowledgeRegistry`

### Descoberta
`ToolDiscovery`

### Planejamento
`ToolPlanner`

### Aprendizado
`ToolLearningEngine`

### Continuidade
`abs_core/continuity.py`

### Atualização
`abs_core/update_manager.py`

### Interface
`InterfaceRuntime`

### Cérebro
`cerebro/`

### Mini-Cérebro
`mini-cerebro/`

Não recriar nenhum desses mecanismos sem primeiro verificar se a função já existe.

---

## 9. DISTINÇÕES CRÍTICAS

### Código ≠ capacidade comprovada

Uma classe implementada não prova que o recurso funciona no ambiente real.

### Catálogo ≠ ferramenta operacional

Uma ferramenta registrada não significa que está instalada, autenticada ou disponível.

### Descoberta ≠ confiança

Descobrir uma ferramenta apenas cria conhecimento/candidato.

### Seleção ≠ execução

O router escolhe uma rota; isso não significa que ela é executável.

### Planejamento ≠ execução

Planner produz plano. Dispatcher/Orchestrator executam.

### Interface ≠ núcleo

Interface controla/acessa o sistema; não é o sistema.

### Documento ≠ verdade operacional

Código + testes + resultados verificáveis têm prioridade para determinar o estado atual.

---

## 10. CÉREBRO E MINI-CÉREBRO

Não apagar.

O `mini-cerebro/` é histórico/arquitetural e contém ideias importantes de ingestão, preservação, hash, inventário, FTS, evidências, relações e investigação.

O `cerebro/` atual contém estado, reconstruções, especificações e mapas.

Existe convergência testada entre cérebro e ABS Core, mas isso não significa que eles tenham virado um único componente completo.

A integração deve preservar:

**fonte histórica → interpretação atual → reconciliação → execução verificável.**

---

## 11. MAPAS

O projeto já possui mapas.

Principalmente:

`cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`

`cerebro/mapas/01_TABULEIRO_72_CAPACIDADES_V0_1.md`

`cerebro/mapas/02_QUADRO_PENDENCIAS_CONSTRUCAO_V0_1.md`

`cerebro/mapas/03_PLANO_REDE_EVOLUTIVA_V0_1.md`

Não criar outro "mapa mestre" sem necessidade.

O tabuleiro de 72 capacidades é dinâmico e serve para orientar a construção; não é uma fila linear.

---

## 12. SEGURANÇA E CONTROLE

Nunca remover o mecanismo de aprovação para capacidades externas apenas para simplificar testes.

Nunca usar execução perigosa sem necessidade e autorização.

Nunca apagar dados históricos porque parecem antigos.

Nunca assumir que uma integração funciona sem testar.

Quando algo não for compreendido:

**inspecionar → pesquisar → testar → documentar.**

Não apagar.

---

## 13. COMO CONTINUAR A CONSTRUÇÃO

A sequência recomendada para o novo chat é:

### Fase A — dominar o existente
Operar ABS V1 e executar testes.

### Fase B — validar fronteiras
Verificar cérebro, recursos, ferramentas, conexões, continuidade e interface.

### Fase C — identificar o próximo gargalo real
Usar o mecanismo de descoberta/reavaliação e o tabuleiro existente.

### Fase D — projetar
Primeiros Princípios + evidência do sistema atual.

### Fase E — implementar
Alteração pequena, testável e reversível.

### Fase F — provar
Testes + execução real quando possível + CI.

### Fase G — registrar
Atualizar continuidade, estado e conhecimento.

### Fase H — reavaliar
Perguntar o que a implementação revelou que ainda falta.

Depois repetir.

---

## 14. AUDITORIA SENIOR DE 2026-09-22

A auditoria atual concluiu:

**ABS V1 = fundação operacional real, ainda incompleta em relação ao Projeto Absoluto total.**

Principais próximos gaps:

1. transformar cérebro + execução em ciclo cognitivo contínuo;
2. fechar descoberta → pesquisa → validação → conexão → teste → operação → aprendizado;
3. fortalecer memória persistente de conhecimento de ferramentas;
4. evoluir roteamento de recursos;
5. evoluir orquestração para objetivos compostos/multietapas;
6. preservar controle do Imperador;
7. manter continuidade e reavaliação permanentes.

Leia a auditoria completa em:

`docs/06_auditoria/AUDITORIA_SENIOR_ABS_V1_2026-09-22.md`

---

## 15. REGRA FINAL PARA O NOVO CHAT

Você não recebeu um projeto vazio.

Você recebeu um sistema já construído, testado e documentado, com partes históricas e partes atuais.

Seu trabalho é:

**entender → operar → auditar → descobrir → planejar → construir → testar → registrar → continuar.**

Não apagar.
Não reinventar.
Não assumir.
Não confundir documentação com capacidade.
Não confundir código com capacidade comprovada.

Quando houver dúvida sobre uma parte do sistema, investigue antes de removê-la.
