# Definição — Interface Adaptativa do ABS

Data: 2026-09-22
Status: conceito/protótipo

## Definição

A Interface Adaptativa do ABS é um ambiente visual e interativo controlado pelo Imperador no qual o mesmo estado real do ABS pode ser representado dinamicamente de diferentes formas, conforme a intenção do usuário.

A interface não deve ser entendida como uma coleção fixa de telas.

Ela é uma camada de representação e comando do ABS.

## Princípio central

> O Imperador não escolhe apenas uma tela. O Imperador determina como quer visualizar e interagir com o ABS.

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
- "Volte para o ambiente."

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
- outras visualizações futuras.

Portanto:

ABS real → representação → interação → ABS real.

A interface não deve criar um "ABS falso" paralelo apenas para funcionar visualmente.

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
- usar linguagem natural para solicitar transformações.

## Regra arquitetural

Modos como mapa, painel e botões não devem ser sistemas independentes.

São representações diferentes de um mesmo ABS.

## Direção futura

A evolução pode seguir:

2D web → 2.5D/profundidade → 3D → ambiente espacial → AR/VR/dispositivos futuros.

A implementação atual deve evitar decisões que bloqueiem essa evolução.

## Limite atual

Esta definição é de protótipo. Não significa que a interface final do ABS esteja definida nem que uma tecnologia específica (VR, AR, 3D, engine ou dispositivo) tenha sido escolhida definitivamente.
