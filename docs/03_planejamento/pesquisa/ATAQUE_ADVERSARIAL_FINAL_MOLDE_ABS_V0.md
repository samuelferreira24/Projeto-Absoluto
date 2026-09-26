# ATAQUE ADVERSARIAL FINAL — MOLDE CANDIDATO ABS V0

**Status:** concluído como simulação conceitual.  
**Natureza:** não é benchmark nem experimento real.

## Objetivo

Tentar destruir o molde candidato depois da auditoria cruzada.

O ataque não procura confirmar o molde. Procura encontrar condições nas quais seus próprios princípios produzam falha, excesso de complexidade ou perda de controle.

## 1. Meta-agente disfarçado

**Ataque:** o Architecture Selector passa a decidir tudo.

**Falha possível:** o Control Plane vira um agente central com outro nome.

**Resultado:** ameaça confirmada.

**Correção:** o selector não deve possuir autoridade ilimitada. Ele seleciona mecanismos dentro de políticas e limites definidos pelo Control Plane/Imperador. A decisão de arquitetura é uma capacidade limitada, não autoridade absoluta.

## 2. Complexidade maior que o problema

**Ataque:** uma tarefa simples passa por estado, contexto, estratégia, brokers, verificador e recovery.

**Falha possível:** overhead maior que o benefício.

**Resultado:** ameaça confirmada.

**Correção:** complexidade elástica deve ser requisito obrigatório. O caminho mínimo deve ser realmente executável sem ativar camadas desnecessárias.

## 3. Oscilação de estratégia

**Ataque:** estratégia A falha, B falha, sistema volta para A.

**Falha possível:** loop de estratégias.

**Resultado:** ameaça confirmada.

**Correção:** registrar estratégias tentadas, motivo da falha e orçamento de tentativas; bloquear ciclos conhecidos; permitir abandono ou intervenção humana.

## 4. Objetivo ambíguo

**Ataque:** objetivo inicial é semanticamente incompleto.

**Falha possível:** o sistema otimiza a interpretação errada.

**Resultado:** não resolvido apenas pelo molde.

**Correção:** representar UNKNOWN/ambiguidade e exigir esclarecimento ou política explícita antes de ações relevantes.

## 5. Objetivo muda durante a execução

**Ataque:** nova instrução contradiz o objetivo anterior.

**Resultado:** o molde suporta mudança, mas precisa de autoridade e versionamento de objetivo.

**Correção:** objetivo deve possuir identidade/versão e origem de autorização.

## 6. Modelo fraco

**Ataque:** modelo não sabe planejar ou usar ferramentas.

**Resultado:** o molde permite trocar executor/modelo, mas não garante que exista um modelo adequado.

**Conclusão:** propriedade de substituição, não garantia de competência.

## 7. Modelo forte, ferramenta ruim

**Ataque:** modelo raciocina corretamente, ferramenta devolve informação incorreta.

**Resultado:** verificação/evidência precisam distinguir resultado de ferramenta de fato verificado.

**Correção:** proveniência e confiança da capacidade precisam acompanhar o resultado.

## 8. Verificador errado

**Ataque:** verificador aceita resultado incorreto.

**Resultado:** ameaça crítica.

**Correção:** verificação deve ser proporcional ao risco e, quando possível, independente do mecanismo que produziu o resultado. Não existe garantia universal.

## 9. Ferramenta maliciosa

**Ataque:** capacidade externa tenta ampliar escopo.

**Resultado:** contrato de capacidade sozinho não basta.

**Correção:** sandbox, escopo, autorização, limites e políticas independentes do tool description.

## 10. Memória inválida

**Ataque:** memória antiga contradiz estado atual.

**Resultado:** memória não pode ser autoridade automática.

**Correção:** memória precisa de proveniência, validade, contexto e possibilidade de invalidação.

## 11. Contexto excessivo

**Ataque:** todo o estado é enviado ao modelo.

**Resultado:** degradação de atenção/custo.

**Correção:** Context Engine seletivo.

Esse princípio possui apoio externo atual: Anthropic trata contexto como recurso finito e enfatiza curadoria do conjunto mínimo de alto sinal. citeturn0search2

## 12. Contexto insuficiente

**Ataque:** o modelo recebe pouco contexto.

**Resultado:** decisões ruins.

**Correção:** recuperação just-in-time, estado explícito e evidência disponível sob demanda.

## 13. Falha do executor

**Ataque:** modelo, ferramenta ou ambiente desaparece.

**Resultado:** o molde sobrevive conceitualmente se houver executor alternativo.

**Limite:** se não existir capacidade alternativa, não há garantia de continuidade.

## 14. Corrupção de estado

**Ataque:** estado persistido fica inconsistente.

**Resultado:** ameaça crítica.

**Correção:** eventos, checkpoints, versionamento e invariantes de estado; recuperação precisa ser testada experimentalmente.

## 15. Concorrência

**Ataque:** centenas de objetivos atualizam recursos compartilhados.

**Resultado:** o molde é compatível conceitualmente, mas não define sozinho locking, isolamento ou resolução de conflitos.

**Status:** aberto.

## 16. Crescimento de subagentes

**Ataque:** cada agente cria vários especialistas.

**Resultado:** explosão de custo e complexidade.

**Correção:** admission control, orçamento, profundidade máxima e escopo.

## 17. Autonomia excessiva

**Ataque:** sistema escolhe ações irreversíveis sem intervenção.

**Resultado:** falha de governança.

**Correção:** autorização baseada em efeitos, risco e contexto; HITL para classes apropriadas de ação.

Mecanismos semelhantes existem em runtimes atuais, incluindo aprovação humana de ferramentas e pausa/retomada. citeturn0search0turn0search6

## 18. Control Plane como gargalo

**Ataque:** todas as microações passam pelo controle central.

**Resultado:** gargalo e acoplamento.

**Correção:** controle por escopo; o Control Plane governa objetivos, políticas e limites, não necessariamente cada microação.

## 19. Seleção de arquitetura errada

**Ataque:** selector escolhe multiagente para tarefa simples.

**Resultado:** desperdício.

**Correção:** fast path como caminho padrão e complexidade adicional justificada por sinais observáveis.

## 20. Tarefa nunca vista

**Ataque:** nenhuma estratégia conhecida serve.

**Resultado:** o molde não garante sucesso, mas permite representar UNKNOWN, explorar capacidades e construir nova estratégia.

**Status:** propriedade de adaptação, não garantia de solução.

# Resultado do ataque

O molde **não foi destruído**, mas sofreu correções importantes.

## Invariantes reforçados

1. Control Plane não pode virar autoridade autônoma.
2. Architecture Selector precisa operar dentro de política e orçamento.
3. Complexidade deve ser elástica.
4. Estratégias tentadas devem ser registradas.
5. Objetivos precisam de identidade/versionamento.
6. Memória não é autoridade absoluta.
7. Verificação deve poder ser independente.
8. Capacidades precisam de limites além da descrição.
9. Subagentes precisam de admission control.
10. Autonomia precisa ser proporcional ao risco.
11. Estado precisa de integridade e recuperação.
12. UNKNOWN precisa existir explicitamente.

## Resultado final

O candidato continua plausível, mas sua principal hipótese agora é mais precisa:

> **O ABS deve possuir um núcleo de controle estável e limitado, enquanto a estratégia de execução pode ser adaptativa e variável.**

Portanto, a adaptatividade não deve significar que o sistema pode redefinir livremente suas próprias regras fundamentais.

## O que o ataque NÃO demonstrou

Não demonstrou:
- superioridade sobre outras arquiteturas em benchmark;
- desempenho;
- custo;
- latência;
- confiabilidade real;
- escalabilidade real.

Esses pontos permanecem experimentais.

## Próxima fronteira

A próxima etapa correta não é adicionar mais mecanismos ao molde.

É construir o **menor experimento real possível** que teste:

1. objetivo persistente;
2. estado externo;
3. estratégia variável;
4. executor substituível;
5. observação;
6. verificação;
7. recuperação;
8. orçamento;
9. autorização;
10. complexidade mínima.

