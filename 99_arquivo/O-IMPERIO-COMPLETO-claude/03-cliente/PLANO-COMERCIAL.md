# PLANO — da planilha ao sistema

Documento de trabalho. Nada aqui está fechado: é o mapa com os custos reais
de cada caminho, para Samuel escolher.

---

## O QUE ESTÁ SENDO CONSTRUÍDO

Não é uma planilha. A planilha é a **prova** de que o problema foi entendido.

O produto é a camada que hoje não existe: **a consolidação das 80 clínicas**,
que hoje é feita por uma equipe de madrugada copiando planilhas do WhatsApp.

Regra que não se quebra: nunca competir com o sistema clínico que cada clínica
já usa. Ele cuida de agenda, prontuário e faturamento. Nós somos a camada de
cima — gestão consolidada, que ele não faz. Complemento não gera resistência
interna; substituto gera.

---

## AS CINCO FASES

### FASE 0 — Isca (agora)
**Entrega:** a planilha de uma clínica, de graça.
**Custo:** tempo de Samuel.
**Ganho:** nenhum em dinheiro. O ganho é a porta aberta.
**Gatilho para avançar:** a líder usar por 2 semanas sem reclamar.

**A regra que define o que entra e o que não entra:**

A planilha resolve a dor da LÍDER — parar de digitar o mesmo número três vezes,
parar de tirar print para o PowerPoint. Isso é real e ela sente todo dia.

A planilha NÃO resolve a dor da GESTORA — juntar as 80 clínicas. Essa fica
intocada de propósito. É ela que se vende na Fase 2.

Não é má-fé: é sequência. Resolver a dor mais cara de graça é entregar o
produto inteiro e ficar sem o que cobrar. A líder ganha tempo hoje; a gestora
vê o problema dela ficar mais evidente, não menor.

Risco aceito: entregar `.xlsx` significa que copiam para as outras 79 sem pagar.
Isso é desejável. Quanto mais clínicas com a planilha boa, mais gritante fica
o gargalo de consolidar todas — que é justamente o que está à venda.

### FASE 1 — Contrato
**Entrega:** proposta escrita, com escopo e preço.
**Ganho:** o primeiro dinheiro.
**Regra:** contrato ANTES do sistema. Construir e depois negociar é entregar poder.

O que precisa estar no contrato desde a primeira versão:
- escopo do que é entregue e do que não é
- prazo de suporte e horário de atendimento
- propriedade: o código é de Samuel; o dado da operação é do cliente
- **cláusula de aprendizado** (ver seção própria abaixo)
- condição de saída dos dois lados

### FASE 2 — Piloto (5 a 10 clínicas)
**Entrega:** sistema web. As clínicas lançam, a gestora vê consolidado —
**é aqui que a equipe da madrugada deixa de copiar planilha.**
Essa peça foi guardada de propósito na Fase 0.
**Ganho:** mensalidade por clínica.
**Aprende:** o que quebra quando é gente de verdade usando.
**Gatilho:** 30 dias sem intervenção manual de Samuel.

Por que piloto e não as 80 direto: com 10 clínicas, um erro é contornável.
Com 80, é crise. E crise no primeiro mês fecha a porta.

### FASE 3 — Escala (80 clínicas)
**Entrega:** o mesmo sistema, com as 80 dentro.
**Ganho:** a recorrência de verdade.
**O que morre:** a equipe da madrugada deixa de copiar planilha.
**Aprende:** o custo real de operar em escala.

Aqui aparece a obrigação séria: 80 clínicas fechando caixa na sexta à noite.
O sistema precisa ser desenhado para quase nunca precisar de Samuel —
funcionar offline, salvar sozinho, e uma clínica travada não derruba as outras.

### FASE 4 — Segunda gestora
**Entrega:** o mesmo sistema, outro cliente.
**Ganho:** deixa de ter um cliente só.
**Por que importa:** 80 clínicas parece diversificado, mas é um contrato.
Se a Pinheiro sair, perde tudo de uma vez.

Consequência para o desenho: nada específico da Pinheiro no código.
Nenhuma regra que só funcione com o jeito deles.

---

## O QUE FICA COM SAMUEL

**O código.** Nunca entregue. O cliente usa; não recebe o fonte.

**O conhecimento de domínio.** Depois de 80 clínicas, saber como uma rede de
saúde funciona, onde dói, quanto custa cada dor, e o que faz um dono pagar.
Isso não está em dado nenhum — está na experiência. E é o que permite vender
para a segunda gestora.

**O aprendizado de uso** (ver abaixo).

## O QUE NÃO FICA

**Dado financeiro identificado da clínica.** É do cliente.
**Qualquer dado de paciente.** Nunca. Dado de saúde é categoria especial na LGPD,
e nem com autorização vale o risco.

---

## A CLÁUSULA DE APRENDIZADO

O que Samuel quer acumular não é o dado da operação — é **como o sistema é usado**.
Isso é diferente, é legítimo, e precisa estar escrito.

### O que pode ser coletado

| O que | Por quê serve | Precisa consentimento? |
|---|---|---|
| Que perguntas os gestores fazem ao sistema | ensina o que realmente importa para quem decide | sim, em cláusula |
| Que caminho seguem depois de ver um número | mostra o fluxo de decisão real | sim, em cláusula |
| Onde travam, o que abandonam | aponta o que está mal desenhado | sim, em cláusula |
| Padrão agregado sem identificar clínica | conhecimento de domínio | sim, e anonimizado |

### O que NÃO pode, mesmo com cláusula

- conteúdo que contenha nome de paciente, procedimento individual, prontuário
- faturamento identificado de uma clínica específica, fora do uso contratado
- qualquer coisa que permita reconstruir quem é quem

### Como escrever

A cláusula precisa dizer, em português claro:
- que o uso do sistema gera registros de como ele é usado
- que esses registros são usados para melhorar o produto
- que nenhum dado identificado de clínica ou paciente sai dali
- que o cliente pode pedir para ver o que é coletado

Pedir isso desde o primeiro contrato é normal e aceito. Pedir depois parece
que estava sendo feito escondido — e aí queima a confiança, que é o ativo
mais caro do projeto.

---

## MODELO DE COBRANÇA — três caminhos

| Modelo | Como funciona | Prós | Contras |
|---|---|---|---|
| **Por clínica/mês** | valor fixo × 80 | previsível, escala com o cliente | precisa provar valor por unidade |
| **Contrato único** | valor mensal pela rede toda | negociação única, mais simples | não cresce se abrirem clínica |
| **Implantação + mensalidade** | entrada + recorrência menor | cobre o esforço inicial | entrada pode travar a decisão |

Não recomendo escolher agora. A resposta da pergunta 16 do questionário
("o que faria o CEO dizer isso eu quero") indica qual argumento pesa mais,
e o modelo deve seguir o argumento.

Referência para calibrar: o custo atual medido do trabalho manual é da ordem
de 1.173 horas/mês nas 80 clínicas, só preenchendo planilha — sem contar a
equipe da madrugada. Qualquer preço deve ser lido contra esse número.

---

## OS RISCOS QUE IMPORTAM

### 1. Fazer igual ou pior que o de hoje
Eles têm sistema que funciona. Trocar por equivalente é risco sem ganho.
**Mitigação:** o ganho tem que ser óbvio e mensurável — tempo devolvido e
consolidação automática. Não "é mais bonito".

### 2. Suporte vira obrigação impossível
80 clínicas, sexta à noite, Samuel no CLT.
**Mitigação:** desenhar para não precisar de suporte. Offline primeiro, salvar
sozinho, isolamento entre clínicas. E horário de atendimento no contrato.

### 3. Um cliente só
**Mitigação:** desde a Fase 2, nada específico da Pinheiro no código.

### 4. Avalanche
80 clínicas de uma vez, com Samuel sozinho, é crescer além da supervisão.
**Mitigação:** o piloto de 10 existe para isso. O freio é de Samuel — mas o
gatilho está escrito: só avança com 30 dias sem intervenção manual.

### 5. Dependência de uma pessoa dentro do cliente
Hoje o canal é a irmã. Se ela sair da empresa, o contrato fica órfão.
**Mitigação:** o contrato é com a empresa, não com ela. E a relação precisa
chegar ao regional e ao CEO antes da Fase 3.

---

## O QUE NÃO FAZER

**Não falar de IA no primeiro pitch.** Fale de tempo devolvido e consolidação
automática — coisas que eles medem. IA que analisa é o segundo contrato, quando
já houver prova de entrega. Na frente, vira promessa vaga.

**Não prometer prazo antes de saber o que a Fase 0 revela.**

**Não construir o sistema antes do contrato.**

**Não substituir o sistema clínico de ninguém.**

---

## O QUE FICA GUARDADO PARA A FASE PAGA

Registrado para não ser entregue por engano:

| Peça | Fase |
|---|---|
| Planilha de uma clínica, sem digitação repetida | 0 — grátis |
| Tela pronta para o print (mata o PowerPoint) | 0 — grátis |
| **Consolidação automática das 80** | 2 — pago |
| **Fim da equipe da madrugada** | 2 — pago |
| Comparação entre clínicas | 2 — pago |
| DRE que se monta sozinho | 2 — pago |
| Análise por IA | 3 — segundo contrato |

A pesquisa sobre a equipe da madrugada continua valendo — precisamos SABER
como funciona para desenhar certo depois. Saber agora, resolver quando pagar.

---

## O PRÓXIMO PASSO CONCRETO

1. Lary usa a planilha por duas semanas
2. As respostas do questionário 2 chegam
3. Com elas: desenhar a proposta com escopo e preço
4. Só então: construir

O que decide tudo é a pergunta 14 do questionário — se já tentaram trocar de
sistema antes e o que deu errado. O motivo do fracasso anterior é o mapa do
que evitar.
