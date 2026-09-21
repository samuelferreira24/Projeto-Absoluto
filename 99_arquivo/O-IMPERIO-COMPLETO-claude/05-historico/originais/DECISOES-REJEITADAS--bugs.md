# DECISÕES REJEITADAS E REVISADAS

Conversa de 04/09 a 08/09/2026 · projeto O IMPÉRIO

Este arquivo existe para que ninguém proponha de novo o que já foi vetado.
**Rejeitada** = descartada. **Revisada** = mudou de forma, não foi jogada fora.

---

## RUMO E PRIORIDADE

### ✗ Reconstruir o aplicativo do zero
**Proposto por:** Claude, na primeira mensagem, ao não encontrar o código.
**Rejeitado por:** Samuel — *"Não é para construir do zero."*
**Motivo:** o app existia com 6.563 linhas e histórico. Recomeçar jogaria fora
meses de calibragem.
**Lição:** falta de acesso ao arquivo não é ausência do arquivo.

### ⟳ REVISADA — A ordem entre sistema e cliente
**Primeira forma:** cliente pagante primeiro; o sistema só provaria valor com
receita entrando.
**Forma final:** sistema primeiro.
**Revisado por:** Samuel — *"os app de terceiros estão me travando... preciso do
sistema para ganhar dinheiro."*
**Motivo:** limite diário de uso e perda de contexto em ferramenta de terceiro
não são incômodo, são o que impede produzir a entrega do cliente. O sistema não
é desvio da receita, é o destravamento dela.
**Registro honesto:** Claude subponderou esse bloqueio na análise original.

### ✗ Loop fechado (IA construindo e aplicando sozinha) agora
**Rejeitado por:** Samuel — *"não preciso fazer o loop fechado agora."*
**Forma aceita:** a IA gera o arquivo, Samuel sobe no GitHub. Manutenção manual
por enquanto.

### ✗ Copiar o modelo da MyHUB.IA
**Rejeitado por:** Samuel — *"eu não quero copiar o que eles fazem."*
**Motivo:** agregador resolve acesso, não memória. Cada modelo lá continua com
conversa própria. O diferencial do Sistema Absoluto é a memória que atravessa
modelos — o oposto do que agregador faz.

---

## MÉTODO E COMPORTAMENTO DA IA

### ✗ Método injetado como prompt rígido — rejeitado DUAS vezes

**Primeira vez:** dez botões de modo na interface.
**Rejeitado por:** Samuel, em sessão anterior. Botões removidos.

**Segunda vez:** dez formatos obrigatórios de resposta no código
(`chat`, `brainstorm`, `guerra`, `gps`, `arca`, `mapa`, `diagnostico`,
`prototipo`, `pesquisa`, `texto`), cada um com campos que a IA precisava
preencher.
**Rejeitado por:** Samuel — *"o método está travando o funcionamento... não
precisei disso para calibrar você."*
**Motivo:** método virado estrutura de dados obrigatória não deixa espaço para
julgamento. A IA deixava de responder para preencher formulário.
**Estado:** os dez moldes foram removidos em 08/09. 120 linhas viraram 22.
**Lição registrada como regra:** o método vive no julgamento, nunca em botão nem
em campo obrigatório.

### ⟳ REVISADA — O contexto fixo enviado em toda mensagem
**Primeira forma:** método, estado, tabuleiro e biblioteca inteiros, sempre.
**Forma final:** método resumido por padrão; íntegra só quando a conversa é de
decisão.
**Motivo:** medido em 1.732 tokens repetidos antes de Samuel escrever qualquer
coisa.
**Pendência:** ainda não há contagem de tokens nem compactação.

---

## MOTOR E MODELOS

### ✗ Rodar modelo MoE no celular
**Rejeitado por:** medição, não por opinião.
**Motivo:** MoE corta cálculo por token, não memória. O Qwen3 30B-A3B ativa 3B
mas precisa dos 30B carregados — cerca de 17 GB em Q4. O aparelho tem 4 GB.
**Consequência:** corrige um erro do documento de 07/09, que afirmava que MoE
"reduz RAM". Planejar em cima daquilo levava a um beco.
**Caminho aceito:** modelo pequeno e denso (Qwen3 1.7B ou 4B, Apache 2.0).

### ✗ Motor offline como prioridade agora
**Rejeitado por:** Samuel — *"no momento não quero me preocupar... nem no motor
offline."*
**Motivo:** a prioridade é o app servir de plataforma para motores de API.

### ✗ Tradutor Bergamot/Firefox em WASM
**Adiado por:** Samuel — *"vamos deixar esse tradutor para depois."*
**Risco que continua registrado:** há relato de exigência de SSE 4.1 e o suporte
nativo a aarch64 no Android está em estágio inicial. Pode não rodar no aparelho.
**Alternativa em uso:** memória de tradução que cresce a cada uso, mais o motor
para frase nova.

### ⟳ REVISADA — Dicionário de tradução fixo PT→EN
**Primeira forma:** lista fixa de termos português-inglês.
**Rejeitado por:** Samuel — *"esqueceu que vamos pegar informações do mundo
todo?"*
**Forma final:** o app lê as línguas que a biblioteca realmente tem e manda o
motor traduzir a consulta só para elas; mais o dicionário da Wikidata colhido
uma vez, que funciona offline em ~20 línguas.
**Motivo:** lista fixa nunca cobriria ~100 línguas do GDELT nem ~300 da
Wikipédia. Era fechar o mapa na raiz — erro que o documento mestre proíbe.

---

## ARQUITETURA

### ⟳ REVISADA — MAPE-K como modelo do sistema inteiro
**Primeira forma:** MAPE-K para tudo.
**Forma final:** MAPE-K só para a máquina; OODA para o jogo.
**Motivo:** MAPE-K assume estado desejado mensurável. "Atender o cliente ou
terminar o sistema" não tem estado desejado — tem tabuleiro que muda.
**Risco evitado:** forçar decisão estratégica dentro de MAPE-K reproduziria
exatamente o erro dos dez moldes.

### ✗ Adotar estrutura pronta de agentes (LangGraph, CrewAI) agora
**Rejeitado por:** Claude, com motivo.
**Motivo:** o sistema roda em Termux num celular. Dependência pesada de Python é
risco de instalação, não ganho. A opção de controle explícito cobra cerca de três
vezes mais linhas de código.
**Quando reavaliar:** na etapa em que o gerente muda para o Termux.

### ⟳ REVISADA — Como o APK se atualiza
**Primeira forma:** APK com os arquivos embutidos.
**Forma final:** casca fina apontando para o GitHub Pages.
**Motivo:** embutido custa 8 minutos de build e reinstalação a cada mudança.
Na fase de iteração diária, isso mata a velocidade.
**Armadilha registrada:** trocar de modo muda a origem, e `localStorage` é por
origem — a memória não vai junto. Exportar antes, importar depois.

### ⟳ REVISADA — O papel da Ponte
**Primeira forma:** só executar comandos do Termux.
**Forma final:** também servir o próprio aplicativo.
**Motivo:** aberto em `https://…github.io`, o Chrome recusa chamada a
`127.0.0.1`. Servido pela Ponte, app e Ponte ficam na mesma origem e o bloqueio
desaparece — sem precisar de APK.

### ✗ `localStorage` para guardar memória grande
**Rejeitado por:** medição. Limite de ~5 MB; texto completo de centenas de
artigos estoura.
**Forma adotada:** IndexedDB comprimido, com espelho em disco pela Ponte.

---

## ESCOPO E VISÃO

### ⟳ REVISADA — Os objetivos do projeto
**Primeira forma (Claude):** quatro objetivos, sendo o quarto "Permanência" —
sobreviver a troca de aparelho e ausência de Samuel.
**Rejeitado por:** Samuel — *"lembra da visão sem limite? Quero futuramente criar
várias IAs, criar empresas, entrar no mercado de tecnologia."*
**Forma final:** cinco objetivos. O quarto virou **Multiplicação** (várias IAs,
várias empresas, sem teto); Permanência passou a ser o quinto.
**Regra violada:** *"NÃO PENSAR PEQUENO / NÃO LIMITAR VISÃO DO PILOTO — nunca
fatiar visão grande em estágios obrigatórios."* Claude fatiou em cinco etapas
obrigatórias e trocou multiplicação por sobrevivência.

### ✗ Resolver de graça a consolidação das 80 clínicas
**Rejeitado por:** Samuel, em sessão anterior. Registro mantido.
**Motivo:** o que tem maior valor fica para engajamento pago.

---

## CONFLITO REGISTRADO, NÃO RESOLVIDO

**Sobre os dois documentos em `99-superado`:**
Eles foram marcados como superados pela Planta, mas a comparação de conteúdo
encontrou **82 trechos** em `01-relatorio-de-estado-08set.md` e **68 trechos** em
`02-analise-estrategica-08set.md` que **não existem** na Planta.

Não são duplicatas. São raciocínio e medição que a Planta absorveu em conclusão,
mas não em detalhe.

**Por isso não foram apagados**, e esta nota existe para que quem chegar depois
saiba que há material vivo ali — especialmente a medição do estado em 08/09 e a
derivação de por que MAPE-K serve só para metade.

---

## DECISÕES QUE CONTINUAM ABERTAS

Não foram rejeitadas nem aceitas. Esperam Samuel.

1. **Das quatro auto-propriedades, quais o sistema exerce sem perguntar?**
   Auto-cura de erro medido é uma coisa; auto-configuração que muda direção é
   outra. A linha precisa ser dita, não deduzida.

2. **Qual conjunto de perguntas define "melhorou"?**
   Proposta de Samuel já registrada: conjunto de referência com respostas que
   ele aprovou, comparadas antes e depois. Falta montar.

3. **Qual negócio vem depois do primeiro, e em que setor?**
   Define para onde a Fábrica é apontada.
