# LINHA DO TEMPO

A ordem em que as coisas aconteceram, e o que cada fase ensinou.

Datas conferidas contra os arquivos, não de memória.

---

## 25 a 28 de agosto — a fundação

**O que se fez:** instruções permanentes, planejamento de renda, primeira versão
do sistema. Os módulos Python nasceram aqui — base, especialistas, jetro,
semente.

**O que ficou:** a estrutura conceitual. Motor, Estrutura, Piloto já estavam
nomeados, mas ainda não reconhecidos como a mesma coisa.

---

## 29 e 30 de agosto — o sistema cresce

**O que se fez:** coletor, executor, orquestrador, governança. O motor local
compilado no Termux. O `ligar.sh` que junta tudo.

**O que se aprendeu:** 3 GB de RAM é teto real. Compilação com 8 núcleos é morta
pelo Android; com 1 núcleo, passa.

**O erro desta fase:** construir muito, exercitar pouco. O executor nasceu com
756 linhas e nunca rodou.

---

## 1 a 2 de setembro — o cliente entra

**O que se fez:** quatro versões da ferramenta do cliente, em dois dias.

| Versão | O que era | Por que caiu |
|---|---|---|
| painel-clinica | relatório HTML gerado por script | exigia rodar script toda vez |
| planilha-unica | primeira com fórmulas vivas | estrutura errada |
| mensal | segunda tentativa | ainda não batia com o processo real |
| **fechamento-v3** | **a que ficou** | construída sobre respostas, não suposição |

**A correção que mudou tudo:** *"não tem como eles usarem você toda vez para
fazer isso"*. Relatório virou planilha que calcula sozinha.

**O erro desta fase, nomeado por Samuel:** construir antes de ler todos os
arquivos. Três versões descartadas por isso.

---

## 2 a 3 de setembro — perguntar antes de construir

**O que se fez:** cinco versões de questionário, cada uma mais precisa que a
anterior.

| Versão | Perguntas | O que a motivou |
|---|---|---|
| 1 | 21 | primeira tentativa |
| 2 | 17 | enxugar — 28 de 36 marcadas "essencial" anula o destaque |
| 3 | 20 | depois de ler o DRE de verdade |
| 4 | 28 | depois de abrir as 19 abas |
| **5** | **40** | **depois de ver o painel do CEO — 20 empresas, 11 setores** |

**A descoberta que mudou a escala:** não é gestora de clínicas. São 20 empresas
em 11 setores — hotel, panificadora, malharia, parque, arquitetura.

**A pesquisa aberta:** CEO identificado, modelo de negócio entendido, 24
empresas listadas no site oficial contra 80 mencionadas pela gestora — diferença
ainda em aberto.

---

## 4 de setembro — a reforma da interface

**O que se fez:** os dez modos viraram um método na cabeça da IA. Streaming,
markdown, menu lateral, tela de projeto, folhas de ação.

**O que se aprendeu:** um `flex:1` ausente deixou telas em branco com sintaxe
perfeita. Sintaxe válida não prova estrutura certa.

---

## 9 de setembro — a virada de ordem

**O que se fez:** auditoria do planejamento, especificação de engenharia, e o
documento unificado.

**A correção estrutural:** *"o sistema é só uma parte do projeto — estamos
invertendo a ordem"*. O e-book foi refeito com o Império no topo.

**A descoberta conceitual:** Motor, Estrutura e Piloto são o Sistema, o Império e
o Imperador. Os três nomes já existiam; faltava reconhecer que eram as três
peças.

**O que a auditoria achou:** todos os números do documento anterior estavam
inflados. Três peças descritas como existentes não existiam.

---

## 9 de setembro, depois — a saída da plataforma

**O que se decidiu:** oficina externa. Não construir plataforma agora.

**O caminho testado e abandonado:** VM no Oracle. A loteria de capacidade do
free tier consome tempo sem produzir.

**O caminho escolhido:** OpenHands Cloud, com crédito grátis para testar.

**O que ficou em aberto:** o LiteLLM, que precisa de máquina própria.

---

## O PADRÃO QUE ATRAVESSA TUDO

Sete dos treze erros registrados têm a mesma raiz: **construir antes de verificar
o terreno.**

| Fase | Manifestação |
|---|---|
| Sistema | executor com 756 linhas que nunca rodou |
| Cliente | três planilhas antes de ler os arquivos |
| Questionário | começar a construir antes de perguntar |
| Documento | números escritos de memória |

**O que se criou por causa disso:** o Portão 1 — primeira conversa é diagnóstico,
nunca código.

---

## O QUE MUDOU DE VERDADE

| Antes | Depois |
|---|---|
| Sistema como objetivo | Sistema como ferramenta do Império |
| Construir e depois perguntar | perguntar e depois construir |
| "Existe" | exercitado, parado ou ausente |
| Números de memória | medidos ou com motivo escrito |
| Plataforma própria | oficina externa, projeto próprio |
| Método em botões | método no julgamento |
