# O IMPÉRIO — material completo

Tudo que foi produzido neste projeto, organizado por tema e com o que foi
superado separado do que vale.

**Setembro de 2026.**

---

## SE VOCÊ TEM POUCO TEMPO

Leia **um** arquivo: `01-projeto/O-IMPERIO.md`.

Ele é a destilação de tudo — o projeto, o método, a engenharia e o estado real.
Os outros arquivos são o material bruto que ele resume.

Versão para celular: `O-IMPERIO.html`, mesma coisa, mais confortável de ler.

---

## SE VOCÊ É UMA IA CONTINUANDO ESTE TRABALHO

Leia nesta ordem, e não pule:

| Ordem | Arquivo | Por quê |
|---|---|---|
| 1 | `01-projeto/O-IMPERIO.md` | o projeto inteiro |
| 2 | `05-historico/DECISOES-REJEITADAS.md` | **o que já foi vetado — não proponha de novo** |
| 3 | `05-historico/LINHA-DO-TEMPO.md` | como se chegou até aqui |
| 4 | `01-projeto/INSTRUCOES-PERMANENTES.md` | como responder |

⚠ **O arquivo 2 é o que mais economiza tempo.** Sem ele, você vai propor coisas
que já foram rejeitadas, e Samuel vai gastar as três horas diárias re-explicando.

---

## O QUE TEM EM CADA PASTA

### `00-COMECE-AQUI`
Este arquivo.

### `01-projeto` — a visão e o método
| Arquivo | O que é |
|---|---|
| `O-IMPERIO.md` | **o documento principal** — 8 livros, 6 apêndices |
| `O-IMPERIO.html` | o mesmo, formatado para ler no celular |
| `AUDITORIA-E-CAMINHO.md` | análise do ecossistema de ferramentas, e o caminho de saída |
| `INSTRUCOES-PERMANENTES.md` | como a IA deve responder neste projeto |

### `02-sistema` — o código
O sistema construído entre agosto e setembro. 25 arquivos.

| Peça | Arquivo | Estado |
|---|---|---|
| Aplicativo | `index.html` | **exercitado** — 32/32 no auto-teste |
| Travas e execução | `executor.py` | **parado** — 756 linhas, nunca rodou |
| Coleta | `coletor.py` | parado — ~25 fontes |
| Especialistas | `orquestrador.py`, `especialistas.py` | parado |
| Memória | `base.py`, `semente*.json` | exercitado |
| Governança | `governanca.py` | parado |

⚑ **O que vale mais aqui:** as travas do `executor.py` — 27 ataques bloqueados,
zero falso positivo. É a única peça testada de verdade.

### `03-cliente` — o trabalho com a Pinheiro
| Arquivo | O que é |
|---|---|
| `FECHAMENTO_V3.xlsx` | a planilha que ficou, com fórmulas vivas |
| `fechamento_v3.py` | o gerador dela |
| `QUESTIONARIO-40-PERGUNTAS.*` | o questionário final, versão 5 |
| `PESQUISA-CLIENTE.md` | quem é o cliente, em fonte aberta |
| `PLANO-COMERCIAL.md` | a estratégia de isca e produto |

### `04-migracao` — sair da plataforma atual
`PASSO-A-PASSO.md` — seis passos para o OpenHands Cloud, mais o anexo com o
caminho de VM própria para quando houver máquina.

### `05-historico` — a memória do processo
| Arquivo | O que é |
|---|---|
| `DECISOES-REJEITADAS.md` | 17 decisões vetadas, com o motivo |
| `LINHA-DO-TEMPO.md` | as sete fases, e o que cada uma ensinou |

### `99-superado` — versões antigas, com valor de estudo
Não use como referência. Servem para ver a evolução.

| Arquivo | Superado por | Por que ainda está aqui |
|---|---|---|
| `v1.md` a `v4.md` | `QUESTIONARIO-40-PERGUNTAS` | mostra como a pergunta melhorou |
| `PAINEL_UNICO.xlsx`, `FECHAMENTO_SETEMBRO.xlsx` | `FECHAMENTO_V3` | mostra as tentativas |
| `extrair.py`, `gerar.py` | — | **ensinam a ler planilha sem depender de posição fixa** |
| `mensal.py` | `fechamento_v3.py` | comparação |
| `ESPECIFICACAO.md` | Livro VI do e-book | está incorporado lá |
| `AUDITORIA-v1.md` | Livro VII do e-book | idem |

---

## O QUE NÃO ESTÁ AQUI

**As conversas.** São 6,6 MB de transcrição, quase quatro vezes o volume deste
pacote. O que elas têm e este material não: o processo, as tentativas erradas, e
o momento exato de cada correção.

O `DECISOES-REJEITADAS.md` e a `LINHA-DO-TEMPO.md` são a destilação delas. Para
o bruto, é preciso exportar os dados da plataforma antes de sair.

**O material do outro chat.** Existe e será juntado depois. Quando isso
acontecer, o índice e a linha do tempo precisam ser refeitos — não apagados,
mesclados.

---

## COMO JUNTAR COM OUTRO MATERIAL

Regras que o e-book estabelece e que valem aqui:

| Regra | Motivo |
|---|---|
| Manter o material anterior íntegro | reescrever perde o que não se sabia que importava |
| Identificar quem contribuiu o quê | atribuição errada corrompe a história |
| Registrar alteração **como** alteração | não substituir em silêncio |
| Não transformar hipótese em fato | o erro mais comum, e o mais caro |
| Não apagar divergência nem decisão rejeitada | são dados |

**Se houver conflito entre duas fontes:** registre o conflito. Não apague uma
versão para fazer a outra parecer definitiva.

---

## O ESTADO DO PROJETO, EM UMA TABELA

| | |
|---|---|
| Estágio do Império | 0 — fundação |
| Clientes pagantes | **0** |
| Marco 1 (R$ 5.000/mês) | R$ 0 |
| Sistema | construído, quase nada exercitado |
| Plataforma | migrando para OpenHands Cloud |
| Restrição real | 3 h/dia, emprego formal, sem caixa |

**A única coisa que muda todas as linhas acima:** o primeiro cliente pagante.
