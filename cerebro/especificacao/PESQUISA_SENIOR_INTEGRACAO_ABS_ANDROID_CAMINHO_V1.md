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



## Mapeamento amplo das portas — rodada 2

### Camada A — Portas disponíveis sem modificar o SO
| Porta | Função para o ABS | Situação conceitual |
|---|---|---|
| App próprio | núcleo/interface inicial | 🟢 |
| Foreground Service | processo persistente em primeiro plano | 🟢/🟡 |
| AccessibilityService | observar/interagir com UI e eventos | 🟡 |
| NotificationListenerService | perceber notificações e eventos de notificação | 🟡 |
| VPN Service | criar interface de rede virtual e controlar o tráfego que passa pelo túnel | 🟡 |
| APIs Android | acessar capacidades expostas pelo framework | 🟢/🟡 |
| Storage/arquivos acessíveis | estado, memória e dados | 🟢 |
| Internet/API | comunicação externa | 🟢 |

Observação: AccessibilityService é deliberadamente restrito pela plataforma ao domínio de acessibilidade e requer ativação explícita pelo usuário; portanto não deve ser tratado como uma porta genérica de controle total. NotificationListenerService fornece eventos de notificações, não controle integral de aplicativos. VpnService fornece uma interface VPN e fluxo de pacotes para o serviço, não acesso irrestrito à rede. citeturn1search0turn1search1turn1search2

### Camada B — Controle administrativo do dispositivo
**Device Owner / Device Policy Controller**

Essa é uma porta especialmente relevante. A documentação do Android identifica Device Owner como o tipo mais poderoso de Device Policy Controller e mostra capacidades adicionais, inclusive operações relacionadas a pacotes e políticas. DeviceAdminService pode manter uma conexão ligada ao proprietário do dispositivo/perfil durante a execução do usuário hospedeiro. citeturn1search7turn0search10turn1search4

Hipótese para o ABS:
**ABS App → Device Owner → controle administrativo amplo → preparação para integração mais profunda.**

Isso não equivale ao Nível 9.

### Camada C — Persistência operacional
O Android impõe restrições ao trabalho em segundo plano e a serviços de primeiro plano. Apps modernos precisam respeitar tipos/permissões de foreground service e existem restrições para iniciar serviços a partir do background. Device Owner está entre as exceções relevantes. citeturn0search3turn0search8

Consequência para o ABS:
**persistência é uma capacidade própria a mapear**, porque “ABS instalado” não significa “ABS continuamente operacional”.

Devemos investigar:
- boot/startup;
- foreground service;
- DeviceAdminService;
- recuperação após encerramento;
- reinicialização;
- battery optimization;
- conectividade perdida/restabelecida;
- estado persistente.

### Camada D — Segurança e sandbox
Apps Android normalmente são isolados por UID/processo e têm acesso limitado ao SO. A partição de sistema também é protegida por integridade e normalmente somente leitura. citeturn0search7turn0search4

Logo, o caminho de integração deve considerar explicitamente:
**sandbox → permissões → privilégios → SELinux → system image → boot integrity.**

Não devemos assumir que uma API disponível elimina essas fronteiras.

### Camada E — System image / componentes privilegiados
A integração pode avançar quando o ABS deixa de ser somente um app distribuído normalmente e passa a ser incorporado à imagem do sistema.

Portas a mapear:
- privileged app;
- allowlist de permissões privilegiadas;
- system service;
- APEX;
- overlays/configuração;
- system/vendor;
- propriedades persistentes;
- init.

AOSP documenta propriedades de sistema com contexto SELinux e mecanismos de configuração no início do boot; também documenta APEX e componentes vendor que podem ser ativados cedo no ciclo de boot. citeturn0search6turn0search12turn0search0

### Camada F — IPC / comunicação interna
**Binder/AIDL** é uma porta estrutural importante.

O Android usa Binder para comunicação entre componentes do framework e HALs. Portanto, uma integração profunda do ABS provavelmente precisará mapear:
- serviço Binder próprio;
- interface AIDL;
- permissões do serviço;
- SELinux service_contexts;
- comunicação ABS ↔ framework;
- comunicação ABS ↔ HAL quando necessário.

A existência dessas interfaces significa que integração não precisa significar “substituir tudo”: o ABS pode entrar no sistema através de interfaces internas bem definidas. citeturn0search16

### Camada G — Boot e ciclo de inicialização
Para integração profunda, investigar:
- bootloader;
- boot image;
- init;
- early-init;
- ramdisk;
- system/vendor;
- AVB;
- slots A/B;
- dynamic partitions;
- recovery;
- OTA.

AOSP documenta que o processo de boot e as imagens são fortemente ligados à verificação de integridade e à configuração do dispositivo. Partições dinâmicas e A/B também alteram como imagens são atualizadas. citeturn0search5turn0search2turn0search17

### Camada H — Framework / System Services
Aqui começa uma integração qualitativamente diferente.

Possibilidades a pesquisar:
- criar um serviço de sistema ABS;
- integrar o serviço ao System Server;
- criar APIs internas;
- criar políticas próprias;
- coordenar recursos Android pelo serviço;
- integrar eventos do sistema diretamente ao ABS.

Isso pode reduzir a dependência de automação por interface e aproximar o ABS do próprio mecanismo de operação do Android.

### Camada I — HAL / Hardware Abstraction
HAL é uma porta quando o ABS precisa controlar capacidades de hardware através das interfaces Android.

Não significa que o ABS precise controlar diretamente cada componente físico. Pode integrar-se às abstrações existentes.

Subáreas:
- câmera;
- áudio;
- sensores;
- biometria;
- gráficos;
- conectividade;
- outros HALs relevantes.

AIDL é atualmente uma interface importante para HALs e a documentação AOSP mantém diretrizes para interfaces HAL estáveis e compatíveis. citeturn0search15turn0search16

### Camada J — Kernel / SELinux
É uma camada de integração profunda, mas deve ser tratada separadamente:
- kernel;
- drivers;
- SELinux policy;
- namespaces/cgroups;
- dispositivos;
- interfaces kernel;
- segurança de boot.

Não devemos assumir que chegar ao kernel seja necessário para qualquer função do ABS.

### Camada K — Android próprio/adaptado
AOSP permite construir imagens próprias e GSI demonstra a possibilidade de substituir a imagem de sistema em dispositivos compatíveis. Isso abre a porta para um Android onde componentes do ABS sejam parte do sistema desde a construção. citeturn0search1

### Camada L — Continuidade e identidade
Independentemente da profundidade técnica, precisamos separar:
- identidade do ABS;
- estado do ABS;
- memória do ABS;
- autorização do Imperador;
- capacidade de reconstrução;
- capacidade de migrar;
- capacidade de recuperar após atualização/falha;
- vínculo com um dispositivo específico.

**Conclusão provisória:** integrar Android ao ABS não deve significar tornar o ABS dependente da identidade física de um único telefone. O Android pode ser uma camada integrada enquanto a identidade/estado do ABS permanece acima dela.

## Mapa geral atual

**Portas de aplicação**
→ App
→ APIs
→ serviços
→ Accessibility
→ notificações
→ VPN

**Portas administrativas**
→ Device Owner
→ DeviceAdminService
→ políticas do dispositivo

**Portas de sistema**
→ privileged app
→ Binder/AIDL
→ system services
→ system properties
→ APEX
→ init

**Portas de plataforma**
→ framework
→ system image
→ system/vendor
→ boot/recovery
→ AOSP

**Portas de baixo nível**
→ HAL
→ SELinux
→ kernel
→ drivers
→ hardware

**Portas de continuidade**
→ estado
→ memória
→ identidade
→ atualização
→ recuperação
→ migração

## Regra de investigação antes da construção

Ainda NÃO construir a integração profunda.

Primeiro devemos completar:
1. inventário das portas;
2. dependências de cada porta;
3. pré-requisitos do aparelho atual;
4. limitações por versão Android;
5. caminho reversível;
6. caminho irreversível;
7. riscos;
8. testes mínimos;
9. relação com os Níveis 0–9;
10. quais portas realmente aumentam a capacidade do ABS;
11. quais portas são redundantes;
12. qual combinação mínima permite a primeira integração real.

Só depois disso selecionar o primeiro caminho de construção.

## Estado
O mapa ainda está aberto. Nenhuma porta foi declarada como arquitetura final.
