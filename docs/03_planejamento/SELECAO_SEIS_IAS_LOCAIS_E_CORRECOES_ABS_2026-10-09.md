# Seleção técnica das seis IAs locais do ABS — 2026-10-09

## Conclusão

O inventário não justifica assumir que as seis tags canônicas são automaticamente as melhores. A VPS tem 5,7 GiB de RAM, cerca de 3,9–4,0 GiB disponíveis em idle, swap de 2 GiB com cerca de 1 GiB em uso e disco 91% cheio. A seleção deve priorizar complementaridade, capacidade real na VPS e teste verificável, não só nome/tamanho de modelo.

## Seis slots recomendados para validação

| Slot | Modelo | Papel | Evidência e condição |
|---|---|---|---|
| 1 | qwen3.5:0.8b | fallback rápido e baixo consumo | Único modelo com smoke funcional atual observado neste checkpoint. Repetir ponta a ponta e confirmar descarregamento. |
| 2 | qwen3.5:2b | modelo local padrão econômico | Passou em teste ponta a ponta no checkpoint operacional anterior; repetir com configuração atual e medir RAM/latência. |
| 3 | qwen3.5:4b | Qwen generalista mais forte instalado | Tag reporta ~3,32 GB e estimativa ABS ~4,2 GB RAM; testar somente com contexto curto, margem de memória e timeout. |
| 4 | ministral-3:3b | segunda família; candidato para structured output/tool calling | A documentação oficial lista function calling e structured outputs. Primeiro resolver duplicidade de manifest/digest e provar tool calling no contrato ABS. |
| 5 | Gemma 4 E2B | modalidade complementar: imagem/áudio no modelo oficial | Tag instalada reporta ~4,59 GB e estimativa ABS ~5,2 GB RAM: risco alto. Testar com contexto curto. Variante Q3 de ~3,11 GB só substitui a canônica se passar texto, visão/áudio suportados e template. |
| 6 | phi4-mini:3.8b (candidato ainda não instalado) | especialista complementar em raciocínio/matemática e function calling | Ollama lista ~2,5 GB em Q4_K_M e function calling. Baixar somente após limpeza física medida; depois validar na VPS. Texto apenas, não substitui as modalidades do Gemma. |

### Por que tirar Gemma E4B do conjunto operacional inicial

A tag canônica reporta ~6,58 GB, a estimativa interna de RAM é ~7 GB e uma variante IQ2_M anterior terminou em timeout de 270 s. Isso não prova que a família seja ruim; indica que as variantes testadas não estão justificadas na VPS atual. Reavaliar apenas após mudar infraestrutura ou obter uma quantização que passe em benchmark controlado.

A lista de seis acima é uma shortlist fundamentada, não a afirmação de que os seis já funcionam. O slot 5 depende de teste real; se Gemma E2B não couber estável e a variante Q3 perder modalidades ou falhar, não marcar o slot como resolvido.

## Inventário: manter, remover ou investigar

### Manter provisoriamente
- qwen3.5:0.8b
- qwen3.5:2b
- qwen3.5:4b
- Uma única tag Ministral 3B, depois de identificar qual digest/manifest é o pretendido.
- Uma única implementação Gemma E2B, escolhida após testes de memória e modalidade.

### Candidatas a remover após confirmar referências e digests
- hf.co/bartowski/Qwen_Qwen3.5-4B-GGUF:Q3_K_S — quantização duplicada do Qwen 4B; não manter ambas sem ganho demonstrado.
- hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S — manter somente se for a variante escolhida em lugar da canônica e passar os testes; caso contrário remover.
- gemma4-e4b-iq2m-ctx1k:latest.
- hf.co/bartowski/google_gemma-4-E4B-it-GGUF:IQ2_M.
- llamacpp:316262d960e27504463e6270bd8c1e8665c957ef2cff620ba333af9e1480df63 — provável alias, remover só após confirmar que a tag Ministral canônica continua íntegra.

### Não remover pelo nome ainda
Há duas entradas reportadas como ministral-3:3b com IDs/digests distintos. Não executar remoção por nome até verificar manifests e referências; pode apagar a tag usada pelo ABS.

### Adicionar somente depois da limpeza
phi4-mini:3.8b Q4_K_M. Não baixar enquanto o disco estiver em 91% de ocupação. Tamanho por tag não garante espaço físico exclusivo: o Ollama pode compartilhar blobs; medir df -h e o uso físico depois de cada remoção.

## Correções necessárias no ABS

### P0 — não confundir cadastro com funcionamento
1. abs_core/runtime.py atribui genericamente reasoning, chat e tools a todos os modelos locais. Isso anuncia tool calling sem evidência. Definir capacidades por modelo e por teste; não declarar ferramentas confiáveis para Qwen 0.8B sem validação.
2. abs_core/intelligence.py define status available quando não existe conexão registrada. Um modelo instalado mas quebrado pode aparecer disponível. Separar configured, installed, smoke_passed, operational, degraded e offline, com timestamp e resultado do último teste.
3. O roteador usa estimated_memory_mb como penalidade, não bloqueio. A preferência explícita adiciona +1000 e pode escolher modelo que não cabe. Aplicar preflight de RAM com margem antes da chamada e fallback automático; calibrar estimativas pela quantização, contexto e medições.
4. A proveniência precisa registrar tag, digest, quantização, timeout, tokens, memória antes/depois, latência, resultado de verificação e motivo de fallback.

### P1 — adaptador e testes
5. O adaptador Ollama precisa de contexto máximo operacional explícito. Janela de catálogo não deve ser o contexto padrão: KV cache pode elevar consumo de RAM.
6. Testar separadamente português, instrução exata, JSON, código, raciocínio, imagem, áudio quando suportado, function calling real, timeout, interrupção do cliente e fallback. Um único smoke test prova só conectividade básica.
7. Rodar um modelo por vez, sempre com keep_alive=0 e confirmação de /api/ps vazio ao final. Não executar os seis simultaneamente.
8. Criar benchmark local repetível com prompts idênticos, temperatura fixa, limites de tokens/contexto, 3 repetições, latência, taxa de acerto, RAM pico e resultado por tarefa. Benchmark do fabricante não substitui teste na VPS.

### P2 — armazenamento e operação
9. Inspecionar manifest/digest antes de remover variantes; nunca remover pelo nome ambíguo do Ministral.
10. Medir /var/lib/ollama, /var/lib/docker, logs, caches e backups. A decomposição física por diretório ainda não foi confirmada. Não executar docker system prune, remover volumes nem apagar o arquivo não rastreado :memory: sem identificar origem.
11. Instalar Phi-4-mini só depois de limpeza com recuperação física medida; interromper se o espaço livre não aumentar como esperado.

## Ordem de validação
1. Capturar baseline de RAM, disco, tags, /api/ps e health ABS.
2. Executar smoke sequencial com keep_alive=0, contexto inicial curto (ex.: 2048), 32–96 tokens e timeout adequado ao tamanho.
3. Executar suite comum: português, instrução exata, JSON, resumo, lógica e código; testar function calling só onde declarado.
4. Testar visão/áudio separadamente para os modelos e caminhos que realmente suportam essas modalidades.
5. Guardar resultados com digest, pico de RAM, latência e proveniência ABS.
6. Só marcar operacional se passar os testes mínimos, respeitar memória e descarregar corretamente. Se falhar, corrigir configuração/adapter ou substituir o modelo.

## Evidências e limites
- VPS/inventário: issue #121, comentários 6081581031 e 6081593606.
- Smoke atual Qwen 0.8B: issue #121, comentário 6081728219.
- RAM/disco posterior: issue #121, comentário 6081731273.
- Configuração: abs_core/runtime.py, abs_core/intelligence.py e .github/workflows/abs-vps-command.yml.
- Referências públicas: Ollama Qwen 3.5, Google Gemma 4, Mistral Ministral 3 3B e Ollama Phi-4-mini. Capacidades anunciadas pelos fabricantes não garantem funcionamento no ABS.

Nenhuma remoção, instalação ou mudança de produção foi executada por este documento. A seleção é uma recomendação a confirmar por testes; não declara seis modelos operacionais antes de os testes passarem.