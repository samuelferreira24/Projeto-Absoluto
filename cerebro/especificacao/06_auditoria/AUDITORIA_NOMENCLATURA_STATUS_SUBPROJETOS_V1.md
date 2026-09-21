# AUDITORIA DE NOMENCLATURA, VERSÕES E SUBPROJETOS — V1

**Data:** 2026-09-20

## Objetivo
Separar nome, função, versão e estado dos artefatos sem apagar patrimônio histórico.

## Base de planejamento
A base atual é composta pelo Mapa Mestre, Tabuleiro de Capacidades, Quadro de Pendências, Plano de Rede Evolutiva e pelas evidências do código, testes e estado real.

O antigo Plano_Projeto.md é uma visão conceitual histórica e não deve continuar com nome genérico de planejamento atual.

## Subprojetos / frentes identificados
- ABS Core — núcleo operacional atual.
- Cérebro — memória, conhecimento e continuidade; construção/integração.
- Mini-Cérebro — investigação e patrimônio histórico.
- Sistema — sistema anterior; histórico.
- O-IMPERIO-COMPLETO-claude — conjunto histórico de projeto, sistema, cliente e migração.
- automação — frente reservada.
- comercial — frente reservada.
- metas_pessoais — frente reservada.

Integração entre unidades não significa fusão.

## Nomenclatura
Documentos atuais usam nomes descritivos e versão quando relevante. Mapas usam numeração funcional de navegação, não ordem obrigatória de execução. Histórico deve explicitar snapshot/data ou estado histórico. Código operacional não deve ser renomeado sem verificar imports, scripts, testes e serviços.

## Correções desta auditoria
1. Plano_Projeto.md → 01_VISAO_CONCEITUAL_HISTORICA.md. Motivo: conteúdo conceitual anterior; evita competir nominalmente com o planejamento dinâmico.
2. TRANSFERENCIA_PROJETO_ABSOLUTO_ESTADO_ATUAL_V1.md → 2026-09-19_TRANSFERENCIA_ESTADO_SNAPSHOT.md em fontes. Motivo: snapshot datado e já superado pela construção posterior.

## Regra de versões
Não apagar V0, V0.1, V1, V2 ou arquivos sem versão automaticamente. Antes de consolidar, verificar informação exclusiva, substituição real, referências, decisões, experimentos e valor histórico.

## Próxima auditoria
Revisar por família: planejamento/mapas; Cérebro; Mini-Cérebro; ABS Core; O-IMPERIO-COMPLETO-claude; Sistema histórico; automação/comercial/metas; scripts/testes.

Resultado desejado: distinguir rapidamente o que existe, está sendo construído, foi planejado, foi testado, é hipótese ou é histórico.