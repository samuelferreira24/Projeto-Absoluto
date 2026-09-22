# Instalação da Interface ABS V1

Este documento marca o ponto de transição entre construção e instalação.

## O que está pronto

- ABS Core V1 operacional.
- interface Web/PWA operacional.
- modos de interface.
- controle de capacidades.
- conexões e recursos.
- catálogo e conhecimento de ferramentas.
- descoberta de novas ferramentas.
- planejamento de missão.
- roteamento de recursos.
- execução por recurso com autorização.
- Internet HTTP como capacidade.
- entrada progressiva por voz no navegador.
- atualização, health check e rollback.
- serviço Termux e inicialização por boot preparados.

## O que a interface não é

A Web V1 não é a forma definitiva da interface.

Ela é a primeira superfície operacional sobre o mesmo ABS Core.

A arquitetura permanece aberta para:

- APK Android;
- desktop;
- voz;
- imagem;
- 2D;
- 3D;
- interfaces espaciais;
- navegador;
- novos modos;
- novos dispositivos;
- novas tecnologias de conectividade.

## Preparação no Android

1. Repositório ABS presente em ~/Projeto-Absoluto.
2. Termux configurado.
3. Serviço ABS instalado.
4. Update Manager instalado.
5. Serviço iniciado e validado em /health.
6. Abrir a interface Web pelo endereço local fornecido pelo ABS.
7. No navegador, usar a opção de instalar/adicionar à tela inicial quando disponível.

## Regra

A instalação não encerra a construção.

Depois da primeira interface instalada, ela passa a ser uma nova superfície para comandar a evolução do próprio ABS.

Fluxo:

Imperador → Interface → ABS → planejamento → execução → teste → atualização → nova versão
