# Operação das seis IAs locais do ABS — 2026-10-09

## Estado do relatório

**Em execução; não declarar conclusão ainda.** Este relatório separa evidência de teste direto do modelo, integração real pelo ABS e validação de capacidades especiais. Uma resposta direta do Ollama não prova que o roteador do ABS consegue selecionar e executar o mesmo modelo.

## Evidências da primeira operação remota

- Comando remoto: [execução do runner reserva](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6082590749).
- Resultado completo reportado pelo runner: [seis testes diretos e falha de integração](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6082426710).
- A VPS estava com 5,7 GiB de RAM, cerca de 3,0 GiB disponíveis ao início da etapa de integração, swap de 2 GiB e 3,0 GB livres no disco (95% ocupado).
- Os seis testes diretos de texto passaram individualmente:
  1. `qwen3.5:0.8b`
  2. `qwen3.5:2b`
  3. `qwen3.5:4b`
  4. `ministral-3:3b`
  5. `hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S`
  6. `phi4-mini:3.8b`
- Isso prova apenas uma resposta textual básica por modelo. Não prova ferramentas, visão, áudio ou integração funcional com o roteador.
- A etapa de integração via `/chat` falhou em 0/6 com `no_approved_intelligence_resource_available`. O script restaurou a cópia de `/etc/abs-local-models.env`; portanto, a nova configuração não ficou aplicada.
- A limpeza de variantes foi condicionada à integração completa e não ocorreu nessa execução. O download de Phi foi pulado por falta de espaço livre suficiente; a tag `phi4-mini:3.8b` já apareceu instalada no inventário da execução posterior.
- A análise não somou tamanhos lógicos das tags como se fossem espaço físico independente.

## Correções de código incorporadas ao `main`

- [PR #131](https://github.com/samuelferreira24/Projeto-Absoluto/pull/131) — limite explícito de contexto Ollama (padrão 2048, faixa 512–8192), reserva de memória e bloqueio seguro quando a RAM não pode ser medida; testes de regressão.
- [PR #132](https://github.com/samuelferreira24/Projeto-Absoluto/pull/132) — o estado de IA configurada não é mais anunciado como `available` sem sinal explícito de verificação; capacidades não comprovadas ficam separadas.
- [PR #133](https://github.com/samuelferreira24/Projeto-Absoluto/pull/133) — permite a admissão de um pedido local sob pressão apenas com memória medida suficiente.
- [PR #134](https://github.com/samuelferreira24/Projeto-Absoluto/pull/134) — corrige o contador de execução ativa: o pedido atual já ocupa uma vaga quando a verificação de capacidade roda; a exceção segura agora exige exatamente uma execução ativa, fila vazia e RAM suficiente.

As verificações CI observadas para o código de #134 passaram em ABS Core, ABS V2 CI e Project Knowledge Tests antes da incorporação.

## Seleção operacional provisória

| Modelo/tag | Papel | Estado da evidência |
|---|---|---|
| `qwen3.5:0.8b` | fallback leve | teste direto de texto PASS |
| `qwen3.5:2b` | chat geral econômico | teste direto de texto PASS |
| `qwen3.5:4b` | Qwen mais capaz; candidato a visão | teste direto de texto PASS; visão ainda precisa de resultado |
| `ministral-3:3b` | família complementar; candidato a tools | teste direto de texto PASS; chamada de ferramenta ainda precisa de resultado |
| `hf.co/dahus/gemma-4-e2b-it-Q3_K_S-GGUF:Q3_K_S` | candidato multimodal leve | teste direto de texto PASS; visão ainda precisa de resultado |
| `phi4-mini:3.8b` | modelo textual complementar; candidato a tools | teste direto de texto PASS; chamada de ferramenta ainda precisa de resultado |

A seleção só se torna final depois de capacidades especiais, integração ABS e limites de memória serem demonstrados. Não foi reivindicada capacidade de áudio.

## Segurança e rollback

- A operação anterior não conseguiu validar integração e restaurou a configuração anterior.
- Tags de digest ambíguo não devem ser removidas pelo nome.
- A remoção de variantes só deve ocorrer após a configuração selecionada estar aplicada e validada, com backup das referências e verificação do espaço físico antes/depois.
- O estado final precisa registrar os testes por modelo, ferramentas/visão, estado do roteador, lista de modelos carregados após `keep_alive=0`, espaço físico recuperado e qualquer bloqueio restante.

## Execução subsequente

### Resultado confirmado da repetição remota

Evidência: [comentário de resultado do runner reserva](https://github.com/samuelferreira24/Projeto-Absoluto/issues/121#issuecomment-6082752032).

- Seis testes diretos de texto passaram: Qwen 0.8B, Qwen 2B, Qwen 4B, Ministral 3B, Gemma E2B Q3 e Phi-4-mini 3.8B.
- Após cada teste, o endpoint `/api/ps` confirmou `models=[]`; isso confirma descarregamento reportado pelo Ollama.
- Ministral 3B passou o teste de chamada estruturada de ferramenta.
- Phi-4-mini **não** passou o teste de ferramenta: respondeu com um bloco de texto/JSON em vez de preencher `message.tool_calls`. Não atribuir capacidade de chamada de ferramentas a esse modelo com base nesta execução.
- Visão de Gemma E2B Q3 e Qwen 4B foi **SKIP_MEMORY**, não FAIL funcional: a memória disponível havia caído para 1.888 MiB e 1.959 MiB, respectivamente, abaixo dos limiares de 3.000/3.400 MiB.
- Por isso, a operação preservou a configuração anterior e **não aplicou a integração de seis modelos**. A saída registrou `INTEGRATION_NOT_APPLIED: no selected local model proved image input`.
- Foi removida somente a tag alias Ministral de digest exato igual ao modelo canônico. O disco continuou em aproximadamente 2,9 GB livres (95% ocupado); não há evidência de recuperação física significativa, pois o blob é compartilhado.
- A nova configuração e a limpeza de outras variantes continuam bloqueadas até a visão ser provada com memória suficiente e a integração passar. As outras tags experimentais permanecem instaladas; não foram apagadas sem rollback confiável.

### Correção de procedimento preparada, mas não implantada

Foi criada na branch `fix/local-ai-finalize-operation-20261009` uma rotina separada que executa a visão primeiro, recupera memória reiniciando Ollama apenas quando `/api/ps` está vazio, repete os testes sequencialmente e só mantém a nova configuração se as seis integrações ABS passarem; o arquivo correspondente é `scripts/ops/local_ai_finalize_operation.sh`, com workflow fixo `.github/workflows/abs-vps-local-ai-finalize.yml`. A tentativa de abrir o PR dessa rotina foi bloqueada pela ferramenta de controle de segurança, então ela **não está no main nem foi executada**. Não declarar conclusão até que a rotina possa ser revisada, aprovada e executada com evidência.

## Estado final deste checkpoint

**Parcial, não concluído.** Seis modelos passaram teste direto de texto; uma chamada de ferramenta passou (Ministral); visão ainda não foi comprovada; integração ABS 0/6 na execução registrada; configuração anterior restaurada/preservada; alias exato removido; limpeza adicional adiada para proteger rollback e dados.
