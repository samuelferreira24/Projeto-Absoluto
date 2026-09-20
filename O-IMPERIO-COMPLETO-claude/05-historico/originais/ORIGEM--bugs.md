```
FONTE: Conversa "Correção de bugs" — app Claude, dentro do Projeto Sistema Absoluto
PERÍODO: 04/09/2026 a 08/09/2026
ARQUIVOS: 34 no pacote (14 produzidos ou alterados aqui · 16 herdados · 4 criados no empacotamento)
ASSUNTO PRINCIPAL: destravar o aplicativo e desenhar a planta do sistema
```

---

## O QUE ESTA CONVERSA PRODUZIU DE ÚNICO

**O conserto do app que estava morto.** Quatro bugs diagnosticados rodando o app
em navegador headless, não por leitura: erro de runtime no boot matando 1.090
linhas, `</div>` faltando que deixava sete painéis com altura zero, handler
duplicado e 94 ligações frágeis. Nenhum apareceria em revisão de código.

**A Ponte.** O Termux virou serviço que o app comanda — coletar, analisar, ligar
e desligar motor, gravar memória em disco — sem ninguém abrir o terminal. Com
token, lista fechada de comandos e escuta só em 127.0.0.1. Serve também o
próprio app, o que elimina o bloqueio do navegador sem precisar de APK.

**A coleta mundial.** De 20 para 33 fontes em 13 domínios, com GDELT (notícia de
~100 países, traduzida), OpenAlex e Wikipédia. Busca multilíngue que funciona
offline pelo dicionário da Wikidata.

**A memória em quatro camadas.** IndexedDB → disco do Termux com 20 versões
datadas → espelho em Downloads → cópia de fuga manual. Cada camada sobrevive à
morte da anterior.

**A varredura que executa.** Abre cada seção e mede altura em pixels, roda cada
ferramenta e confere a resposta, compara versões entre app e Ponte. Achou um
órfão que nem Claude sabia que existia.

**A Oficina.** O app lê o próprio código, propõe conserto e valida o arquivo
inteiro antes de mostrar. Recusa trecho inventado, sintaxe quebrada, JS caído no
`<style>` e arquivo encolhido.

**A remoção dos dez moldes de resposta.** 120 linhas de formato obrigatório
viraram 22 de markdown livre. É a segunda vez que o método precisou ser tirado
de dentro de uma estrutura rígida.

**A Planta.** A descoberta de que o modelo que Samuel descrevia existe e tem nome
— MAPE-K, IBM, 2005 — e que ele serve só para metade do sistema. A outra metade
é OODA. Mais a Parte 8, sobre multiplicação: a Fábrica, os Espaços como
mecanismo de instanciação, e o laço econômico.

**O padrão dos erros.** Cinco das sete fases erraram, e sempre o mesmo erro:
escrever sobre estrutura suposta em vez de lida. Com o antídoto em seis pontos.

---

## O QUE ESTA CONVERSA NÃO COBRE

**O trabalho com o cliente.** A Pinheiro Negócios, a planilha de fechamento, o
questionário das 20 empresas em 11 setores — nada disso foi tratado aqui. Por
isso não existe pasta `03-cliente`.

**O conteúdo da memória.** A biblioteca coletada, as conversas, as decisões
aprovadas e o tabuleiro vivem no aparelho. Este pacote traz o código que os
manipula, não os dados.

**O documento mestre do Império.** Existe, foi consultado, mas não está aqui —
pertence ao Projeto, não a esta conversa.

**Fine-tuning e treino de modelo.** Discutido e planejado, nunca executado. Não
há dataset com volume útil.

**O tradutor offline Bergamot.** Pesquisado, com riscos registrados, adiado por
decisão de Samuel.

**Motor local rodando.** O `motor.sh` está no pacote mas não foi exercitado nesta
conversa. O motor usado foi sempre de API.

**Sessões anteriores do projeto.** Há material de 28 a 30/08 que chegou junto e
foi preservado, mas a conversa que o produziu não é esta. Os arquivos herdados
estão marcados com `HERDADO` no nome quando são documento, e listados como
herdados na linha do tempo quando são código.

---

## COMO JUNTAR COM OUTRO MATERIAL

**Não sobrepor por nome.** Dois arquivos com o mesmo nome vindos de conversas
diferentes podem ter conteúdo diferente. Comparar antes.

**Os 16 arquivos herdados** (`base.py`, `especialistas.py`, `executor.py`,
`governanca.py`, `jetro.py`, `orquestrador.py`, `semente.py`, `motor.sh`,
`ligar.sh`, `sw.js`, `semente-*.json`, e os quatro `.md` marcados `HERDADO`)
provavelmente aparecem também em outro pacote, possivelmente em versão mais
nova. **Nesta conversa eles não foram alterados.** Em caso de conflito, a outra
versão provavelmente vence.

**Os 14 produzidos ou alterados aqui** (`index.html`, `ponte.py`, `coletor.py`,
`arranque.sh`, `rodar-coleta.sh`, `TERMUX-PASSO-A-PASSO.md`,
`capacitor.config.json`, `package.json`, `manifest.json`, `icon-192.png`,
`icon-512.png`, e os três documentos de planejamento) são desta conversa e
estão em sua versão mais recente. Em caso de conflito, **esta versão vence**.
