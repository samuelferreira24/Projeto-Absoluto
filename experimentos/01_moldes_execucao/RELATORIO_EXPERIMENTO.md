# Relatório — Experimento 01: Família de Moldes de Execução

## Estado
Protótipo isolado — não integrado ao núcleo ABS e não oficial.

## Hipótese
O ABS pode manter uma família de moldes e ativá-los automaticamente por critérios, explicitamente pelo Imperador, em composição quando critérios independentes apontarem para capacidades diferentes, e em recuperação quando o estado exigir.

## Moldes iniciais
DIRECT, WORKFLOW, AGENT, MULTIAGENT, RESEARCH e RECOVERY. Os seis não são considerados definitivos.

## Rodadas
### A — casos básicos
Passou: execução direta, workflow, agente, multiagente, pesquisa, recuperação, override explícito, composição explícita, independência de recurso e mudança de contexto.

### B — ataque adversarial
A primeira versão ingênua falhou conceitualmente em dois casos: pesquisa + paralelização e workflow + agente. O motivo foi precedência fixa, que descartava critérios simultâneos.

### Correção
A versão V0.1 transforma critérios em candidatos e permite composição automática. RECOVERY permanece como transição especial porque representa uma condição de estado.

### C — restrições
Testada filtragem por moldes proibidos e orçamento máximo de complexidade. Quando nenhum molde especializado permanece, o protótipo cai para DIRECT.

## Resultado
O protótipo demonstra que família de moldes + seleção + composição + override é implementável sem criar um superagente central.

Ainda não demonstra que os critérios são suficientes, que as seis famílias são completas, que a composição produz execução semanticamente correta, que regras fixas são a forma final de seleção, que o modelo é adequado para produção ou que o ABS precisa adotar um framework externo.

## Próxima barreira
Testar missões reais do ABS com contexto incompleto, critérios conflitantes, recurso indisponível, executor que falha, necessidade de autorização, mudança de estado durante execução e aquisição de nova capacidade.

Somente após essa rodada deve-se decidir se o contrato entra no núcleo do ABS.
