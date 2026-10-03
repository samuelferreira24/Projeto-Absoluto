# INVENTÁRIO DE CAPACIDADES — ABS EM CONSTRUÇÃO V1

## Função

Este documento é o índice humano do inventário de capacidades do ABS em construção. Ele não redefine o Projeto Absoluto, não substitui o código e não transforma planejamento em implementação.

A fonte quantitativa das 72 capacidades do tabuleiro é:
`cerebro/mapas/01_TABULEIRO_72_CAPACIDADES_V0_1.md`

O registro machine-readable é:
`continuidade/07_conhecimento/capability_registry.json`

## Regra de classificação

- **governança** — pertence à direção/autoridade do Projeto, não é feature do ABS.
- **operacional** — há implementação e evidência suficiente para considerar a capacidade presente.
- **parcial** — há materialização, mas falta fechamento end-to-end.
- **planejada** — ainda não materializada ou é exploratória.

A classificação não é uma nota de qualidade.

## 1. Núcleo operacional

| Capacidade | Evidência principal | Estado |
|---|---|---|
| Registro de capacidades | `abs_core/capabilities.py` | operacional |
| Orquestração de Work | `abs_core/orchestrator.py` | operacional |
| Persistência de Work | `abs_core/store.py` | operacional |
| API/servidor | `abs_core/api.py`, `server.py` | operacional |
| Runtime/composição | `abs_core/runtime.py` | operacional |
| Contexto cognitivo | `abs_core/cognitive_context.py` | operacional |
| Runtime cognitivo/chat | `abs_core/intelligence.py` | operacional |
| Dados | `abs_core/data_layer.py` | operacional |
| Verificação | `abs_core/verification.py` | operacional |
| Conhecimento do projeto | `abs_core/project_knowledge.py` | operacional |
| Proveniência/trajectory | `abs_core/trajectory.py` | operacional |
| Continuidade/checkpoint | `abs_core/continuity.py` | operacional |

## 2. Execução e inteligências

| Capacidade | Implementação | Estado |
|---|---|---|
| Codex | `codex_adapter.py` | operacional |
| Internet HTTP | `internet_adapter.py` | operacional |
| GitHub | `github_adapter.py` | operacional |
| OpenAI | `openai_adapter.py` | disponível condicionalmente |
| Claude | `ai_adapters.py` | disponível condicionalmente |
| Gemini | `ai_adapters.py` | disponível condicionalmente |
| OpenRouter | `openrouter_adapter.py` | disponível condicionalmente |
| IA local | `local_ai_adapter.py` | disponível quando configurada |
| Nós externos | `node_gateway.py` | parcial |
| Ponte GitHub → Work | `bridge.py` | operacional |

## 3. Recursos, ferramentas e rotas

A base já separa descoberta, conhecimento, planejamento, seleção e despacho:

`tool_discovery.py` → descoberta

`tool_knowledge.py` + `tool_knowledge_store.py` → conhecimento persistente

`tool_planner.py` → planejamento

`resource_router.py` → seleção de rota

`resource_dispatcher.py` → despacho/execução

`tool_learning.py` → aprendizado de uso

`connections.py` → conexões

`resources.py` → recursos/dispositivos

Isso é uma separação funcional importante: **descobrir não significa confiar; planejar não significa executar; selecionar não significa autorizar**.

## 4. Controle, segurança e evolução

Já existem fronteiras para:

- aprovação;
- sandbox/política do Codex;
- ações de maior impacto;
- verificação de resultado;
- atualização controlada;
- health check;
- rollback;
- continuidade operacional;
- auditoria por testes;
- registro de evidências.

Fontes principais:

- `abs_core/verification.py`
- `abs_core/update_manager.py`
- `abs_core/update_daemon.py`
- `abs_core/continuity.py`
- `tests/`

## 5. Interface

A interface já possui runtime próprio e contratos de entrada:

- `abs_core/interface_runtime.py`
- `20_interface/`
- API `/chat`
- API de modo, input e contexto.

A interface continua sendo camada de acesso. Ela não define o ABS.

## 6. Continuidade e conhecimento

A arquitetura de continuidade agora possui:

`00_IA_NAVEGACAO.md`
→ porta de entrada

`project_knowledge.json`
→ estado derivado observável

`MAPA_AUTO_ESTADO_PROJETO.md`
→ projeção humana

`trajectory_registry.json`
→ relações semânticas de trajetória

`capability_registry.json`
→ inventário das 72 capacidades

handoff/session
→ ponte de retomada, não fonte universal

Git
→ histórico temporal primário

## 7. O que estava escondido e agora está identificado

A auditoria encontrou uma diferença entre **capacidade existente** e **capacidade catalogada**.

O Project Knowledge antigo observava diretamente apenas três capacidades principais: orquestrador, Codex e Internet HTTP. O código atual contém uma superfície muito maior: recursos, conexões, descoberta, planejamento, despacho, aprendizado, múltiplas inteligências, interface, continuidade, atualização, verificação, GitHub e nós.

A partir deste inventário, essas peças deixam de depender apenas do nome dos arquivos para serem encontradas.

## 8. O que ainda não deve ser marcado como fechado

As capacidades classificadas como **parciais** continuam abertas. Em especial:

- Cérebro plenamente integrado ao ciclo operacional;
- memória temporal completa;
- pesquisa contínua como capacidade interna;
- experiência → aprendizado → sabedoria;
- validação end-to-end;
- observabilidade consolidada;
- auditoria independente;
- multi-IA/supervisão em nível completo;
- idempotência e processamento durável;
- monitoramento contínuo;
- interoperabilidade ampla;
- detecção de conflitos;
- red team independente;
- escala.

Isso não significa que nada exista nessas áreas. Significa que a auditoria não encontrou base suficiente para marcá-las como fechadas.

## 9. Critério para fechar uma capacidade

Uma capacidade só passa de **parcial** para **operacional** quando houver, conforme o caso:

1. implementação identificável;
2. contrato/entrada/saída compreensíveis;
3. integração com o runtime correto;
4. teste automatizado ou evidência operacional;
5. tratamento de falha relevante;
6. autoridade/permissão definida;
7. persistência/proveniência quando necessária;
8. caminho de recuperação quando necessário;
9. registro no inventário;
10. navegação para a evidência.

Não basta existir um arquivo com o nome da capacidade.

## 10. Regra de fechamento

O trabalho de organização deve seguir:

**identificar → classificar → separar → verificar → integrar → testar → registrar → só então marcar como operacional.**

A próxima lacuna estrutural identificada fora deste inventário é a granularidade da proveniência semântica: decisões, evidências, implementações e resultados ainda precisam de entidades e relações específicas para que perguntas como “qual decisão foi substituída?” sejam respondidas sem depender de documentos amplos.
