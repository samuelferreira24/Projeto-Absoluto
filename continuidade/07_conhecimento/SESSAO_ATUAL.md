# CHECKPOINT DE SESSÃO — 2026-09-23

## Projeto
Projeto Absoluto.

## Definição consolidada
- Projeto Absoluto = visão, método, princípios e objetivos do Imperador; é o projeto maior.
- **Sistema Absoluto / ABS geral** = o ecossistema aberto de capacidades e recursos que o Imperador pode utilizar, combinar, substituir, ampliar ou criar. Não é uma lista fechada de IAs, agentes, modelos, ferramentas, APIs, servidores, dispositivos ou serviços.
- **ABS em construção** = o sistema que está sendo construído para operar/orquestrar o ABS geral sob autoridade do Imperador.
- **ABS V1** = primeira versão operacional do ABS em construção; não é o Sistema Absoluto inteiro nem sua definição permanente.
- O ABS em construção não deve ser confundido com uma IA, agente, modelo, ferramenta, servidor, interface, Cérebro, Android ou qualquer outro componente.
- Outros projetos poderão surgir dentro do Projeto Absoluto e poderão reutilizar, substituir ou não depender do ABS em construção.
- O Imperador está aprendendo a construir enquanto constrói; a arquitetura futura não deve ser presumida como totalmente conhecida.
- Quando “ABS” aparecer sem qualificador, o contexto deve deixar explícito se se trata do **ABS geral** ou do **ABS em construção**.

## Estado da reorganização
- PR #68: Project Knowledge/continuidade — merged.
- PR #69: governança, modelo conceitual e inventário — merged.
- PR #70: consolidação da arquitetura documental — merged.
- PR #72: estado, continuidade e interface — merged.
- PR #73: auditoria fontes/histórico/Mini-Cérebro/arquivo — merged.
- Último merge antes da rodada atual: PR #80, commit `5c7de8b64fc2cb8fe58dfd4c4e4c7c5f9b3e1454`.
- Handoff detalhado criado em `continuidade/05_handoffs/04_HANDOFF_ARQUITETURA_PROJETO_ABSOLUTO_2026-09-23.md`.
- Commit do novo handoff: `d967adad57bcb824366d8db6938fe1daef3632bc`.

## O que já foi organizado
- governança da informação;
- modelo conceitual Projeto Absoluto → Sistema → projetos/ABS;
- portas de entrada para IA;
- autoridade por tipo de informação;
- Project Knowledge como estado estruturado derivado;
- distinção entre estado, projeção, decisão, evidência, continuidade e histórico;
- arquitetura consolidada em `docs/02_arquitetura/`;
- documentação temática de interface retirada de `continuidade/` e distribuída por função;
- estado/snapshots antigos reclassificados;
- planejamento × mapas auditado;
- fontes × histórico × Mini-Cérebro × arquivo auditados;
- nenhuma fonte-base foi reescrita;
- nenhum código foi movido por estética;
- patrimônio histórico foi preservado.

## Próxima etapa exata
Consolidar a validação de **índices, referências cruzadas e documentos órfãos** após a auditoria de caminhos antigos.

A auditoria de referências antigas já foi executada nos PRs #74–#76. Foram removidas cópias comprovadamente redundantes e corrigida a referência obsoleta a `docs/architecture/`.

Agora verificar:
- índices que apontem para arquivos inexistentes;
- links relativos quebrados;
- documentos atuais sem ponto de entrada quando deveriam ter um;
- contradições entre índices e a árvore física;
- referências históricas que estejam sendo apresentadas como estado atual.

Corrigir somente problemas comprovados e preservar documentos históricos como históricos.

## Regra
Não alterar automaticamente visão, princípios ou decisões do Imperador.


## Atualização desta rodada — 2026-09-24

A auditoria de índices começou sobre o `main` pós-PR #80. Foi confirmado que alguns documentos de navegação ainda apontavam para handoffs antigos e que o inventário documental V0.1 estava sendo apresentado como se fosse uma fotografia atual. Esses pontos estão sendo corrigidos sem alterar fontes-base, código ou testes.

- PR #81: consistência dos índices e checkpoints — merged em `d248bad33754c087007d91759b5c52a647896022`.


## Atualização semântica — 2026-10-03

A definição conceitual foi refinada pelo Imperador e incorporada às fontes canônicas:

- **Sistema Absoluto / ABS geral** = ecossistema aberto de capacidades e recursos.
- **ABS em construção** = sistema operador/orquestrador desse ecossistema.
- O ABS em construção não é o ecossistema inteiro nem é definido por uma IA, modelo, ferramenta, servidor, dispositivo, interface ou arquitetura específica.
- **ABS V1** refere-se à primeira versão operacional do ABS em construção.
- A partir desta atualização, documentos novos devem desambiguar “ABS geral” e “ABS em construção” quando houver risco de confusão.

Esta atualização é semântica e não autoriza alteração de visão, princípios ou decisões além da distinção acima.


## Atualização de continuidade — 2026-10-03 — conhecimento a preservar antes da construção

### Entendimento que não pode ficar dependente desta conversa

O Projeto Absoluto é maior que qualquer implementação. O Imperador define visão, direção e autoridade. O Sistema Absoluto/ABS geral é entendido como um ecossistema aberto de capacidades e recursos. O ABS em construção é o operador/orquestrador que está sendo criado para operar esse ecossistema.

A relação operacional atual é:

```
IMPERADOR
   ↓
PROJETO ABSOLUTO
   ↓
SISTEMA ABSOLUTO / ABS GERAL
   └── ecossistema aberto de capacidades e recursos
              ↑
              │ opera/orquestra
              │
      ABS EM CONSTRUÇÃO
              ↓
   seleção / combinação / autorização
              ↓
          execução
              ↓
     verificação / evidência
              ↓
       estado / memória
              ↓
        continuidade
              ↓
        novo ciclo
```

Nenhum componente individual é o ABS inteiro. Modelos, IAs, agentes, ferramentas, APIs, servidores, dispositivos, interfaces, Cérebro, Android, Codex e outros são meios/capacidades/recursos que podem ser usados, combinados, substituídos, abandonados ou criados conforme necessidade.

### O que estamos fazendo agora

Esta etapa de organização não substituiu a construção do ABS. Ela existe para garantir que a construção prossiga sobre uma base de conhecimento e continuidade confiável.

O objetivo imediato é **terminar todas as atualizações automáticas necessárias para preservar o entendimento, o estado, as decisões, as evidências, o histórico e o próximo ponto de construção**.

Depois dessa consolidação, a atividade volta para a construção do ABS em construção, sem reiniciar a organização do projeto nem reabrir decisões já consolidadas sem nova evidência.

### Regra de continuidade

Uma nova IA deve conseguir entender, sem depender desta conversa:
1. o que é o Projeto Absoluto;
2. o que significa ABS geral;
3. o que é o ABS em construção;
4. o que significa ABS V1;
5. quem possui autoridade;
6. o que já existe de fato;
7. o que é conhecimento, hipótese, decisão, planejamento ou histórico;
8. o que estamos construindo;
9. por que a etapa atual de consolidação existe;
10. onde a construção deve continuar.

A conversa pode terminar; esse entendimento não pode terminar com ela.


## Atualização crítica de continuidade — 2026-10-03 — sincronização integral de contexto

A organização desta sessão não deve ser interpretada como uma simples correção da definição do ABS.

Foi realizada uma preservação ampla do contexto recuperável do trabalho, incluindo:
- entendimento conceitual;
- distinção ABS geral / ABS em construção / ABS V1;
- decisões e correções de governança;
- pesquisas arquiteturais;
- famílias de moldes investigadas;
- experimentos e simulações 01–30;
- ataques adversariais e invariantes reforçados;
- estado do ABS Core/Cérebro/interface;
- Open WebUI como canal substituível;
- estado da infraestrutura VPS/Coolify;
- bloqueio conhecido do Code Server;
- regras de não reconstrução;
- método PP + BN + AV;
- evolução e independência;
- estado epistemológico e limites das conclusões;
- ponto exato para retomada da construção.

O handoff vigente consolidado é:
`continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md`

Esse handoff existe para impedir que outra IA tenha de reconstruir o entendimento apenas lendo commits ou documentos isolados.

A construção do ABS em construção deve continuar a partir desse estado, sem reiniciar a organização documental salvo quando surgir nova evidência ou uma mudança real de estado.


## Atualização — 2026-10-03 — pesquisa de preservação de contexto
Foi concluída uma pesquisa específica sobre como preservar o entendimento de uma IA e transferi-lo entre sessões. A conclusão corrige a interpretação anterior: o handoff atual é válido, mas não deve ser tratado como preservação integral.

Referência: `docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md`.

Modelo adotado: **conhecimento + decisões + pesquisas + evidências + estado + memória/experiências + histórico + artefatos + checkpoints + handoff + mapas + proveniência**. A conversa permanece temporária. O handoff funciona como ponte para as fontes, não como fonte universal.

Esta pesquisa passa a ser referência para futuras operações de continuidade e para a evolução do Cérebro/Project Knowledge.

## Atualização de continuidade — 2026-10-10 — construção do local de trabalho na VPS

### Decisão e ordem de construção

O Imperador definiu a sequência de trabalho:

1. Construir primeiro um ambiente de trabalho remoto, permanente, integrado, seguro e recuperável na VPS, operado pelo Android.
2. Usar esse ambiente para continuar a construção do ABS em construção.
3. Somente depois delegar gradualmente ao ABS responsabilidades para observar, diagnosticar, operar e recuperar a própria infraestrutura, mantendo limites e mecanismos de emergência independentes.

O ABS não pode ser o único mecanismo capaz de recuperar a infraestrutura da qual depende.

### Componentes previstos

- Coolify: aplicações, serviços, contêineres e implantações.
- Cockpit: administração do sistema operacional.
- SSH pelo Android: acesso técnico direto e rota de emergência.
- Tailscale: conectividade privada para administração.
- Guacamole/desktop remoto: acesso a ambientes gráficos quando necessário.
- Monitoramento e alertas, incluindo detecção externa da indisponibilidade total da VPS.
- Backups externos, com restauração testada.
- Ambiente de desenvolvimento remoto persistente, utilizável pelo celular.
- GitHub como trilha versionada do código, da documentação e das mudanças.

A lista não significa que todos os componentes precisem ser instalados novamente. Primeiro é necessário verificar o que já existe, o que está configurado e o que foi realmente testado.

### Fonte canônica do plano

Plano detalhado, fases, requisitos de aceitação, regras de segurança e próximo passo:

- `docs/03_planejamento/PLANO_AMBIENTE_TRABALHO_VPS_ANDROID.md`

A localização segue a governança documental: o plano temático fica em `docs/03_planejamento/`; este checkpoint de continuidade registra a decisão e aponta para a fonte canônica, evitando duplicar o plano inteiro em continuidade.

### Próxima ação

Auditar o estado real da VPS e dos acessos pelo Android; comparar com o plano; priorizar correções comprovadas. Não começar por uma instalação geral, não reinstalar componentes funcionais sem evidência e não realizar alterações destrutivas sem avaliação e validação.


## Correção crítica de continuidade — 2026-10-10 — versão atual do ABS

A atualização sobre o ambiente de trabalho na VPS não deve ser interpretada como retorno à V1 nem como recomeço do ABS.

A continuidade recuperada indica:
- **ABS V3 ativo** como estado de referência documentado.
- **V4 Completa planejada**, com plano mestre, pesquisa de capacidades e matrizes de fechamento em PR #127, aberto/em rascunho no momento da consulta.
- PR #128 contém uma correção de segurança para rejeitar planos operacionais com etapas sem `capability_id`; estava aberto/em rascunho e não deve ser considerado incorporado à `main` sem nova verificação.

A meta imediata é melhorar o ambiente e as ferramentas que estavam limitando o trabalho, preservando o que já foi construído e retomando do estado real. Não reiniciar o desenvolvimento na V1, não recriar componentes já existentes e não tratar planejamento da V4 como implementação concluída.

Referências:
- `docs/03_planejamento/PLANO_AMBIENTE_TRABALHO_VPS_ANDROID.md`
- PR #127: https://github.com/samuelferreira24/Projeto-Absoluto/pull/127
- PR #128: https://github.com/samuelferreira24/Projeto-Absoluto/pull/128

Próximo passo: auditar o ambiente de trabalho e, em paralelo ao planeamento de infraestrutura, reconciliar os PRs e o estado de código/testes para que a continuação da construção preserve a trajetória existente.
