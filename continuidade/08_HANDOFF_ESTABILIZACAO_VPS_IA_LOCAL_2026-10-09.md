# Handoff — estabilização da VPS e IA local
Data: 2026-10-09
Host: abs-vps-01

## Estado confirmado
- ABS V3 ativo; health check alive.
- Runner principal e reserva ativos e executando trabalhos.
- Última verificação: V3 healthy, cerca de 4,3 GiB de RAM disponível e 16 GiB livres em disco.
- Testes na VPS: 202 passed.
- CI: ABS Core, Project Knowledge Tests, Project Knowledge Sync e validação de navegação passaram após as correções.

## Proteções
Os dois runners têm reinício automático após falha, limite de 1 GiB de RAM e 512 MiB de swap por serviço, encerramento do grupo de processos e timeout de parada de 60 segundos.
Ollama tem limite de 3,5 GiB de RAM, 1 GiB de swap, uma inferência/modelo por vez, contexto 2048 e descarregamento do modelo ao terminar a chamada.
O lote automático de seis modelos foi bloqueado. Testes devem ser sequenciais.

## IA local
Configuração padrão: qwen3.5:0.8b, 64 tokens, temperatura zero, thinking desativado.
- qwen3.5:0.8b — teste direto e chat do ABS V3 passaram; proveniência e verificação aceitas.
- qwen3.5:2b — teste direto e chat do ABS V3 passaram; proveniência e verificação aceitas.
- qwen3.5:4b, ministral-3:3b, gemma4:e2b e gemma4:e4b — permanecem registrados, mas ainda não validados nesta VPS. Os pesos/consumo estimado não deixam margem segura sob o limite atual; não carregar em lote nem testar em paralelo.

## Correções
- O teste do adaptador local simula a resposta nativa do Ollama, usando message.content.
- O validador do smoke test aceita provenance como lista de eventos.
- Capacidade desconhecida é negada mesmo quando o V3 está sob pressão.
- Echo determinístico continua permitido em estado critical para health checks e recuperação.
- /abs v3-test passou com 202 testes.
- /abs v3-local-ai-test passou para qwen3.5:0.8b.
- /abs v3-local-ai-test-qwen2b e /abs v3-local-ai-qwen2b-test passaram para qwen3.5:2b.

## Próximos passos
1. Manter os dois runners ativos e limitados.
2. Preservar qwen3.5:0.8b como fallback padrão.
3. Avançar apenas com testes sequenciais, limites de tokens/contexto, validação de proveniência e verificação de memória.
4. Para os quatro modelos maiores, usar quantização menor ou um nó com mais RAM antes de validar execução.
5. Após cada teste, verificar health, estado V3, memória e se não há modelo ainda carregado.
