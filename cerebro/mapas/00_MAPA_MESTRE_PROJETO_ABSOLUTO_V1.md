# MAPA MESTRE ATUAL — PROJETO ABSOLUTO V1

**Status:** referência mestre de navegação do projeto  
**Data:** 2026-09-20  
**Objetivo:** impedir perda de contexto, mistura de mapas e uso de documentos históricos como se fossem estado atual.

---

## 1. REGRA CENTRAL

Este arquivo não substitui os mapas existentes.

Ele é o **índice mestre** que diz:

- qual mapa responde a qual pergunta;
- qual documento é atual, histórico ou operacional;
- onde procurar cada tipo de informação;
- qual é o estado atual conhecido;
- qual é o foco atual sem transformar o projeto em uma fila linear.

**Nenhum mapa individual deve ser usado como se contivesse todo o Projeto Absoluto.**

---

# 2. HIERARQUIA DAS FONTES

Quando houver dúvida, consultar nesta ordem:

### NÍVEL 1 — ESTADO REAL DO SISTEMA
Fonte de verdade para saber o que realmente existe:
- código atual em `abs_core/`;
- testes;
- CI;
- commits/PRs;
- resultados operacionais verificados;
- documentação operacional V1.

### NÍVEL 2 — MAPA MESTRE
Este arquivo:
`cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`

Responde:
- onde está cada mapa;
- qual mapa usar;
- qual é o estado atual;
- como separar passado/presente/futuro;
- qual frente está atualmente em foco.

### NÍVEL 3 — TABULEIRO ESTRATÉGICO
`cerebro/mapas/01_TABULEIRO_72_CAPACIDADES_V0_1.md`

Responde:
- quais capacidades existem no universo do projeto;
- relações;
- dependências;
- caminhos;
- oportunidades;
- estados possíveis.

É uma **rede dinâmica**, não uma lista de tarefas.

### NÍVEL 4 — PLANEJAMENTO DINÂMICO
- `cerebro/mapas/02_QUADRO_PENDENCIAS_CONSTRUCAO_V0_1.md`
- `cerebro/mapas/03_PLANO_REDE_EVOLUTIVA_V0_1.md`

Respondem:
- o que falta;
- quais frentes estão abertas;
- como selecionar movimentos;
- quais capacidades devem ser integradas;
- quais caminhos podem avançar em paralelo.

### NÍVEL 5 — MEMÓRIA / TRANSFERÊNCIA
- `cerebro/TRANSFERENCIA_PROJETO_ABSOLUTO_ESTADO_ATUAL_V1.md`
- `cerebro/STATUS_CEREBRO_LIGADO.md`

Servem para:
- continuidade entre conversas/IA;
- reconstrução de contexto;
- registro de decisões.

**A transferência de 2026-09-19 é um snapshot histórico. Não deve vencer o estado operacional posterior.**

### NÍVEL 6 — HISTÓRICO / PESQUISA
Documentos `RECONSTRUCAO_*`, `RECUPERACAO_*`, resultados históricos e materiais do Sistema antigo.

Servem para:
- descobrir por que uma decisão surgiu;
- recuperar ideias;
- verificar experiências;
- evitar repetir erros;
- recuperar patrimônio perdido.

Não devem ser usados automaticamente como arquitetura atual.

### NÍVEL 7 — MINI-CÉREBRO
`mini-cerebro/`

É patrimônio histórico e camada de investigação/recuperação.

**Não é sinônimo do Cérebro atual do ABS.**

---

# 3. MAPAS EXISTENTES E FUNÇÃO DE CADA UM

| Artefato | Função | Estado de uso |
|---|---|---|
| **MAPA MESTRE ATUAL** | Índice e navegação de todos os mapas | **ATUAL / PRINCIPAL** |
| **TABULEIRO COMPLETO 72** | Universo de capacidades e relações | **ATUAL / ESTRATÉGICO** |
| **QUADRO DE PENDÊNCIAS** | Lacunas e construção | **ATUAL / DINÂMICO** |
| **PLANO REDE EVOLUTIVA** | Método de execução não linear | **ATUAL / MÉTODO** |
| **QUADRO MESTRE STATUS V1 (2026-09-22)** | Estado real consolidado da V1 contra auditoria/código/testes | **ATUAL / FECHAMENTO V1** |
| **ABS FUNDAÇÃO V1** | Contrato da fundação operacional | **ATUAL / OPERACIONAL** |
| **STATUS CÉREBRO LIGADO** | Estado do Cérebro persistente | **ATUAL / ESTADO** |
| **TRANSFERÊNCIA V1** | Pacote de continuidade | **SNAPSHOT / HISTÓRICO** |
| **RECONSTRUÇÕES** | Recuperação causal/histórica | **HISTÓRICO / EVIDÊNCIA** |
| **Plano_Projeto.md** | Visão conceitual antiga | **HISTÓRICO / CONCEITUAL** |
| **mini-cerebro/** | Recuperação e investigação do patrimônio antigo | **HISTÓRICO / PESQUISA** |
| **abs_core/** | Implementação real atual do ABS | **ATUAL / CÓDIGO** |

---

# 4. O QUE É O PROJETO ABSOLUTO

A visão maior permanece:

**Imperador → Visão → Projeto Absoluto → Sistema + Império**

O ABS é o sistema sob controle do Imperador.

Definição de trabalho:

> ABS é o sistema sob controle do Imperador, criado para realizar aquilo que ele determina, utilizando, adquirindo, combinando, criando, substituindo ou desenvolvendo as capacidades, estruturas, recursos e meios necessários.

O ABS não é definido por:
- Android;
- uma IA;
- Codex;
- Cérebro;
- aplicativo;
- servidor;
- arquitetura atual;
- interface;
- Marte.

Esses elementos são meios, capacidades, ambientes ou objetivos.

---

# 5. MAPA DE CONSTRUÇÃO

A arquitetura de construção deve ser lida como capacidades, não como tecnologia:

```
CAPACIDADES
   ↓
INTEGRAÇÕES
   ↓
ORQUESTRAÇÃO
   ↓
EXECUÇÃO
   ↓
CONTINUIDADE
   ↓
CONTROLE
   ↓
INTERFACE
```

Regra:
**capacidades primeiro; interface depois.**

A interface futurística continua sendo uma camada posterior/evolutiva.

---

# 6. ESTADO REAL ATUAL

## 6.1 Fundação ABS

A V1 operacional já possui uma base funcional de:

- intenção;
- trabalho persistente;
- registro de capacidades;
- orquestração;
- execução;
- eventos/estado;
- resultado;
- proveniência;
- continuidade;
- controle;
- adaptador Codex;
- ponte GitHub/Termux;
- atualização externa;
- rollback;
- serviço/continuidade no Android.

Portanto, documentos antigos que dizem que a construção do ABS ainda não começou devem ser tratados como **snapshots anteriores**.

## 6.2 Código atual

`abs_core/` é a implementação operacional atual.

Entre os componentes atuais estão:
- modelos;
- store SQLite;
- API;
- servidor;
- CLI;
- capabilities;
- orchestrator;
- Codex adapter;
- bridge;
- local;
- update manager.

## 6.3 Cérebro

O Cérebro persistente existe como camada documental/persistente no repositório.

Mas ainda há diferença entre:

**Cérebro persistente/documental**

e

**Cérebro plenamente integrado ao ciclo operacional do ABS.**

Essa diferença é uma das principais fronteiras atuais.

---

# 7. FOCO ATUAL

O foco atual não é reconstruir tudo.

O foco é:

> **transformar o conjunto atual de ABS + Cérebro + patrimônio histórico em um sistema coerente de continuidade e construção.**

A frente principal atual é:

```
AUDITAR BASE ATUAL
      ↓
INTEGRAR CÉREBRO
      ↓
LIGAR MEMÓRIA + PROVENIÊNCIA + HISTÓRICO
      ↓
RECUPERAR ESTRUTURAR O PATRIMÔNIO HISTÓRICO
      ↓
TORNAR O CÉREBRO ÚTIL PARA O ABS
      ↓
CONTINUIDADE ENTRE IAs
      ↓
AMPLIAR ORQUESTRAÇÃO E AQUISIÇÃO DE CAPACIDADES
```

Isso representa uma **direção de foco**, não uma fila obrigatória.

---

# 8. FRENTES ATIVAS

### FRENTE A — Estado e organização
Objetivo:
- consolidar a fonte de verdade;
- separar atual/histórico/hipótese;
- eliminar ambiguidades documentais;
- criar navegação confiável.

### FRENTE B — Cérebro vivo
Objetivo:
- ingestão;
- memória;
- temporalidade;
- relações;
- proveniência;
- recuperação;
- aprendizado;
- experiência;
- sabedoria operacional.

### FRENTE C — ABS operacional
Objetivo:
- manter V1 estável;
- corrigir lacunas;
- testar contratos;
- ampliar capacidades sem quebrar continuidade.

### FRENTE D — Patrimônio histórico
Objetivo:
- recuperar Sistema antigo;
- Mini-Cérebro;
- experimentos;
- decisões;
- erros;
- descobertas;
- versões anteriores.

### FRENTE E — Continuidade entre IAs
Objetivo:
- contexto transferível;
- estado transferível;
- handoff;
- portabilidade;
- registro de agentes;
- substituição de IA.

### FRENTE F — Orquestração e aquisição
Objetivo:
- descobrir capacidades;
- avaliar;
- integrar;
- testar;
- registrar;
- substituir;
- criar novas capacidades quando necessário.

### FRENTE G — Interface do Imperador
Objetivo futuro:
- CLI/Web/Android;
- multimodalidade;
- 2D;
- 3D;
- espacial;
- AR/MR/XR;
- interfaces futuras.

**Não usar esta frente para justificar antecipação da interface antes da consolidação operacional.**

---

# 9. O TABULEIRO DE 72 CAPACIDADES

O tabuleiro de 72 capacidades continua válido.

Ele não deve ser convertido em:
- checklist;
- fila;
- cronograma;
- lista de tarefas.

Ele é o **universo de capacidades do Projeto**.

Inclui explicitamente:
- capacidades conhecidas;
- capacidades desconhecidas;
- oportunidades descobertas durante a construção.

A prioridade é determinada dinamicamente pelas relações do tabuleiro.

---

# 10. COMO ESCOLHER UMA AÇÃO

Quando surgir uma necessidade:

```
NECESSIDADE
   ↓
LOCALIZAR NO MAPA
   ↓
VER O QUE JÁ EXISTE
   ↓
CONSULTAR HISTÓRICO
   ↓
VER DEPENDÊNCIAS
   ↓
MAPEAR POSSIBILIDADES
   ↓
PESQUISAR
   ↓
VALIDAR
   ↓
DECIDIR
   ↓
EXECUTAR
   ↓
TESTAR
   ↓
REGISTRAR
   ↓
ATUALIZAR CÉREBRO + ESTADO + MAPA
```

Nunca começar simplesmente por:
**"qual arquivo devo editar?"**

Primeiro descobrir:
**"qual capacidade estamos tentando construir ou corrigir?"**

---

# 11. COMO ENCONTRAR A INFORMAÇÃO CERTA

Esta é a regra operacional de consulta.

### Pergunta: "Isso já existe?"
Consultar primeiro:
1. código atual;
2. testes;
3. documentação V1;
4. commits/PRs;
5. estado do Cérebro.

### Pergunta: "Por que foi feito assim?"
Consultar:
1. decisões;
2. reconstruções causais;
3. histórico;
4. commits;
5. experiências.

### Pergunta: "O que falta?"
Consultar:
1. quadro de pendências;
2. tabuleiro 72;
3. estado atual;
4. testes;
5. lacunas encontradas na auditoria.

### Pergunta: "Qual caminho seguir?"
Consultar:
1. tabuleiro 72;
2. plano de rede evolutiva;
3. dependências;
4. evidências;
5. reversibilidade;
6. valor multiplicador.

### Pergunta: "Qual é o estado real?"
Consultar:
1. código;
2. testes;
3. runtime;
4. GitHub/commits;
5. documentação operacional atual.

### Pergunta: "O que aconteceu no passado?"
Consultar:
1. Mini-Cérebro;
2. reconstruções;
3. arquivos históricos;
4. ZIPs preservados;
5. histórico Git.

---

# 12. REGRA CONTRA CONFUSÃO

Nunca misturar:

**MAPA ≠ IMPLEMENTAÇÃO**

**HIPÓTESE ≠ DECISÃO**

**DECISÃO ≠ CAPACIDADE COMPROVADA**

**CÓDIGO HISTÓRICO ≠ CÓDIGO ATUAL**

**DOCUMENTO DE TRANSFERÊNCIA ≠ ESTADO VIVO**

**MINI-CÉREBRO ≠ CÉREBRO ABS**

**INTERFACE ≠ NÚCLEO**

**ANDROID ≠ IDENTIDADE DO ABS**

**TABULEIRO ≠ FILA DE TAREFAS**

---

# 13. MODELO DE CONTINUIDADE

A fonte da continuidade deve ser:

```
PROJETO ABSOLUTO
       ↓
MAPA MESTRE
       ↓
CÉREBRO
       ↓
ESTADO ATUAL
       ↓
EVIDÊNCIAS
       ↓
DECISÕES
       ↓
HISTÓRICO
       ↓
NOVA IA
```

A conversa é apenas uma interface temporária.

---

# 14. PRÓXIMA OPERAÇÃO

Antes de construir outra grande peça, fazer:

**AUDITORIA DE CONVERGÊNCIA DO ABS ATUAL**

Verificar:

1. o que o ABS V1 realmente faz;
2. o que o Cérebro atual realmente faz;
3. o que o Mini-Cérebro já faz;
4. o que existe duplicado;
5. o que é histórico;
6. o que é atual;
7. o que está faltando;
8. quais capacidades do tabuleiro já estão operacionais;
9. quais capacidades estão parcialmente implementadas;
10. qual integração produz maior valor multiplicador agora.

Resultado esperado:

**um mapa de estado verificável, não uma nova lista inventada.**

---

# 15. PRINCÍPIO FINAL

> **O Projeto Absoluto não precisa ter todos os mapas iguais. Precisa saber qual mapa responde a qual pergunta e qual fonte possui autoridade sobre cada tipo de informação.**

O objetivo deste índice é fazer com que uma IA nova consiga navegar pelo Projeto sem depender da memória de uma conversa específica.

**Mapa mestre → fonte correta → evidência → decisão → execução → resultado → atualização do mapa.**
