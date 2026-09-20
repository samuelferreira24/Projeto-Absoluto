# SISTEMA ABSOLUTO — ESPECIFICAÇÃO DE ENGENHARIA

Planta com medidas. Para cada peça: o que entra, o que sai, quais números,
e como saber se está certo.

Não descreve o que existe. Descreve o que **deve** existir, para que qualquer
motor de IA construa e Samuel confira.

---

## COMO USAR ESTE DOCUMENTO

Cada peça tem cinco campos fixos:

- **Promete** — a frase única que define a peça
- **Entra / Sai** — os formatos exatos, sem ambiguidade
- **Números** — parâmetros com valor e motivo
- **Prova** — o teste que passa ou falha, sem opinião
- **Pronto quando** — o critério de aceitação

Se uma peça construída não passa na **Prova**, ela não está pronta, mesmo que
pareça funcionar.

---

# PARTE 1 — O DESENHO EM UMA PÁGINA

```
   Samuel
     │  tarefa em texto
     ▼
┌─────────────┐
│  CONVERSA   │  guarda o diálogo em papéis separados
└──────┬──────┘
       │  histórico + ferramentas disponíveis
       ▼
┌─────────────┐      falhou      ┌──────────────┐
│   MOTOR     │─────────────────▶│  FILA RESERVA│
│  chama API  │◀─────────────────│  próximo     │
└──────┬──────┘                  └──────────────┘
       │  pedido de ferramenta OU resposta final
       ▼
┌─────────────┐
│   TRAVAS    │  o comando é permitido?
└──────┬──────┘
       │  liberado
       ▼
┌─────────────┐
│ FERRAMENTAS │  escrever · ler · rodar · listar
└──────┬──────┘
       │  resultado (inclusive erro)
       ▼
┌─────────────┐
│    LAÇO     │  devolve ao motor e repete até resolver ou desistir
└──────┬──────┘
       │  entrega
       ▼
┌─────────────┐
│  VERIFICADOR│  sintaxe válida? teste passa? arquivo cresceu?
└──────┬──────┘
       │  aprovado
       ▼
┌─────────────┐
│   MEMÓRIA   │  guarda o que funcionou e o que falhou
└─────────────┘
```

**Regra estrutural:** o motor nunca toca em arquivo direto. Ele **pede**, as
travas julgam, as ferramentas executam. Essa separação é o que permite trocar
de motor sem trocar a segurança.

---

# PARTE 2 — AS PEÇAS

## PEÇA 1 — CONVERSA

**Promete:** guardar o diálogo de um jeito que qualquer motor entenda, e que
caiba na janela dele.

**Entra:** texto de Samuel, resultado de ferramenta, resposta do motor.

**Sai:** lista de mensagens, cada uma com papel declarado.

```json
[
  {"papel": "sistema",    "texto": "instrução permanente"},
  {"papel": "samuel",     "texto": "crie um arquivo x.py"},
  {"papel": "ia",         "texto": null,
   "pede": {"ferramenta": "escrever", "args": {"caminho": "x.py", "conteudo": "..."}}},
  {"papel": "ferramenta", "nome": "escrever", "resultado": "gravado, 40 linhas"},
  {"papel": "ia",         "texto": "Pronto. Quer que eu rode?"}
]
```

**Por que papéis separados importa:** sem isso não dá para saber o que o motor
disse e o que Samuel disse; a API não consegue usar cache de prefixo; e a
chamada de ferramenta vira texto solto que precisa ser adivinhado de volta.

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Janela assumida quando desconhecida | 8.000 tokens | pior caso seguro |
| Reserva para a resposta | 25% da janela | resposta cortada é pior que pergunta menor |
| Gatilho de compactação | 70% da janela | com folga para a próxima volta |
| Mensagens sempre preservadas | 4 primeiras + 6 últimas | as pontas carregam o contexto |
| Estimativa de token | caracteres ÷ 3,5 | serve para português; erra ~10% para mais |

### Prova

1. Montar conversa com 200 mensagens curtas.
2. Compactar.
3. Conferir: a primeira e a última mensagem estão intactas, e o total ficou
   abaixo de 70% da janela.

### Pronto quando

Trocar de motor no meio de uma conversa longa e continuar sem perder contexto
e sem erro de formato.

---

## PEÇA 2 — MOTOR

**Promete:** falar com qualquer API compatível com OpenAI, Gemini ou Anthropic,
e cair para o próximo quando um falha.

**Entra:** lista de mensagens da Peça 1 + lista de ferramentas disponíveis.

**Sai:** ou texto, ou pedido de ferramenta.

### Cadastro de motor — formato exato

```json
{
  "id": "m1",
  "nome": "Claude Sonnet",
  "dialeto": "anthropic",
  "url": "https://api.anthropic.com/v1/messages",
  "modelo": "claude-sonnet-4-6",
  "chave": "...",
  "janela": 200000,
  "custo_entrada": 3.00,
  "custo_saida": 15.00,
  "ordem": 1
}
```

`dialeto` só aceita: `openai`, `gemini`, `anthropic`. Todo motor novo cai num
dos três — não existe quarto formato em uso relevante.

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Tempo limite por chamada | 120 s | modelo grande com resposta longa passa de 90 s |
| Tentativas no mesmo motor | 3 | erro de rede costuma passar na segunda |
| Espera entre tentativas | 2 s, 6 s, 15 s | crescente, evita bater na parede |
| Troca de motor | após as 3 tentativas | não antes: pode ser rede, não motor |
| Temperatura para código | 0,2 | código precisa de previsível, não criativo |
| Temperatura para conversa | 0,8 | aqui variedade ajuda |
| Teto de resposta | 8.192 tokens | arquivo grande precisa caber inteiro |

### Quando NÃO trocar de motor ⚑

Trocar de motor não conserta:

| Erro | Código | Ação certa |
|---|---|---|
| Chave errada | 401, 403 | parar e avisar Samuel |
| Requisição malformada | 400 | parar — é bug nosso, trocar esconde |
| Modelo inexistente | 404 | parar e avisar |
| Cota estourada | 429 | **trocar** — é exatamente o caso |
| Erro do servidor | 500, 502, 503 | tentar de novo, depois trocar |
| Tempo esgotado | — | tentar de novo, depois trocar |

Trocar de motor num erro 401 dá a impressão de que o sistema se recuperou,
quando na verdade a chave continua errada e o problema volta amanhã.

### Prova

1. Cadastrar dois motores, o primeiro com chave inválida.
2. Rodar uma tarefa.
3. Conferir: o sistema **parou e avisou**, não trocou.
4. Trocar o erro para cota estourada (429).
5. Conferir: agora **trocou** e terminou a tarefa.

### Pronto quando

O mesmo pedido roda igual em três dialetos diferentes, e o log mostra por que
cada troca aconteceu.

---

## PEÇA 3 — FERRAMENTAS

**Promete:** as mãos. Tudo que o motor faz no mundo passa por aqui.

### Contrato de cada ferramenta

| Ferramenta | Entra | Sai | Falha quando |
|---|---|---|---|
| `escrever` | caminho, conteúdo | bytes gravados | fora da cerca, disco cheio |
| `ler` | caminho | conteúdo ou trecho | não existe, grande demais |
| `rodar` | comando | saída + código de erro | proibido, passou do tempo |
| `listar` | pasta | nomes e tamanhos | fora da cerca |

**Toda ferramenta devolve o mesmo envelope:**

```json
{"ok": true, "resultado": "...", "erro": null}
{"ok": false, "resultado": null, "erro": "motivo em uma linha"}
```

Sem exceção. Isso permite que o laço trate erro sem conhecer a ferramenta.

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Tempo limite de comando | 90 s | build costuma passar de 30 s |
| Tempo limite de instalação | 300 s | `pip install` é lento no celular |
| Tamanho máximo para ler | 200 KB | acima disso, ler em trechos |
| Trecho quando maior | 300 linhas por vez | cabe na janela sem estourar |
| Saída de comando devolvida | últimas 3.000 letras | o erro fica no fim, não no começo |

**Por que as últimas letras:** um `pytest` que falha imprime centenas de linhas,
e a mensagem de erro está no final. Cortar pelo começo entrega o cabeçalho e
esconde a causa.

### Prova

1. `escrever` um arquivo com 500 linhas.
2. `ler` de volta — o conteúdo bate letra por letra.
3. `rodar` um comando que falha de propósito.
4. Conferir: `ok:false`, e o erro devolvido contém a mensagem real, não o
   cabeçalho.

---

## PEÇA 4 — TRAVAS

**Promete:** nenhum comando destrutivo chega às ferramentas.

**Entra:** comando ou caminho.
**Sai:** liberado, ou bloqueado com motivo.

### As quatro categorias

| Categoria | Exemplos | Regra |
|---|---|---|
| Destruição | `rm -rf /`, `mkfs`, `dd` | bloqueio absoluto |
| Sistema | `/system`, `/proc`, dados de outro app | bloqueio absoluto |
| Segredo | `.ssh`, chave, token | bloqueio absoluto |
| Publicação | `git push`, baixar-e-executar | pede Samuel |

### A cerca

Todo caminho é resolvido para absoluto **antes** de comparar. Comparar texto
sem resolver deixa passar `pasta/../../fora`.

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Falso positivo tolerado | 0 | trava que atrapalha trabalho legítimo será desligada |
| Falso negativo tolerado | 0 | uma passada basta para perder tudo |
| Comandos legítimos no teste | mínimo 15 | menos que isso não prova nada |
| Ataques no teste | mínimo 25 | cobre as quatro categorias |

### Prova

Rodar a lista de ataques e a lista de legítimos. **Os dois números têm que ser
zero**: nenhum ataque passou, nenhum legítimo foi barrado.

Um teste que só mede ataques bloqueados aprova uma trava que bloqueia tudo.

---

## PEÇA 5 — O LAÇO

**Promete:** transformar tarefa em resultado, corrigindo os próprios erros até
resolver ou desistir de forma limpa.

```
recebe tarefa
  │
  ├─▶ pergunta ao motor
  │      │
  │      ├── pediu ferramenta? ──▶ travas ──▶ executa ──▶ devolve resultado ──┐
  │      │                                                                     │
  │      └── respondeu texto? ──▶ verificador                                  │
  │                                    │                                       │
  │                                    ├── passou ──▶ entrega                  │
  │                                    └── falhou ──▶ devolve o erro ──────────┤
  │                                                                            │
  └────────────────────────────────────────────────────────────────────────────┘
                                   até MAX_VOLTAS
```

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Máximo de voltas | 7 | acima disso costuma ser laço, não progresso |
| Voltas sem mudar arquivo | 3 → para | o motor está andando em círculo |
| Custo máximo por tarefa | definido por Samuel, padrão US$ 0,50 | trava antes de cobrar |
| Tempo máximo por tarefa | 15 min | além disso, algo travou |

### O sinal de desistência

Desistir bem é parte da especificação. Ao atingir qualquer teto, o sistema deve
entregar: o que tentou, o que falhou, o último erro, e o que ele acha que falta.
Nunca um "não consegui" seco.

### Prova

1. Dar uma tarefa impossível de propósito ("conserte o arquivo que não existe").
2. Conferir: parou em no máximo 7 voltas, e o relatório diz o que tentou.

---

## PEÇA 6 — VERIFICADOR

**Promete:** nada é aceito sem prova. É a peça que separa "o motor disse que
terminou" de "terminou".

### As cinco verificações, em ordem

| # | Verifica | Como | Reprova quando |
|---|---|---|---|
| 1 | Sintaxe | `python -m py_compile`, `node --check` | não compila |
| 2 | Tamanho | compara com a versão anterior | encolheu mais de 20% sem motivo |
| 3 | Âncora | o trecho alterado existe no arquivo | a substituição não encontrou o alvo |
| 4 | Teste | roda o teste do projeto, se houver | falha nova apareceu |
| 5 | Execução | roda o arquivo | erro em tempo de execução |

**A verificação 3 é a que mais pega erro real:** uma alteração que não acha o
alvo e passa calada é uma alteração que não aconteceu — e o motor reporta
sucesso.

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Encolhimento que reprova | > 20% | abaixo disso pode ser limpeza legítima |
| Tempo limite do teste | 120 s | suíte de projeto pequeno cabe |
| Verificações obrigatórias | 1, 2 e 3 | sempre, para qualquer arquivo |
| Verificações condicionais | 4 e 5 | só quando há teste ou o arquivo é executável |

### Prova

Pedir ao motor uma alteração com âncora que não existe. O verificador tem que
reprovar — mesmo que o arquivo continue com sintaxe válida.

---

## PEÇA 7 — MEMÓRIA

**Promete:** o que aconteceu vira material, e o que Samuel corrigiu vira regra.

### O que guardar

| Tipo | Peso | Por quê |
|---|---|---|
| Correção de Samuel | **1,0** | único sinal que diz qual era o certo |
| Erro que o sistema corrigiu sozinho | 0,7 | ensina o caminho da correção |
| Discordância entre dois motores | 0,5 | marca onde o problema é difícil |
| Sucesso na primeira tentativa | 0,1 | confirma, não ensina |

### Formato — uma linha por exemplo

```json
{"tarefa":"...", "contexto":"...", "saida":"...", "resultado":"aprovado",
 "correcao":null, "peso":0.1, "motor":"m1", "quando":"2026-09-08T14:22:00"}
```

### Números

| Parâmetro | Valor | Motivo |
|---|---|---|
| Volume mínimo para treinar | 300 exemplos | abaixo disso o ajuste não sai do ruído |
| Volume confortável | 1.000 a 3.000 | faixa onde LoRA rende |
| Proporção de peso 1,0 desejada | ≥ 15% | correção humana é o que ensina |
| Conjunto de referência | 30 perguntas fixas | mede antes e depois |

**⚑ Verificar antes de treinar:** os termos de serviço da maioria dos
fornecedores proíbem usar saídas para treinar modelo concorrente. O risco está
no conjunto de dados, não na licença do modelo base.

---

# PARTE 3 — TODOS OS NÚMEROS NUM LUGAR SÓ

Para conferir de relance se o que foi construído usa os valores certos.

| Onde | Parâmetro | Valor |
|---|---|---|
| Motor | tempo limite | 120 s |
| Motor | tentativas | 3 |
| Motor | espera entre tentativas | 2 s, 6 s, 15 s |
| Motor | temperatura (código) | 0,2 |
| Motor | temperatura (conversa) | 0,8 |
| Motor | teto de resposta | 8.192 tokens |
| Conversa | reserva para resposta | 25% |
| Conversa | gatilho de compactação | 70% |
| Conversa | estimativa de token | letras ÷ 3,5 |
| Ferramenta | tempo de comando | 90 s |
| Ferramenta | tempo de instalação | 300 s |
| Ferramenta | leitura máxima | 200 KB |
| Ferramenta | saída devolvida | últimas 3.000 letras |
| Laço | máximo de voltas | 7 |
| Laço | voltas sem progresso | 3 |
| Laço | custo por tarefa | US$ 0,50 |
| Laço | tempo por tarefa | 15 min |
| Verificador | encolhimento que reprova | 20% |
| Travas | falso positivo aceito | 0 |
| Travas | falso negativo aceito | 0 |
| Memória | mínimo para treinar | 300 exemplos |

---

# PARTE 4 — AS PROVAS DE ACEITAÇÃO

Sete testes. Enquanto um falhar, o sistema não está pronto.

| # | Prova | Passa quando |
|---|---|---|
| 1 | Conversa de 200 mensagens compacta | pontas intactas, abaixo de 70% |
| 2 | Mesmo pedido em 3 dialetos | resultado equivalente nos três |
| 3 | Chave errada | **para**, não troca de motor |
| 4 | Cota estourada | **troca** e termina |
| 5 | 25 ataques + 15 legítimos | 0 e 0 |
| 6 | Alteração com âncora falsa | reprovada |
| 7 | Tarefa impossível | para em ≤ 7 voltas com relatório |

**A prova final, que resume todas:**

> Dar ao sistema a tarefa *"crie um script que some dois números, escreva um
> teste, rode o teste, e conserte se falhar"* — e ele terminar sozinho, com o
> teste passando, sem Samuel tocar em nada.

Se isso funciona, o sistema constrói o sistema.

---

# PARTE 5 — ORDEM DE CONSTRUÇÃO

Cada peça só depende das anteriores. Nenhuma precisa de todas.

| Ordem | Peça | Depende de | Dá para testar sozinha? |
|---|---|---|---|
| 1 | Ferramentas | nada | sim |
| 2 | Travas | nada | sim |
| 3 | Motor | nada | sim |
| 4 | Conversa | nada | sim |
| 5 | Laço | 1, 2, 3, 4 | sim |
| 6 | Verificador | 1 | sim |
| 7 | Memória | 5 | sim |

**As quatro primeiras são independentes entre si.** Podem ser construídas e
testadas em qualquer ordem, o que significa que um erro numa não trava as
outras.

---

# PARTE 6 — O QUE REAPROVEITAR

Levantado do código atual, não de memória.

| Peça nova | Material existente | Estado | Trabalho |
|---|---|---|---|
| Ferramentas | `executor.py` — escrever, ler, rodar, listar | funciona | padronizar o envelope de retorno |
| Travas | `executor.py` — `proibido`, `dentro_da_cerca` | funciona, testado | manter como está |
| Motor | `executor.py` — `perguntar` | funciona parcial | ler de `motores.json`, tratar códigos de erro |
| Laço | `executor.py` — `executar` | existe, nunca rodou | separar do resto, provar |
| Verificador | `julgar` no executor | existe, é IA julgando | trocar por verificação objetiva |
| Conversa | — | **não existe** | construir |
| Memória | — | **não existe** | construir |

**Duas observações honestas:**

O `julgar` atual usa IA para avaliar a entrega. Isso é caro e não determinístico.
As cinco verificações da Peça 6 são objetivas e não custam token — melhor
começar por elas e usar IA só onde a verificação objetiva não alcança.

Cinco das sete peças têm material aproveitável. Isso não é reconstrução, é
remontagem sobre planta.

---

*Fim. Qualquer número aqui pode ser mudado — mas o valor novo precisa de motivo
escrito, senão vira chute em cima de chute.*
