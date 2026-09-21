# O IMPÉRIO — material completo

Todo o material produzido no projeto, reunido de duas conversas.

**10 de setembro de 2026.**

---

## SE VOCÊ TEM POUCO TEMPO

Leia **um** arquivo: `01-projeto/O-IMPERIO.md`.

É a destilação do projeto inteiro — visão, método, engenharia e estado real.
Versão para celular: `O-IMPERIO.html`.

---

## SE VOCÊ É UMA IA CONTINUANDO ESTE TRABALHO

Leia nesta ordem, sem pular:

| Ordem | Arquivo | Por quê |
|---|---|---|
| 1 | `01-projeto/O-IMPERIO.md` | o projeto inteiro |
| 2 | `05-historico/DECISOES-REJEITADAS.md` | **o que já foi vetado** |
| 3 | `00-COMECE-AQUI/FUSAO.md` | como os conflitos foram resolvidos |
| 4 | `05-historico/LINHA-DO-TEMPO.md` | como se chegou até aqui |
| 5 | `01-projeto/PLANTA-DO-SISTEMA.md` | arquitetura detalhada do Sistema |
| 6 | `01-projeto/INSTRUCOES-PERMANENTES.md` | como responder |

⚠ **O arquivo 2 é o que mais economiza tempo.** Sem ele, você propõe o que já
foi rejeitado — e Samuel gasta as três horas diárias re-explicando.

---

## O QUE TEM EM CADA PASTA

### `00-COMECE-AQUI`
| Arquivo | O que é |
|---|---|
| `LEIA-PRIMEIRO.md` | este arquivo |
| `FUSAO.md` | o registro de como as duas conversas foram unidas |

### `01-projeto` — visão, método, arquitetura
| Arquivo | O que é |
|---|---|
| `O-IMPERIO.md` / `.html` | **o documento principal** — 8 livros, 6 apêndices |
| `PLANTA-DO-SISTEMA.md` | arquitetura detalhada do Sistema — MAPE-K, OODA, a Fábrica |
| `AUDITORIA-E-CAMINHO.md` | análise do ecossistema e o caminho de saída |
| `INSTRUCOES-PERMANENTES.md` | como a IA deve responder |
| `conceito-de-memoria-HERDADO.md` | material de sessão anterior, preservado |
| `visao-sistema-proprio-HERDADO.md` | idem |

### `02-sistema` — o código
| Pasta | Conteúdo |
|---|---|
| `app/` | `index.html` (463 KB), manifesto, ícones, service worker |
| `termux/` | 14 arquivos — Ponte, coletor, executor, orquestrador, memória |
| `nativo/` | configuração para empacotar como aplicativo |

**Estado das peças:**

| Peça | Estado |
|---|---|
| Aplicativo | exercitado |
| Travas do `executor.py` | **exercitado** — 27 ataques, 0 falso positivo |
| Ponte | parado |
| Coletor — 33 fontes | parado |
| Orquestrador, governança, especialistas | parado |

### `03-cliente` — o trabalho com a Pinheiro
| Arquivo | O que é |
|---|---|
| `FECHAMENTO_V3.xlsx` | a planilha que ficou, com fórmulas vivas |
| `fechamento_v3.py` | o gerador dela |
| `QUESTIONARIO-40-PERGUNTAS.*` | o questionário final |
| `PESQUISA-CLIENTE.md` | quem é o cliente, em fonte aberta |
| `PLANO-COMERCIAL.md` | a estratégia de isca e produto |

### `04-migracao`
| Arquivo | Quando usar |
|---|---|
| `PARA-OPENHANDS-CLOUD.md` | **o caminho atual** |
| `INSTALAR-NO-TERMUX.md` | o que existe hoje no aparelho |
| `como-usar-o-app-HERDADO.md` | manual do app |

### `05-historico` — a memória do processo
| Arquivo | O que é |
|---|---|
| `DECISOES-REJEITADAS.md` | as duas conversas, mescladas |
| `LINHA-DO-TEMPO.md` | as duas frentes, em paralelo |
| `originais/` | os arquivos antes da fusão, intactos |

### `99-superado` — versões antigas
Não use como referência. Servem para ver a evolução, e alguns ensinam técnica:
`extrair.py` e `gerar.py` mostram como ler planilha sem depender de posição fixa.

---

## O QUE NÃO ESTÁ AQUI

**As conversas.** São milhões de caracteres de transcrição. O que elas têm e
este pacote não: as tentativas erradas e o momento exato de cada correção.

Os arquivos em `05-historico` são a destilação delas.

**Os dados da memória.** A biblioteca coletada, as conversas gravadas e o
tabuleiro vivem no aparelho. Aqui está o código que os manipula, não o conteúdo.

---

## O ESTADO DO PROJETO

| | |
|---|---|
| Estágio do Império | 0 — fundação |
| Clientes pagantes | **0** |
| Marco 1 (R$ 5.000/mês) | R$ 0 |
| Sistema | construído, pouco exercitado |
| Plataforma | migrando para OpenHands Cloud |
| Restrição real | 3 h/dia, emprego formal, sem caixa |

**A única coisa que muda todas as linhas acima:** o primeiro cliente pagante.
