# Definição — Interface Adaptativa do ABS

Data: 2026-09-22
Status: conceito/protótipo

## Definição

A Interface Adaptativa do ABS é um ambiente visual e interativo controlado pelo Imperador no qual o mesmo estado real do ABS pode ser representado dinamicamente de diferentes formas, conforme a intenção do usuário.

A interface não deve ser entendida como uma coleção fixa de telas nem como um simples site.

Ela é uma camada de representação, comando, acesso e composição do ABS.

## Princípio central

> O Imperador não escolhe apenas uma tela. O Imperador determina como quer visualizar, acessar e interagir com o ABS.

Exemplos:
- "Mostre o mapa."
- "Mostre em modo de botões."
- "Abra o Cérebro."
- "Aproxime o Cérebro."
- "Mude o ângulo."
- "Coloque os recursos ao redor."
- "Retire os recursos."
- "Mostre somente as conexões."
- "Transforme isso em painel."
- "Abra um chat com o ChatGPT."
- "Abra o Claude ao lado."
- "Coloque o Chatbox aqui também."
- "Mostre todas as IAs disponíveis."
- "Mostre somente as conversas."
- "Compare as respostas."
- "Esconda tudo e me dê apenas o campo de comando."

A representação pode mudar sem que o objeto real do ABS seja recriado.

## Separação fundamental

### Estado real

O ABS possui os objetos, entidades, missões, projetos, recursos, conexões, capacidades, resultados e estados reais.

### Representação

A interface decide como representar esses elementos naquele momento:
- mapa;
- cena espacial;
- objetos;
- imagens;
- painéis;
- botões;
- gráficos;
- listas;
- detalhes;
- chats;
- páginas web;
- navegadores;
- outras visualizações futuras.

Portanto:

ABS real → representação → interação → ABS real.

A interface não deve criar um "ABS falso" paralelo apenas para funcionar visualmente.

## Interface como ambiente de acesso

A interface deve poder concentrar diferentes formas de acesso e utilização das capacidades disponíveis ao ABS.

Exemplos de meios que podem ser incorporados conforme a capacidade técnica:
- chat;
- plataformas de IA;
- ChatGPT;
- Claude;
- Chatbox e outros clientes;
- navegador Web;
- APIs;
- SDKs;
- MCP;
- conectores;
- plugins;
- aplicativos;
- dispositivos;
- serviços locais;
- serviços remotos;
- servidores;
- outros meios e protocolos futuros.

A interface não precisa recriar internamente todas as funções de cada plataforma. Quando apropriado, ela deve utilizar o mecanismo de integração adequado e preservar o acesso às funções relevantes.

Assim, a interface pode funcionar como um ambiente unificado no qual o Imperador determina quais serviços, plataformas, recursos e capacidades deseja visualizar e utilizar.

## Navegação Web

A capacidade de navegador Web faz parte da direção arquitetural da interface, mas não precisa estar totalmente implementada na primeira versão.

O uso atual da Web é principalmente o meio pelo qual a interface é acessada.

Isso não deve ser confundido com a capacidade futura do ABS de utilizar a própria Web como recurso operacional.

A arquitetura deve permitir evoluir de:

acesso à interface pela Web

para:

interface + capacidade de navegação Web

e, posteriormente, combinar navegação com IA, ferramentas, missões e outras capacidades do ABS.

A implementação concreta pode começar somente com o que é tecnicamente viável na V1, sem bloquear a expansão futura.

## Múltiplos meios de acesso

A Web é o meio atual de acesso à interface, não a definição da interface.

A evolução pode incluir, conforme viabilidade:
- navegador;
- Web app;
- APK;
- celular;
- computador;
- tablet;
- voz;
- visão;
- dispositivos espaciais;
- AR/VR;
- outros dispositivos e meios futuros.

O ABS não deve depender estruturalmente de uma única forma de apresentação ou acesso.

## Preservação das funções das plataformas

Quando plataformas externas forem integradas, suas funções relevantes devem continuar acessíveis sempre que tecnicamente e legalmente possível.

Exemplo conceitual:

Interface Adaptativa
→ ChatGPT
→ Claude
→ Chatbox
→ outras IAs

ou:

Interface Adaptativa
→ navegador
→ página/serviço
→ ação

ou:

Interface Adaptativa
→ API
→ serviço
→ resultado

A representação pode mudar, mas a capacidade conectada não deve ser perdida simplesmente porque a forma visual mudou.

## Múltiplos caminhos e redundância

A arquitetura deve admitir diferentes caminhos para uma mesma capacidade quando isso for útil.

Uma capacidade de IA, por exemplo, pode futuramente ter acesso por:
- API;
- SDK;
- navegador;
- conector;
- MCP;
- aplicativo;
- serviço local;
- outro caminho disponível.

Isso permite substituir, combinar ou criar caminhos alternativos sem transformar uma plataforma específica em dependência estrutural do ABS.

## Regra arquitetural

Modos como mapa, painel e botões não devem ser sistemas independentes.

Da mesma forma, ChatGPT, Claude, navegador, Chatbox e outros serviços não devem definir a arquitetura central do ABS.

São recursos, capacidades ou meios que a camada ABS pode acessar, combinar, substituir ou deixar de utilizar.

A separação fundamental é:

ABS = estado, controle, capacidades, execução e evolução.

Interface = representação, comando e acesso.

Serviços externos = recursos/capacidades que podem ser conectados ao ABS.

## Características visuais

Direção atual:
- realista;
- viva;
- profunda;
- tecnológica;
- espacial;
- clara;
- materiais e iluminação com aparência real;
- cores com significado;
- sem estética cyberpunk como direção principal;
- evitar dependência de neon e hologramas artificiais.

As cores podem comunicar estado/categoria, mas devem funcionar como linguagem visual e não apenas decoração.

## Características de interação

O protótipo deve permitir progressivamente:
- mover;
- aproximar;
- afastar;
- girar;
- redimensionar;
- abrir;
- fechar;
- agrupar;
- separar;
- adicionar elementos;
- remover elementos;
- reorganizar;
- mudar câmera/ângulo;
- mudar modo de visualização;
- abrir e organizar serviços/conexões;
- usar linguagem natural para solicitar transformações e ações.

## Direção futura

A evolução pode seguir:

2D web → 2.5D/profundidade → 3D → ambiente espacial → AR/VR/dispositivos futuros.

Em paralelo:

acesso Web → navegador integrado → múltiplos meios de acesso e interação.

A implementação atual deve evitar decisões que bloqueiem essas evoluções.

## Limite atual

Esta definição é de protótipo. Não significa que a interface final do ABS esteja definida nem que uma tecnologia específica (VR, AR, 3D, engine, navegador ou dispositivo) tenha sido escolhida definitivamente.

O objetivo atual é preservar a arquitetura aberta e construir apenas as capacidades que possam ser comprovadas e integradas de forma operacional em cada etapa.
