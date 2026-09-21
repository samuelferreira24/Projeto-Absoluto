# LEIA PRIMEIRO

Pacote do projeto **O IMPÉRIO** · conversa de 04/09 a 08/09/2026
O Sistema Absoluto é a ferramenta do Império, não o projeto inteiro.

---

## SE VOCÊ TEM 10 MINUTOS

Leia só isto, nesta ordem:

1. `05-historico/LINHA-DO-TEMPO.md` — a seção final, **O padrão que atravessa os
   erros**. Uma página. É o que mais economiza tempo de quem chega agora.
2. `01-projeto/PLANTA-DO-SISTEMA.md` — as Partes 1 e 2. O que o sistema é e a
   arquitetura de dois laços.
3. `05-historico/DECISOES-REJEITADAS.md` — a seção **DECISÕES QUE CONTINUAM
   ABERTAS**, no fim.

---

## SE VOCÊ É UMA IA QUE VAI CONTINUAR ESTE TRABALHO

Leia nesta ordem, e não pule:

**1º — `05-historico/DECISOES-REJEITADAS.md`**
Antes de propor qualquer coisa. Muita coisa já foi vetada com motivo, e algumas
foram vetadas **duas vezes**. Propor de novo o que já foi rejeitado queima a
confiança de Samuel e o tempo dele.

**2º — `05-historico/LINHA-DO-TEMPO.md`**
Especialmente o padrão dos erros no fim. O erro que se repetiu em cinco das sete
fases é **escrever sobre estrutura suposta em vez de lida**. Você vai sentir a
mesma tentação. O arquivo lista o antídoto.

**3º — `01-projeto/PLANTA-DO-SISTEMA.md`**
O documento operativo. As seções marcadas com ⚑ são decisões fechadas — não
reabra sem motivo novo.

**4º — `02-sistema/app/index.html`**
O código. 9.496 linhas num arquivo só. Antes de editar: leia como o dado é
criado, não suponha o formato.

**5º — `99-superado/`**
Só se precisar do raciocínio detalhado por trás das conclusões da Planta.

### Regras de trabalho que esta conversa produziu

- Rodar em navegador de verdade antes de entregar; compilar não basta
- `assert` antes de substituir por âncora, `grep` depois
- Confirmar em que bloco do arquivo o código caiu (`<style>` ou `<script>`)
- Ler a estrutura de dados antes de escrever contra ela
- Classe nova em arquivo único precisa de prefixo — o escopo é global
- Mensagem de erro distingue a causa e diz o conserto daquela causa
- Nunca deduzir o limite de uma ambição; perguntar

---

## O QUE TEM EM CADA PASTA

| Pasta | Arquivos | O que é |
|---|---|---|
| `00-COMECE-AQUI` | 2 | este índice e a marcação de origem |
| `01-projeto` | 3 | a Planta e dois documentos de visão herdados |
| `02-sistema/app` | 5 | o aplicativo: html, manifesto, service worker, ícones |
| `02-sistema/termux` | 15 | o que roda no celular: Ponte, coletor, orquestrador, especialistas, governança, Jetro, executor, scripts |
| `02-sistema/nativo` | 3 | configuração do APK via Capacitor |
| `04-migracao` | 2 | instalação passo a passo no Termux e uso do app |
| `05-historico` | 2 | decisões rejeitadas e linha do tempo |
| `99-superado` | 2 | versões anteriores — **não apagar**, ver aviso abaixo |

**Total: 34 arquivos.**

### Aviso sobre `99-superado`

Os dois arquivos ali foram superados pela Planta **em função**, mas não em
conteúdo. A comparação encontrou 82 e 68 trechos que não existem na Planta — são
medições e raciocínio que ela absorveu como conclusão, sem o detalhe.

Há material vivo ali. Não é lixo.

---

## O QUE **NÃO** ESTÁ NESTE PACOTE

- **A memória do aplicativo** — biblioteca coletada, conversas, decisões e
  material de treino vivem no aparelho de Samuel, não em arquivo. Saem por
  Ajustes → Memória no aparelho → Baixar cópia.
- **As chaves de API** — nunca entraram em arquivo, por decisão.
- **O token da Ponte** — gerado no aparelho, fica em `~/.sa-ponte-token`.
- **Modelos de IA** — nenhum peso de modelo está aqui.
- **A planilha do cliente** — o trabalho com a Pinheiro Negócios não foi tratado
  nesta conversa. Por isso não existe a pasta `03-cliente`.
- **Material de outras conversas do projeto** — este pacote cobre 04/09 a 08/09.

---

## O ESTADO DO PROJETO AO FIM DESTA CONVERSA

### O que funciona, verificado
- App com 9.496 linhas, 237 funções, 17 ferramentas, 10 seções
- Conversa livre, sem formatos obrigatórios — os dez moldes foram removidos
- Fila de motores: cai para o próximo quando um falha, testado
- Lê e cria planilha e documento do Office, testado com arquivos reais
- Coletor com 33 fontes em 13 domínios; trouxe 111 itens numa rodada real
- Memória em quatro camadas com redundância verificada
- Varredura que executa: 27 de 33 verificações passando no ambiente de teste
- Oficina que valida o arquivo inteiro e recusa conserto inventado, testado

### O que existe e nunca foi exercitado
- Nenhum cliente pagou nada
- Nenhum ciclo de 24 horas rodou de ponta a ponta
- Nenhuma análise do orquestrador virou decisão executada
- Nenhum conserto da Oficina foi aprovado e aplicado
- Material de treino sem volume útil

### O que está quebrado agora
- A Ponte não estava rodando no último teste de Samuel
  (`ERR_CONNECTION_REFUSED`). Conserto: `bash ~/sa/arranque.sh`
- O motor devolvia HTTP 400 — provável nome de modelo incorreto. O app agora
  mostra a mensagem real do provedor em vez de só o número

### A próxima coisa a fazer
Terminar o núcleo de conversa: formato interno de mensagens com papéis,
traduzido para o dialeto de cada fornecedor. Hoje o histórico inteiro vira um
bloco de texto só, o que impede cache, chamada de ferramenta correta e
compactação.

Está descrito na Planta, Parte 4.2.

---

## A FRASE QUE ORDENA TUDO

O sistema está pronto quando Samuel conseguir montar a entrega do cliente dentro
dele, do começo ao fim, sem abrir chat de terceiro.

Não é "quando estiver bonito". É isso.
