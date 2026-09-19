# MINI-CÉREBRO — PRIMEIRA RECONSTRUÇÃO DO SISTEMA ABSOLUTO A PARTIR DO ZIP

## Fonte
- Repositório: `samuelferreira24/Sistema`
- Arquivo: `sistema-absoluto.zip`
- SHA-256 do ZIP interno: `3fd4f17ec890c6c940f1d618498074f384007d33b91e4217e46b30a483565380`
- Conteúdo analisado: 29 arquivos extraídos.
- Método: aquisição pelo fluxo do Mini-Cérebro, preservação do original, extração textual e classificação/investigação por termos e estrutura documental.

## 1. Achado central

O ZIP não é apenas um aplicativo isolado.

Ele contém, simultaneamente:
1. implementação do aplicativo;
2. memória e formato de dados;
3. regras de operação e governança;
4. mecanismos de coleta e proveniência;
5. executor protegido;
6. orquestração/especialistas;
7. ponte com o ambiente Android/Termux;
8. experimentos de motor local;
9. continuidade/arranque;
10. um conjunto extenso de calibragens, decisões e lições registradas em `semente-nucleo.json` e `semente-operacao.json`.

Portanto, o patrimônio histórico recuperado é maior que o código do app.

## 2. Evidência documental importante

### MEMORIA.md
O documento estabelece explicitamente que a memória deve sobreviver à casca/interface. Uma casca nova deve:
- ler o mesmo JSON;
- falar com qualquer motor compatível;
- gravar novamente no mesmo formato;
- não decidir sozinha.

Também define compatibilidade por versão e preservação semântica do formato.

### NATIVO.md
Registra uma estratégia de envelope nativo sobre o mesmo `index.html`, mantendo web e nativo simultaneamente. Também registra uma escada de integração Android, incluindo notificação, segundo plano, sobreposição, compartilhamento, acessibilidade, app de sistema e ROM própria.

O próprio documento registra a distinção: aumentar acesso ao Android não aumenta automaticamente a inteligência do motor.

### P1-SISTEMA-PROPRIO.md
Identifica como gargalo histórico a ausência de um sistema próprio rodando sozinho. Propõe:
motor local → validação no celular → VPS → n8n/filtro → MCP → migração dos apps para workflows.

O documento afirma que o motor local resolve apenas parte do problema; o orquestrador é tratado como componente necessário para transformar peças em sistema que roda sozinho.

### TERMUX-PASSO-A-PASSO.md
Documenta uma arquitetura operacional em Android/Termux com:
- ponte HTTP local;
- token;
- coleta;
- arranque automático;
- wake lock;
- agendamento;
- recuperação após reinício;
- divisão de responsabilidades entre Termux, piloto e usuário.

Isso constitui evidência de uma tentativa concreta de continuidade operacional, não apenas uma ideia abstrata.

## 3. Calibragem da IA encontrada

O `semente-nucleo.json` contém registros explícitos de erros, correções, decisões e lições.

Entre os registros recuperados:

- não descartar possibilidades grandes ou múltiplas prematuramente;
- quando existem várias rotas, mostrar o mapa e as consequências, deixando a decisão ao Piloto;
- trabalhar frentes em paralelo quando tecnicamente independentes;
- o freio da Avalanche pertence ao Piloto, não à IA;
- memória é copiada entre máquinas, não deve existir em um único lugar;
- distinguir limitação do modelo de limitação da plataforma/implementação;
- mostrar alternativas antes de recomendar uma tecnologia;
- afirmar somente o que foi testado e declarar o que não foi;
- entender que o projeto era usar uma IA para construir a IA própria;
- preservar contexto entre sessões por meio de uma memória independente da casca.

## 4. Decisões históricas recuperadas

O arquivo registra decisões como:
- motor local via llama.cpp no Termux em vez de Ollama no Android;
- IndexedDB + gzip para armazenamento;
- nuvem cifrada antes do envio;
- módulos gerados por IA passarem por análise, isolamento e aprovação;
- VPS somente depois do primeiro caixa;
- motor como peça substituível;
- memória como patrimônio próprio.

Estas são **decisões históricas do Sistema antigo**. Não são automaticamente decisões aprovadas para o ABS atual.

## 5. O que o Mini-Cérebro está descobrindo

A reconstrução já permite separar quatro camadas que anteriormente estavam misturadas:

### A — Produto/casca
`index.html`, PWA, Capacitor, interface, modos.

### B — Sistema operacional experimental
memória, coleta, executor, governança, orquestrador, ponte, continuidade.

### C — Conhecimento/calibragem
`semente-nucleo.json`, `semente-operacao.json`, decisões, erros, lições, regras aprendidas.

### D — Hipóteses futuras
motor local maior, VPS, MCP, integração Android profunda, sistema próprio etc.

Essa separação é uma reconstrução analítica do material; não significa que o projeto original usava exatamente essas quatro categorias.

## 6. Convergências com o Projeto Absoluto atual

Há convergências fortes e documentadas em:
- memória independente da interface;
- motor substituível;
- separação entre capacidade e autorização;
- execução protegida;
- proveniência;
- orquestração;
- continuidade;
- Android como meio operacional;
- aprendizado por erros e calibragem;
- preservação de alternativas.

Mas o Mini-Cérebro também encontrou diferenças importantes entre o Sistema histórico e o ABS atual.

O histórico estava muito mais centrado em um **aplicativo/assistente operacional** e em chegar a um sistema próprio. O ABS atual possui uma definição mais ampla e não deve ser reduzido à arquitetura daquele aplicativo.

## 7. Pergunta que permanece aberta

Ainda não foi demonstrado pelo ZIP, sozinho:
- qual foi exatamente o último estado operacional do aplicativo;
- quais componentes funcionaram continuamente no aparelho real;
- quais falhas provocaram o abandono do aplicativo;
- quais limitações eram do modelo;
- quais eram da plataforma;
- quais eram bugs;
- quais capacidades foram realmente usadas em operação prolongada.

Essas questões exigem cruzamento com histórico Git, logs, commits, artefatos e demais evidências.

## 8. Próxima investigação do Mini-Cérebro

A próxima etapa não é construir.

É reconstruir causalmente:

`ideia → decisão → implementação → teste → resultado → falha/limitação → correção → descoberta → nova decisão`

Prioridade:
1. cruzar os arquivos do ZIP com os commits do repositório;
2. localizar a origem de cada decisão importante;
3. separar afirmação/documentação de resultado comprovado;
4. identificar os experimentos efetivamente realizados;
5. reconstruir a evolução do sistema;
6. localizar o que foi abandonado por falha real versus o que apenas ficou para depois;
7. extrair o conhecimento que ainda pode alimentar o ABS atual.

## Regra de preservação

Nenhuma descoberta histórica deste relatório deve ser transformada automaticamente em arquitetura do Projeto Absoluto.

O Mini-Cérebro recupera evidências e conhecimento. O ABS atual decide posteriormente o que incorporar.
