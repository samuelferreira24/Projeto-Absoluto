# CHECKPOINT DE SESSÃO — 2026-09-23

## Projeto
Projeto Absoluto.

## Definição consolidada
- Projeto Absoluto = visão, método, princípios e objetivos do Imperador; é o projeto maior.
- Sistema = peça/infraestrutura criada para aumentar a capacidade de pesquisar, aprender, planejar, construir, testar e executar.
- ABS = primeiro projeto que o Imperador está tentando construir.
- ABS V1 = segundo protótipo do ABS; futuras versões continuam previstas.
- Outros projetos poderão surgir dentro do Projeto Absoluto e poderão reutilizar, substituir ou não depender do Sistema/ABS.
- O Imperador está aprendendo a construir enquanto constrói; a arquitetura futura não deve ser presumida como totalmente conhecida.

## Organização concluída nesta etapa
- PR #69 consolidou governança, modelo conceitual e inventário inicial.
- PR #70 consolidou a área de arquitetura e eliminou `docs/architecture/`.
- A auditoria seguinte classificou a concorrência entre estado e continuidade.
- Documentação temática de interface foi retirada de `continuidade/` e distribuída por função:
  - pesquisa → `docs/90_fontes/`;
  - arquitetura → `docs/02_arquitetura/`;
  - planejamento → `docs/03_planejamento/`.
- Snapshots antigos de estado/construção foram reclassificados como históricos ou handoffs, sem apagar conteúdo.

## Autoridade atual
- visão/direção → fontes autorizadas do Imperador;
- estado operacional → código + testes + CI + evidências;
- estado estruturado derivado → Project Knowledge;
- projeção humana → `MAPA_AUTO_ESTADO_PROJETO.md`;
- decisões → `continuidade/03_decisoes/`;
- continuidade → checkpoints/handoffs;
- histórico → fontes/snapshots/arquivo preservado.

## Auditoria planejamento × mapas — concluída
- `docs/03_planejamento/` permanece como entrada documental do planejamento.
- `cerebro/mapas/` permanece como rede de capacidades, dependências, pendências e caminhos.
- Não houve necessidade de fundir as áreas nem criar nova camada documental.
- O quadro de status ABS foi o único item desta zona que precisava de reclassificação física: saiu de `cerebro/mapas/` e foi para `cerebro/00_estado/STATUS_ABS_V1_2026-09-22.md`, preservando o conteúdo.
- Os índices e referências foram atualizados para impedir nova confusão entre planejamento e estado.

## Próxima etapa
Auditar **fontes × histórico × Mini-Cérebro × 99_arquivo** antes de nova migração física.

## Regra
Não alterar automaticamente visão, princípios ou decisões do Imperador.
