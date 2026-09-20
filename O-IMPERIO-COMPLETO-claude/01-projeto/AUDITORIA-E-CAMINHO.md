# AUDITORIA — o ecossistema contra o que você já construiu

Cada item do seu documento cruzado com: o que você tem, o que ele resolve, e se
vale trocar.

---

## O ACHADO PRINCIPAL

**1.932 linhas de Python que você escreveu têm equivalente pronto e mantido por
outros.**

| Sua peça | Linhas | Equivalente pronto |
|---|---|---|
| `executor.py` | 756 | OpenHands |
| `orquestrador.py` | 660 | LiteLLM |
| `coletor.py` | 516 | n8n / Make |
| Fila de motores (no app) | — | LiteLLM + Circuit Breaker |
| 15 ferramentas da IA | — | MCP |
| Memória e busca | — | Supabase pgvector |

Isso não significa que o trabalho foi perdido — significa que **construir a
segunda versão dessas peças seria erro**, e que o valor está no que sobra depois
de tirá-las.

---

## 1. O QUE EU TINHA DEIXADO PASSAR — E É O MAIS IMPORTANTE

### LiteLLM — a peça que resolve seu maior risco

Seu documento chama de *"padrão ouro em código livre"*, e a descrição é exata:
proxy local que traduz chamadas e gerencia fallback **dentro do seu próprio
servidor**.

**Por que isso importa mais que OpenRouter:**

Eu recomendei OpenRouter e não vi a contradição. O seu método diz:

> ⚑ Decisão 10 — contexto em nuvem própria, para não depender de fornecedor único.
> ⚠ Risco registrado — dependência de fornecedor único.

**OpenRouter é fornecedor único.** Ele agrega 400 modelos, mas se ele cair, mudar
preço, ou for absorvido pela Stripe de um jeito que não te sirva — você para.

LiteLLM roda no **seu** servidor. Ele fala com OpenRouter, com Anthropic direto,
com Groq, com o motor local — todos ao mesmo tempo. Se um cair, o próximo assume,
e a lógica de decidir isso é sua.

| | OpenRouter | LiteLLM |
|---|---|---|
| Onde roda | servidor deles | **seu** |
| Se cair | você para | você troca de rota |
| Quem define a regra de fallback | eles | **você** |
| Custo do serviço | margem embutida | zero, é código aberto |
| Complexidade | zero | precisa hospedar |

⚑ **O certo não é escolher entre os dois. É LiteLLM na frente, e OpenRouter como
uma das rotas dentro dele.**

### Circuit Breaker — o que falta na sua fila de motores

Você tem fila de motores. Não tem disjuntor.

**A diferença:** hoje, se um motor falha, você tenta de novo. Se ele estiver fora
do ar, você tenta de novo toda vez, e cada tentativa gasta tempo esperando o
tempo limite.

O disjuntor conta as falhas. Depois de N seguidas, ele **desarma** — para de
tentar aquele motor por um tempo, e manda tudo direto para o reserva. Depois de
um intervalo, testa uma vez para ver se voltou.

⚑ Isso já está na especificação como "quando NÃO trocar de motor", mas faltava o
mecanismo. O nome do padrão é este, e a implementação é conhecida.

---

## 2. MCP — o padrão que suas 15 ferramentas deveriam falar

Você construiu 15 ferramentas customizadas: buscar memória, gravar memória,
pesquisar web, analisar dados, calcular.

**MCP** é o protocolo aberto que faz exatamente isso, de forma padronizada. A
diferença que seu documento descreve bem: em vez de você injetar dado no prompt,
a IA se conecta a um servidor MCP e **decide sozinha** quando consultar.

**O que muda se suas ferramentas falarem MCP:**

| Hoje | Com MCP |
|---|---|
| Só funcionam no seu app | funcionam em qualquer cliente MCP |
| Você mantém o protocolo | o protocolo é mantido por outros |
| Trocar de interface = reescrever | trocar de interface = zero trabalho |

E o OpenHands suporta MCP. Suas ferramentas passariam a funcionar dentro dele
sem adaptação.

⚑ **Este é o caminho para a "casca 100% modificável" que seu método defende** —
mas de verdade, não por promessa: a ferramenta deixa de estar presa à casca.

---

## 3. A MEMÓRIA — o que você está construindo já existe

Você quer RAG: memória própria, busca por relevância, contexto que persiste.

**BaaS com busca vetorial** (Supabase, Firebase) entrega isso pronto: banco de
dados, autenticação e busca vetorial no mesmo lugar.

| Sua peça | O que faz | Equivalente |
|---|---|---|
| `base.py` + FTS5 | busca por palavra | busca vetorial de verdade |
| memória em 4 camadas | redundância | replicação nativa |
| sincronização entre aparelhos | manual | nativa |

⚠ **A ressalva honesta:** migrar para um BaaS significa que sua memória mora no
servidor de outra pessoa. Isso contradiz "nuvem própria" — a menos que você use
Supabase auto-hospedado, que é possível e é código aberto.

**A decisão real:** memória em serviço gerenciado é mais rápida de ter e mais
fácil de perder. Memória própria é mais lenta de construir e não some.

---

## 4. O CELULAR — resolvido por uma peça que estava no seu documento

Seu problema: trabalha do celular, 3 GB de RAM, e o agente precisa rodar.

**Serverless GPU** (Modal, RunPod, Together) — você aluga processamento por
segundo, em vez de por token.

E a conexão que você não viu: **o OpenHands usa Modal como backend remoto**. O
agente roda na nuvem, não no seu aparelho. Você fecha o celular e ele continua.

⚑ Isso resolve a limitação que está no e-book como restrição estrutural: *"3 GB
de RAM, motor local limitado a modelo pequeno"*. Com backend remoto, o modelo
local deixa de ser o teto.

---

## 5. AS PLATAFORMAS TUDO-EM-UM — a que serve ao seu cliente

| Plataforma | Para quê | Serve a você? |
|---|---|---|
| **Dify** | RAG corporativo | ⚠ exige 3–8 GB de RAM. **Você tem 3 GB** — não roda local |
| **Flowise** | prototipagem visual | ⚠ sem fila longa nem auditoria — não serve para produção |
| **Gumloop** | **lotes de dados, planilhas, CRM** | **sim — é o problema do seu cliente** |
| **Relevance AI** | equipes de agentes | sobrepõe sua Malha |

### Gumloop merece atenção especial

Seu cliente tem **80 planilhas para consolidar**, feitas à mão por uma equipe de
madrugada.

O seu documento descreve Gumloop como "automação profunda voltada para o
processamento massivo de lotes de dados, planilhas e CRMs". É a descrição
literal do problema.

⚑ **A pergunta que isso levanta, e que muda a estratégia:** você vai *construir*
a consolidação, ou *configurar* uma ferramenta que já faz isso e cobrar pela
solução?

O método diz para deletar a peça. Se Gumloop resolve, o produto vendável deixa
de ser o software e passa a ser **o entendimento do problema + a configuração**
— que é justamente o que ninguém mais tem, porque exigiu os dois questionários.

⚠ **Contraponto:** ferramenta de terceiro no meio do serviço significa que o
cliente pode contratá-la direto e dispensar você. A defesa é o mesmo argumento
da casca vazia: a ferramenta é genérica, o entendimento do negócio dele não é.

---

## 6. NO-CODE + AGENTE — a arquitetura que seu documento propõe

O desenho que está no seu material:

```
gatilho no-code (n8n/Make) → OpenHands (constrói e testa) → ação no-code (entrega)
```

**Onde isso encaixa no seu caso:**

| Etapa | Ferramenta | Substitui |
|---|---|---|
| Coletar de fontes, agendar | n8n | `coletor.py` — 516 linhas |
| Construir, testar, corrigir | OpenHands | `executor.py` — 756 linhas |
| Entregar, notificar | n8n | scripts soltos |

⚠ **A ressalva do seu próprio documento:** no-code quebra quando a estrutura do
dado muda, e exige conserto manual. Para coleta de fonte instável — que é o seu
caso — isso é fraqueza real.

---

## 7. IA LOCAL — o que muda pouco

Ollama e LM Studio são mais fáceis que llama.cpp compilado, mas **o teto continua
sendo a RAM**. Em 3 GB, modelo pequeno é modelo pequeno em qualquer ferramenta.

⚑ Confirma o que já está no e-book: motor local serve para volume mecânico
(traduzir, classificar, resumir), não para decisão nem código.

**A exceção interessante:** `SELECT ai_generate(...) FROM clientes` — IA dentro
do banco de dados. Para o problema do cliente, onde os dados já estão em tabela,
isso elimina a camada de script intermediária.

---

## 8. O QUE ESTA AUDITORIA MUDA NO E-BOOK

| Registro atual | Correção |
|---|---|
| "motor intercambiável — resolvido ✓" | ⚠ resolvido no app, **não** no back-end. Falta LiteLLM |
| "fila de motores" | falta o disjuntor — mecanismo, não só regra |
| "15 ferramentas" | deveriam falar MCP, não protocolo próprio |
| "3 GB de RAM é teto" | ⚑ deixa de ser, com backend remoto |
| "consolidação das 80 = produto pago" | ⚑ pode ser configuração, não construção |
| Riscos | falta: **agregador único também é fornecedor único** |
---

# O CAMINHO — por onde sair daqui

Ordem definida por um critério só: **cada passo precisa funcionar sozinho e
custar pouco antes do próximo.**

---

## PASSO 1 — Provar que dá para trabalhar fora (1 dia, US$ 10)

**Fazer:** conta no OpenRouter, US$ 10 de crédito. Instalar OpenHands. Uma tarefa
real, pequena.

**Por que US$ 10 e não R$ 100:** dez dólares medem seu consumo real por uma
semana. Minha estimativa foi de 30 voltas com 60k de contexto — pode estar errada
para mais ou para menos. Medir custa dez dólares; errar o orçamento mensal custa
mais.

**Resultado esperado:** você sabe quanto gasta por sessão de verdade, e se a
qualidade serve.

⚠ **Não migre nada ainda.** Se não passar aqui, os passos seguintes não importam.

---

## PASSO 2 — Levar a memória (1 dia, R$ 0)

**Fazer:** o e-book vira `00_VISAO.md` dentro do projeto. Os dez arquivos de
contexto criados.

**Por que antes de tudo:** é o que impede recomeçar do zero a cada sessão. Sem
isso, você troca o limite de mensagem por um problema pior — perda de contexto.

**Resultado esperado:** um agente novo lê os arquivos e entende o projeto sem
você explicar.

---

## PASSO 3 — LiteLLM na frente (2 a 3 dias, R$ 0)

**Fazer:** subir LiteLLM como proxy. Configurar as rotas: OpenRouter, Groq,
Gemini, motor local. Apontar o OpenHands para o LiteLLM, não para o OpenRouter.

**Por que este passo existe:** é o que impede trocar uma dependência por outra.
Depois dele, mudar de fornecedor é editar um arquivo de configuração.

**O que ganha junto:** disjuntor, balanceamento, e um único lugar para ver
quanto cada modelo custou.

**Resultado esperado:** derrubar o OpenRouter de propósito e ver o trabalho
continuar por outra rota.

---

## PASSO 4 — Primeira entrega paga (o que realmente importa)

**Fazer:** a planilha da clínica, com o entendimento que os dois questionários
deram.

**Por que aqui e não depois:** os três passos acima levam menos de uma semana.
Adiar o cliente além disso é a armadilha registrada no e-book — sistema que só
se mantém a si mesmo.

⚑ **A pergunta a decidir antes:** construir a consolidação, ou configurar uma
ferramenta que já faz? A segunda entrega mais rápido; a primeira mantém o
produto sob seu controle.

---

## PASSO 5 — Só depois de haver receita

| O quê | Por quê depois |
|---|---|
| Ferramentas falando MCP | melhora arquitetura, não gera caixa |
| Memória em busca vetorial | idem |
| Backend remoto | custa mensalidade |
| Coleta via n8n | o coletor atual já roda |

---

## O QUE NÃO FAZER

| Não fazer | Por quê |
|---|---|
| Migrar tudo de uma vez | o passo 1 pode reprovar o plano inteiro |
| Colocar R$ 100 antes de medir | você não sabe o consumo real ainda |
| Apontar direto para OpenRouter | troca uma dependência por outra |
| Dify local | 3 GB de RAM não roda |
| Reescrever o que já funciona | travas e memória calibrada são suas, e prontas |

---

## O RESUMO EM UMA TABELA

| Passo | Tempo | Custo | Prova de que funcionou |
|---|---|---|---|
| 1 · Testar fora | 1 dia | US$ 10 | uma tarefa real terminou |
| 2 · Levar memória | 1 dia | R$ 0 | agente novo entende sem explicação |
| 3 · LiteLLM | 2–3 dias | R$ 0 | derrubar uma rota e continuar |
| 4 · Cliente | dias | R$ 0 | **alguém pagou** |
| 5 · Refinar | depois | conforme caixa | — |

**Até o passo 3 você gastou dez dólares e uma semana.** Se algo reprovar antes
disso, você descobriu barato.
