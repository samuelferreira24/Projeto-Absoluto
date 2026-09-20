# DECISÕES REJEITADAS

O que foi proposto, tentado ou considerado — e **por que não seguiu**.

Este é o arquivo que mais se perde e mais custa recriar. Sem ele, quem chegar
depois propõe de novo o que já foi vetado, e o tempo se gasta re-explicando.

**Regra:** decisão revogada não se apaga. Marca-se como rejeitada, com o motivo.

---

## SOBRE A INTERFACE

### Dez botões de modo — REJEITADO
**Proposto:** Chat, Conselho, GPS, Guerra, Arca, Brainstorm, Mapa, Texto,
Protótipo, Diagnóstico — cada um um botão.

**Rejeitado porque:** o método vive no julgamento, não em botão. Transformar
raciocínio em clique reduz o método a formulário.

**Quem rejeitou:** Samuel, duas vezes.

### Resposta em JSON com campos fixos — REJEITADO
**Proposto:** cada modo devolvia JSON com estrutura própria, e o app renderizava
os campos.

**Rejeitado porque:** mesma raiz do anterior. Além disso, impedia streaming e
markdown — a IA não conseguia responder no tamanho que a pergunta pedia.

### Modo de resposta obrigatório — REJEITADO
**Proposto:** toda resposta passa pelas cinco camadas, explicitamente.

**Rejeitado porque:** pergunta simples merece resposta simples. As camadas
aparecem no julgamento, não como seções.

---

## SOBRE A ARQUITETURA

### Construir plataforma própria agora — REJEITADO
**Proposto:** construir o sistema completo antes de usar qualquer coisa pronta.

**Rejeitado porque:** o Algoritmo diz para deletar a peça. Plataforma de agentes
com terminal, edição e execução isolada já existe. Construir a segunda versão
consumiria meses sem produzir nada vendável.

**Registrado:** a decisão pode ser reaberta depois de rodar seis meses na
plataforma externa — aí se sabe o que falta de verdade.

### Refazer o sistema do zero — REJEITADO
**Proposto:** demolir o que existe e reconstruir com planta.

**Rejeitado porque:** perde travas já testadas e bugs já corrigidos. E a
pergunta perdeu o sentido quando a oficina passou a ser externa — o que importa
é o que o sistema faz, não quanto do código antigo sobrevive.

### VM própria no Oracle — REJEITADO NA PRÁTICA
**Tentado:** free tier com 2 núcleos e 12 GB.

**Rejeitado porque:** a loteria de capacidade do free tier consome tempo sem
produzir. Substituído por OpenHands Cloud.

**Ressalva:** volta a valer quando houver PC — é o único caminho para rodar
LiteLLM.

---

## SOBRE O MOTOR

### Assinatura de consumidor no OpenHands — REJEITADO
**Considerado:** usar a assinatura já paga em vez de API.

**Rejeitado porque:** fornecedores não permitem assinatura de consumidor em
cliente de terceiro. Rotear por HTTP alheio já causou banimento de conta.

### Assinatura mensal de plataforma agregadora — REJEITADO
**Considerado:** R$ 155,99/mês por acesso a vários modelos pela tela.

**Rejeitado porque:** é acesso por tela, não chave de API. O sistema não
consegue usar — só a pessoa, no navegador.

### OpenRouter sozinho, sem LiteLLM — REJEITADO EM PRINCÍPIO
**Proposto:** apontar tudo direto para o agregador.

**Rejeitado porque:** agregador também é fornecedor único. Contradiz a decisão de
não depender de um só.

**Ressalva:** aceito temporariamente enquanto não há máquina para o LiteLLM —
com a lacuna registrada, não escondida.

### Motor local como base do sistema — REVISADO
**Decisão original:** motor local é a base, API é reforço.

**Revisado porque:** a prática mostrou que local dá conta de volume mecânico —
traduzir, classificar, resumir — mas decisão e código exigem motor forte.

**O que continua valendo:** o sistema não pode **parar** sem internet.
**O que mudou:** sem motor forte ele funciona, mas não constrói.

---

## SOBRE O CLIENTE

### Painel HTML estático — REJEITADO
**Entregue:** relatório gerado por script, atualizado sob demanda.

**Rejeitado porque:** exigia rodar script toda vez. Não era automação — era
relatório de uma vez só.

**Quem rejeitou:** Samuel, com a frase que redirecionou tudo — *"não tem como
eles usarem você toda vez para fazer isso"*.

### Planilha com uma linha por venda — REJEITADO
**Construído:** aba de movimento pedindo cada venda individualmente.

**Rejeitado porque:** eles lançam o **total do dia**, não venda por venda.
Pedir mais detalhe que o processo atual é aumentar trabalho, não reduzir.

**Como se descobriu:** Samuel questionou, e a verificação no arquivo original
confirmou — 30 dias, 30 linhas, nenhuma data repetida.

### Resolver a consolidação das 80 na fase grátis — REJEITADO
**Considerado:** entregar tudo de uma vez para impressionar.

**Rejeitado porque:** resolver a dor mais cara de graça é entregar o produto
inteiro e ficar sem o que cobrar.

### Automatizar a digitação tripla — REJEITADO
**Considerado:** fazer o sistema digitar nas três abas automaticamente.

**Rejeitado porque:** automatizar processo ruim produz processo ruim mais rápido.
O certo era eliminar a repetição.

---

## SOBRE O DOCUMENTO

### Planejar o Sistema como se fosse o projeto — REJEITADO
**Feito:** primeira versão do e-book tratava o Sistema Absoluto como o objetivo.

**Rejeitado porque:** o Sistema é ferramenta. O projeto é o Império. Planejar a
ferramenta antes da obra é construir casa sem planta.

**Quem corrigiu:** Samuel.

### Números afirmados de memória — REJEITADO
**Feito:** a versão 1 do documento tinha todos os números inflados — 9.496
linhas contra 6.563 reais, 17 ferramentas contra 15.

**Rejeitado porque:** documento que serve de fonte de verdade não pode ter número
que não bate. Passou a valer: medir ou escrever o motivo ao lado.

### Marcar "existe" para peça que nunca rodou — REJEITADO
**Feito:** a tabela da Fábrica dizia que as cinco peças existiam.

**Rejeitado porque:** escondia que quatro nunca rodaram. Substituído por três
estados — exercitado, parado, ausente.

---

## COMO USAR ESTE ARQUIVO

**Ao propor algo:** procure aqui primeiro. Se já foi rejeitado, ou você tem
argumento novo, ou está repetindo.

**Ao rejeitar algo:** acrescente aqui. Formato: o que foi proposto, por que não
seguiu, e quem decidiu.

**Ao reabrir uma decisão:** não apague o registro. Acrescente o motivo novo e a
data. A história de ter sido rejeitada uma vez é informação.
