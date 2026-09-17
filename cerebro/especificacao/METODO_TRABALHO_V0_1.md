# Método de Trabalho V0.2 — Abordagem Sênior Sistêmica

## Objetivo

Definir como o Projeto Absoluto deve pensar, pesquisar, decidir, construir, testar, operar, aprender e evoluir em qualquer área — não apenas em bugs ou código.

Este método é adaptativo. A profundidade deve ser proporcional ao risco, à incerteza, ao impacto, ao custo e à reversibilidade.

> Não executar apenas a tarefa visível. Entender o objetivo, o sistema, o contexto, as evidências, as restrições e o próximo ciclo antes de escolher a ação.

## 1. Princípios

### 1.1 Objetivo antes da solução

Identificar o resultado desejado, por que ele importa, quem é afetado, restrições, critérios de sucesso e o que não precisa ser resolvido agora.

Uma solicitação, erro, arquivo ou ideia pode ser sintoma de uma necessidade maior.

### 1.2 Sistema antes do componente

Antes de alterar uma parte, entender onde ela se encaixa, suas entradas e saídas, dependências, interfaces, consumidores, efeitos colaterais e relação com o objetivo maior.

### 1.3 Evidência antes de convicção

Separar:

- fato observado;
- dado medido;
- fonte;
- hipótese;
- inferência;
- decisão;
- opinião/preferência;
- desconhecido.

Hipótese plausível não é fato.

### 1.4 Inspeção antes de criação

Antes de criar arquivo, módulo, processo, API, automação ou estrutura:

1. procurar o que já existe;
2. entender seu contrato e finalidade;
3. identificar quem já usa;
4. verificar se pode ser corrigido ou estendido;
5. verificar equivalentes em outras camadas;
6. criar somente se houver necessidade real não atendida.

A falha anterior envolvendo `cerebro/ingestao.py` tornou esta regra concreta: o sistema existente deve ser descoberto antes de uma nova estrutura ser criada.

### 1.5 Pequenos ciclos, visão grande

Trabalhar em incrementos pequenos para obter feedback rápido, sem perder a visão arquitetural e os requisitos futuros.

Iteração não significa improvisação. Cada ciclo deve produzir valor ou evidência.

### 1.6 Aprendizado volta para o sistema

Experiência só vira ativo quando, conforme o caso, altera teste, código, documentação, requisito, arquitetura, processo, decisão, planejamento, checklist ou automação.

### 1.7 Ferramenta não é o projeto

GitHub, APIs, bancos, modelos, IDEs, bibliotecas e serviços são meios. Preservar dados, identidade, histórico, proveniência, contratos e possibilidade de migração.

---

## 2. Ciclo universal

```text
OBJETIVO
   ↓
CONTEXTO REAL
   ↓
INSPEÇÃO
   ↓
PESQUISA / EVIDÊNCIAS
   ↓
MODELO DO PROBLEMA
   ↓
HIPÓTESES / ALTERNATIVAS
   ↓
RISCOS / TRADE-OFFS
   ↓
DECISÃO
   ↓
MENOR AÇÃO ÚTIL
   ↓
EXECUÇÃO
   ↓
VERIFICAÇÃO
   ↓
VALIDAÇÃO REAL
   ↓
OBSERVAÇÃO
   ↓
APRENDIZADO
   ↓
ATUALIZAÇÃO DO SISTEMA
   ↓
PRÓXIMO CICLO
```

O ciclo pode voltar a qualquer etapa quando novas evidências mostrarem que o modelo, hipótese ou decisão estava errado ou incompleto.

---

## 3. Entendimento do objetivo

Antes de agir, responder o suficiente para orientar o trabalho:

```text
O que queremos mudar?
Por quê?
Para quem?
Em qual contexto?
Qual resultado esperamos?
Como saberemos que funcionou?
Quais são as restrições?
Qual é o custo de errar?
```

Não inventar requisitos silenciosamente quando uma incerteza for importante.

---

## 4. Inspeção do estado real

Inspecionar, conforme o caso:

- arquivos e repositórios;
- código e testes;
- documentos e histórico;
- APIs e integrações;
- dados;
- configurações e dependências;
- ambiente de execução;
- decisões anteriores;
- processos e limitações;
- recursos já disponíveis.

Pergunta central:

> Como o sistema realmente funciona hoje e qual é o ponto correto para esta necessidade?

Quando documentação, memória, plano e sistema real divergirem, a divergência é evidência e deve ser investigada.

---

## 5. Pesquisa sênior

Pesquisa não é acumular links. É reduzir uma incerteza que influencia uma decisão ou execução.

Escalonar conforme a necessidade:

```text
conhecimento existente
        ↓
inspeção local
        ↓
fontes primárias
        ↓
fontes técnicas reconhecidas
        ↓
comparação de alternativas
        ↓
experimento / prova
```

Para temas atuais, técnicos, críticos ou mutáveis, verificar fontes atualizadas.

A pesquisa deve produzir, quando pertinente:

- fatos;
- evidências;
- limitações;
- alternativas;
- riscos;
- implicações;
- lacunas;
- decisão ou próximo experimento.

Se ainda não existe informação suficiente, declarar a incerteza em vez de preencher a lacuna com suposição.

---

## 6. Modelo do problema

Quanto maior a complexidade, risco ou incerteza, mais importante externalizar o modelo.

Considerar:

- entradas e saídas;
- estados;
- dependências;
- interfaces;
- atores;
- dados;
- pontos de falha;
- observabilidade;
- efeitos colaterais;
- limites do sistema.

Perguntar se o problema está na camada correta. Um problema local pode ser consequência de uma decisão arquitetural, processo, dado ou requisito.

---

## 7. Hipóteses e alternativas

Não assumir que a primeira solução é a correta.

Para decisões relevantes, comparar alternativas por:

- benefício;
- custo;
- complexidade;
- risco;
- reversibilidade;
- dependências;
- manutenção;
- impacto futuro;
- compatibilidade com os princípios do projeto.

Quando um teste puder responder uma questão, preferir evidência a preferência.

---

## 8. Risco, trade-off e reversibilidade

Avaliar conforme o caso:

- risco técnico;
- segurança;
- dados;
- operação;
- dependências externas;
- manutenção;
- arquitetura;
- perda de informação;
- irreversibilidade.

Quanto mais difícil desfazer uma decisão, maior deve ser a evidência exigida.

Quando a incerteza for alta, preferir experimentos reversíveis.

Para sistemas de IA, riscos devem ser tratados continuamente durante o ciclo de vida, e não apenas no final.

---

## 9. Decisão explícita

Decisões relevantes devem registrar:

```text
DECISÃO:
CONTEXTO:
ALTERNATIVAS:
EVIDÊNCIAS:
TRADE-OFFS:
RISCOS:
MOTIVO:
O QUE FICOU DE FORA:
COMO VALIDAR:
CONDIÇÃO PARA REVISÃO:
```

Uma decisão pode ser provisória. Registrar o que faria a decisão mudar.

---

## 10. Menor ação útil

Depois de decidir, executar a menor ação capaz de produzir valor ou informação relevante.

Pode ser:

- protótipo;
- teste mínimo;
- integração pequena;
- migração limitada;
- experimento controlado;
- alteração isolada.

A menor ação útil não é necessariamente a menor alteração de código; é a menor ação que reduz uma incerteza ou produz valor significativo.

---

## 11. Verificação ≠ validação

### Verificação

> Construímos corretamente o que foi especificado?

Exemplos: testes, schema, lint, análise estática, invariantes, comparação de saída.

### Validação

> Construímos algo que resolve a necessidade no contexto real?

Exemplos: uso real, dados representativos, aceitação, cenário operacional, experimento.

Uma etapa importante só deve ser considerada suficientemente validada quando houver evidência apropriada ao seu risco.

---

## 12. Erros e mudança de perspectiva

Um erro é evidência sobre uma hipótese, não apenas obstáculo.

Ao falhar, investigar conforme pertinência:

1. código;
2. estrutura;
3. integração;
4. contrato;
5. ambiente;
6. dados;
7. arquitetura;
8. processo;
9. objetivo original.

Fluxo:

```text
FALHA
 ↓
REPRODUZIR
 ↓
EVIDÊNCIA
 ↓
HIPÓTESE
 ↓
MUDAR PERSPECTIVA
 ↓
TESTAR
 ↓
CORRIGIR
 ↓
VALIDAR
 ↓
APRENDER
```

Não mudar de perspectiva aleatoriamente. A mudança deve ser orientada pela evidência.

---

## 13. Evitar loops

Uma nova tentativa precisa apresentar uma diferença relevante:

- evidência nova;
- hipótese nova;
- perspectiva nova;
- mecanismo diferente;
- escopo diferente;
- dado diferente;
- condição ambiental diferente.

Se nada mudou, repetir provavelmente é loop.

Encerrar uma linha quando:

- hipótese foi confirmada e solução validada;
- hipótese foi refutada;
- estratégia falhou sem nova variável relevante;
- outra linha oferece mais informação;
- custo superou benefício esperado;
- depende de recurso externo;
- deve virar questão aberta.

Parar uma linha não significa abandonar o problema. Significa preservar o aprendizado e escolher outro caminho conscientemente.

---

## 14. Observar o resultado real

“Funcionou” não significa automaticamente “resolveu”.

Após executar, observar conforme o caso:

- comportamento real;
- métricas;
- logs;
- erros;
- desempenho;
- efeitos colaterais;
- manutenção;
- experiência de uso;
- impacto sobre outras partes.

Feedback curto e observável permite corrigir direção mais cedo.

---

## 15. Transformar experiência em conhecimento

Para eventos relevantes:

```text
EVENTO
 ↓
IMPACTO
 ↓
CONTEXTO
 ↓
HIPÓTESES
 ↓
TENTATIVAS
 ↓
EVIDÊNCIAS
 ↓
CAUSAS / FATORES CONTRIBUINTES
 ↓
CORREÇÃO
 ↓
VALIDAÇÃO
 ↓
APRENDIZADO
 ↓
AÇÃO PREVENTIVA
```

Não buscar apenas culpados ou uma única causa quando o fenômeno for sistêmico.

Registrar tentativas importantes para não repetir caminhos já descartados.

---

## 16. Atualizar o sistema com o aprendizado

```text
APRENDIZADO
 ├──→ TESTE
 ├──→ CÓDIGO
 ├──→ ARQUITETURA
 ├──→ DOCUMENTAÇÃO
 ├──→ REQUISITO
 ├──→ PROCESSO
 ├──→ DECISÃO
 ├──→ CHECKLIST
 ├──→ AUTOMAÇÃO
 └──→ NOVA PESQUISA
```

O objetivo é que o projeto fique melhor depois de cada ciclo, e não apenas que a tarefa atual seja encerrada.

---

## 17. Revisões proporcionais ao risco

Nem tudo precisa de burocracia.

### Baixo risco

```text
entender → executar → verificar
```

### Médio risco

```text
entender → inspecionar → pesquisar → testar → validar → registrar
```

### Alto risco

```text
objetivo
→ requisitos
→ pesquisa
→ alternativas
→ riscos
→ decisão
→ revisão
→ experimento
→ verificação
→ validação
→ revisão
→ execução
→ monitoramento
→ aprendizado
```

A formalidade deve ser proporcional ao impacto, incerteza, custo e irreversibilidade.

---

## 18. Pesquisa, execução e aprendizado são um único sistema

```text
PESQUISA
   ↓
DECISÃO
   ↓
EXECUÇÃO
   ↓
RESULTADO
   ↓
NOVA EVIDÊNCIA
   ↓
PESQUISA MELHOR
   ↓
NOVA DECISÃO
```

A execução também pode ser um experimento quando produz evidência sobre uma hipótese.

---

## 19. Trabalho orientado por informação

Não pensar apenas em atividades:

```text
pesquisar → programar → testar → documentar
```

Perguntar:

```text
Qual pergunta precisamos responder?
Qual evidência falta?
Qual ação produz essa evidência?
Qual decisão ela permite?
Qual resultado precisamos alcançar?
```

Isso reduz trabalho que gera artefatos sem aumentar conhecimento ou valor.

---

## 20. IA no processo

Quando uma IA participar:

- separar geração de verificação;
- registrar fontes quando pesquisa externa for relevante;
- explicitar incertezas;
- testar saídas importantes;
- não tratar texto plausível como evidência;
- preservar decisões e motivos;
- manter possibilidade de substituir o modelo;
- usar erros para melhorar contexto, processo, ferramenta ou avaliação.

IA é participante do processo, não autoridade automática.

---

## 21. Autonomia operacional

Quando o próximo passo estiver claramente determinado pelo objetivo, evidências e estado real, executar sem interromper o fluxo para pedir autorização sobre detalhes operacionais.

Parar para decisão humana quando houver:

- escolha estratégica não inferível com segurança;
- autorização necessária;
- custo ou risco relevante não autorizado;
- recurso externo inexistente;
- informação essencial que só o usuário possui;
- conflito entre objetivos;
- decisão irreversível ou de alto impacto.

Autonomia operacional reduz interrupções; não substitui a agência humana.

---

## 22. Regra operacional antes de cada ação relevante

```text
1. Qual é o objetivo?
2. O que realmente existe hoje?
3. O que sei e o que estou supondo?
4. Que evidência falta?
5. Preciso pesquisar?
6. Já existe algo que devo reutilizar?
7. Quais alternativas importam?
8. Quais riscos e trade-offs importam?
9. Qual é a menor ação útil?
10. Como vou verificar?
11. Como vou validar no contexto real?
12. O que farei se falhar?
13. Como evitarei repetir um loop?
14. O que devo registrar?
15. O aprendizado precisa alterar o sistema?
```

Tarefas simples não exigem responder tudo explicitamente. Isso é um modelo mental, não um formulário obrigatório.

---

## 23. Critério de qualidade

Uma etapa está suficientemente concluída, proporcionalmente ao risco, quando:

```text
OBJETIVO ENTENDIDO
      +
ESTADO REAL INSPECIONADO
      +
EVIDÊNCIA SUFICIENTE
      +
DECISÃO COERENTE
      +
EXECUÇÃO
      +
VERIFICAÇÃO
      +
VALIDAÇÃO
      +
APRENDIZADO REGISTRADO
      +
PRÓXIMO PASSO CLARO
```

O objetivo é maximizar valor e aprendizado por ciclo, não maximizar quantidade de tarefas executadas.

---

## 24. Evolução do próprio método

O método também é parte do sistema e pode estar errado.

Se a experiência mostrar que uma regra é inadequada:

```text
observar
→ formular hipótese sobre o método
→ testar
→ avaliar
→ registrar
→ atualizar o método
→ aplicar no próximo ciclo
```

O Projeto Absoluto deve aprender não apenas sobre o que constrói, mas também sobre como constrói.

---

## 25. Aplicação ao Projeto Absoluto

Este método orienta o Cérebro, o Sistema e futuras áreas do Projeto Absoluto.

Prioridades permanentes:

1. objetivo antes da solução;
2. sistema antes do componente;
3. inspeção antes da criação;
4. evidência antes de convicção;
5. pesquisa proporcional ao problema;
6. alternativas antes de decisões relevantes;
7. risco e reversibilidade antes de mudanças difíceis de desfazer;
8. pequenos ciclos com visão arquitetural ampla;
9. verificação e validação separadas;
10. erro como evidência;
11. mudança de perspectiva quando necessário;
12. critérios explícitos para parar;
13. validação no contexto real;
14. aprendizado transformado em ativo do sistema;
15. revisão proporcional ao risco;
16. independência de ferramentas e plataformas;
17. autonomia operacional com decisões humanas preservadas;
18. evolução contínua do próprio método.

### Referências-base consultadas

- NASA Systems Engineering Handbook e processos de engenharia de sistemas.
- NASA Lessons Learned / Knowledge Services.
- NIST AI Risk Management Framework.
- Google SRE — cultura de postmortem e aprendizado com falhas.
- Martin Fowler — desenvolvimento iterativo, feedback e redução de ciclo.

Essas referências são fundamentos de pesquisa, não regras absolutas. O método deve ser adaptado ao contexto do Projeto Absoluto e continuar sendo validado pela experiência real.
