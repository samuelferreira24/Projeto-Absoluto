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
