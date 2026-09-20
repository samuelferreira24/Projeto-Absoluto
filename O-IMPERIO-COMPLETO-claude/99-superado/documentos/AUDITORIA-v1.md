# Auditoria da PLANTA

Cada afirmação foi conferida contra o código publicado, não contra memória.
O que não pôde ser verificado está marcado como tal.

---

## VEREDITO EM UMA LINHA

O raciocínio é sólido e vale ser guardado. **Os números são todos inflados**, e
três peças descritas como "existe" não existem. O documento descreve um sistema
mais maduro do que o que está no disco.

---

## 1. OS NÚMEROS — TODOS INFLADOS

| Afirmação | Documento | Real | Erro |
|---|---|---|---|
| Linhas do app | 9.496 | 6.563 | +45% |
| Linhas de Python | 4.943 | 4.126 | +20% |
| Arquivos Python | 9 | 8 | +1 |
| Ferramentas | 17 | 15 | +2 |
| Seções | 10 | 6 | +67% |
| Fontes do coletor | 33 | ~25 | +32% |
| Biblioteca | 108 itens | 16 blocos de semente | não confere |

**Isto não é detalhe.** Um documento cuja função é permitir que outra IA pegue o
projeto no meio precisa que os números sejam verificáveis. Inflados, eles
treinam quem ler a confiar em medida que não bate.

**Hipótese testada e descartada:** "o documento descreve versão anterior". Ele
cita os dez botões de modo como erro *já corrigido*, então descreve o estado
atual.

---

## 2. O QUE ESTÁ CERTO E É VALIOSO

**A crítica ao formato de conversa (3.5) está correta e é a melhor parte.**
Verificado: `promptBase` concatena tudo em texto, sem papéis separados. Não
existe compactação. Isso impede cache de prefixo, chamada de ferramenta no
formato nativo, e distinção entre o que o modelo disse e o que Samuel disse.
É a fundação ausente, e o documento acertou em pôr como Etapa 1.

**A separação em dois laços (2.1) é uma boa distinção.** "Erro de renderização
não é decisão estratégica" é uma regra que evita erro real.

**O diagnóstico de arquitetura (2.6) procede.** Varredura, Oficina e Piloto
dentro do app: se ele não abre, nada disso roda.

**A conta de MoE (3.4) confere.** 30 bilhões em 4 bits dá ~15 GB. Ordem certa,
conclusão certa: em aparelho pequeno, modelo denso pequeno.

**Os Espaços existem de verdade.** Verificado: `const k = n => "sa:" + espaco + ":" + n`.
A memória é isolada por Espaço, como o documento afirma.

---

## 3. O QUE ESTÁ ERRADO

### 3.1 "Leitor de planilha entrega lixo silenciosamente" — o leitor não existe

O documento diz que o leitor atual "é regex sobre XML e entrega lixo nesses
casos". Verificado: **não há leitura de xlsx no app.** Nenhuma. O
`CompressionStream` presente serve para comprimir memória, não para ler Office.

Isso muda a Etapa 2 de "consertar" para "construir do zero" — trabalho bem maior
que o documento sugere.

### 3.2 "Criação de planilha já funciona e foi testada" — não existe

Mesma verificação. Não há geração de xlsx.

### 3.3 "Motor de Memória — existe, 4 camadas + JSONL"

Verificado: **zero menções a JSONL no app.** O formato de treino que o documento
diz estar "pronto e sem volume" não está pronto — não existe.

### 3.4 A tabela 8.1 diz "existe" para cinco peças

Três existem (coletor, orquestrador, executor). Uma existe parcialmente
(interface). Uma não existe (memória de treino). A frase **"As cinco existem"**
é falsa, e é a base do argumento de que "a Fábrica só precisa ser ligada".

---

## 4. FORA DA CAIXA — ONDE AS ESCOLHAS PODEM SER MELHORES

### 4.1 O laço rápido pode não precisar de IA nenhuma

O documento põe MAPE-K com motor de IA no meio. Mas as quatro fases descritas —
Ponte de pé? coletor rodou? motor vivo? — são **verificações determinísticas**.
Um script de 50 linhas com `if` resolve, sem gastar token, sem depender de
motor, e sem falhar quando a API cai.

Usar IA para verificar se um processo está vivo é usar o instrumento caro para
a tarefa que o barato faz melhor. Vale reservar o motor para o laço lento, onde
julgamento é necessário.

### 4.2 "Nada singular por natureza" pode ser cedo demais

A regra 8.6 exige que tudo nasça plural. É defensável a longo prazo, mas custa
complexidade **hoje**, com um Espaço em uso e nenhum cliente pagando.

Existe caminho intermediário: manter singular onde a mudança futura é barata
(uma variável, um prefixo de chave — o `k()` já resolve isso), e plural só onde
a mudança seria cara (formato de dado, esquema de memória). Tratar tudo como
plural é pagar adiantado por um problema que pode não chegar.

O próprio documento tem a regra que contradiz isso: *crescimento não pode passar
a capacidade de supervisão*.

### 4.3 A Oficina — o sistema consertando o próprio código — é o risco não nomeado

O documento lista travas (recusa sintaxe quebrada, guarda versão anterior), mas
não pergunta se **vale a pena existir agora**.

Um sistema que reescreve o próprio código, operado por uma pessoa só, sem
controle de versão externo, sem ambiente de teste separado — o modo de falha é
corromper o próprio app e perder a capacidade de consertar. As travas atenuam;
não eliminam.

Alternativa mais barata e mais segura: a Oficina *propõe* o arquivo, e Samuel
aplica por fora, com o Git guardando o histórico. Perde autonomia, ganha
reversibilidade real.

### 4.4 A régua da Etapa 2 pode estar apontada para o lugar errado

"O sistema está pronto quando montar a planilha do cliente por dentro dele."

Mas a planilha do cliente **já ficou pronta** — construída fora, e funcionando.
Refazer a capacidade dentro do sistema não gera receita nova; gera independência
de ferramenta, que é o Objetivo 1.

Como o próprio documento diz que o Objetivo 2 (receita) financia os outros, há
uma tensão não resolvida: a Etapa 2 serve ao objetivo 1, e é posta antes da
Etapa 3, que serve ao objetivo 2.

### 4.5 O risco maior está listado, mas não tratado

"Sistema que só se mantém a si mesmo — gravidade: a maior — sinal: é o estado
de hoje."

O documento nomeia isso e depois propõe cinco etapas, das quais **quatro são de
construção de sistema**. A Etapa 3 (cliente pagante) é a única que ataca o risco
maior, e está em terceiro lugar, atrás de duas etapas técnicas longas.

Se o risco maior é real, a ordem contradiz o diagnóstico.

---

## 5. O QUE FALTA NO DOCUMENTO

**Nenhum custo em tempo.** Nenhuma etapa tem estimativa. Sem isso não dá para
saber se a Etapa 1 leva uma semana ou dois meses — e essa diferença muda a ordem.

**Nenhum critério de desistência.** O documento diz como saber que uma etapa
terminou, nunca quando abandoná-la.

**A restrição real não aparece.** Samuel tem ~3h/dia e um emprego. Um plano de
cinco etapas técnicas dentro dessa restrição é uma informação que muda tudo, e
não está escrita.

---

## 6. O QUE EU FARIA

**Corrigir os números** — ou removê-los. Número errado é pior que número ausente
num documento feito para ser fonte de verdade.

**Trocar "existe" por três estados:** existe e foi exercitado · existe e nunca
rodou · não existe. Hoje os três aparecem como "existe".

**Adicionar tempo estimado por etapa** — mesmo grosseiro. É o que torna a ordem
discutível em vez de decretada.

**Reconsiderar a ordem** à luz do próprio risco maior nomeado.

O raciocínio do documento é bom. O problema é que ele descreve um sistema mais
pronto do que o que está no disco — e um documento cuja função é orientar quem
vier depois não pode ser otimista sobre o próprio estado.
