# Pesquisa Senior — Integração ABS + Android — Caminho V1

## Estado da investigação
Data: 2026-09-19
Projeto: Projeto Absoluto
Branch: base-cerebro-v0.1

## Hipótese de trabalho
O ABS atualmente pode morar no Android como software e utilizar o Android como ambiente operacional. A direção investigada é ir além do uso: ampliar progressivamente o domínio operacional e, eventualmente, integrar o Android ao próprio ABS.

A integração do Android NÃO redefine a identidade do ABS. Android é um primeiro ambiente/meio que pode ser incorporado ao ABS; o ABS continua sendo o Sistema do Imperador.

## Distinções
1. ABS usa Android: Android é ambiente/recurso externo.
2. ABS controla Android: aumenta o domínio operacional sobre o dispositivo.
3. ABS integra Android: partes necessárias do Android passam a constituir uma camada da estrutura operacional do ABS.
4. Android integrado não significa que todo Android, em qualquer dispositivo, automaticamente vire ABS.

## Caminho técnico investigado
AOSP/Android oferece uma progressão de integração:
- aplicativo normal;
- controle administrativo/Device Owner;
- serviços próprios associados ao gerenciamento do dispositivo;
- componentes privilegiados/system image;
- integração/modificação de framework e system services;
- construção de imagem Android adaptada;
- integração mais profunda das camadas Android necessárias ao ABS.

## Evidências pesquisadas
- DevicePolicyManager define Device Owner como o tipo mais poderoso de Device Policy Controller e permite afetar políticas em todo o dispositivo.
- DeviceAdminService pode ser mantido pelo sistema para Device Owner/Profile Owner enquanto o usuário hospedeiro estiver em execução.
- Permissões privilegiadas são destinadas a apps pré-instalados nos caminhos privilegiados da imagem do sistema e dependem de allowlist.
- AOSP permite construção de imagens de sistema e desenvolvimento de versões Android próprias.
- Root, por si só, não equivale a integração: SELinux continua restringindo processos root e Verified Boot protege a integridade do SO.
- Desbloqueio/instalação de sistema alternativo depende do dispositivo e de suas condições de bootloader/hardware.

## Mapa conceitual
ABS
→ roda no Android
→ usa recursos do Android
→ controla progressivamente o Android
→ assume funções administrativas
→ integra serviços/componentes necessários
→ modifica/adapta o ambiente Android
→ cria/usa uma imagem Android adaptada
→ Android torna-se camada integrada do ABS

## Critério provisório de integração
Um componente deixa de ser apenas recurso externo quando sua função passa a estar sob identidade, controle e continuidade operacional do ABS e sua operação passa a ser necessária/constitutiva para aquela configuração do ABS.

Esse critério é provisório e será validado/refinado durante a pesquisa.

## Nível 9
Nível 9 não deve ser interpretado apenas como “mais permissões”. Nesta investigação, é uma hipótese de domínio operacional máximo suficiente para que o ABS possa incorporar, modificar e utilizar as camadas Android necessárias como partes de sua própria estrutura.

Nível 9 continua sendo objetivo de investigação, não uma capacidade já comprovada no aparelho atual.

## Portas que permanecem abertas
- Android como nó/servidor do ABS.
- VPS como recurso separado quando útil.
- Android adaptado/AOSP.
- Integração de serviços Android.
- Integração de framework.
- Integração de componentes de baixo nível.
- Possibilidade futura de incorporar outros ambientes sem tornar Android a definição do ABS.

## Regras de preservação
- Não apagar hipóteses anteriores.
- Não transformar possibilidades amarelas em vermelhas apenas por dificuldade.
- Não tratar subquadro futuro como capacidade atual.
- Não confundir controle, integração e identidade.
- Não fechar a arquitetura antes do mapeamento das portas reais.

## Fontes principais
Android Developers — DevicePolicyManager:
https://developer.android.com/reference/kotlin/android/app/admin/DevicePolicyManager

Android Developers — DeviceAdminService:
https://developer.android.com/reference/android/app/admin/DeviceAdminService

Android AOSP — Segurança do sistema e kernel:
https://source.android.com/docs/security/overview/kernel-security

Android AOSP — Android 17 CDD / permissões privilegiadas:
https://source.android.com/docs/compatibility/17/android-17-cdd

Android AOSP — Generic System Images:
https://source.android.com/docs/core/tests/vts/gsi

## Próxima investigação
Mapear sistematicamente as portas reais de integração ABS → Android, da integração menos invasiva até AOSP/framework/kernel, identificando para cada porta:
- o que o ABS ganha;
- pré-requisitos;
- dependências do aparelho;
- limitações;
- reversibilidade;
- risco de perder controle;
- evidência prática necessária;
- classificação V1 (🟢/🟡/🔴).

Este documento registra o caminho, não uma arquitetura final.
