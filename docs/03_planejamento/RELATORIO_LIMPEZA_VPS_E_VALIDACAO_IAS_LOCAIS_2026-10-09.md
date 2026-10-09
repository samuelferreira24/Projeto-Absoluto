# Relatório de limpeza e validação da VPS ABS — 2026-10-09

## Estado executivo

A limpeza dos modelos redundantes e dos caches regeneráveis foi executada na VPS real por comandos allowlistados do runner reserva. A configuração de seis modelos foi aplicada após seis testes diretos e seis chamadas de integração ABS passarem.

**Estado observado após a limpeza:** disco de 58 GB, 36 GB usados, 22 GB livres (62%); RAM disponível observada entre 3,9 e 4,0 GiB; swap de 2 GiB, com cerca de 1,2 GiB em uso. O serviço `abs.service` respondeu `alive`, versão V3.

## Conjunto local configurado

| ID ABS | Tag Ollama | Teste de chat direto | Integração ABS | Decisão |
|---|---|---|---|---|
| `qwen3.5-0.8b` | `qwen3.5:0.8b` | PASS | PASS | Fallback leve e modelo padrão |
| `qwen3.5-2b` | `qwen3.5:2b` | PASS | PASS | Modelo geral de uso diário |
| `qwen3.5-4b` | `qwen3.5:4b` | PASS | PASS | Modelo mais forte da família Qwen; teste de imagem passou neste ciclo |
| `ministral-3b` | `ministral-3:3b` | PASS | PASS | Família complementar; chamada de ferramenta passou em teste direto |
| `gemma4-e2b-q3` | `hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S` | PASS | PASS | Variante quantizada para caber melhor na VPS |
| `phi4-mini-3.8b` | `phi4-mini:3.8b` | PASS | PASS | Família complementar para texto |

Cada teste direto confirmou resposta com marcador esperado e `/api/ps` sem modelos ativos após `keep_alive=0`. O fluxo de integração reportou `ABS_INTEGRATION_COUNT=6/6`.

## Limites funcionais comprovados

- **Ferramentas:** Ministral passou no teste de chamada de ferramenta. Phi-4 Mini falhou: retornou texto descrevendo uma chamada em JSON, em vez de uma chamada de ferramenta estruturada. Não declarar suporte funcional a ferramentas para todos os modelos.
- **Visão:** Qwen 3.5 4B passou no teste de imagem neste ciclo. Gemma E2B Q3 falhou porque o servidor informou que a entrada de imagem não é suportada sem o artefato `mmproj`. A capacidade multimodal da Gemma permanece não validada.
- **Estado do ABS:** o PR #132 mudou o status padrão de adapters configurados para `configured`, evitando declarar `available` sem sinal explícito de verificação de saúde. A existência de uma configuração não é prova de saúde ou de capacidades.
- **Memória/contexto:** o PR #131 adicionou limite de contexto Ollama configurável (padrão 2048, intervalo 512–8192), reserva de memória aumentada e bloqueio seguro quando não é possível medir RAM.

## Variantes removidas após aprovação dos testes

O script salvou o Modelfile de cada tag removida e só executou esta etapa depois de seis testes diretos e seis integrações passarem:

| Tag removida | Digest observado |
|---|---|
| `gemma4:e2b` | `b37049369adfe3d2b653af0ab301a062ca5cbe96ace6aa0d3f2559ee9b563fc2` |
| `gemma4:e4b` | `dc35e8d9c6061baa6f0fa870975ab6932e2542b579b13ea0f199fa4bb7300c9c` |
| `gemma4-e4b-iq2m-ctx1k:latest` | `1ddeb41c9edaf7f3f89e722917d083c98230aa598be51c208e6f7e505baa8b57` |
| `hf.co/bartowski/google_gemma-4-E4B-it-GGUF:IQ2_M` | `6595341a11cf300429efa1e6f27294ac83de52d9c67f1e9045848254af3be0d8` |
| `hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_S` | `4e895d6d171655c0ac56f55af79310bca8cd7609f281bd94c7c23db3cf8f4c07` |

O script reportou `CLEANUP_PHYSICAL_BYTES_DELTA=19248005120` bytes para a remoção das variantes. A leitura arredondada de `df` passou de 55 GB usados / 2,9 GB livres para 37 GB usados / 21 GB livres após essa etapa.

## Cache regenerável removido

Um comando separado e allowlistado limpou somente caches npm e apt, após verificar que não havia uma operação npm de instalação/cache em andamento:

- `/home/absadmin/.npm`: 337.380.269 → 47.707 bytes.
- `/root/.npm`: 324.632.098 → 335.785 bytes.
- `apt-get clean`: PASS.
- Espaço físico adicional reportado: 1.027.313.664 bytes.
- Depois da limpeza: 36 GB usados / 22 GB livres (62%).

Nenhum log, backup, workspace de runner, volume Docker, imagem de rollback, serviço ou tag selecionada foi removido nesta etapa.

## Infraestrutura preservada

O inventário real confirmou estes componentes em execução e/ou relevantes:

- `abs.service`, Ollama e OpenClaw Gateway.
- Runner principal e runner reserva do GitHub Actions.
- Docker/Coolify: containers `coolify`, `coolify-db`, `coolify-redis`, `coolify-sentinel` e `coolify-proxy) saudáveis.
- Imagens antigas do Coolify/Sentinel e imagens sem container atual foram mantidas como rollback ou componentes potencialmente necessários. Não executar `docker system prune` nem remover volumes sem auditoria adicional.
- Diretórios de backups, inventários e logs foram preservados.

## Pendências e limites de rollback

1. **Ambiguidade de Ministral não resolvida:** o inventário posterior ainda lista duas entradas com o mesmo nome `ministral-3:3b`, mas digests diferentes:
   - `316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63`
   - `cb991b54b0223e5de2706780b88bb9bca50f49654e39d4608e016e9ff0413a41`
   
   Também continua listada a tag `llamacpp:316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63`, que compartilha o primeiro digest. Não apagar nenhuma dessas referências até correlacionar os manifests físicos e confirmar qual digest a configuração usa.

2. **Rollback de modelos removidos:** a configuração anterior e os Modelfiles foram guardados em `/home/absadmin/abs-local-ai-operation-backups/20261009T143518Z`. Os pesos removidos não foram copiados integralmente para outro armazenamento; a restauração desses modelos exige baixá-los novamente. Os seis modelos selecionados foram preservados.

3. **Limpeza restante:** `/var/log` ocupava aproximadamente 2,2 GB e `/var/lib` aproximadamente 4,1 GB no inventário. Não foram apagados porque contêm logs/estado do sistema ainda não classificados. O diretório `/usr/share/ollama` ocupava aproximadamente 18 GB, esperado para os modelos retidos. Os diretórios dos dois runners foram preservados para não comprometer os canais remoto principal e reserva.

## Evidências operacionais

- Execução completa dos seis modelos e limpeza de variantes: [comentário do runner](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6083390002).
- Inventário detalhado de serviços, tags e disco: [inventário da VPS](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6087970189).
- Limpeza de caches npm/apt e medição de bytes físicos: [resultado da limpeza de caches](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6088001956).
- Correções de segurança de memória/contexto: [PR #131](https://github.com/samuelferreira24/Projeto-Absoluto/pull/131).
- Status honesto de capacidades e adapters: [PR #132](https://github.com/samuelferreira24/Projeto-Absoluto/pull/132).

## Conclusão

A seleção de seis modelos está configurada e os seis passaram por chat direto e integração ABS. Foram removidas cinco variantes redundantes e caches regeneráveis, recuperando espaço substancial. A operação **não deve ser marcada como 100% concluída** até resolver a ambiguidade de digest de Ministral e validar separadamente a chamada de ferramenta do Phi-4 Mini e a entrada multimodal da Gemma com o artefato correto.
