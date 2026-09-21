# SISTEMA ABSOLUTO
## A planta: o que é, para que serve, e como se constrói

Versão 1 · 08/09/2026
Documento de planejamento. Nada aqui foi construído a partir dele ainda.

---

## COMO LER ESTE DOCUMENTO

Ele tem três públicos ao mesmo tempo:

**Samuel** — para entender o que está sendo construído e por quê, sem precisar
saber programar.

**Outra IA que continue este trabalho** — para pegar o projeto no meio sem
precisar refazer as descobertas. As seções marcadas com ⚑ contêm decisões já
fechadas que não devem ser reabertas sem motivo novo.

**O próprio sistema, um dia** — quando ele for capaz de ler e propor mudanças
na própria planta.

Se este documento contradisser uma decisão de Samuel tomada depois, a decisão
vence e o documento se atualiza.

---

# PARTE 1 — O QUE É O SISTEMA ABSOLUTO

## 1.1 A frase que resume

Um sistema que trabalha sozinho, aprende com o próprio uso, e só chama Samuel
quando existe uma decisão de verdade a tomar.

E, no horizonte declarado desde o primeiro desenho: uma infraestrutura capaz de
gerar múltiplas inteligências, múltiplos produtos e múltiplos negócios — não um
aplicativo, uma **fábrica**.

## 1.2 O que ele não é

Não é um aplicativo de IA. Um aplicativo de IA é uma peça dentro dele — a boca
e os olhos, o lugar onde Samuel conversa. O sistema é maior que o aplicativo,
e o aplicativo é gerenciado pelo sistema, não o contrário.

Não é uma tentativa de treinar uma inteligência artificial do zero. Isso custa
centenas de milhões de dólares e não é o caminho. O caminho é pegar modelos
abertos já treinados e construir em volta deles a memória, o comportamento e a
autonomia que os tornam *seus*.

Não é um sistema totalmente autônomo. Isso não existe hoje, nem nos melhores
laboratórios do mundo. O que existe são sistemas que agem sozinhos dentro de
fronteiras declaradas, e param para perguntar fora delas.

## 1.3 O problema real que ele resolve

Samuel depende de aplicativos de terceiros para construir qualquer coisa. Esses
aplicativos têm limite diário de uso, perdem o contexto entre sessões, e não
guardam memória do que já foi decidido. Cada conversa nova começa explicando
tudo de novo.

Isso trava duas coisas ao mesmo tempo: a construção do próprio sistema, e a
produção das ferramentas que Samuel venderia a clientes.

O sistema existe para tirar esse teto do caminho.

## 1.4 Os quatro objetivos, em ordem ⚑

**Objetivo 1 — Independência de ferramenta.**
Construir o sistema dentro do sistema, sem depender de chat de terceiro.
*Como se mede:* uma semana inteira de trabalho sem abrir aplicativo externo.

**Objetivo 2 — Independência financeira.**
Marco 1: R$5.000 por mês recorrente. Sair do emprego formal.
*Como se mede:* o dinheiro entra na conta, três meses seguidos.

**Objetivo 3 — Independência de motor.**
A fração do trabalho resolvida por modelo próprio sobe; a dependência de API
paga cai. Não desaparece — cai.
*Como se mede:* percentual local versus percentual API, medido, não estimado.

**Objetivo 4 — Multiplicação.**
Um sistema vira muitos. Várias IAs, várias empresas, várias fontes de renda —
sem teto declarado. A infraestrutura que serve a um cliente serve a cem, e a
que serve a um negócio serve a vários setores.
*Como se mede:* o segundo negócio nasce reaproveitando a Fábrica, não do zero.

**Objetivo 5 — Permanência.**
O sistema sobrevive à troca de aparelho, à queda de um fornecedor, à entrada num
mercado novo, e à ausência de Samuel. Projeto multigeracional.
*Como se mede:* pode ser reconstruído do zero a partir da memória exportada, e
continua fazendo sentido para quem vier depois.

**Sobre a ordem.** O 2 financia o 3 e o 4. O 1 acelera o 2. Isso é dependência
de recurso, não hierarquia de importância — e **a arquitetura de todos os cinco
nasce desenhada desde já**. O que a capacidade atual controla é a vazão, nunca
a abertura. Fechar área na raiz porque "ainda não é hora" é o erro que este
projeto proíbe explicitamente.

Trabalhar no 3 antes do 2 é caro. Mas *desenhar* o 4 desde já é obrigatório,
porque decisão tomada hoje sem ele fecha porta amanhã.

---

# PARTE 2 — A ARQUITETURA

## 2.1 A descoberta que organiza tudo ⚑

O sistema tem duas naturezas diferentes, e cada uma pede um modelo diferente.
Confundir as duas foi a origem de vários erros já cometidos.

**A máquina.** A Ponte está de pé? O coletor rodou? O aplicativo tem erro? A
memória foi gravada? Tudo isso tem resposta objetiva e um estado desejado claro.

**O jogo.** Vale atender o cliente agora ou terminar o sistema? Esta notícia é
oportunidade ou ruído? Cobrar por hora ou por resultado? Não existe estado
desejado a comparar. Existe um tabuleiro que muda e uma decisão que só faz
sentido no contexto do momento.

## 2.2 O laço rápido — a máquina

Segue o modelo **MAPE-K**, criado pela IBM em 2005 e usado desde então para
sistemas auto-adaptativos. Ele separa o subsistema que *gerencia* do subsistema
*gerenciado*, e o que gerencia roda quatro fases sobre um Conhecimento comum:

| Fase | O que faz | No Sistema Absoluto |
|---|---|---|
| **Monitor** | sente o estado | varredura, saúde da Ponte, motor vivo |
| **Analisa** | compara com o esperado | o que está fora do lugar |
| **Planeja** | decide o conserto | qual mudança resolve |
| **Executa** | aplica | Oficina, piloto |
| **Conhecimento** | memória comum às quatro | a base única |

As quatro propriedades que o modelo busca: auto-configuração, auto-cura,
auto-otimização e auto-proteção.

Ciclo: minutos a horas.

## 2.3 O laço lento — o jogo

Segue **OODA** (Observar, Orientar, Decidir, Agir), criado por John Boyd para
combate aéreo e usado em estratégia competitiva. A diferença essencial em
relação ao MAPE-K está no **Orientar**: não é comparar com um alvo, é
reinterpretar o tabuleiro à luz da experiência acumulada. É onde mora o
julgamento.

| Fase | O que faz | No Sistema Absoluto |
|---|---|---|
| **Observar** | junta o que há | coletor, biblioteca, dados do cliente |
| **Orientar** | interpreta | especialistas + memória + método |
| **Decidir** | escolhe | **Samuel** — este é o portão |
| **Agir** | executa a escolha | projetos, propostas, entregas |

Ciclo: dias a semanas.

O método de Samuel — melhor jogada agora, problema que ela cria depois, início
do plano para esse problema — já é OODA. Ele não precisa ser inventado, precisa
ser reconhecido.

## 2.4 O padrão de quadro-negro

Dentro do Orientar existe uma terceira arquitetura clássica: vários
especialistas leem um espaço comum, cada um contribui quando reconhece algo do
seu domínio, e um controlador decide quem fala.

Os dez especialistas por domínio, com o Jetro decidindo o que sobe a Samuel,
são exatamente isso. Também já existe.

## 2.5 Como os dois laços se ligam

```
                    ┌─────────────────────────┐
                    │      CONHECIMENTO       │
                    │  memória · biblioteca   │
                    │  decisões · treino      │
                    └───────────┬─────────────┘
              lê e escreve      │      lê e escreve
        ┌───────────────────────┴──────────────────────┐
        │                                              │
┌───────▼────────┐                            ┌────────▼───────┐
│  LAÇO RÁPIDO   │                            │  LAÇO LENTO    │
│    MAPE-K      │                            │     OODA       │
│  mantém vivo   │───── o que está de pé ────▶│  decide o rumo │
│                │◀──── para que serve ───────│                │
└───────┬────────┘                            └────────┬───────┘
        │ age sobre                                    │ propõe a
┌───────▼────────┐                            ┌────────▼───────┐
│  O GERENCIADO  │                            │     SAMUEL     │
│ app · coletor  │                            │   decide       │
│ Ponte · motor  │                            └────────────────┘
└────────────────┘
```

**Regra que evita o erro já cometido:** um erro de renderização não é decisão
estratégica, e escolher trilho de negócio não é auto-cura. Os laços não se
misturam.

## 2.6 Onde cada coisa mora ⚑

| Camada | Onde roda | Por quê |
|---|---|---|
| Laço rápido inteiro | Termux | precisa rodar com o celular no bolso |
| Laço lento (Observar, Orientar) | Termux | idem |
| Decidir | Samuel | é o portão |
| Conhecimento | Termux, fonte única | as duas fases precisam ver o mesmo |
| Aplicativo de IA | navegador | é a boca e os olhos |

**O erro atual, nomeado:** varredura, Oficina e piloto foram construídos dentro
do aplicativo. Isso põe o sensor dentro do paciente e o executor dentro do que
ele conserta. Se o aplicativo não abrir, nada disso roda — e é exatamente aí que
mais se precisaria deles.

Isso não exige reescrita. Exige remanejamento.

---

# PARTE 3 — AS PEÇAS, UMA A UMA

## 3.1 O Conhecimento

A memória do sistema. Tudo que ele sabe e tudo que já viveu.

Contém: biblioteca coletada, memória de blocos calibrada por Samuel, decisões
tomadas, tabuleiro (alertas, prazos, o que não fazer), conversas, material de
treino em JSONL, dicionário multilíngue, e a memória de tradução.

**Regra de ouro:** fonte única. Hoje está partido entre o navegador e o Termux,
e isso significa que quem analisa não vê tudo que quem executa fez.

**Redundância obrigatória:** quatro camadas — armazenamento do navegador, disco
do Termux com versões datadas, espelho em Downloads, e cópia manual que sai do
aparelho. Cada camada sobrevive à morte da anterior. Esta é a única parte do
sistema hoje com redundância real, e é o padrão que o resto deve seguir.

## 3.2 O Coletor

Traz matéria-prima do mundo. Hoje: 33 fontes em 13 domínios, incluindo notícia
de cerca de 100 países com tradução automática, produção científica mundial, e
enciclopédia em centenas de línguas.

Neutraliza tentativa de injeção de comando antes de gravar — dado da internet
é dado hostil até prova em contrário.

**Regra:** o mapa de fontes nasce completo. A capacidade atual controla o que é
*processado*, nunca o que é *cadastrado*. Abrir uma fonte represada é decisão
simples, não retrabalho.

## 3.3 A Ponte

O canal entre o aplicativo e o Termux. Serve o aplicativo, executa comandos de
uma lista fechada, entrega biblioteca, dicionário, memória e plantão.

**Segurança, em ordem:** escuta apenas em 127.0.0.1, exige token, e só roda
comandos previamente autorizados. Sem o token, qualquer aplicativo instalado no
celular poderia mandar no Termux.

**Fraqueza conhecida e não resolvida:** é ponto único de falha. Ela cai, o
sistema inteiro para. Precisa de vigia que a levante, e o aplicativo precisa
saber funcionar degradado em vez de só falhar.

**Falta:** o sentido inverso. Hoje o aplicativo chama a Ponte; a Ponte nunca
chama o aplicativo. Sem isso, quem gerencia não tem como agir sobre o
gerenciado.

## 3.4 O Motor

A capacidade de raciocínio. Dois tipos, papéis diferentes:

**Motor pago (API).** Onde mora a inteligência boa. Usado para decisão, código,
estratégia. Não desaparece do plano — a expectativa realista é reduzir a
*fração* de uso, não eliminá-la.

**Motor local.** Roda no aparelho, sem internet e sem custo. Serve para o
volume mecânico: traduzir, classificar, resumir. Um modelo pequeno não vai
raciocinar como os grandes — isso é limite de tamanho, não de treino.

⚑ **Correção importante:** modelos de Mistura de Especialistas (MoE) cortam
*cálculo por token*, não *memória*. Um modelo de 30 bilhões com 3 ativos
responde rápido como um de 3, mas precisa dos 30 carregados — cerca de 17 GB.
Num aparelho de 4 GB, o caminho é modelo pequeno e denso.

**Fila de reserva:** vários motores cadastrados, em ordem. Falhou por motivo que
trocar resolve, cai para o próximo sem perguntar. Erro de configuração não faz
troca — trocar de motor não conserta chave errada.

**Licença importa quando virar produto:** Apache 2.0 e MIT são os únicos sem
armadilha. Outras licenças impõem condição para quem revende inferência, que é
exatamente o plano com clientes.

## 3.5 O Aplicativo de IA

A boca e os olhos. Comporta-se como qualquer aplicativo de IA: conversa, lê
arquivo, cria arquivo, busca na biblioteca.

**Regra que já foi violada duas vezes ⚑:** o método vive no julgamento, não na
forma. Não existe modo, formulário nem campo obrigatório. A resposta sai em
texto livre, do tamanho que a pergunta pedir. Método é calibragem que Samuel
corrige na conversa e o sistema guarda como memória — nunca esquema de dados.

**O que falta e é fundação:** formato interno de conversa com papéis separados,
traduzido para o dialeto de cada fornecedor no momento do envio. Hoje o
histórico inteiro vira um único bloco de texto, o que impede cache de prefixo,
chamada de ferramenta correta, compactação, e distinção entre o que o modelo
disse e o que Samuel disse.

## 3.6 Os Especialistas

Dez domínios: dados, técnico, financeiro, negócio, jurídico, segurança,
pesquisa, operações, científico, e os que a Governança abrir depois. Cada um
com escopo fechado, sem invadir o do outro.

O Maestro lê o pedido, escolhe quem responde, e junta as respostas.

## 3.7 A Varredura

O sistema se examina. **Executa, não conta.** Abre cada seção e mede altura em
pixels, roda cada ferramenta e confere a resposta, grava e lê de volta, pergunta
ao motor, compara versões.

Contar o que existe não é diagnóstico: um botão pode existir sem dono, um painel
pode ter conteúdo e altura zero, uma ferramenta pode estar registrada e falhar.

**Deve migrar para o Termux.** Sensor dentro do paciente não serve.

## 3.8 A Oficina

O sistema conserta o próprio código. A Varredura acha, a Oficina lê a fonte,
propõe a mudança, valida o arquivo inteiro antes de mostrar, Samuel aprova, e
o arquivo sai pronto.

**Travas obrigatórias:** recusa trecho inventado, recusa quebra de sintaxe,
recusa código que caiu no lugar errado do arquivo, recusa arquivo que encolheu
demais. Guarda a versão anterior sempre.

**Deve migrar para o Termux.** Quem conserta não pode morrer com o paciente.

## 3.9 O Piloto

O relógio. Olha o estado e faz o que está atrasado: coletar, completar artigo,
analisar, atualizar dicionário, gravar memória. Liga o motor quando a análise
precisa e desliga quando ocioso, porque motor consome bateria.

**Deve migrar para o Termux.** Um piloto que só voa com Samuel olhando não é
piloto.

## 3.10 O Motor de Memória e Treino

Todo uso vira material. Formato JSONL: entrada, saída, resultado, retorno.

**Prioridade do que treinar** (literatura consolidada, não escolha):
correção manual de Samuel é o sinal mais valioso que existe, porque é o único
que diz não só que estava errado, mas qual era o certo. Discordância entre
motores diferentes vem em seguida. Repetitivo e já certo se descarta.

**Risco a verificar antes de treinar ⚑:** os termos de serviço da maioria dos
fornecedores restringem usar saídas para treinar modelo concorrente. O risco
não está na licença do modelo base, está no conjunto de dados. Ler antes.

## 3.11 A Arquitetura de Plugue

Módulo novo entra sem mexer no sistema. Um módulo pode registrar ferramenta que
a IA passa a chamar sozinha, criar tela própria, engatar em evento, falar com o
Termux, e ter memória isolada.

**Auditoria obrigatória antes de rodar:** recusa código que apaga memória, vaza
chave, entra em laço infinito ou reescreve a página. Avisa sobre o que acessa
rede, executa código montado na hora, ou roda sozinho para sempre.

---

# PARTE 4 — A SEMENTE: O QUE CONSTRUIR, EM ORDEM

## 4.1 O princípio ⚑

Construir a menor peça capaz de provar que serve, usar essa peça para construir
a próxima, e nunca construir tudo de uma vez. É o mesmo princípio de um
compilador que compila a si mesmo.

A ordem abaixo é intencionalmente invertida em relação à complexidade: o que
vem primeiro não é o mais simples, é o que **destrava** o resto.

**Aviso sobre esta lista.** Ela é sequência de *destravamento*, não hierarquia de
importância nem etapa obrigatória. O documento mestre proíbe fatiar visão grande
em estágios obrigatórios. O que está na Parte 8 — a Fábrica, a multiplicação, o
mercado — é desenhado desde já e restringe cada decisão aqui. Nada abaixo pode
fechar porta lá.

## 4.2 Etapa 1 — O núcleo de conversa

**Por que primeiro:** sem isto, toda melhoria futura vai ter que contornar a
mesma limitação. É a fundação que hoje não existe.

O que precisa existir:

- Formato interno de mensagem com papéis separados (sistema, Samuel, IA,
  ferramenta pedida, resultado da ferramenta)
- Tradutor para o dialeto de cada fornecedor no envio: o campo de instrução do
  sistema tem nome diferente em cada API, e ferramenta tem formato diferente em
  cada uma
- Contagem de tokens antes de enviar
- Compactação: quando não couber, resumir o meio da conversa e preservar as
  pontas
- Ordem estável para aproveitar cache de prefixo: o que não muda vem primeiro
- Limite de resposta grande o bastante para código longo

**Como saber que terminou:** trocar de motor no meio de uma conversa longa e
continuar de onde parou, sem perder nada e sem erro.

## 4.3 Etapa 2 — Trabalho real de arquivo

**Por que segundo:** é a régua que Samuel definiu. O sistema está pronto quando
ele consegue montar a planilha do cliente por dentro dele, do começo ao fim.

O que precisa existir:

- Leitor de planilha que trate fórmula, data e célula mesclada — o leitor atual
  é regex sobre XML e entrega lixo silenciosamente nesses casos, que é pior que
  falhar
- Leitor de PDF que funcione com arquivo comprimido, que é a maioria
- Criação de planilha e documento já funciona e foi testada

**Como saber que terminou:** o DRE real da clínica entra, sai analisado, e a
planilha de entrega sai pronta — tudo dentro do sistema.

## 4.4 Etapa 3 — A primeira entrega paga

**Por que terceiro:** é a única coisa capaz de dizer se o sistema serve. Até
aqui, o único recurso gerenciado pelo sistema é o próprio sistema — motor
girando em neutro.

Não é etapa técnica. É contato com a realidade.

## 4.5 Etapa 4 — Mudar o gerente de lado

**Por que só agora:** é o que dá mais vontade de fazer primeiro, e é exatamente
por isso que fica por último. Sem receita, é sofisticação sobre um sistema que
não provou nada.

O que precisa existir:

- Varredura, Oficina e Piloto migrados para o Termux
- Conhecimento unificado em fonte única
- Ponte de mão dupla, para o gerente agir sobre o aplicativo
- Aplicativo expondo estado para ser lido de fora
- Vigia que levante a Ponte quando ela cair

## 4.6 Etapa 5 — Aprender de verdade

- Volume suficiente de exemplos: ordem de centenas a alguns milhares, com peso
- Conjunto de referência para medir antes e depois
- Primeiro ciclo de ajuste fino em nuvem alugada por hora
- Medição da fração local versus API

## 4.7 Sobre usar uma estrutura pronta de agentes

Existem estruturas maduras para orquestrar agentes, com aprovação humana antes
de ação irreversível já embutida. A mais indicada quando se precisa de controle
explícito de estado, execução durável com pontos de retomada, e interrupção para
aprovação humana como recurso de primeira classe, cobra isso em verbosidade —
cerca de três vezes mais linhas que alternativas de mais alto nível, e o que se
compra são transições inspecionáveis.

**Recomendação para este projeto:** não adotar agora. O sistema roda em Termux
num celular, e uma dependência pesada de Python é risco de instalação, não
ganho. Reavaliar na Etapa 4, quando o gerente mudar de lado — que é quando
orquestração de verdade começa a existir.

---

# PARTE 5 — AS REGRAS QUE NÃO SE NEGOCIAM ⚑

**Visão antes do caminho.** Entender o terreno antes de construir. Foi violado
quando se escreveu código sobre uma estrutura de dados suposta que nunca
existiu.

**O método vive no julgamento.** Nunca em botão, nunca em campo obrigatório.
Violado duas vezes: nos dez botões de modo, e nos dez formatos de resposta.

**Executar, não contar.** Diagnóstico que conta o que existe não é diagnóstico.

**Toda camada sobrevive à morte da anterior.** Cumprido na memória. Ausente na
Ponte e no motor.

**O mapa nasce completo.** A capacidade atual controla o que é processado,
nunca o que é cadastrado.

**Nunca decidir no lugar de Samuel.** Se ele não consegue explicar a decisão sem
reler a proposta, decidiu-se demais por ele.

**Não resolver de graça o que vale caro.** O que tem maior valor fica para
engajamento pago.

**Crescimento não pode passar a capacidade de supervisão.** É o único freio
legítimo, e chama-se avalanche disfarçada de avanço.

**Substituição por âncora exige verificação.** Uma alteração que não encontra o
alvo e passa calada é uma alteração que não aconteceu.

**Toda entrega passa por navegador de verdade.** Sintaxe válida não prova
estrutura certa.

---

# PARTE 6 — OS RISCOS

| Risco | Gravidade | Sinal de que aconteceu |
|---|---|---|
| Sistema que só se mantém a si mesmo | **a maior** | é o estado de hoje |
| Sistema pronto, receita zero | alta | mais um mês sem cliente |
| Complexidade além da supervisão | alta | Samuel não consegue explicar uma peça |
| Ponte como ponto único | média | já aconteceu |
| Atenção dividida entre trilhos | alta | nenhum dos dois avança |
| Dado de saúde sem separação | alta | primeiro arquivo real entra sem política |
| Termos de uso sobre treino | média | descoberto depois de treinar |
| Dependência de fornecedor único | média | um provedor muda preço ou some |
| Peça nascida singular | **alta** | o segundo Espaço exige reescrita |
| Memória de clientes misturada | **alta** | dado de um aparece no contexto de outro |
| Fábrica presa à instância | alta | o 2º negócio custa como o 1º |

---

# PARTE 7 — O QUE SÓ SAMUEL DECIDE

**1. Quando a resposta da irmã chegar, o sistema para e o cliente é atendido?**
Já respondida na prática: o sistema vem primeiro, porque sem ele o atendimento
é travado por limite de ferramenta de terceiro. Registrada aqui para não se
perder.

**2. Das quatro auto-propriedades, quais o sistema exerce sem perguntar?**
Auto-cura de erro medido é uma coisa. Auto-configuração que muda direção é
outra. A linha precisa ser dita, não deduzida.

**3. Até onde vai a ambição declarada, e em que ordem?**
Várias IAs, várias empresas, entrada no mercado de tecnologia, dinastia
multigeracional. A Parte 8 desenha a arquitetura que sustenta isso. O que ela
não decide é qual negócio vem depois do primeiro, e em que setor — e essa é a
escolha que define para onde a Fábrica é apontada.

**4. Qual conjunto de perguntas define "melhorou"?**
Sem isso, nenhum treino pode ser avaliado, e a Etapa 5 inteira fica em suspenso.
Proposta de Samuel, já registrada: um conjunto de perguntas com respostas que
ele aprovou, comparadas antes e depois. É um método real e tem nome — conjunto
de referência.

---

# PARTE 8 — A ESCALA: DE UM SISTEMA PARA MUITOS

## 8.1 A Fábrica ⚑

O objetivo de longo prazo não é construir um produto. É construir a
infraestrutura reutilizável capaz de gerar produtos repetidamente.

Cinco peças, já nomeadas no documento mestre:

| Peça | O que faz | Estado |
|---|---|---|
| **Motor de Pesquisa** | busca informação externa | existe — 33 fontes |
| **Motor de Raciocínio** | a IA calibrada | existe — motor + memória |
| **Motor de Execução** | gera código, testa, corrige | existe — Oficina + plugues |
| **Motor de Memória** | grava tudo e alimenta o aprendizado | existe — 4 camadas + JSONL |
| **Interface de Comando** | por onde Samuel direciona | existe — o aplicativo |

**As cinco existem.** Não estão integradas, não foram exercitadas juntas, e três
estão do lado errado. Mas a Fábrica não precisa ser inventada — precisa ser
ligada.

Cada produto novo consome as cinco. É isso que faz o segundo negócio custar uma
fração do primeiro.

## 8.2 O mecanismo de multiplicação já existe

O aplicativo tem **Espaços** — hoje Núcleo (CPF) e Operação (CNPJ), cada um com
memória, conversas e nuvem separadas.

Esse é o mecanismo. Um Espaço é uma instância da Fábrica:

```
                    ┌──────────────────────────┐
                    │        A FÁBRICA         │
                    │  pesquisa · raciocínio   │
                    │  execução · memória      │
                    │  interface               │
                    └────────────┬─────────────┘
         instancia               │              instancia
    ┌───────────────┬────────────┼────────────┬───────────────┐
    ▼               ▼            ▼            ▼               ▼
 Núcleo         Operação      Cliente A    Cliente B      Negócio 2
 (CPF)           (CNPJ)       (clínicas)   (outro setor)  (o que vier)

 memória própria · nuvem própria · permissão própria
 Fábrica compartilhada · aprendizado que atravessa
```

**A consequência que muda decisão hoje:** nada no sistema pode assumir que
existe *um* de qualquer coisa. Uma memória, uma nuvem, um cliente, um motor, um
negócio. Tudo que hoje é singular precisa nascer plural, mesmo com um só em uso.

Isso é a diferença entre vazão e abertura. Hoje roda um Espaço. A arquitetura
tem que aguentar cem.

## 8.3 O que "várias IAs" significa na prática

Não são várias cópias do mesmo assistente. São inteligências com escopos
diferentes, cada uma dona de um pedaço:

**Por camada de operação** — a IA que gerencia o sistema, a IA que conversa com
Samuel, a IA que atende o cliente. Já desenhado nos dois laços.

**Por domínio** — os dez especialistas. Já existe.

**Por negócio** — cada Espaço com sua IA, treinada no que aquele negócio viveu.
A IA das clínicas aprende clínica; a do próximo setor aprende aquele setor. Elas
compartilham a Fábrica e não compartilham a memória.

**Por cliente, dentro do negócio** — o documento mestre é explícito: o produto
não é um painel para o chefe, é produtividade distribuída por papel em toda a
organização. Chefe vê consolidado estratégico, gerente vê a própria unidade,
equipe vê o dia a dia. Um motor, camadas de acesso por papel.

Isso último não é ambição vaga: o painel do CEO do primeiro cliente já revelou
20 empresas em 4 carteiras, abrangendo 11 setores. O mercado da primeira porta é
maior que a porta.

## 8.4 O laço econômico ⚑

```
   cliente paga ──▶ caixa ──▶ equipamento e capacidade
        ▲                              │
        │                              ▼
   mais valor ◀── IA mais forte ◀── comportamento de uso
```

Dois ativos correm em paralelo e não se confundem:

**Caixa** — curto prazo, financia a máquina.
**Comportamento** — longo prazo, fortalece a inteligência.

O segundo é o que não se compra e o que ninguém copia. Modelo é mercadoria:
qualquer um usa o mesmo. Memória e comportamento acumulado, não.

## 8.5 Entrar no mercado de tecnologia

A estratégia declarada é a do seguidor rápido: lançar simples, gerar receita,
reinvestir com dado de uso real, e ficar superior **no nicho** — não no geral.

Traduzido em decisões que valem desde hoje:

- **Nunca entregar o código-fonte.** Controlar servidor, login e chave. Cortar o
  acesso corta o serviço.
- **Registrar comportamento, nunca dado pessoal.** O "o quê" pode; o "quem" não.
  Com dado de saúde, cuidado redobrado.
- **Licença do modelo importa quando virar produto.** Apache 2.0 e MIT são os
  únicos sem condição para quem revende inferência.
- **Planejar para a permanência, não para a entrada.** O primeiro contrato é
  porta, não destino. Preparar as rodadas 2, 3 e 4 de problemas que aparecem
  depois.

## 8.6 O que a escala exige da arquitetura, desde agora

Estas não são etapas futuras. São restrições que decisões de hoje precisam
respeitar para não fechar porta:

| Exigência | Por quê | Custa caro depois? |
|---|---|---|
| Nada singular por natureza | um Espaço hoje, muitos amanhã | sim — reescrita |
| Memória isolada por Espaço | dado de cliente não se mistura | sim — e é risco legal |
| Fábrica separada da instância | é o que faz o 2º custar pouco | sim — refatoração |
| Permissão por papel desde o desenho | o produto é a hierarquia inteira | sim |
| Motor intercambiável | não depender de fornecedor | não — já resolvido |
| Conhecimento exportável e reimportável | reconstruir em qualquer lugar | não — já resolvido |

As quatro primeiras ainda não estão garantidas. As duas últimas já estão.

## 8.7 A régua honesta

Nada disso muda a etapa de agora. O primeiro cliente pagante continua sendo o
que prova que o sistema serve, e continua vindo antes.

O que muda é o **desenho**: cada peça construída daqui em diante nasce
perguntando "e quando forem cem?" — mesmo enquanto for um. É a diferença entre
represar uma fonte e fechá-la na raiz.

---

# APÊNDICE A — O ESTADO EM 08/09/2026

**Aplicativo:** 9.496 linhas, 237 funções, 17 ferramentas, 10 seções, 24
subpáginas de ajustes.

**Python no Termux:** 4.943 linhas em 9 arquivos.

**Conhecimento:** 108 itens na biblioteca, memória em 4 camadas, formato de
treino pronto e ainda sem volume.

**Peças do MAPE-K que já existem:** todas. Três estão do lado errado.

**O que nunca aconteceu:** nenhum cliente pagou, nenhum ciclo de 24 horas rodou
inteiro, nenhuma análise virou decisão executada, nenhum conserto da Oficina foi
aplicado.

---

# APÊNDICE B — GLOSSÁRIO

**MAPE-K** — Monitor, Analisa, Planeja, Executa, sobre um Conhecimento comum.
Modelo da IBM para sistemas que se gerenciam.

**OODA** — Observar, Orientar, Decidir, Agir. Modelo de decisão em ambiente
competitivo.

**Quadro-negro** — arquitetura onde vários especialistas leem e escrevem num
espaço comum e um controlador decide quem age.

**MoE (Mistura de Especialistas)** — modelo dividido em partes, das quais só a
relevante é ativada por token. Corta cálculo, não memória.

**LoRA** — técnica de ajuste fino barata, que altera uma fração pequena dos
pesos em vez do modelo inteiro.

**JSONL** — um exemplo por linha, em JSON. Formato padrão de conjunto de treino.

**Quantização** — comprimir os pesos do modelo para ocupar menos memória, com
perda pequena de qualidade. Q4 é o corte comum.

**Ponto único de falha** — peça cuja queda derruba o sistema inteiro.

**Cache de prefixo** — desconto que os fornecedores dão quando o começo da
mensagem se repete idêntico. Exige que a parte estável venha primeiro.

---

*Fim da versão 1. O que estiver errado aqui deve ser corrigido aqui, não
contornado no código.*
