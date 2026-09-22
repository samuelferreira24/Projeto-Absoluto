# Interface

A interface é a camada de acesso e controle do ABS; não constitui o núcleo do sistema.

## V1 atual

- `web/` — Web App/PWA do ABS.
- O mesmo ponto de acesso expõe controle de execução, capacidades e visão dos dispositivos.
- A interface é responsiva para celular e desktop e pode ser instalada como aplicativo por navegadores compatíveis.
- O ABS Core permanece separado da interface.

## Dispositivos

A V1 introduz o conceito de **Resource Manager** no ABS Core:

```
VOCÊ
 ↓
INTERFACE ABS
 ↓
ABS CORE
 ↓
RECURSOS / DISPOSITIVOS
 ↓
CAPACIDADES
 ↓
EXECUÇÃO
```

Um dispositivo pode representar celular, computador, servidor ou outro recurso futuro. O registro remoto e heartbeat já possuem contrato HTTP básico. Isso não significa que execução distribuída esteja pronta: o próximo passo dessa camada é validar agente remoto, autenticação, descoberta, seleção de recurso e despacho seguro.

## Direção

As interfaces futuras podem incluir Web, APK Android e Desktop sem transformar nenhuma delas no núcleo do ABS. Todas devem falar com o mesmo ABS Core.

O princípio é:

> **Interface única para o Imperador; infraestrutura substituível por baixo.**

A Web V1 é, portanto, uma primeira interface operacional e uma base de produto, não a forma definitiva do ABS.

## Arquitetura evolutiva

A direção da interface está registrada em `20_interface/01_ARQUITETURA_INTERFACE_EVOLUTIVA_V1.md`.

A interface é deliberadamente **extensível e multimodal**. Ela não é limitada a chat, dashboard ou navegador. Voz, texto, imagem, navegação web, 2D, 3D, experiências espaciais e futuras formas de interação podem coexistir ou ser adicionadas conforme a necessidade.

O navegador é uma capacidade da interface, não a definição do ABS. A arquitetura também prevê troca de modos e múltiplos dispositivos sobre o mesmo ABS Core.

O inventário atual de modos e tecnologias não é fechado: novas necessidades devem poder gerar novas capacidades sem redefinir o núcleo do ABS.


## Contas

A Web App também expõe o registro de contas do ABS. O sistema pode manter várias contas do mesmo serviço, cada uma associada a uma identidade lógica e a uma conexão. A interface não exibe segredos. O cadastro persistido guarda apenas referência à credencial externa.

Isso permite que ChatGPT, GitHub, Claude, Gemini e outros serviços tenham múltiplas contas sem transformar uma conta específica no núcleo do ABS.


## Inteligências

A interface agora possui uma primeira superfície operacional para conversar com capacidades de IA externas já registradas no ABS e para consultar múltiplas dessas capacidades em uma **Sala de Inteligências** experimental.

Isso não significa que o ABS já possua IA-pessoais, uma arquitetura multiagente completa ou AGI. A superfície usa as capacidades disponíveis e mantém essas futuras camadas separadas.

A quantidade de IAs controladoras não é fixa. Ela deve crescer ou diminuir conforme necessidade, especialização, risco e capacidade de supervisão.

A pesquisa ABS × AGI permanece aberta: AGI pode ser uma capacidade incorporada ao ABS, enquanto também permanece em investigação a possibilidade de alcançar maior generalidade por composição e evolução do próprio ecossistema.
