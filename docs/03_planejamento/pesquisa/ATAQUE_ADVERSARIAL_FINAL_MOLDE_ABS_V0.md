# ATAQUE ADVERSARIAL FINAL — MOLDE CANDIDATO ABS V0

**Status:** concluído como simulação conceitual.  
**Natureza:** não é benchmark nem experimento real.

## Objetivo

Tentar destruir o molde candidato depois da auditoria cruzada, procurando pontos de falha, complexidade excessiva, perda de controle e loops.

## Ataques decisivos

1. **Meta-agente disfarçado:** o Architecture Selector pode virar autoridade autônoma. **Ameaça confirmada.** Deve operar dentro de políticas, orçamento e autoridade externa.
2. **Complexidade maior que o problema:** ativar todas as camadas em tarefas simples gera overhead. **Ameaça confirmada.** Exige complexidade elástica e caminho mínimo.
3. **Oscilação de estratégia:** A→B→A pode gerar loop. **Ameaça confirmada.** Registrar estratégias tentadas e impor orçamento.
4. **Objetivo ambíguo:** interpretação errada pode contaminar toda execução. **Não resolvido apenas pelo molde.** UNKNOWN/esclarecimento são necessários.
5. **Mudança de objetivo:** precisa de identidade/versionamento e autoridade da mudança.
6. **Modelo fraco:** substituição permite trocar executor, mas não garante competência.
7. **Ferramenta incorreta:** resultado de ferramenta não é automaticamente verdade; proveniência e verificação são necessárias.
8. **Verificador errado:** é um ponto crítico; verificação independente é necessária quando o risco justificar.
9. **Ferramenta maliciosa:** contrato não basta; limites, sandbox e autorização precisam existir fora da descrição da ferramenta.
10. **Memória inválida:** memória antiga não pode ter autoridade automática; precisa de proveniência e validade.
11. **Contexto excessivo:** enviar tudo ao modelo degrada eficiência; contexto deve ser seletivo.
12. **Contexto insuficiente:** recuperar informação sob demanda e manter estado externo.
13. **Executor desaparece:** substituição funciona apenas se houver capacidade alternativa.
14. **Corrupção de estado:** exige eventos, checkpoints, invariantes e recuperação real.
15. **Concorrência:** o molde não resolve sozinho locking, conflitos e isolamento em escala; permanece aberto.
16. **Explosão de subagentes:** exige admission control, profundidade e orçamento.
17. **Autonomia excessiva:** ações irreversíveis precisam de política de autorização proporcional ao risco.
18. **Control Plane como gargalo:** deve governar objetivos, políticas e limites, não cada microação.
19. **Selector escolhe arquitetura complexa demais:** fast path deve ser padrão quando suficiente.
20. **Tarefa nunca vista:** o molde pode representar UNKNOWN e explorar novas capacidades, mas não garante sucesso.

## Resultado

O candidato **não foi destruído**, mas não sobrevive sem correções.

Invariantes reforçados:
- autoridade externa;
- selector limitado por política;
- complexidade elástica;
- identidade/versionamento de objetivo;
- memória não é autoridade absoluta;
- verificação proporcional e, quando possível, independente;
- capacidades com limites além do schema;
- admission control para subagentes;
- orçamento de autonomia;
- integridade de estado;
- UNKNOWN explícito.

## Conclusão

A hipótese mais precisa passa a ser:

> **O ABS deve possuir um núcleo de controle estável e limitado, enquanto a estratégia de execução pode ser adaptativa e variável.**

A adaptatividade não significa liberdade para o sistema redefinir suas próprias regras fundamentais.

## Limites

Este ataque é simulação conceitual. Não demonstra desempenho, custo, latência, confiabilidade ou escalabilidade real.

## Próxima fronteira

Construir o menor experimento real que teste:
- objetivo persistente;
- estado externo;
- estratégia variável;
- executor substituível;
- observação;
- verificação;
- recuperação;
- orçamento;
- autorização;
- caminho mínimo.
