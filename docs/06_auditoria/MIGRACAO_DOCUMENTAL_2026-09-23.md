# MIGRAÇÃO DOCUMENTAL — 2026-09-23

## Escopo

Primeiro lote de migração física da reorganização iniciada no PR #69.

Objetivo: eliminar a duplicação estrutural entre `docs/architecture/` e `docs/02_arquitetura/` sem alterar conteúdo técnico.

## Critério

A migração foi considerada segura porque os oito documentos tinham função arquitetural/contratual atual ou evolutiva e `docs/02_arquitetura/` já era a área semântica destinada a essa função.

Nenhum código, teste, histórico ou fonte-base foi alterado.

## Movimentos

| Origem | Destino | Tratamento |
|---|---|---|
| `docs/architecture/ABS_INTEGRATION_V1.md` | `docs/02_arquitetura/ABS_INTEGRATION_V1.md` | mesmo conteúdo |
| `docs/architecture/PROJECT_KNOWLEDGE_V1.md` | `docs/02_arquitetura/PROJECT_KNOWLEDGE_V1.md` | mesmo conteúdo |
| `docs/06_ROTEAMENTO_DE_RECURSOS_V1.md` | `docs/02_arquitetura/ROTEAMENTO_DE_RECURSOS_V1.md` | mesmo conteúdo |
| `docs/04_EVOLUCAO_AUTONOMA_ASSISTIDA_ABS.md` | `docs/02_arquitetura/EVOLUCAO_AUTONOMA_ASSISTIDA_ABS.md` | mesmo conteúdo |
| `docs/05_CONTROLE_DE_EVOLUCAO_PELA_INTERFACE.md` | `docs/02_arquitetura/CONTROLE_DE_EVOLUCAO_PELA_INTERFACE.md` | mesmo conteúdo |
| `docs/07_CONHECIMENTO_E_DESCOBERTA_DE_FERRAMENTAS_V1.md` | `docs/02_arquitetura/CONHECIMENTO_E_DESCOBERTA_DE_FERRAMENTAS_V1.md` | mesmo conteúdo |
| `docs/08_PLANEJAMENTO_E_APRENDIZAGEM_DE_FERRAMENTAS_V1.md` | `docs/02_arquitetura/PLANEJAMENTO_E_APRENDIZAGEM_DE_FERRAMENTAS_V1.md` | mesmo conteúdo |
| `docs/09_MEMORIA_PERSISTENTE_DE_FERRAMENTAS_V1.md` | `docs/02_arquitetura/MEMORIA_PERSISTENTE_DE_FERRAMENTAS_V1.md` | mesmo conteúdo |

## Preservação

Os arquivos foram reconstruídos no Git tree usando os mesmos blob SHAs das fontes originais. Isso preserva o conteúdo byte a byte e evita uma reescrita sem necessidade.

## Validação necessária

Após o commit:
1. confirmar destinos presentes;
2. confirmar origens ausentes;
3. pesquisar referências aos caminhos antigos;
4. verificar links internos relevantes;
5. executar testes/CI documental;
6. regenerar Project Knowledge;
7. atualizar o inventário e o checkpoint.

## Limites

Este lote não:
- altera `abs_core/`;
- altera testes;
- altera fontes-base;
- altera `99_arquivo/`;
- altera o histórico do Sistema;
- redefine a visão do Projeto Absoluto.

## Próximo lote

Auditar a concorrência **estado/continuidade**, sem misturar Project Knowledge, snapshots, handoffs e decisões.
