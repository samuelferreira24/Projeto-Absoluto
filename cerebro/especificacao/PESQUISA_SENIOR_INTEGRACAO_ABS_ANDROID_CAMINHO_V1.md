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


## Pesquisa aprofundada — novas evidências

### Portas adicionais de integração identificadas
A arquitetura AOSP mostra que a integração não precisa ocorrer em um único salto. Há pontos distintos:
- propriedades e configuração do sistema;
- system services/framework;
- Binder/AIDL para comunicação entre componentes;
- apps privilegiados na system image;
- HALs e interfaces com hardware;
- partições system/vendor/odm;
- init/boot e imagens de sistema;
- kernel/boot image.

AOSP documenta que o framework e componentes HAL se comunicam por Binder, e que a separação system/vendor cria fronteiras de integração entre plataforma e código específico do dispositivo. Isso é relevante porque o ABS pode ser projetado como componente que atravessa essas interfaces sem precisar inicialmente substituir todas as camadas. citeturn1search3turn1search48

### Integração por administração do dispositivo
Device Owner é uma porta real para o ABS assumir controle administrativo amplo do dispositivo. A documentação atual descreve Device Owner como o tipo mais poderoso de Device Policy Controller, capaz de afetar políticas em todo o dispositivo. Também existe DeviceAdminService, que o sistema tenta manter conectado enquanto o usuário hospedeiro estiver em execução. citeturn0search0turn0search7

### Integração por system image
Permissões privilegiadas são associadas a apps pré-instalados nos caminhos privilegiados da system image e dependem de allowlists. Isso cria uma rota concreta para transformar o ABS de um app comum em um componente integrado à imagem do sistema, quando o dispositivo/build permitir. citeturn0search8

### Integração por AOSP
AOSP permite criar imagens de sistema próprias; GSI é um exemplo de imagem baseada no AOSP que pode substituir a imagem de sistema em dispositivos compatíveis. Isso confirma que “Android adaptado” é uma possibilidade técnica real, mas a implantação concreta depende da compatibilidade e das condições do dispositivo. citeturn1search2

### Baixo nível não é simplesmente “root”
AOSP documenta que SELinux continua restringindo processos mesmo com root e que Verified Boot protege a integridade do sistema. Portanto, root deve ser tratado como uma porta de privilégio, não como sinônimo de integração integral. citeturn0search3turn1search4

### Nova leitura arquitetural
A pesquisa reforça uma arquitetura de integração por camadas:

1. **Presença** — ABS roda no Android.
2. **Recursos** — ABS usa CPU/RAM/armazenamento/rede/processos.
3. **Administração** — ABS controla políticas e estado do dispositivo.
4. **Serviços** — ABS integra serviços persistentes e comunicação com o sistema.
5. **Privilégio** — ABS ocupa posições privilegiadas na system image quando possível.
6. **Framework** — ABS passa a participar/modificar serviços e APIs do Android.
7. **Hardware abstraction** — ABS pode integrar-se às interfaces HAL necessárias.
8. **Boot/system image** — ABS passa a fazer parte da imagem e do ciclo de inicialização.
9. **Integração operacional** — Android adaptado torna-se camada constitutiva da configuração do ABS.

Esta sequência é uma hipótese de investigação, não uma exigência de que todos os passos sejam necessários.

### Critério prático para os próximos testes
Para cada porta, pesquisar:
- acesso necessário;
- mecanismo oficial/real;
- se funciona no aparelho atual;
- se exige bootloader desbloqueado;
- se exige imagem própria;
- se exige root;
- se exige alteração de SELinux;
- se exige AOSP/build;
- persistência após reinicialização;
- reversibilidade;
- risco de perda de controle;
- possibilidade de preservar o Android original;
- evidência mínima para classificar a porta como 🟢, 🟡 ou 🔴.

### Regra importante
Não assumir que “mais profundo” significa automaticamente “melhor”. O objetivo é **integração do Android ao ABS**, e não obter privilégios por si mesmos. Uma porta menos profunda pode ser suficiente para uma função específica; uma porta mais profunda só deve ser perseguida quando acrescentar capacidade real ao ABS.

### Próximo ramo da pesquisa
**Android → Portas de Integração ABS**

Sub-ramos iniciais:
- Administração do dispositivo
- Serviços persistentes
- System apps / privileged apps
- System services / framework
- Binder / AIDL
- System image / AOSP
- Boot / init
- HAL
- Kernel / SELinux / Verified Boot

