# DOIS CÉREBROS — EXECUÇÃO DA FASE 0
## Auditoria inicial e arquitetura de integração
## 2026-09-19

> Documento complementar. Não substitui nem apaga histórico.

### 1. OBJETIVO

Estabelecer a ligação futura entre:

- Cérebro do Projeto Absoluto: estado, conhecimento e operação atuais.
- Mini-Cérebro histórico: recuperação e investigação do patrimônio do repositório Sistema.

A Fase 0 é não destrutiva.

### 2. REGRA DE PRESERVAÇÃO

O repositório `samuelferreira24/Sistema` permanece somente como fonte histórica nesta etapa.

Não foram realizadas alterações, commits, exclusões, renomeações ou reorganizações nele.

O conhecimento derivado deve manter referência à fonte quando possível.

### 3. CONSTATAÇÕES NO SISTEMA ANTIGO

Foram lidos diretamente, entre outros, os seguintes materiais:

- `MEMORIA.md`
- `NATIVO.md`
- `P1-SISTEMA-PROPRIO.md`
- `base.py`
- `coletor.py`
- `executor.py`
- `orquestrador.py`
- `ponte.py`
- `semente-nucleo.json`

A análise inicial confirma que o Sistema antigo já continha componentes que são diretamente relevantes para o desenho do Mini-Cérebro.

### 4. DESCOBERTA IMPORTANTE — MEMÓRIA INDEPENDENTE DA INTERFACE

`MEMORIA.md` estabelece explicitamente que o dado deve sobreviver à troca da interface.

O contrato descrito permite que diferentes cascas leiam/escrevam o mesmo formato e determina separação entre memória de método/estado e CONTEXTO externo.

Isto é uma ideia arquitetural relevante para o Mini-Cérebro:

**fonte de conhecimento ≠ interface que o consulta.**

### 5. DESCOBERTA — BASE CONSULTÁVEL

`base.py` já implementa conceitualmente uma infraestrutura de dados com:

- SQLite;
- FTS5;
- impressão digital/deduplicação;
- busca textual;
- busca semântica por vetores;
- busca combinada;
- metadados de fonte;
- registro de uso.

Portanto, não é necessário assumir que o Mini-Cérebro precisa começar de uma base vazia.

### 6. DESCOBERTA — INGESTÃO E PROVENIÊNCIA

`coletor.py` demonstra experiência anterior com:

- múltiplas fontes;
- classificação;
- neutralização de conteúdo externo;
- identificação de conteúdo suspeito;
- geração de blocos de contexto;
- biblioteca de conhecimento.

Isso fornece material para estudar uma camada de ingestão segura.

### 7. DESCOBERTA — EXECUÇÃO SEPARADA DE AUTORIZAÇÃO

`executor.py` contém uma separação importante:

**capacidade disponível ≠ capacidade autorizada.**

Também há experimentos com:

- sandbox;
- snapshots;
- rollback;
- bloqueio de comandos;
- isolamento de privilégios;
- escalada humana para ações sensíveis.

Esse princípio deve ser preservado na futura ponte dos cérebros.

### 8. DESCOBERTA — ORQUESTRAÇÃO

`orquestrador.py`, `especialistas.py` e `jetro.py` registram experimentos anteriores de coordenação de múltiplos componentes.

Não serão tratados automaticamente como arquitetura definitiva.

Devem ser estudados como patrimônio de engenharia e como evidência das soluções já experimentadas.

### 9. DESCOBERTA — PONTE

`ponte.py` demonstra uma experiência anterior de comunicação local entre componentes por HTTP, incluindo autenticação e tarefas.

É candidato natural para investigação como antecedente da futura Ponte dos Cérebros, mas não está aprovado para reutilização direta.

### 10. CÉREBRO ABS ATUAL

O conhecimento atual do Projeto Absoluto já estabelece:

- ABS sob controle do Imperador;
- memória/conhecimento estruturados;
- proveniência como requisito;
- distinção entre fato, hipótese, experimento e capacidade;
- preservação histórica;
- Android como primeiro território tecnológico;
- arquitetura ainda evolutiva;
- princípio de não apagar conhecimento para simplificar.

### 11. ARQUITETURA PROVISÓRIA DOS DOIS CÉREBROS

```
                    IMPERADOR
                        |
                        v
                 CÉREBRO ABS
                        |
                  consulta/correção
                        |
                        v
                PONTE DOS CÉREBROS
                        |
                  evidência/pesquisa
                        |
                        v
                MINI-CÉREBRO
                        |
             +----------+----------+
             |          |          |
          arquivos      Git     histórico
             |
             v
       SISTEMA ANTIGO
```

### 12. REGRA DE COMUNICAÇÃO

A ponte não sincronizará automaticamente todas as memórias.

O fluxo preferencial é:

**consulta → recuperação → evidência → resposta → decisão de incorporação.**

Isso preserva a independência dos dois cérebros.

### 13. DIREÇÃO DOS DADOS

Mini-Cérebro → ABS:

- evidências históricas;
- documentos;
- conclusões registradas;
- experimentos;
- falhas;
- descobertas;
- lacunas;
- hipóteses históricas.

ABS → Mini-Cérebro:

- perguntas;
- solicitações de investigação;
- correções de interpretação;
- novas classificações;
- relações descobertas;
- pedidos de aprofundamento.

### 14. REGRA EPISTEMOLÓGICA

A fonte original não será reescrita para concordar com o conhecimento atual.

Quando houver divergência:

**histórico antigo permanece histórico; interpretação atual permanece atual.**

A reconciliação ocorre em uma camada superior.

### 15. PRIMEIRA INTERFACE DE CONSULTA

A primeira versão deve poder receber uma consulta com:

- origem;
- destino;
- pergunta;
- escopo;
- profundidade;
- filtros opcionais.

E retornar:

- resultado;
- evidências;
- fontes;
- conflitos;
- lacunas;
- inferências.

O protocolo exato permanece aberto até a conclusão da auditoria.

### 16. ESTADO DA EXECUÇÃO

FASE 0 — Auditoria: **em execução**

Já realizado:
- identificação dos dois repositórios;
- validação de acesso ao repositório histórico;
- leitura direta de documentos e componentes-chave;
- identificação de infraestrutura de memória, busca, coleta, execução, orquestração e ponte;
- leitura do estado consolidado do Cérebro ABS;
- primeira identificação das convergências.

Ainda falta:
- varredura integral dos documentos históricos;
- reconstrução completa da evolução por commits;
- identificação completa das conclusões e relatórios;
- auditoria integral do Cérebro ABS;
- definição final do contrato da ponte.

### 17. LIMITAÇÃO ATUAL DO CONECTOR

O repositório histórico está acessível, mas a instalação do GitHub informa que o code search não está indexado para esse repositório.

Por isso, a descoberta automática de todos os documentos por busca textual não é confiável.

A estratégia adotada é leitura direta de arquivos conhecidos + investigação incremental, sem inventar conteúdo ausente.

### 18. PRÓXIMA ETAPA

Não construir ainda uma ponte definitiva.

Primeiro concluir:

1. inventário do Sistema antigo;
2. inventário do Cérebro ABS;
3. mapa de convergências;
4. mapa de divergências;
5. mapa de componentes reaproveitáveis;
6. mapa de conhecimento histórico;
7. mapa de interfaces possíveis;
8. requisitos mínimos da ponte.

Depois disso:

**Mini-Cérebro V0 → consulta local → evidência → teste → Ponte V0 → ligação bilateral.**

### 19. PRINCÍPIO DE PROJETO

O objetivo não é recuperar código velho.

É recuperar:

**o que já foi construído + o que já foi testado + o que já foi descoberto + o que falhou + o que foi aprendido + o que foi esquecido.**

Somente depois decidir o que o ABS deve herdar.

### STATUS

**FASE 0 — EXECUTADA PARCIALMENTE E REGISTRADA**

Próximo marco: **auditoria histórica completa antes da construção da Ponte dos Cérebros.**
