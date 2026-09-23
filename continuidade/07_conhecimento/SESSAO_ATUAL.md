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

## Trabalho executado nesta continuidade

1. PR #69 foi concluído e incorporado ao `main`, consolidando governança, modelo conceitual, inventário e rastreabilidade.
2. A análise dos dois repositórios confirmou:
   - `Projeto-Absoluto` = construção atual;
   - `Sistema` = repositório histórico do sistema anterior, preservado separadamente.
3. Foi identificada uma duplicação estrutural clara na documentação:
   - `docs/architecture/`;
   - `docs/02_arquitetura/`.
4. Foi iniciado um lote controlado de migração para consolidar arquitetura em `docs/02_arquitetura/`.
5. Nenhum código operacional, fonte-base ou patrimônio histórico foi alterado.

## Migração em andamento

Os oito documentos arquiteturais de `docs/architecture/` e quatro documentos arquiteturais que estavam soltos em `docs/` foram consolidados em `docs/02_arquitetura/`.

A operação usa os mesmos blobs Git dos arquivos originais, preservando conteúdo.

## Estado dos dois repositórios

### Projeto-Absoluto

É o repositório da construção atual e contém:
- ABS Core;
- Cérebro;
- continuidade;
- interface atual;
- documentação;
- testes;
- automação;
- patrimônio histórico preservado.

### Sistema

Está separado como patrimônio/repositório histórico do sistema anterior. Sua árvore atual contém runtime, interface, continuidade, integração e arquivo legado.

Ele deve servir para:
- recuperar ideias;
- comparar soluções;
- recuperar código/experimentos;
- entender decisões anteriores.

Não deve competir silenciosamente com o ABS atual como fonte de implementação.

## Próximo ponto

Depois de validar o lote arquitetural:

1. auditar estado/continuidade;
2. definir autoridade entre Project Knowledge, snapshots, handoffs e decisões;
3. reduzir documentos concorrentes sem apagar histórico;
4. auditar planejamento versus mapas;
5. auditar histórico versus fontes/arquivo;
6. somente então fazer novos lotes de migração.

## Regra

Não alterar automaticamente visão, princípios ou decisões do Imperador.
