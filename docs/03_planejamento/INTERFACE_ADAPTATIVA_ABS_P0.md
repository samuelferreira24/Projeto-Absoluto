# Planejamento Atual — Interface Adaptativa ABS P0

Data: 2026-09-22
Status: planejamento para próximo ciclo de construção

## Objetivo

Construir uma primeira prova de conceito da Interface Adaptativa do ABS sem tentar resolver a interface final.

A P0 deve provar uma ideia específica:

> O Imperador solicita uma forma de visualizar ou manipular algo, a interface muda dinamicamente e a representação continua ligada ao ABS real.

## Estratégia

Não reconstruir a interface atual do zero.

Primeiro aproveitar:
- interface web existente;
- endpoints já funcionais;
- mapa existente;
- chat/comando existente;
- estado real do ABS;
- capacidades e execução já existentes.

A nova camada deve ser adicionada progressivamente.

## P0 — capacidades mínimas

### 1. Cena

Criar um espaço visual único onde diferentes elementos possam aparecer e ser reorganizados.

### 2. Objetos

Representar inicialmente:
- ABS;
- Cérebro;
- projetos;
- missões;
- recursos;
- IAs;
- imagens;
- textos;
- painéis.

Os objetos devem ter identidade visual e, progressivamente, vínculo com entidades reais do ABS.

### 3. Manipulação

Implementar inicialmente:
- mover;
- aproximar/afastar;
- redimensionar;
- girar quando tecnicamente adequado;
- abrir/fechar;
- agrupar/separar;
- mudar posição relativa.

### 4. Comando

Usar o canal de comando existente para interpretar solicitações simples, por exemplo:
- "modo mapa";
- "modo botões";
- "abra o Cérebro";
- "coloque o Cérebro à esquerda";
- "aproxime";
- "afaste";
- "mostre os recursos";
- "esconda os recursos".

No começo, não é necessário que linguagem natural resolva qualquer comando possível. O objetivo é provar o ciclo.

### 5. Modos de representação

Primeiros modos:
- livre/espacial;
- mapa;
- painel;
- botões.

Esses modos devem representar o mesmo estado, não criar estados paralelos.

## Arquitetura de referência

Imperador
↓
intenção/comando
↓
interpretação
↓
estado real do ABS
↓
modelo de cena/representação
↓
interface
↓
interação visual
↓
ação no ABS
↓
novo estado
↓
interface atualizada

## Evolução planejada

P0 — cena adaptativa e manipulação básica
↓
P1 — objetos ligados ao ABS real
↓
P2 — comandos naturais mais amplos
↓
P3 — visualizações 3D mais completas
↓
P4 — câmera/ambiente espacial
↓
P5 — multimodalidade: voz, imagem e visão
↓
P6 — AR/VR e outros dispositivos, se fizer sentido

## Critérios de sucesso da P0

A P0 será considerada demonstrada quando for possível:

1. abrir a interface;
2. criar/mostrar elementos na cena;
3. mover pelo menos alguns elementos;
4. alterar a representação;
5. usar um comando para mudar o modo;
6. manter os elementos vinculados ao estado que o ABS realmente conhece;
7. retornar à visualização anterior sem perder o estado real.

## O que NÃO fazer agora

- não tentar construir a interface final;
- não substituir o ABS core;
- não transformar tudo imediatamente em 3D complexo;
- não criar dezenas de modos;
- não prender o projeto a VR/AR;
- não adotar estética cyberpunk;
- não abandonar funcionalidades atuais que já funcionam;
- não criar um armazenamento visual paralelo que finja ser o ABS real.

## Regra de construção

> Já existe? Verificar → funciona? Testar → integrar → só construir se realmente faltar.

A P0 é uma prova de conceito da nova direção da interface, não uma autorização para reescrever indiscriminadamente o repositório.
