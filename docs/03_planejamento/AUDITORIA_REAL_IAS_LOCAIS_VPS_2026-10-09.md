# Auditoria real das seis IAs locais na VPS — 2026-10-09

## Escopo e limites

Auditoria baseada em comandos executados pela interface operacional do GitHub Actions na VPS `abs-vps-01`, no inventário da API do Ollama e em evidências anteriores do ABS. Não houve remoção de modelos, reinício de serviços ou alteração de configuração durante esta auditoria.

Evidências primárias:
- [Estado da VPS, runners, ABS V3 e disco](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6081581031)
- [Inventário de tags, tamanhos e modelos ativos do Ollama](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6081593606)
- [Teste funcional atual do Qwen 0.8B](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6081728219)
- [Estado atual de RAM, swap, disco e ABS](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6081731273)

Limite importante: o canal de comandos atualmente disponível não possui um comando de auditoria por diretório (`du`) nem um inventário de camadas físicas Docker/Ollama. Portanto, os tamanhos por tag não devem ser somados como se todos fossem armazenamento físico exclusivo. A decomposição completa dos 52 GB usados continua pendente.

## 1. Estado observado

- Disco: 58 GB reportados, 52 GB usados, 5,3 GB disponíveis (91%).
- RAM: 5,7 GiB total; cerca de 3,9–4,0 GiB disponíveis nas medições de estado sem modelo ativo.
- Swap: 2 GiB, cerca de 1,0–1,1 GiB em uso.
- ABS V3: serviço ativo, endpoint de saúde retornou `alive`.
- Ollama: serviço ativo; no momento do inventário, nenhum modelo estava carregado.
- Runner principal e runner reserva: ambos ativos no mesmo host. Isso não é redundância física.
- Git checkout da VPS: `main...origin/main`, com arquivo não rastreado `?? :memory:`. Deve ser inspecionado antes de removê-lo; não foi apagado.
- Logs do ABS incluem um `BrokenPipeError` ocorrido em resposta a uma conexão que fechou. É compatível com um cliente que encerrou a conexão, mas requer correlação com os timeouts anteriores; não prova falha permanente do serviço.

## 2. As seis tags principais configuradas

A configuração de instalação em `.github/workflows/abs-vps-command.yml` associa os seguintes seis IDs de capacidade aos modelos canônicos:

| ID de capacidade | Tag canônica | Tamanho reportado |
|---|---|---:|
| `local-ai:qwen3.5-0.8b` | `qwen3.5:0.8b` | 1,32 GB |
| `local-ai:qwen3.5-2b` | `qwen3.5:2b` | 2,68 GB |
| `local-ai:qwen3.5-4b` | `qwen3.5:4b` | 3,32 GB |
| `local-ai:ministral-3b` | `ministral-3:3b` | 2,95 GB |
| `local-ai:gemma4-e2b` | `gemma4:e2b` | 4,59 GB |
| `local-ai:gemma4-e4b` | `gemma4:e4b` | 6,58 GB |
| **Total lógico reportado** | | **21,45 GB** |

Tamanhos retornados pela API do Ollama em GB decimais; não equivalem necessariamente a espaço físico exclusivo por causa de camadas compartilhadas.

## 3. Entradas adicionais observadas

Além das seis tags canônicas, o inventário apresentou estas entradas de experimento:

| Tag/entrada adicional | Tamanho reportado | Ação recomendada |
|---|---:|---|
| `gemma4-e4b-iq2m-ctx1k:latest` | 4,95 GB | Candidata a remoção após confirmar que nenhuma configuração ainda a referencia |
| `hf.co/bartowski/google_gemma-4-E4B-it-GGUF:IQ2_M` | 4,95 GB | Candidata a remoção; variante experimental não canônica |
| `hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S` | 3,11 GB | Candidata a remoção; variante experimental não canônica |
| `hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_S` | 3,13 GB | Candidata a remoção; variante experimental não canônica |
| segunda entrada `ministral-3:3b` (ID/digest diferente) | 2,95 GB | Investigar manifests antes de remover; não executar remoção por nome ambíguo |
| `llamacpp:316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63` | 2,95 GB | Alias que reporta o mesmo ID/digest que uma entrada Ministral; provável remoção segura depois de confirmar que o tag canônico permanece intacto |

Há 12 linhas no inventário, mas não 12 modelos independentes. O alias `llamacpp:...` compartilha o ID reportado `316262d...` com uma das entradas Ministral. Duas tags Gemma E4B IQ2_M têm tamanho semelhante, mas manifests diferentes; é necessário confirmar compartilhamento de camadas antes de estimar a economia física.

Não executar `ollama rm ministral-3:3b` até resolver a duplicidade do mesmo nome com IDs distintos: uma remoção por nome pode atingir a tag usada pelo ABS ou deixar ambiguidade sobre o resultado.

## 4. Estado funcional: disponibilidade não é validação

| Modelo | Evidência atual disponível | Estado correto |
|---|---|---|
| Qwen 0.8B | Teste atual direto via Ollama passou: `PASS qwen3.5:0.8b` | **PASS funcional básico** |
| Qwen 2B | Evidência anterior de teste sequencial; não repetido nesta auditoria | Passou em checkpoint anterior; retestar se necessário |
| Qwen 4B | Registrado no ABS e tag canônica instalada; sem prova ponta a ponta nesta auditoria | **Não validado neste checkpoint** |
| Ministral 3B | Registrado; múltiplas entradas/tag ambígua | **Não validado; resolver duplicidade** |
| Gemma E2B | Registrado; tag canônica instalada; sem prova ponta a ponta | **Não validado neste checkpoint** |
| Gemma E4B | Registrado; tag canônica instalada; tentativa anterior com variante IQ2_M terminou em timeout de 270 s | **Não validado; risco alto de memória/latência** |

O runtime do ABS estima aproximadamente 1,8 GB para Qwen 0.8B, 3,0 GB para Qwen 2B, 4,2 GB para Qwen 4B, 3,5 GB para Ministral 3B, 5,2 GB para Gemma E2B e 7,0 GB para Gemma E4B. São estimativas de capacidade, não medições exatas. Com 5,7 GiB de RAM total, Gemma E2B e especialmente E4B não devem ser carregados para testes automáticos sem um plano de memória e uma janela controlada. A tentativa anterior da variante Gemma E4B IQ2_M excedeu o timeout e foi limpa/reiniciada depois.

## 5. Plano de limpeza recomendado — ainda não executado

Ordem segura:
1. Preservar as seis tags canônicas e a configuração `ABS_LOCAL_AI_MODELS`.
2. Capturar novo inventário `/api/tags`, digest por tag e configuração ativa antes de qualquer remoção.
3. Remover, uma a uma, as variantes experimentais Qwen 4B Q3, Gemma E2B Q3 e as duas tags Gemma E4B IQ2_M, depois de verificar referências e compartilhamento.
4. Remover o alias `llamacpp:...` somente após confirmar que `ministral-3:3b` continua apontando para o digest canônico pretendido.
5. Resolver a dupla entrada Ministral por digest/manifest; não apagar pelo nome ambíguo.
6. Após cada remoção, comparar `df -h /` e o inventário de tags. Parar se o espaço não aumentar ou se alguma tag canônica mudar.
7. Validar as seis capacidades sequencialmente, com `keep_alive=0`, limite de tempo, memória monitorada e evidência de provenance do ABS. Não executar o lote de seis simultaneamente.
8. Auditar depois `docker system df`, diretórios de dados, logs, cache e backups; só então decidir outras limpezas.

A remoção de tags só recupera espaço físico quando deixa blobs sem referências. A soma das entradas adicionais não é promessa de espaço recuperado.

## 6. Ações deliberadamente não feitas

- Nenhuma tag ou arquivo foi apagado.
- Nenhum serviço foi reiniciado nesta auditoria.
- Não foi executado `docker system prune`, remoção de volumes ou limpeza de diretórios.
- O arquivo não rastreado `:memory:` no checkout foi preservado até identificar origem e conteúdo.
- Não foi afirmado que as seis IAs estão todas funcionais: apenas Qwen 0.8B tem teste funcional atual observado nesta auditoria.

## Conclusão

A prioridade é conservar as seis tags canônicas, limpar as variantes experimentais após inspeção de manifests e, sobretudo, obter uma auditoria de uso físico por diretório/camada. O disco está em 91% de ocupação e o Qwen 0.8B passou no teste atual. As outras cinco capacidades ainda não têm, neste checkpoint, evidência atual uniforme de sucesso ponta a ponta. A limpeza de modelos não deve ser confundida com a validação funcional das seis IAs.
