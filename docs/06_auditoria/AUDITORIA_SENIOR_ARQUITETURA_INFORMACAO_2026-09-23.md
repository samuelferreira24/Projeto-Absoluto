# AUDITORIA SENIOR — ARQUITETURA DE INFORMAÇÃO DOS DOIS REPOSITÓRIOS

Data: 2026-09-23

## 1. Escopo

Auditoria estrutural de:

- `samuelferreira24/Projeto-Absoluto` — construção atual;
- `samuelferreira24/Sistema` — patrimônio histórico/anterior.

Objetivo: determinar se a organização atual separa corretamente estado atual, conhecimento, decisões, planejamento, operação, evidências, continuidade e histórico, sem apagar conteúdo nem mover código por estética.

Esta auditoria **não executa a reorganização física**. Ela produz a classificação e a arquitetura-alvo para uma etapa posterior.

## 2. Fotografia auditada

### Projeto-Absoluto

- Branch: `main`
- Revisão auditada: `732e47e218b1086b8af1b055b3d4e80358ac1c39`
- Arquivos versionados: 296
- Principais áreas: `abs_core/`, `cerebro/`, `continuidade/`, `docs/`, `20_interface/`, `50_frentes/`, `mini-cerebro/`, `scripts/`, `tests/`, `tools/`, `99_arquivo/`.

### Sistema

- Branch: `main`
- Revisão auditada: `3a973647b76423ed0ab3b7a4293b3ac42b048b2e`
- Arquivos versionados: 60
- Principais áreas: documentação, runtime histórico, interface histórica, continuidade histórica, integração e arquivo.

## 3. Diagnóstico executivo

A organização atual **já possui uma separação conceitual muito melhor do que uma simples sequência cronológica**, mas ainda existe sobreposição entre funções documentais.

O principal problema não é falta de pastas. É a existência de **múltiplas fontes concorrentes para o mesmo tipo de pergunta**.

Exemplos:

- estado atual aparece em `cerebro/00_estado/`, `continuidade/02_estado/`, handoffs e mapas;
- arquitetura aparece em `docs/02_arquitetura/` e `cerebro/especificacao/`;
- histórico aparece em `cerebro/especificacao/07_historico/`, `docs/90_fontes/`, `mini-cerebro/` e `99_arquivo/`;
- continuidade aparece em `continuidade/`, partes de `cerebro/data/` e documentos de operação;
- planejamento aparece em `docs/03_planejamento/` e `cerebro/mapas/`.

Isso não significa que esses documentos sejam duplicados. Muitos têm funções diferentes. O problema é que a função e a autoridade ainda precisam ser mais explícitas.

## 4. O que está correto e deve ser preservado

### 4.1 Dois repositórios com papéis diferentes

A separação entre:

- Projeto-Absoluto = construção atual;
- Sistema = patrimônio histórico;

é correta e deve permanecer.

O repositório `Sistema` não deve ser transformado artificialmente em código atual.

### 4.2 ABS, Cérebro e Mini-Cérebro separados

A separação conceitual está correta:

- `abs_core/` = implementação operacional atual;
- `cerebro/` = conhecimento/estado/mapas/especificações do projeto;
- `mini-cerebro/` = investigação e patrimônio histórico auxiliar.

Não fundir esses papéis apenas para reduzir número de diretórios.

### 4.3 Arquivo histórico preservado

`99_arquivo/` contém patrimônio que deve permanecer preservado e claramente marcado como histórico.

O conteúdo antigo não deve ser tratado como capacidade atual sem validação.

### 4.4 Continuidade como infraestrutura

`continuidade/` já evoluiu de simples "handoff" para mecanismo de transferência entre sessões/IAs.

Isso é correto, mas sua organização precisa ser refinada para evitar que vire um segundo repositório documental paralelo.

### 4.5 Evidência e autoridade

A regra atual está correta:

código/testes/CI/evidência operacional têm precedência para afirmar o que existe atualmente.

Documentação, mapa e histórico explicam; não substituem prova.

## 5. Problemas estruturais encontrados

### P1 — Estado atual distribuído demais

Há vários documentos chamados ou funcionando como "estado atual".

Risco: uma IA nova pode encontrar versões diferentes e escolher a errada.

Correção arquitetural: existir uma **fonte canônica de estado**, com projeções derivadas para navegação/handoff.

### P2 — Handoffs concorrentes

`continuidade/05_handoffs/01_HANDOFF_ATUAL_OPERACIONAL.md` é tratado como oficial, mas existe também:

- `02_HANDOFF_NOVO_CHAT_ABS_V1_PLANEJAMENTO.md`;
- `04_construcao/02_HANDOFF_CONSTRUCAO_ABS_V1.md`;
- `07_conhecimento/SESSAO_ATUAL.md`.

São documentos válidos para contextos diferentes, mas a distinção não é suficientemente forte.

Além disso, o handoff operacional registrado aponta para uma revisão remota anterior (`3d1316d4...`), enquanto a revisão auditada atual é `732e47e...`. Isso demonstra que handoff estático envelhece e não pode ser a fonte primária do estado vivo.

### P3 — Arquitetura dividida entre docs e cérebro

`docs/02_arquitetura/` e `cerebro/especificacao/` possuem funções próximas.

A divisão pode permanecer, mas precisa de uma regra inequívoca:

- arquitetura/contrato estável;
- especificação de comportamento/estado/construção do Cérebro;
- projeções não devem competir pela mesma autoridade.

### P4 — Histórico espalhado em quatro mecanismos

Há histórico em:

- `cerebro/especificacao/07_historico/`;
- `docs/90_fontes/`;
- `mini-cerebro/`;
- `99_arquivo/`.

Eles não são equivalentes.

O problema é de taxonomia, não necessariamente de conteúdo.

### P5 — Continuidade mistura tipos de informação

Dentro de `continuidade/` existem:

- contexto;
- estado;
- decisões;
- construção;
- handoff;
- interface;
- conhecimento;
- legado.

A ideia é válida, mas "interface" é uma frente temática, enquanto os demais são funções de continuidade. Isso cria uma mistura de **tipo de informação** com **assunto**.

### P6 — Numeração física ainda sugere sequência

A numeração atual é melhor que uma sequência cronológica pura, mas nomes como `01`, `02`, `03` podem continuar sendo interpretados como ordem de execução.

O próprio projeto já afirma que a numeração é classificatória. Essa regra deve ser mantida e reforçada nos índices.

### P7 — Raiz possui mais de uma porta de entrada

Existem:

- `README.md`;
- `00_IA_NAVEGACAO.md`;
- `00_ESTRUTURA_REPOSITORIO.md`;
- `ESTRUTURA_REPOSITORIOS.md);
- `AGENTS.md).

Cada um possui função legítima, mas uma IA nova ainda precisa descobrir qual ler primeiro.

A solução não é apagar os arquivos. É declarar uma cadeia de autoridade:

`AGENTS.md` → navegação → estrutura → estado vivo → fonte específica.

### P8 — Fontes e patrimônio estão bem preservados, mas muito grandes

`99_arquivo/O-IMPERIO-COMPLETO-claude/` contém um grande pacote histórico, incluindo código, documentação e material de cliente.

Isso é correto como preservação, mas não deve contaminar a navegação operacional.

O índice precisa deixar explícito: **preservado não significa recomendado para construção atual**.

## 6. Classificação funcional definitiva proposta

A arquitetura de informação deve usar estas classes:

| Classe | Pergunta que responde | Autoridade |
|---|---|---|
| Estado | O que existe agora? | código + testes + runtime + evidência |
| Conhecimento | O que o projeto sabe? | Cérebro/conhecimento estruturado |
| Decisão | O que foi decidido pelo Imperador? | registro de decisão autorizado |
| Arquitetura | Como o sistema deve ser estruturado? | contratos/arquitetura atuais |
| Planejamento | Quais possibilidades e direções existem? | mapas/tabuleiro/planejamento |
| Operação | Como usar o que existe? | documentação operacional + código |
| Evidência | O que foi realmente observado/testado/executado? | evidência verificável |
| Continuidade | O que uma nova sessão precisa recuperar? | estado + checkpoint derivado |
| Histórico | O que aconteceu antes? | histórico/legado/fontes |
| Fonte | De onde veio uma informação? | documento/arquivo/origem |
| Código | O que está implementado? | repositório executável |
| Teste | O que foi verificado? | suíte/CI/resultados |

## 7. Arquitetura-alvo de informação

Não é necessário criar dezenas de pastas imediatamente.

A estrutura lógica-alvo é:

```
Projeto-Absoluto/
├── código atual
│   ├── abs_core/
│   ├── cerebro/
│   ├── mini-cerebro/
│   └── 20_interface/
│
├── conhecimento e estado
│   └── continuidade/07_conhecimento + estado vivo
│
├── decisões
│   └── registros autorizados
│
├── arquitetura e documentação
│   └── docs/
│
├── mapas e planejamento
│   └── cerebro/mapas/ + planejamento
│
├── evidências
│   └── Project Knowledge / testes / CI / registros
│
├── sessões
│   └── checkpoints de sessão
│
├── fontes
│   └── docs/90_fontes/
│
├── histórico
│   ├── cerebro/especificacao/07_historico/
│   ├── mini-cerebro/
│   └── 99_arquivo/
│
└── operação
    ├── scripts/
    ├── tests/
    └── ferramentas
```

A consequência importante é: **a classificação lógica deve vir antes da mudança física**.

## 8. O que NÃO deve ser movido agora

Não mover apenas por estética:

- `abs_core/`;
- `cerebro/`;
- `mini-cerebro/`;
- `20_interface/`;
- `tests/`;
- `scripts/`.

Esses caminhos possuem identidade operacional e referências existentes.

Também não mover o conteúdo de `99_arquivo/` antes de inventariar dependências e valor histórico.

## 9. O que deve ser consolidado primeiro

A primeira consolidação deve ser documental:

1. definir uma única fonte canônica de estado vivo;
2. fazer `project_knowledge.json` representar o estado estruturado;
3. tratar `MAPA_AUTO_ESTADO_PROJETO.md` como projeção humana;
4. transformar handoff em projeção/checkpoint, não fonte primária;
5. registrar sessões em estrutura própria;
6. separar decisão de planejamento;
7. separar evidência de documentação;
8. criar índices por pergunta, não apenas por pasta.

## 10. Regra para duplicatas

Nunca comparar somente pelo título.

Para cada documento aparentemente duplicado, classificar:

`tema + função + autoridade + temporalidade + origem`.

Somente se os cinco forem equivalentes considerar consolidação.

Se o conteúdo for historicamente valioso, preservar o original e criar referência para a fonte canônica.

## 11. Regra para o Sistema histórico

O repositório `Sistema` deve ser tratado como:

**patrimônio histórico/P&D**, não como segundo runtime concorrente.

Seu código pode alimentar investigação, comparação, reconstrução e recuperação de conhecimento, mas não deve competir com `Projeto-Absoluto/abs_core/` como implementação atual.

## 12. Resultado da auditoria

### Classificação

- Organização conceitual: **boa e em evolução**.
- Separação atual/histórico: **boa**.
- Preservação histórica: **forte**.
- Fonte única de estado: **ainda insuficientemente consolidada**.
- Continuidade entre IAs: **funcional, mas parcialmente documental**.
- Taxonomia documental: **precisa refinamento**.
- Duplicação literal: **não é o principal problema**.
- Duplicação semântica/função: **principal problema documental**.
- Risco de quebrar código por reorganização: **alto se houver movimentação prematura**.

## 13. Próxima etapa correta

A próxima etapa não deve ser "mover tudo".

Deve ser:

**INVENTÁRIO → CLASSIFICAÇÃO → AUTORIDADE → ÍNDICE → REFERÊNCIAS → MIGRAÇÃO CONTROLADA**

Somente depois:

**MOVER/RENOMEAR → TESTAR → ATUALIZAR REFERÊNCIAS → CI → VALIDAR CONTINUIDADE**

## 14. Princípio final

> O Projeto Absoluto não precisa de menos informação. Precisa que cada informação tenha lugar, função, autoridade, temporalidade e caminho de recuperação claramente definidos.

A organização deve permitir que uma nova IA responda rapidamente:

**onde estou → o que existe → o que é verdade agora → por que existe → o que foi decidido → o que foi provado → o que é histórico → qual é o próximo contexto de trabalho.**
