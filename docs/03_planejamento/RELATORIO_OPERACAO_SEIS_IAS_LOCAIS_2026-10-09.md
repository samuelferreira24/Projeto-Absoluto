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

A execução remota disparada após a correção de admissão #134 está em andamento. Atualizar esta seção com seu comentário de resultado e evidência final antes de declarar conclusão.
