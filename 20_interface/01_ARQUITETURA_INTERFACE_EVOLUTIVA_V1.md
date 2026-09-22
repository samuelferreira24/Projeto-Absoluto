# Arquitetura da Interface ABS — Evolutiva e Multimodal

## 1. Objetivo

A interface do ABS é a camada de interação e controle do Imperador.

Ela não é definida por uma tela, um chat, um navegador, um dispositivo, uma tecnologia de visualização ou um meio de entrada específico.

A interface deve poder adquirir, substituir, combinar e criar novos meios de interação conforme as necessidades do ABS.

**Princípio central:**

> A interface pode evoluir sem exigir que o ABS Core seja redefinido.

## 2. O que a interface NÃO é

A interface não deve ser tratada como:

- um chat fixo;
- um dashboard fixo;
- um navegador isolado;
- uma aplicação presa ao celular;
- uma aplicação presa ao navegador;
- uma única tecnologia visual;
- uma lista fechada de funcionalidades.

Chat, navegador, voz, imagem, 2D, 3D e experiências espaciais são possibilidades de interação/capacidade, não limites da interface.

## 3. Modelo conceitual

```text
                         IMPERADOR
                             |
                     INTERFACE ABS
                             |
                   INTERFACE RUNTIME
                             |
              +--------------+--------------+
              |                             |
       ORQUESTRADOR DE ENTRADA       ORQUESTRADOR DE EXPERIÊNCIA
              |                             |
      +-------+--------+             +------+-------+
      |       |        |             |      |       |
     voz    texto    imagem          2D     3D   espacial
      |       |        |             |      |       |
      +-------+--------+             +------+-------+
              |                             |
              +-------------+---------------+
                            |
                         ABS CORE
                            |
              RECURSOS / CAPACIDADES / DISPOSITIVOS
```

O desenho acima é uma referência arquitetural, não uma lista fechada.

## 4. Entradas multimodais

A interface deve permitir diferentes canais de entrada.

Exemplos iniciais:
- texto;
- voz;
- imagem;
- câmera;
- seleção/interação visual;
- comandos estruturados;
- contexto produzido por outras capacidades.

Novos canais podem ser adicionados posteriormente.

Fluxo esperado:
```text
ENTRADA
  ↓
INTERPRETAÇÃO
  ↓
INTENÇÃO
  ↓
CONTEXTO
  ↓
ABS CORE
```

O ABS Core não deve precisar conhecer detalhes de cada mecanismo de entrada.

## 5. Modos de experiência

A apresentação também deve ser extensível.

Exemplos:
- controle 2D;
- navegador;
- chat;
- visão de rede;
- modo engenharia;
- visualização 3D;
- experiência espacial/imersiva.

Esses modos são substituíveis e expansíveis.

Um novo modo deve poder ser incorporado sem criar um novo ABS.

## 6. Navegador como capacidade

O navegador é uma capacidade da interface, não a definição da interface.

O usuário poderá utilizar a interface para:
- abrir páginas;
- navegar;
- pesquisar;
- fornecer páginas como contexto;
- trabalhar com serviços web;
- utilizar resultados da web em missões do ABS;
- retornar resultados da navegação ao ABS.

A implementação futura deve considerar que muitos sites não permitem incorporação por iframe. Portanto, a arquitetura não deve depender de iframe como mecanismo universal.

O navegador deve ser tratado como um recurso de execução/navegação que poderá utilizar um runtime de navegador apropriado.

## 7. Troca de modo

A interface deve permitir troca de experiência por comando ou interação direta.

Exemplos conceituais:
- “ABS, modo comando.”
- “ABS, abrir navegador.”
- “ABS, modo Cérebro.”
- “ABS, mostrar dispositivos.”
- “ABS, modo 3D.”
- “ABS, conversar.”

Esses comandos são exemplos, não uma API fechada.

O princípio é:
```text
MODO ATUAL
   ↓
INTENÇÃO DE MUDANÇA
   ↓
GERENCIADOR DE MODOS
   ↓
NOVA EXPERIÊNCIA
   ↓
MESMO ABS
```

## 8. Multi-dispositivo

A interface deve funcionar sobre a arquitetura de recursos do ABS.

```text
                         ABS
                          |
                GERENCIADOR DE RECURSOS
                          |
          +---------------+---------------+
          |               |               |
       celular        computador       servidor
          |               |               |
        interface       execução        serviços
```

Web, Android, Desktop e futuras interfaces são pontos de acesso possíveis ao mesmo ABS.

Nenhum dispositivo individual deve se tornar a definição do sistema.

## 9. Tecnologia de conectividade

Tecnologias atuais e futuras de conectividade, incluindo redes móveis futuras como 6G, devem ser tratadas como meios de comunicação disponíveis ao ABS.

O ABS não deve depender conceitualmente de uma tecnologia específica.

```text
ABS
 ↓
camada de comunicação
 ↓
tecnologia disponível
 ↓
recurso/dispositivo
```

Se uma tecnologia mudar, o núcleo do ABS permanece.

## 10. Extensibilidade

A interface deve permitir:

```text
NECESSIDADE
   ↓
NOVA CAPACIDADE / NOVO MODO / NOVA ENTRADA
   ↓
PESQUISA
   ↓
DESENHO
   ↓
IMPLEMENTAÇÃO
   ↓
TESTE
   ↓
VALIDAÇÃO
   ↓
INTEGRAÇÃO
```

Nenhum inventário atual deve ser interpretado como completo.

## 11. Contrato arquitetural

A interface conversa com o ABS por intenções e contratos estáveis, não por dependência direta de cada tecnologia interna.

Conceitualmente:
```text
INTERFACE
   ↓
INTENÇÃO / COMANDO
   ↓
ABS CORE
   ↓
ORQUESTRAÇÃO
   ↓
CAPACIDADE / RECURSO
   ↓
EXECUÇÃO
   ↓
RESULTADO
   ↓
INTERFACE
```

Isso permite substituir navegador, modelo de IA, dispositivo, mecanismo 3D, mecanismo de voz, protocolo de comunicação ou plataforma da interface sem redefinir o ABS.

## 12. Estado atual versus direção futura

### Já existente na V1
- Web App/PWA;
- controle de execução;
- capacidades;
- Resource Manager;
- registro de dispositivos;
- heartbeat;
- ABS Core separado da interface;
- base para múltiplas interfaces.

### Ainda não comprovado como capacidade operacional
- navegador integrado ao runtime do ABS;
- execução remota entre dispositivos;
- autenticação/agentes remotos;
- entrada por voz;
- entrada por imagem como canal operacional;
- visualização 3D operacional;
- experiência espacial;
- interface Android nativa;
- interface Desktop;
- integração de novas tecnologias de conectividade.

Esses itens são direção de evolução, não capacidades já implementadas.

## 13. Regra de evolução

Quando surgir uma necessidade que não esteja contemplada:

> Não forçar a necessidade para dentro da interface existente.

Em vez disso:
1. identificar a necessidade;
2. pesquisar alternativas;
3. determinar se é entrada, apresentação, navegação, recurso ou capacidade;
4. definir o contrato mínimo;
5. implementar de forma substituível;
6. testar;
7. validar;
8. integrar;
9. registrar a nova capacidade no estado do ABS.

## 14. Princípio final

> **A interface do ABS não deve ser uma coleção fechada de funções. Deve ser uma camada evolutiva capaz de incorporar novas formas de interação conforme o ABS descubra ou adquira novas capacidades.**

O Web V1 é o primeiro ponto operacional dessa camada.

Ele não define a forma final da interface.


## 15. Gerenciador de recursos e conexões

A interface pode alcançar um mesmo recurso por diferentes meios. A arquitetura agora possui um registro explícito de conexões no ABS Core.

Exemplos:

- Codex via Termux/CLI;
- GitHub via API;
- GitHub via Termux;
- ChatGPT Connector administrado pela plataforma;
- Claude via API;
- Gemini via API;
- IA local;
- Internet/HTTP;
- APIs externas;
- rede local;
- dispositivos remotos;
- futuros transportes.

O registro de conexão não é a implementação da capacidade. Ele permite ao ABS conhecer quais meios existem, como são transportados, seu estado de configuração e quais capacidades estão associadas.

O princípio é:

RECURSO
↓
UM OU MAIS MEIOS DE CONEXÃO
↓
ADAPTER / CAPABILITY
↓
ABS CORE

A mesma capacidade pode, portanto, possuir múltiplos caminhos de acesso.

## 16. Evolução pelo próprio ABS

A primeira interface operacional deve ser também um ponto de entrada para a construção das próximas versões.

O fluxo futuro é:

IMPERADOR
↓
INTERFACE
↓
ABS
↓
RECURSOS E FERRAMENTAS
↓
IMPLEMENTAÇÃO
↓
TESTE
↓
GIT / CONTINUIDADE
↓
UPDATE / ROLLBACK
↓
NOVA VERSÃO

Isso não elimina autorização humana. A interface fornece o meio; o ABS executa o ciclo controlado; o Imperador permanece como autoridade.

O registro de conexões e o update manager formam parte dessa fundação. Capacidades ainda não validadas continuam explicitamente classificadas como futuras ou planejadas.


## 17. Múltiplas contas e identidades

O ABS não deve assumir uma única conta por serviço.

A arquitetura separa:

PROVEDOR / SERVIÇO
↓
UMA OU MAIS CONTAS
↓
UMA OU MAIS CONEXÕES
↓
CAPACIDADES
↓
RECURSOS

Exemplo: ChatGPT pode possuir conta 1, conta 2 e conta 3; GitHub pode possuir conta 1 e conta 2.

Uma conta identifica uma identidade lógica e pode apontar para uma conexão específica. Contas do mesmo provedor podem coexistir e podem utilizar caminhos diferentes quando o serviço oferecer essas possibilidades.

Credenciais, tokens, cookies e segredos não fazem parte do cadastro público de contas. O registro mantém apenas uma referência externa à credencial, quando existente.

A seleção de conta deve ser uma dimensão de planejamento e roteamento, e não deve ser confundida com a existência de uma conexão ou com a implementação de uma capacidade.

A V1 agora possui o registro de múltiplas contas e a superfície de interface para visualização. A execução efetivamente autenticada por conta ainda exige adapters/credential providers capazes de receber a identidade selecionada sem recorrer a uma credencial global única.

Esse último ponto é deliberadamente separado para não declarar como operacional algo que ainda não foi validado.


## 18. Ecossistema de inteligências e pesquisa ABS × AGI

A interface pode ser uma superfície de acesso ao ecossistema de inteligências do ABS. Isso não transforma o ABS em uma IA única nem define AGI como requisito do sistema.

A arquitetura deve permanecer aberta para diferentes caminhos:

- utilizar modelos e inteligências existentes;
- combinar múltiplas IAs;
- permitir que inteligências especializadas cooperem e se fiscalizem;
- experimentar ambientes de múltiplas IAs;
- incorporar uma eventual AGI como capacidade do ecossistema;
- pesquisar se capacidades de inteligência geral podem surgir de uma composição de modelos, memória, ferramentas, planejamento, execução, aprendizado e supervisão;
- futuramente criar IA-pessoais persistentes sobre modelos/molde adaptáveis.

O número de inteligências controladoras não é fixo. A quantidade deve ser determinada pela necessidade, complexidade, especialização, risco e capacidade de supervisão. Qualquer quantidade registrada em um experimento é uma configuração daquele experimento, não um limite arquitetural.

### Camadas conceituais

```
MODELO / MOTOR
      ↓
CAPACIDADE DE IA
      ↓
IA-PESSOAL (quando houver identidade persistente)
      ↓
ECOSSISTEMA DE INTELIGÊNCIAS
      ↓
MATRIZ DE CONTROLE / SUPERVISÃO
      ↓
ABS
```

Essas camadas não devem ser confundidas. Uma API de modelo não é uma IA-pessoal; uma IA-pessoal não é o ABS; uma AGI, caso exista como capacidade disponível, também não redefine o ABS.

A pesquisa ABS × AGI permanece uma linha de investigação aberta. Hipóteses históricas, simulações e comparações devem ser preservadas como pesquisa até que experimentos forneçam evidência operacional.

## 19. Interface de inteligência na V2

A Web App pode oferecer:

- conversa com uma inteligência selecionada;
- troca entre inteligências disponíveis;
- sala experimental para consultar múltiplas IAs;
- comparação das respostas;
- histórico local de conversa;
- passagem de contexto para o ABS;
- futura interação com IA-pessoais;
- futuras experiências de pesquisa, debate, supervisão e criação de novas inteligências.

A sala experimental não deve ser descrita como uma arquitetura multiagente completa. Na primeira implementação ela é uma superfície de orquestração sobre capacidades já disponíveis. A coordenação autônoma, memória própria das IA-pessoais, supervisão distribuída e criação de novas inteligências continuam sendo linhas de construção.

## 20. Visão sem limite, implementação com evidência

A interface deve permitir que novas descobertas alterem sua forma.

```
VISÃO
↓
PESQUISA
↓
HIPÓTESE
↓
EXPERIMENTO
↓
EVIDÊNCIA
↓
CAPACIDADE
↓
INTERFACE
↓
NOVA DESCOBERTA
```

Não limitar a interface ao que já existe hoje também não significa declarar capacidades futuras como prontas. A interface deve conseguir incorporar novos meios quando o ABS adquirir ou comprovar essas capacidades.


## 21. Ambiente interativo, painéis e construção

A interface possui duas formas de apresentar o controle:

1. **Painel contextual** — aparece associado ao objeto ou área selecionada dentro da experiência interativa.
2. **Painel fixo** — permanece disponível para comandos recorrentes, independentemente do foco atual.

A navegação visual e os painéis são complementares:

```
MAPA
 ↓
FOCO
 ↓
PAINEL CONTEXTUAL
 ↓
AÇÃO
```

O usuário também pode manter o painel fixo quando quiser operar por controles diretos.

### Modos de interação

```
EXPLORAR
   ↓
EDITAR / CONSTRUIR
   ↓
OPERAR
```

- **Explorar:** navegar, aproximar, afastar e selecionar sem modificar o ambiente.
- **Editar/Construir:** reorganizar a representação visual do ambiente.
- **Operar:** executar ações reais do ABS por comandos explícitos e pelos contratos operacionais existentes.

Uma alteração visual não deve ser interpretada automaticamente como alteração do sistema real.

### Ferramentas do ambiente

A superfície de construção pode oferecer:

- criar;
- editar;
- mover;
- duplicar;
- remover;
- redimensionar;
- conectar;
- agrupar;
- desfazer;
- refazer;
- salvar;
- restaurar.

Na primeira implementação dessas ferramentas, a persistência é do **workspace visual da interface**, não de uma alteração estrutural do ABS Core. Capacidades futuras poderão promover determinadas operações para ações reais quando existir contrato, teste, autorização e persistência apropriados.

### Personalização

O ambiente pode possuir layouts diferentes para diferentes finalidades:

- operação;
- pesquisa;
- desenvolvimento;
- monitoramento;
- inteligências;
- projetos;
- ambientes definidos pelo Imperador.

A personalização da visualização não altera a identidade ou a arquitetura do ABS. Ela altera a forma de acessar e organizar a experiência.

### Reversibilidade

Toda alteração visual significativa deve ser reversível sempre que possível.

```
AÇÃO
 ↓
ESTADO ANTERIOR
 ↓
DESFAZER
 ↓
REFAZER
```

A interface deve preservar liberdade de exploração sem transformar uma manipulação acidental em mudança operacional irreversível.

### Interação direta com alternativas

Arrastar, zoom, toque e gestos são meios de interação, não os únicos meios. A interface deve manter controles explícitos e, quando aplicável, atalhos de teclado para as mesmas operações.

Essa regra prepara a experiência para múltiplos dispositivos e para futura evolução 2D → 2.5D → 3D → espacial.

