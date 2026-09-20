# LINHA DO TEMPO

Conversa de 04/09 a 08/09/2026 · projeto O IMPÉRIO

Datas conferidas contra a data de modificação dos arquivos reais, não escritas
de memória.

---

## FASE 1 — Recuperar o contexto perdido
**04/09, início da conversa**

**O que se fez:** Samuel trocou de chat e o código não veio junto. Foi preciso
descobrir que o histórico de conversa é recuperável dentro de um Projeto, mas o
arquivo gerado não — o container de execução zera entre sessões.

**O que se aprendeu:** existem dois canais de atualização diferentes e isso
confundiu a sessão inteira. O `index.html` mora no GitHub Pages; o `ponte.py`
mora em `~/sa` no celular. Atualizar o site não atualiza o Termux.

**O erro desta fase:** Claude anunciou que ia reconstruir o app do zero antes de
confirmar que ele não existia. Samuel cortou: *"Não é para construir do zero."*

---

## FASE 2 — Consertar o app morto
**04/09**

**O que se fez:** diagnóstico do app que não respondia. Quatro bugs reais, todos
confirmados rodando o app em navegador headless, não por leitura de código:

1. `$("#novaConversaRapida")` no topo do JS — botão removido numa mudança
   anterior. TypeError no boot matou 1.090 linhas e 86 listeners.
2. Faltava um `</div>` — sete painéis ficaram aninhados dentro do chat e
   herdavam `display:none`, com altura zero.
3. Dois handlers no mesmo botão de motor; o legado abria um `prompt()` que
   travava tudo.
4. 94 ligações de topo sem proteção — qualquer elemento removido repetiria o
   bug 1.

**O que se aprendeu:** sintaxe válida não prova nada. Nenhum desses quatro
apareceria em revisão de código nem em `node --check`. Painel com conteúdo no
DOM e altura zero é bug, não é vazio.

**O erro desta fase:** nenhum. Esta fase foi bem feita.

---

## FASE 3 — Reforma visual e reorganização
**05/09, 02:36 às 03:51**

**O que se fez:** ícone refeito no modelo enviado, tela inicial, tema
claro/escuro com opção Sistema, Ajustes reorganizado em índice com subpáginas,
botão de motor redesenhado, Capacitor configurado como casca fina.

**O erro desta fase:** o JavaScript novo caiu **dentro do bloco `<style>`** — e
isso aconteceu **duas vezes**. Não quebra a sintaxe do script, não aparece em
`node --check`, e mata o CSS em silêncio. Virou regra permanente: confirmar em
que bloco o código caiu, não só se compila.

---

## FASE 4 — Termux, Ponte e coleta mundial
**05/09, 13:54 às 14:06**

**O que se fez:** a Ponte foi criada — o Termux virou serviço que o app comanda
sem ninguém abrir o terminal. O coletor cresceu de 20 para 33 fontes em 13
domínios, com GDELT (notícia de ~100 países, traduzida), OpenAlex e Wikipédia.
Scripts de arranque e coleta agendada.

**Resultado real, medido na primeira execução:** 111 itens novos numa rodada,
232 na biblioteca. Nenhuma fonte falhou naquela primeira vez.

**O erro desta fase:** a mensagem de erro da Ponte era genérica — *"não achei a
Ponte"* — e escondia três causas com consertos opostos: servidor desligado,
token recusado, navegador bloqueando https→http local. Custou tempo de
diagnóstico que não precisava existir.

---

## FASE 5 — Memória permanente, tradução e piloto
**05/09 ao 08/09**

**O que se fez:** memória em quatro camadas com versões datadas e cópia de fuga.
Página de leitura com texto completo. Dicionário da Wikidata para busca
multilíngue offline. Memória de tradução que cresce a cada uso. Piloto
automático que decide o que rodar e liga/desliga o motor sozinho. Ponte capaz de
se atualizar do GitHub.

**O que se aprendeu:** busca multilíngue não se faz com lista fixa. O app precisa
ler as línguas que a biblioteca realmente tem.

**O erro desta fase:** uma substituição por âncora **não encontrou o alvo e
passou calada**. O corte pelo dicionário nunca foi aplicado, e o app continuou
chamando o motor à toa. Só apareceu porque a saída do teste dizia "motor não
respondeu" onde deveria dizer "dicionário". Virou regra: `assert` antes,
`grep` depois.

---

## FASE 6 — Varredura, Oficina e material de treino
**08/09, até 20:28**

**O que se fez:** varredura que **executa** em vez de contar — abre cada seção e
mede altura em pixels, roda cada ferramenta e confere a resposta, compara
versões entre app e Ponte. Oficina que lê o próprio código, propõe conserto,
valida o arquivo inteiro e entrega para Samuel aprovar. Motor de memória em
JSONL. Auditoria de código gerado. Os dez moldes de resposta removidos.

**O que se aprendeu:** a varredura se provou no primeiro uso, achando um órfão
que Claude não sabia que existia (`#btnTema`).

**O erro desta fase — o mais grave da conversa:** Claude escreveu três funções
sobre `conversaAtual().blocos` — **nome de função e estrutura de dados que nunca
existiram**. O real é `conv().hist` com `{pergunta, resposta}`. Passou em
`node --check`, foi entregue, e **o Motor de Memória não gravava nada**. Votos e
correções caíam no vazio.

---

## FASE 7 — Planejamento
**08/09, 20:19 às 21:23**

**O que se fez:** três documentos em progressão — relatório de estado medido,
análise estratégica, e a Planta completa. Descoberta de que o modelo que Samuel
descrevia existe e tem nome: MAPE-K, da IBM, 2005. E de que ele serve só para
metade do sistema; a outra metade é OODA.

**O erro desta fase:** Claude **amputou a visão**. Fatiou o projeto em cinco
etapas obrigatórias e trocou o objetivo de Multiplicação por Permanência —
violando a regra escrita no documento mestre de nunca fatiar visão grande em
estágios obrigatórios. Samuel corrigiu: *"lembra da visão sem limite?"*

---

# O PADRÃO QUE ATRAVESSA OS ERROS

Cinco fases tiveram erro. Todos os cinco são **o mesmo erro**:

| Fase | O que foi suposto em vez de verificado |
|---|---|
| 1 | que o app não existia |
| 3 | em que bloco o código estava caindo |
| 4 | qual era a causa, dentro de uma mensagem genérica |
| 5 | que a substituição tinha encontrado o alvo |
| 6 | o nome da função e a estrutura dos dados |
| 7 | o tamanho da ambição de Samuel |

**Nome do padrão: escrever sobre estrutura suposta em vez de lida.**

Não é desatenção. É uma tentação específica: quando algo *parece* óbvio — o nome
de uma função, o formato de um dado, o alvo de uma substituição, o limite de uma
ambição —, verificar parece perda de tempo. E é exatamente aí que o erro entra,
porque nada avisa. Sintaxe válida não reclama. `node --check` passa. A entrega
sai.

O antídoto que a conversa produziu, e que virou rotina:

1. Ler a estrutura antes de escrever contra ela
2. `assert` antes de substituir, `grep` depois
3. Confirmar em que bloco o código caiu
4. Rodar em navegador de verdade, não só compilar
5. Erro de rede distingue a causa e diz o conserto daquela causa
6. Nunca deduzir o limite de uma visão — perguntar

O item 6 é o mais recente e o menos praticado.

---

## OBSERVAÇÃO SOBRE AS DATAS

A conversa aparenta cinco dias (04/09 a 08/09), mas os arquivos se concentram em
três blocos: 04-05/09 (conserto e infraestrutura), 05/09 tarde (Termux e
coleta), e 08/09 (varredura, treino e planejamento). Os arquivos com data de
28-30/08 **não foram produzidos nesta conversa** — são herdados e chegaram no
pacote que Samuel enviou.
