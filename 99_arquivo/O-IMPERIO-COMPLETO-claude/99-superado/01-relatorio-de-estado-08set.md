# SISTEMA ABSOLUTO — RELATÓRIO DE PLANEJAMENTO

Levantado em 08/09/2026 por medição do código, não por memória.
Documento de trabalho: serve para pensar, não para obedecer.

---

# PARTE I — COMO O SISTEMA FUNCIONA HOJE

## O que existe, medido

| Peça | Tamanho | Onde roda |
|---|---|---|
| App (`index.html`) | 9.534 linhas · 235 funções · 17 ferramentas | navegador |
| Ponte | 453 linhas · 11 comandos · 12 rotas | Termux |
| Coletor | 871 linhas · 33 fontes (15 ativas) | Termux |
| Orquestrador | 660 linhas | Termux |
| Especialistas, Governança, Jetro, Executor, Base, Semente | 2.950 linhas | Termux |

Total: cerca de 14 mil linhas. Não é protótipo.

## As quatro camadas

**1. Coleta** — o coletor puxa de 33 fontes em 13 domínios, incluindo GDELT
(notícia de ~100 países), OpenAlex (ciência mundial) e Wikipédia. Roda a cada
3h pelo agendador do Android, com a tela apagada. Neutraliza injeção de prompt
antes de gravar.

**2. Memória** — quatro camadas com redundância real:
IndexedDB comprimido → `~/sa-memoria` com 20 versões datadas → espelho em
Downloads → cópia de fuga manual. É a única parte do sistema que sobrevive à
morte de qualquer uma das outras.

**3. Raciocínio** — motor pago via API ou local via `llama-server`. O app
conversa, chama ferramenta, lê e cria arquivo (docx, xlsx, pptx, pdf, csv),
busca na biblioteca em qualquer língua.

**4. Autonomia** — piloto a cada 5 minutos decide o que está atrasado: coleta,
completa artigo, roda análise, atualiza dicionário, grava no disco. Liga o
motor quando a análise precisa e desliga 10 min depois de ocioso.

## Como as peças se ligam

```
Android liga
   └─ Termux:Boot → arranque.sh → trava de sono + Ponte
                                       │
   agendador (3h) → coletor ───────────┤
                                       │
   Chrome → app ──── Ponte ────────────┤
              │        ├─ comandos (11)
              │        ├─ biblioteca, dicionário, plantão
              │        └─ memória versionada
              │
              └─ motor (API ou local) → resposta, análise, tradução
```

## O que o sistema deve fazer, em ordem de importância

1. **Não perder nada.** Informação boa entra e nunca sai. — cumprido
2. **Trabalhar sem Samuel.** Coletar, completar, analisar, gravar. — depende da Ponte
3. **Só chamar Samuel para decidir.** O que precisa dele sobe ao Plantão. — parcial
4. **Ser a plataforma de trabalho dele.** Substituir o chat externo. — quase
5. **Consertar a si mesmo.** Varredura acha, Oficina propõe, Samuel aprova. — construído, não exercitado
6. **Virar material de treino.** Todo uso vira JSONL. — construído, sem volume ainda

---

# PARTE II — OS PROBLEMAS REAIS

## Problema 1 — A trava dos dez modos (o mais grave)

O app espera dez formatos de resposta: `chat`, `brainstorm`, `guerra`, `gps`,
`arca`, `mapa`, `diagnostico`, `prototipo`, `pesquisa`, `texto`. São dez blocos
de renderização presos a campos obrigatórios — `brainstorm` exige `grupos`,
`guerra` exige `gravidade` e `solucao`, `diagnostico` exige `restricao_unica`.

A IA não responde: ela escolhe um molde e preenche campos.

Isto é o mesmo erro que Samuel já corrigiu uma vez, quando mandou remover os
dez botões de modo da interface. Os botões saíram; os moldes ficaram no código.
Método virou estrutura de dados obrigatória, e estrutura obrigatória não deixa
espaço para julgamento.

**Caminho:** tirar os moldes, deixar markdown livre. O método vira bloco de
memória que Samuel corrige na conversa — calibragem, não formato. Custo real:
as telas bonitas de `guerra` e `brainstorm` viram texto.

## Problema 2 — A Ponte é ponto único de falha

Ela concentra 11 comandos e serve o app, a biblioteca, o dicionário, a memória,
o plantão e a busca de texto. **Não existe segundo caminho.** Ela cai, o sistema
inteiro para — foi o que aconteceu hoje, com `ERR_CONNECTION_REFUSED`.

**Caminho:** o app precisa saber funcionar degradado — dizer o que consegue
fazer sem a Ponte em vez de só falhar. E a Ponte precisa de um vigia que a
levante quando cair.

## Problema 3 — Um motor por vez, sem reserva

Um único motor configurado, sem fila e sem queda automática. Um HTTP 400 num
nome de modelo errado parou análise, tradução e Oficina ao mesmo tempo.

**Caminho:** lista ordenada por classe de tarefa. Falhou, cai para o próximo.
Tarefa mecânica (traduzir, classificar) vai para o barato ou local; decisão vai
para o forte. Isso também gera a métrica que o documento pede: fração resolvida
localmente.

## Problema 4 — Cinco capacidades presas na mesma corrente

```
motor fora   → análise, tradução, Oficina param
Ponte fora   → coleta, piloto, biblioteca, memória em disco param
```

Não há degradação graciosa em lugar nenhum. É tudo ou nada.

## Problema 5 — Contexto fixo de ~1.732 tokens

Enviado inteiro em toda mensagem, com data e hora no topo — o que quebra o
cache de prefixo que os provedores oferecem. Paga-se caro por repetir o que
não muda.

**Caminho:** três blocos em ordem — fixo idêntico (cacheável), semi-estável,
volátil.

## Problema 6 — Sem plano de avaliação

Não existe como saber se uma versão ficou melhor que a anterior. Sem conjunto
de teste, sem métrica, sem comparação. Isto invalida o ciclo de melhoria
contínua inteiro: melhorar sem medir é fé.

Esta é a lacuna mais séria do planejamento, e a mais barata de resolver.

## Problema 7 — `semente.py` sem caminho

Único arquivo Python sem rota na Ponte. Roda apenas no Termux, na mão.

## Problema 8 — Duas estratégias em conflito

O documento de 07/09 diz que o primeiro nicho é o próprio sistema, não um
mercado externo. O documento mestre diz: prova social → cliente pago → Marco 1
(R$5.000/mês) → sair do CLT, com a Pinheiro Negócios esperando.

As duas são defensáveis. Não são compatíveis como prioridade simultânea.
**Só Samuel decide.**

---

# PARTE III — O PLANO DO PROJETO

## O que o projeto é

Uma IA própria que trabalha sozinha e só chama Samuel para decidir, construída
sobre modelos abertos já treinados, financiada por consultoria enquanto não se
sustenta.

Não é: treinar modelo do zero, nem substituir Claude/GPT em raciocínio, nem
sistema 100% autônomo. Nenhuma das três existe hoje nem nos melhores
laboratórios.

## Os dois trilhos

**Trilho A — o sistema.** Construir a ferramenta que Samuel usa para construir
tudo o mais. Métrica: fração do trabalho feita no próprio app em vez de chat
externo.

**Trilho B — o caixa.** Consultoria via Pinheiro Negócios. Métrica: Marco 1,
R$5.000/mês.

O Trilho B financia o A. O A torna o B mais rápido. Correm juntos, mas a
atenção não se divide bem — e é aí que está a decisão do Problema 8.

## Estágios

**Estágio 0 — Fundação** (agora)
Sistema roda 24h sozinho e Samuel trabalha dentro dele.
Saída: uma semana inteira sem abrir chat externo para construir o sistema.

**Estágio 1 — Caixa**
Primeiro cliente pagante. Saída: Marco 1 batido.

**Estágio 2 — Aprendizado**
Volume de JSONL suficiente para o primeiro ciclo de LoRA. Ordem de centenas a
alguns milhares de exemplos com peso. Saída: modelo local assume a maior parte
das tarefas mecânicas, medido.

**Estágio 3 — Escala**
Máquina melhor, modelo maior, mais clientes. Saída: não depender do celular.

## Princípios que sobreviveram a esta sessão

**Visão antes do caminho.** Entender o terreno antes de construir. Foi
violado hoje quando escrevi funções sobre `conversaAtual().blocos` — nome e
estrutura que eu supus e nunca existiram.

**O método vive no julgamento, não em botões nem em campos.** Violado duas
vezes: primeiro nos botões de modo, depois nos moldes de resposta.

**Executar, não contar.** Varredura que conta o que existe não é diagnóstico.
A que abre cada seção, mede altura e roda cada ferramenta é.

**Toda camada precisa sobreviver à morte da anterior.** Cumprido na memória.
Ausente na Ponte e no motor.

**Não resolver de graça o que vale caro.** A consolidação das 80 clínicas fica
para engajamento pago.

## Riscos abertos

| Risco | Prazo | Gatilho de ação |
|---|---|---|
| Ponte é ponto único | agora | já aconteceu hoje |
| Sem cliente pagante | meses | Marco 1 não chega |
| Termos de uso de API sobre treino | antes do Estágio 2 | ler antes de treinar com saída de API |
| LGPD com dado de clínica | antes do primeiro arquivo real | separar antes, não depois |
| Atenção dividida entre trilhos | contínuo | nenhum dos dois avança |

## As três decisões que travam o resto

1. **Trilho A ou B primeiro?** Bloqueia a alocação da sua atenção.
2. **Tirar os dez moldes?** Bloqueia a IA ser útil de verdade na conversa.
3. **Como medir que melhorou?** Bloqueia todo o Estágio 2.

Nenhuma delas é técnica. Todas são suas.

---

*Este documento descreve um estado e um caminho. Se contradisser o que Samuel
decidir depois, quem vale é a decisão dele.*
