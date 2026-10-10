# Plano — Ambiente de trabalho permanente na VPS, operado pelo Android

**Estado:** planejamento aprovado pelo Imperador; execução ainda não iniciada por este documento.  
**Data de registro:** 2026-10-10  
**Escopo:** transformar a VPS existente em um ambiente de trabalho remoto integrado, seguro, persistente e recuperável, operável pelo Android.  
**Regra de precedência:** aproveitar e auditar o que já existe; não reinstalar nem substituir componentes sem necessidade comprovada.

## 1. Objetivo e ordem de construção

A construção seguirá três etapas distintas:

1. **Construir o local de trabalho na VPS.** O Imperador deve conseguir acessar, administrar, desenvolver, monitorar e recuperar o ambiente pelo Android.
2. **Usar esse ambiente para continuar construindo o ABS em construção.** O repositório GitHub, o desenvolvimento remoto, os testes, a documentação e a implantação devem formar um fluxo persistente e recuperável.
3. **Delegar gradualmente ao ABS a operação da própria infraestrutura.** O ABS poderá observar e diagnosticar primeiro, depois executar operações autorizadas e reversíveis e, por último, realizar recuperação automatizada dentro de limites explícitos.

A terceira etapa não deve começar antes de existir uma rota de recuperação independente do ABS. O ABS não pode ser o único mecanismo capaz de reparar a infraestrutura da qual depende.

## 2. Ferramentas e funções previstas

As ferramentas abaixo são componentes complementares, não substitutos umas das outras. A presença ou o estado de instalação de cada uma precisa ser verificado antes de qualquer alteração.

- **Coolify:** administrar aplicações, contêineres, serviços e implantações.
- **Cockpit:** administrar e observar o sistema operacional e seus recursos por interface web.
- **SSH pelo Android:** acesso técnico direto e caminho de emergência para tarefas que não possam ser realizadas pelos painéis.
- **Tailscale:** fornecer conectividade privada entre o Android e os serviços administrativos, reduzindo a exposição pública.
- **Apache Guacamole / desktop remoto:** oferecer acesso pelo navegador a ambientes gráficos quando isso tiver utilidade real para o trabalho.
- **Monitoramento e alertas:** detectar indisponibilidade e problemas de recursos; não depender exclusivamente de um serviço hospedado na mesma VPS para detectar falha total da VPS.
- **Backups e recuperação:** preservar dados e configurações, manter cópias fora da VPS e testar restaurações.
- **Ambiente de desenvolvimento remoto persistente:** permitir trabalhar pelo navegador do celular, editar arquivos, executar testes e operar o repositório sem depender de um computador físico nem de manter o celular ligado.
- **GitHub:** manter código e documentação versionados, com histórico de alterações e possibilidade de retorno a versões anteriores.

Não é requisito instalar todos os componentes imediatamente. A seleção final depende da auditoria, da sobreposição de funções, do consumo de recursos, da segurança e da necessidade demonstrada.

## 3. Requisitos de qualidade

O ambiente deverá evoluir para atender aos seguintes requisitos:

1. **Android-first:** acessos e fluxos essenciais utilizáveis no celular.
2. **Persistência:** arquivos, sessões de trabalho e serviços não podem depender da sessão do navegador nem do estado ligado do celular.
3. **Acesso centralizado:** mapa claro dos pontos de entrada, endereços e funções, sem expor segredos na documentação.
4. **Segurança por padrão:** autenticação forte, permissões mínimas, portas públicas estritamente necessárias e interfaces administrativas preferencialmente privadas.
5. **Redundância de acesso:** manter caminhos de administração e recuperação adequados quando uma interface falhar; reconhecer que o Tailscale, se for a única rota privada, também pode falhar.
6. **Observabilidade independente:** detectar tanto falhas de serviços quanto indisponibilidade da VPS, com alertas que não dependam apenas da própria máquina.
7. **Backups reais:** cópias externas, retenção definida, proteção contra exclusão acidental e teste de restauração.
8. **Recuperabilidade:** procedimentos documentados e testados para recuperar serviços, configurações e dados.
9. **Controle humano:** operações destrutivas, de alto impacto ou de difícil reversão exigem autorização explícita.
10. **Mudanças verificáveis:** antes/depois registrado, validação de saúde e rollback quando tecnicamente possível.
11. **Uso eficiente dos recursos:** medir CPU, RAM, swap, disco e consumo dos contêineres antes de acrescentar serviços.
12. **Independência de componentes:** uma falha de interface não deve significar perda dos dados, do repositório ou de todas as rotas de administração.

## 4. Sequência de execução

### Fase A — Auditoria do estado real

- Inventariar VPS, sistema operacional, firewall do provedor, UFW, portas, Docker, Coolify, contêineres, volumes, serviços, armazenamento e backups.
- Confirmar o estado de Cockpit, SSH Android, Tailscale, Guacamole/desktop remoto, monitoramento e ambiente de desenvolvimento; distinguir instalado, configurado, testado e apenas planejado.
- Verificar recursos e capacidade disponível antes de instalar novos serviços.
- Identificar acessos públicos, conflitos de portas, credenciais mal armazenadas, dados sem backup externo e dependências de ponto único.
- Preservar componentes e volumes existentes até comprovar que são redundantes ou desnecessários.
- Não publicar senhas, chaves privadas, tokens, URLs privadas sensíveis ou saídas contendo segredos no GitHub ou em issues públicas.

**Saída da fase:** inventário confirmado, riscos priorizados e plano de mudanças sem duplicar o que já funciona.

### Fase B — Acesso administrativo confiável

- Confirmar SSH seguro e utilizável pelo Android.
- Configurar/verificar o Tailscale e os acessos privados.
- Definir o papel do Coolify e do Cockpit, evitando sobreposição desnecessária.
- Manter uma rota de emergência compatível com o provedor e com o cenário em que a conectividade privada ou um painel não funcione.
- Testar cada rota de acesso, não apenas verificar se o serviço está instalado.

**Saída da fase:** acesso pelo celular validado e procedimentos de emergência documentados.

### Fase C — Ambiente de trabalho persistente

- Validar ou corrigir o ambiente de desenvolvimento remoto já existente antes de substituí-lo.
- Integrar o fluxo de trabalho ao repositório samuelferreira24/Projeto-Absoluto.
- Garantir persistência de arquivos e configurações, autenticação e acesso seguro.
- Confirmar que alterações podem ser versionadas, testadas e recuperadas.
- Separar desenvolvimento, teste e produção na medida compatível com os recursos disponíveis.

**Saída da fase:** conseguir trabalhar no ABS pelo Android e retomar o trabalho sem depender da sessão anterior.

### Fase D — Monitoramento, backup e recuperação

- Monitorar disponibilidade, CPU, memória, swap, disco, contêineres e serviços críticos.
- Configurar alertas que continuem úteis quando a VPS estiver indisponível.
- Criar ou validar cópias fora da própria VPS.
- Testar restauração de dados e de pelo menos um serviço representativo.
- Documentar cenários de falha e procedimentos de recuperação.
- Só automatizar reinícios e correções depois de verificar idempotência, limites e efeitos colaterais.

**Saída da fase:** evidência de monitoramento funcional e de recuperação testada, não apenas de backups existentes.

### Fase E — Aceitação do local de trabalho

Considerar a primeira etapa pronta quando:

- [ ] o acesso pelo Android funciona;
- [ ] os serviços administrativos necessários estão protegidos;
- [ ] o ambiente de desenvolvimento é persistente;
- [ ] o repositório e as alterações são recuperáveis;
- [ ] o monitoramento gera sinais úteis;
- [ ] há backup externo e restauração testada;
- [ ] existe rota de emergência documentada e testada;
- [ ] as limitações e os riscos remanescentes estão registrados.

### Fase F — Construção do ABS sobre essa base

- Usar o ambiente validado para desenvolvimento, testes, pesquisa, documentação e implantação do ABS.
- Manter Git e testes como trilha verificável das alterações.
- Não confundir a infraestrutura operacional com o ABS em construção: a infraestrutura é um recurso que o ABS poderá usar, não a definição do ABS.

### Fase G — Operação gradual da infraestrutura pelo ABS

1. **Observação:** inventário e leitura de saúde, sem alterar o sistema.
2. **Diagnóstico:** identificar causas prováveis e apresentar evidências.
3. **Ações autorizadas e reversíveis:** executar tarefas de baixo risco com limites e registro.
4. **Recuperação supervisionada:** propor ou executar recuperação com validação posterior.
5. **Automação limitada:** automatizar apenas ações testadas, idempotentes e recuperáveis, com alertas e escalonamento humano.
6. **Evolução:** ampliar autonomia conforme evidências reais de segurança e confiabilidade.

A autorização humana, a proveniência, a verificação e a capacidade de interromper ou reverter operações devem permanecer explícitas. O ABS não pode remover seus próprios limites nem desativar o mecanismo independente de emergência.

## 5. Regras de decisão

- Objetivo primeiro; ferramentas depois.
- Auditar antes de instalar, reinstalar, remover ou migrar.
- Não reconstruir componentes existentes antes de verificar o estado real, testes e integrações.
- Não realizar mudanças destrutivas apenas para simplificar a arquitetura.
- Não considerar um painel saudável como prova de que a VPS inteira está recuperável.
- Não considerar backup concluído como prova de que a restauração funciona.
- Não considerar um teste isolado como prova de confiabilidade contínua.
- Registrar fatos observados, hipóteses, decisões, resultados e pendências separadamente.
- Mudanças de arquitetura e de segurança devem ser feitas por etapas, com validação após cada etapa.

## 6. Próximo ponto de retomada

**Próxima ação:** realizar uma auditoria do estado real da VPS e do que já foi configurado para acesso e operação pelo Android. Comparar os resultados com este plano e produzir uma lista curta e priorizada de correções. Não começar por uma instalação geral.

Este documento é a referência de planejamento para o ambiente de trabalho. O estado operacional observado, as evidências e o próximo passo concreto devem continuar registrados na área de continuidade e ser atualizados conforme a execução.
