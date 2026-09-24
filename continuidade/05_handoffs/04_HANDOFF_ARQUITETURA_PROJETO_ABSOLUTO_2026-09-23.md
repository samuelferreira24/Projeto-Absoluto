# HANDOFF — ARQUITETURA DO PROJETO ABSOLUTO — 2026-09-23

## 1. PONTO EXATO

Este handoff transfere a sessão para outra IA.

Repositório principal:
`samuelferreira24/Projeto-Absoluto`

Branch de continuidade:
`main`

Estado verificado no GitHub:
- PR #69 — merged
- PR #70 — merged
- PR #72 — merged
- PR #73 — merged
- PR #71 — fechado sem merge
- último merge verificado nesta auditoria: PR #76 → commit `d506d120b69c7330f6580d0172f714bb360645cd`

Não começar novamente. O trabalho de arquitetura de informação já avançou várias etapas.

---

## 2. DEFINIÇÃO CONCEITUAL CONSOLIDADA

### Projeto Absoluto

É o projeto maior.

É onde está a visão, método, princípios, objetivos e direção do Imperador.

Não é sinônimo de:
- Sistema;
- ABS;
- aplicativo;
- IA;
- repositório.

A implementação completa ainda está em descoberta.

### Sistema

É uma peça/infraestrutura criada para aumentar a capacidade do Imperador de:
- pesquisar;
- aprender;
- descobrir ferramentas;
- planejar;
- construir;
- testar;
- executar;
- registrar resultados;
- preservar continuidade;
- aprender com resultados.

O Sistema é meio de execução e ampliação de capacidade, não o objetivo superior.

### ABS

ABS é o primeiro projeto que o Imperador está tentando construir dentro do Projeto Absoluto.

ABS não é sinônimo do Sistema.

ABS V1 é o segundo protótipo do ABS. Futuras versões continuam abertas.

Outros projetos poderão surgir no Projeto Absoluto e poderão:
- reutilizar o Sistema/ABS;
- usar apenas algumas capacidades;
- criar capacidades próprias;
- não depender do Sistema/ABS.

### Aprender enquanto constrói

O Imperador não sabe antecipadamente como implementar tudo que imaginou.

O processo real é:

VISÃO → necessidade → pesquisa → aprendizagem → hipótese → experimento → construção → teste → resultado → conhecimento → capacidade → novo ciclo.

IAs são ferramentas de pesquisa, aprendizagem e construção.

A arquitetura futura não deve ser presumida como totalmente conhecida.

---

## 3. FONTE CONCEITUAL PRINCIPAL

Documento criado e versionado:

`docs/00_MODELO_PROJETO_ABSOLUTO.md`

Ele formaliza a relação:

Projeto Absoluto → Sistema + Projetos + Império + Histórico/Conhecimento

e define ABS como primeiro projeto.

Os arquivos-base da visão original continuam sendo fontes de origem e não devem ser reescritos como documentação técnica do ABS.

---

## 4. O QUE FOI CONSTRUÍDO NA ORGANIZAÇÃO

### PR #68 — Project Knowledge / continuidade

Foi criada a primeira camada estruturada de continuidade e conhecimento observável.

Principais elementos:
- `AGENTS.md`
- `continuidade/07_conhecimento/project_knowledge.json`
- `continuidade/07_conhecimento/MAPA_AUTO_ESTADO_PROJETO.md`
- modelo de evidências;
- paths;
- proveniência;
- runtime snapshot;
- registro de execução;
- projeções automáticas;
- workflow de atualização.

Correção importante feita durante essa etapa:
o workflow não detectava arquivos novos com `git diff --quiet`; isso foi corrigido para usar `git status --porcelain`, permitindo persistir corretamente as projeções.

### PR #69 — Governança e modelo conceitual

Criou:
- `docs/00_GOVERNANCA_INFORMACAO.md`
- `docs/00_MODELO_PROJETO_ABSOLUTO.md`
- inventário documental;
- inventário físico inicial;
- portas de entrada para IA;
- regras de autoridade;
- distinção estado/projeção/handoff;
- regra de persistência de sessão.

### PR #70 — Arquitetura

Foi consolidada a área arquitetural em:
`docs/02_arquitetura/`

A antiga:
`docs/architecture/`

foi eliminada como área concorrente.

Nenhum código operacional foi movido.

### PR #72 — Estado, continuidade e interface

Foram auditadas e reclassificadas:
- estado;
- continuidade;
- handoffs;
- interface.

A documentação temática de interface deixou de ficar em `continuidade/06_interface/` e foi distribuída por função:
- pesquisa → `docs/90_fontes/`;
- arquitetura → `docs/02_arquitetura/`;
- planejamento → `docs/03_planejamento/`.

Snapshots antigos foram preservados como históricos/handoffs.

O quadro de status ABS foi reclassificado para:
`cerebro/00_estado/STATUS_ABS_V1_2026-09-22.md`

### PR #73 — Fontes, histórico, Mini-Cérebro e arquivo

Foi concluída a auditoria dessa fronteira.

Conclusão:
- `docs/90_fontes/` = fontes de origem/preservadas;
- `cerebro/especificacao/07_historico/` = conhecimento histórico derivado;
- `cerebro/especificacao/legado_reintegrado/` = especificações recuperadas do legado;
- `mini-cerebro/` = investigação histórica;
- `99_arquivo/` = patrimônio histórico/legado.

Nenhuma migração ampla foi considerada necessária.

Regra de promoção histórica:
1. fonte identificada;
2. interpretação explícita;
3. decisão/autorização quando necessária;
4. implementação atual;
5. teste/evidência correspondente.

---

## 5. ESTADO ATUAL DA ARQUITETURA DE INFORMAÇÃO

### Autoridade

Para saber o que existe agora:
**código + testes + CI + evidência operacional > documentação antiga/handoff**

Para visão, princípios e direção:
**registros autorizados do Imperador**

Para estado estruturado:
**Project Knowledge**

Para projeção humana:
**MAPA_AUTO_ESTADO_PROJETO.md**

Para decisões:
`continuidade/03_decisoes/`

Para continuidade:
checkpoints/handoffs

Para passado:
fontes/histórico/arquivo preservado

### Taxonomia

A organização utiliza as classes:
- Estado
- Conhecimento
- Decisão
- Arquitetura
- Planejamento
- Operação
- Evidência
- Continuidade
- Histórico
- Fonte
- Referência
- Tutorial/How-to

### Regra central

Organização não significa criar uma árvore bonita.

Significa tornar explícito:

**onde está → o que é → qual autoridade possui → como verificar.**

---

## 6. ESTADO OPERACIONAL DO ABS

O ABS Core já existe em `abs_core/`.

A fundação inclui, conforme estado documentado:
- intenção;
- Work persistente;
- registro de capacidades;
- orquestração;
- execução;
- estado/eventos;
- resultados;
- proveniência;
- sessões;
- continuidade;
- servidor/local;
- bridge;
- Codex adapter;
- update manager;
- rollback.

O estado operacional real deve ser confirmado por código/testes/CI antes de qualquer nova conclusão.

Não confundir:
- documentação com prova;
- código com capacidade comprovada;
- capacidade com autorização.

---

## 7. CÉREBRO E MINI-CÉREBRO

### Cérebro

`cerebro/` contém:
- conhecimento;
- mapas;
- especificações;
- estado;
- testes.

O Cérebro persistente/documental existe, mas a integração operacional completa continua sendo uma fronteira de evolução.

### Mini-Cérebro

`mini-cerebro/` é patrimônio e ferramenta de investigação histórica do Sistema antigo.

Não é:
- o ABS;
- o Cérebro atual;
- arquitetura operacional atual.

Sua função é recuperar evidências, experimentos, decisões, falhas e descobertas do passado.

---

## 8. MAPAS

Mapa Mestre:
`cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`

O mapa mestre é índice/navegação.

O Tabuleiro de 72 capacidades é universo de capacidades e relações.

O Quadro de Pendências representa lacunas/construção.

O Plano de Rede Evolutiva representa método de execução não linear.

Mapas não são:
- código;
- prova operacional;
- fila obrigatória;
- substituto do estado vivo.

Planejamento:
`docs/03_planejamento/`

Mapas:
`cerebro/mapas/`

Essas áreas foram auditadas e consideradas complementares.

---

## 9. PRINCIPAIS DOCUMENTOS DE ENTRADA PARA A NOVA IA

Ordem recomendada:

1. `AGENTS.md`
2. `00_IA_NAVEGACAO.md`
3. `docs/00_GOVERNANCA_INFORMACAO.md`
4. `docs/00_MODELO_PROJETO_ABSOLUTO.md`
5. `00_ESTRUTURA_REPOSITORIO.md`
6. `continuidade/07_conhecimento/project_knowledge.json`
7. `continuidade/07_conhecimento/MAPA_AUTO_ESTADO_PROJETO.md`
8. `continuidade/07_conhecimento/SESSAO_ATUAL.md`
9. `cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`
10. fonte específica conforme a pergunta.

Depois verificar código/testes relevantes.

---

## 10. ETAPA DE AUDITORIA CONCLUÍDA

A auditoria de referências e órfãos documentais foi executada após o PR #73.

Foram concluídas as correções comprovadas:
- PR #74 — remoção de seis cópias antigas já migradas e correção de referência obsoleta a `docs/architecture/`;
- PR #75 — remoção do quadro de status duplicado de `cerebro/mapas/`;
- PR #76 — remoção da cópia duplicada do snapshot de transferência em `cerebro/00_estado/`.

Validação final:
- caminhos antigos auditados não aparecem mais na árvore atual;
- não restam documentos Markdown/TXT com blob SHA idêntico entre caminhos diferentes;
- código, testes e cinco fontes-base não foram alterados nessa rodada.

A próxima etapa é **auditar a consistência dos índices, referências cruzadas e documentos órfãos sem conteúdo duplicado**, corrigindo apenas problemas comprovados.

---

## 11. O QUE NÃO FAZER

Não:
- começar novamente o ABS;
- reconstruir Project Knowledge;
- recriar mapas;
- recriar Mini-Cérebro;
- mover código por estética;
- apagar patrimônio histórico;
- reescrever fontes-base;
- assumir que arquitetura antiga é final;
- transformar hipótese em fato;
- tratar ABS como sinônimo do Sistema;
- tratar Projeto Absoluto como sinônimo do ABS;
- transformar o repositório na definição conceitual do projeto;
- criar uma arquitetura futura antes de existir evidência.

---

## 12. REGRA DE TRABALHO

O usuário quer trabalho profissional/sênior.

Método:

**Já existe? → verificar.  
Funciona? → testar.  
É necessário? → validar.  
Pode integrar? → integrar.  
Só construir se realmente faltar.**

A organização deve servir à construção, não virar um projeto de organização infinito.

O objetivo final desta frente é permitir que qualquer nova IA consiga recuperar:

**visão → Sistema → projeto → ABS → estado → decisão → evidência → planejamento → histórico → ponto de retomada**

sem depender da conversa anterior.

---

## 13. PONTO DE RETOMADA

A nova IA deve começar lendo este handoff e os documentos de entrada, depois verificar o estado real de `main`.

Em seguida:

**referências e órfãos → validação → correções pequenas → testes/validação → próxima decisão.**

Não avançar para nova migração física antes de concluir essa auditoria.

