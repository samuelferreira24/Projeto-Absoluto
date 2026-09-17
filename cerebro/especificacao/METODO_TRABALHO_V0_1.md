# Método de Trabalho V0.2 — Abordagem Sênior Sistêmica

## Objetivo

Definir como o Projeto Absoluto deve pensar, pesquisar, decidir, construir, testar, operar, aprender e evoluir em diferentes tipos de trabalho — não apenas na correção de bugs.

O método deve funcionar para pesquisa, planejamento, arquitetura, código, dados, documentos, automação, integração, experimentos, decisões, gestão de riscos e problemas ainda não conhecidos.

O princípio é simples:

> Não executar apenas a tarefa visível. Entender o sistema, o objetivo, as restrições, as evidências e o próximo ciclo antes de escolher a ação.

O método não é uma sequência rígida. É um sistema de decisão adaptativo. A profundidade de cada etapa deve ser proporcional ao risco, à incerteza, ao custo e ao impacto.

---

## 1. Princípios centrais

### 1.1 Objetivo antes da solução

Antes de escolher uma solução, identificar:

- qual resultado precisa ser alcançado;
- por que esse resultado importa;
- quem ou o que será afetado;
- quais restrições existem;
- como saberemos que deu certo;
- o que não precisa ser resolvido agora.

Uma solicitação, arquivo, erro ou ideia pode ser apenas um sintoma de uma necessidade maior.

### 1.2 Sistema antes do componente

Não analisar uma parte isoladamente quando ela depende de outras partes.

Perguntar:

- onde isso se encaixa;
- o que já existe;
- quem depende disso;
- de onde vêm os dados;
- para onde vão os resultados;
- quais contratos e interfaces existem;
- quais efeitos podem surgir fora do componente analisado.

### 1.3 Evidência antes de convicção

Distinguir explicitamente:

- fato observado;
- dado medido;
- fonte externa;
- hipótese;
- inferência;
- decisão;
- opinião ou preferência;
- informação ainda desconhecida.

Não transformar uma hipótese em fato apenas porque parece plausível.

### 1.4 Reutilizar antes de duplicar

Antes de criar qualquer coisa:

1. procurar o mecanismo existente;
2. entender sua finalidade e contrato;
3. verificar se pode ser estendido;
4. verificar se já existe algo equivalente em outra camada;
5. somente então criar algo novo.

Isso vale para arquivos, módulos, APIs, dados, processos, documentação, automações e conhecimento.

### 1.5 Pequenos ciclos, visão grande

Trabalhar em ciclos pequenos o suficiente para produzir feedback rápido, mas sempre verificando o efeito sobre a arquitetura e o objetivo maior.

Uma pequena implementação não deve criar uma arquitetura pequena demais para o futuro.

Iteração não significa improvisação: cada ciclo deve produzir evidência utilizável.

### 1.6 Aprendizado precisa voltar ao sistema

Uma experiência só se torna ativo do projeto quando o aprendizado é registrado e, quando aplicável, incorporado a:

- código;
- teste;
- documentação;
- requisito;
- arquitetura;
- processo;
- checklist;
- decisão;
- planejamento;
- treinamento ou automação.

NASA descreve um ciclo semelhante de coletar, registrar, disseminar e aplicar lições aprendidas. citeturn0search0turn0search10

---

## 2. Ciclo universal de trabalho

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
OPÇÕES / HIPÓTESES
   ↓
RISCOS E TRADE-OFFS
   ↓
DECISÃO
   ↓
MENOR AÇÃO ÚTIL
   ↓
EXECUÇÃO
   ↓
VERIFICAÇÃO
   ↓
VALIDAÇÃO NO CONTEXTO REAL
   ↓
OBSERVAÇÃO DO RESULTADO
   ↓
APRENDIZADO
   ↓
ATUALIZAÇÃO DO SISTEMA
   ↓
PRÓXIMO CICLO
```

Esse ciclo pode voltar para qualquer etapa quando uma evidência mostrar que a hipótese ou o modelo estava errado.

A NASA utiliza ciclos de vida, pontos de decisão e revisões técnicas para acompanhar progresso, trade-offs, fraquezas, riscos e prontidão. citeturn0search1turn0search6turn0search7

---

## 3. Etapa 1 — Entender o objetivo

Antes de agir, responder o suficiente para orientar o trabalho:

```text
O que queremos mudar?
Por quê?
Para quem?
Em qual contexto?
Qual é o resultado esperado?
Como mediremos o resultado?
Quais são as restrições?
Qual é o custo de errar?
```

Se o objetivo estiver ambíguo, não inventar requisitos silenciosamente. Inferir apenas o que for seguro e registrar as incertezas relevantes.

---

## 4. Etapa 2 — Inspecionar antes de criar

A inspeção deve preceder a implementação sempre que houver algo existente que possa afetar a solução.

Inspecionar, conforme o caso:

- arquivos;
- repositórios;
- código;
- APIs;
- dados;
- documentos;
- histórico;
- decisões anteriores;
- testes;
- configurações;
- dependências;
- processos;
- limitações do ambiente;
- recursos já disponíveis.

A pergunta não é apenas “onde devo colocar isso?”.

É:

> “Como o sistema já funciona e qual é o ponto correto para esta necessidade?”

O erro anterior com `cerebro/ingestao.py` demonstrou essa regra na prática.

---

## 5. Etapa 3 — Pesquisar com profundidade proporcional ao problema

Pesquisa sênior não significa pesquisar indefinidamente.

A pesquisa deve responder uma pergunta operacional e terminar quando houver informação suficiente para uma decisão responsável.

### 5.1 Escalonamento

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
experimento/prova
```

Quando o tema for atual, técnico, crítico ou sujeito a mudanças, pesquisar fontes atualizadas antes de afirmar fatos.

Quando uma fonte secundária contradizer uma fonte primária, investigar a divergência em vez de escolher automaticamente uma delas.

### 5.2 Pesquisa deve produzir

- fatos relevantes;
- limitações;
- alternativas;
- evidências;
- riscos;
- implicações para o projeto;
- lacunas de conhecimento;
- recomendação técnica apenas quando a decisão exigir uma escolha.

A pesquisa não deve virar uma coleção de links sem decisão ou aplicação.

---

## 6. Etapa 4 — Construir um modelo do problema

Antes de alterar o sistema, representar mental ou explicitamente:

- entradas;
- processamento;
- saídas;
- dependências;
- interfaces;
- estados;
- atores;
- riscos;
- pontos de falha;
- observabilidade;
- efeitos colaterais.

Quanto maior o impacto ou a incerteza, mais importante é externalizar o modelo.

---

## 7. Etapa 5 — Gerar hipóteses e alternativas

Não assumir que a primeira solução é a solução correta.

Para problemas relevantes, formular alternativas suficientes para descobrir diferenças reais.

Para cada alternativa, considerar:

- benefício esperado;
- custo;
- complexidade;
- reversibilidade;
- dependências;
- risco;
- manutenção;
- impacto futuro;
- compatibilidade com os princípios do projeto.

Não comparar alternativas por preferência pessoal quando uma evidência ou teste puder responder à questão.

---

## 8. Etapa 6 — Risco, trade-offs e reversibilidade

Toda decisão relevante deve considerar o que pode dar errado.

Classificar, conforme necessário:

- risco técnico;
- risco de segurança;
- risco de dados;
- risco operacional;
- risco de dependência externa;
- risco de manutenção;
- risco de arquitetura;
- risco de perda de informação;
- risco de irreversibilidade.

Preferir experimentos reversíveis quando a incerteza for alta.

Decisões difíceis de reverter exigem mais evidência do que decisões fáceis de desfazer.

Para sistemas de IA, o NIST AI RMF organiza a gestão contínua em Govern, Map, Measure e Manage, reforçando que risco deve ser tratado ao longo de todo o ciclo de vida, e não somente no final. citeturn0search2turn0search4

---

## 9. Etapa 7 — Decidir explicitamente

Quando houver uma decisão relevante, registrar:

```text
DECISÃO:
CONTEXTO:
ALTERNATIVAS:
EVIDÊNCIAS:
TRADE-OFFS:
RISCOS:
POR QUE ESTA OPÇÃO:
O QUE FICOU DE FORA:
COMO VALIDAR:
CONDIÇÃO PARA REVISÃO:
```

Uma decisão pode ser provisória. Nesse caso, registrar o que poderá fazê-la mudar.

Não confundir “decisão atual” com “verdade permanente”.

---

## 10. Etapa 8 — Executar a menor ação que gere aprendizado ou valor

Depois da decisão, evitar grandes mudanças simultâneas quando uma ação menor puder testar a hipótese.

Preferir:

- protótipo;
- teste mínimo;
- integração pequena;
- migração limitada;
- experimento controlado;
- mudança isolada.

A menor ação útil não é necessariamente a menor alteração de código. É a menor ação capaz de produzir evidência ou valor relevante.

---

## 11. Etapa 9 — Verificar e validar são coisas diferentes

### Verificação

Pergunta:

> “Construímos corretamente o que foi especificado?”

Exemplos:

- teste unitário;
- teste de integração;
- validação de schema;
- lint;
- análise estática;
- comparação de saída;
- verificação de invariantes.

### Validação

Pergunta:

> “Construímos algo que realmente resolve a necessidade no contexto em que será usado?”

Exemplos:

- uso real;
- teste com dados representativos;
- avaliação do usuário;
- cenário operacional;
- experimento;
- teste de aceitação.

A engenharia de sistemas da NASA trata verificação e validação como atividades relacionadas, mas distintas, e recomenda planejar como cada requisito será verificado e como a solução será validada. citeturn0search1turn0search3turn0search60

---

## 12. Etapa 10 — Quando algo falhar, mudar a perspectiva

Um erro é evidência sobre uma hipótese, não apenas um obstáculo.

Investigar:

1. código;
2. estrutura;
3. integração;
4. contrato;
5. ambiente;
6. dados;
7. arquitetura;
8. processo;
9. objetivo original.

A nona perspectiva é importante: às vezes estamos tentando executar corretamente uma coisa que não deveria ser feita daquela maneira.

O fluxo é:

```text
FALHA
 ↓
REPRODUZIR
 ↓
OBSERVAR EVIDÊNCIA
 ↓
IDENTIFICAR HIPÓTESE
 ↓
MUDAR PERSPECTIVA SE NECESSÁRIO
 ↓
TESTAR
 ↓
CORRIGIR
 ↓
VALIDAR
```

---

## 13. Etapa 11 — Evitar loops

Não repetir a mesma estratégia apenas porque ainda não funcionou.

Uma nova tentativa precisa apresentar pelo menos uma diferença relevante:

- evidência nova;
- hipótese nova;
- perspectiva nova;
- mecanismo novo;
- escopo diferente;
- dado diferente;
- condição de ambiente diferente.

Se nada mudou, provavelmente não há nova informação a ser obtida.

### Critérios de parada

Parar uma linha de investigação quando:

- a hipótese foi confirmada e validada;
- a hipótese foi refutada;
- a estratégia falhou sem nova variável relevante;
- outra linha oferece maior valor informativo;
- o custo superou o benefício esperado;
- existe dependência externa;
- existe uma questão aberta que precisa ser registrada.

Parar não significa abandonar o problema. Significa preservar o aprendizado e escolher conscientemente o próximo caminho.

---

## 14. Etapa 12 — Observar o resultado real

Depois da execução, não assumir que “funcionou” significa “resolveu”.

Observar:

- comportamento real;
- métricas;
- logs;
- erros;
- desempenho;
- efeitos colaterais;
- manutenção;
- experiência de uso;
- impacto sobre outras partes do sistema.

Em sistemas complexos, feedback curto e observável permite corrigir direção mais cedo. citeturn0search15turn0search18

---

## 15. Etapa 13 — Transformar falhas e sucessos em conhecimento

Para problemas relevantes, registrar:

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

Não procurar apenas “quem errou” ou uma causa única quando o problema é sistêmico.

Google SRE utiliza postmortems para registrar impacto, ações, causas e medidas de prevenção, com foco em aprendizado e redução de recorrência. citeturn0search5turn0search14

---

## 16. Etapa 14 — Atualizar o próprio sistema

O aprendizado deve retornar ao projeto.

Possíveis destinos:

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

NASA trata lições aprendidas como conhecimento que deve ser aplicado de volta em práticas, processos, políticas e procedimentos. citeturn0search0turn0search10

---

## 17. Revisões técnicas e pontos de decisão

Nem todo trabalho precisa de uma revisão formal.

Quanto maior o impacto, irreversibilidade, risco ou complexidade, maior deve ser a formalidade da revisão.

Possíveis pontos de revisão:

```text
IDEIA
 ↓
HIPÓTESE
 ↓
PROVA / EXPERIMENTO
 ↓
DECISÃO DE ARQUITETURA
 ↓
IMPLEMENTAÇÃO
 ↓
INTEGRAÇÃO
 ↓
VALIDAÇÃO
 ↓
OPERAÇÃO
```

Em cada ponto, perguntar:

- o objetivo continua válido;
- as evidências mudaram;
- os riscos estão aceitáveis;
- a solução continua coerente com o sistema;
- devemos continuar, alterar, pausar ou encerrar.

NASA utiliza revisões técnicas para avaliar progresso, trade-offs, fraquezas, riscos e prontidão para as próximas etapas. citeturn0search6turn0search13

---

## 18. Escalonamento da profundidade

Não aplicar a mesma burocracia a tudo.

### Baixo risco / baixo impacto

```text
entender → executar → verificar
```

### Médio risco / impacto

```text
entender → inspecionar → pesquisar → testar → validar → registrar
```

### Alto risco / alto impacto

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

A formalidade deve ser adaptada ao problema, não imposta indiscriminadamente. A própria engenharia de sistemas da NASA prevê tailoring/customização dos processos conforme o projeto. citeturn0search7turn0search13

---

## 19. Pesquisa, execução e aprendizado formam um único ciclo

Não separar pesquisa e execução como mundos independentes.

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

A execução também é instrumento de pesquisa quando produz evidência sobre uma hipótese.

---

## 20. O trabalho deve ser orientado por informação, não por atividade

Evitar pensar apenas:

```text
pesquisar → programar → testar → documentar
```

Preferir:

```text
qual pergunta precisamos responder?
qual evidência falta?
qual ação produz essa evidência?
qual decisão essa evidência permite tomar?
qual resultado precisamos alcançar?
```

Isso reduz trabalho que produz documentos, código ou tarefas sem aumentar conhecimento ou valor.

---

## 21. Estado real sempre vence modelo mental

Quando a documentação, memória, expectativa e sistema real divergirem, investigar a divergência.

Não assumir automaticamente que:

- a documentação está correta;
- o código está correto;
- a memória está correta;
- a hipótese está correta;
- o plano continua adequado.

A divergência é informação.

---

## 22. Independência de ferramenta

Ferramentas são meios, não o projeto.

GitHub, APIs, bancos de dados, IDEs, modelos de IA, bibliotecas, serviços e plataformas devem ser tratados como componentes substituíveis quando possível.

Decisões importantes devem preservar:

- dados essenciais;
- identidade própria;
- histórico;
- proveniência;
- contratos;
- possibilidade de migração;
- conhecimento sobre como reconstruir o sistema.

---

## 23. IA como participante do processo, não como autoridade automática

Quando uma IA participar do trabalho:

- separar geração de verificação;
- registrar fontes quando pesquisa externa for relevante;
- explicitar incertezas;
- testar saídas importantes;
- não tratar texto plausível como evidência;
- preservar decisões e seus motivos;
- manter possibilidade de substituição do modelo;
- usar o erro da IA como dado para melhorar processo, contexto, ferramenta ou avaliação.

A governança deve acompanhar todo o ciclo de vida e não apenas a etapa final. O NIST AI RMF enfatiza gestão contínua de riscos e responsabilidades transversais de governança. citeturn0search2

---

## 24. O que significa trabalhar como um profissional sênior

Neste projeto, “sênior” não significa apenas conhecer mais ferramentas.

Significa conseguir:

- enxergar o sistema antes da tarefa;
- distinguir sintoma de problema;
- formular perguntas melhores;
- buscar evidência relevante;
- reconhecer incerteza;
- comparar alternativas;
- antecipar consequências;
- escolher o nível correto de complexidade;
- evitar duplicação;
- reduzir ciclos de tentativa e erro;
- validar no mundo real;
- registrar decisões;
- transformar experiência em método;
- mudar de estratégia quando os dados exigirem;
- saber quando parar;
- preservar a capacidade de evolução futura.

---

## 25. Regra operacional permanente

Antes de cada ação relevante, perguntar:

```text
1. Qual é o objetivo?
2. O que realmente existe hoje?
3. O que eu sei e o que estou supondo?
4. Que evidência falta?
5. Preciso pesquisar?
6. Já existe algo que devo reutilizar?
7. Quais são as alternativas?
8. Quais riscos e trade-offs importam?
9. Qual é a menor ação que produz valor ou informação?
10. Como vou verificar?
11. Como vou validar no contexto real?
12. O que farei se falhar?
13. Como evitarei repetir um loop?
14. O que devo registrar para o próximo ciclo?
15. O aprendizado precisa alterar alguma parte do sistema?
```

Não é necessário responder todas as perguntas explicitamente em tarefas simples. Elas formam o modelo mental de trabalho.

---

## 26. Regra especial para erros e bugs

O método anterior de investigação continua válido dentro deste método geral:

```text
OBSERVAR
   ↓
REPRODUZIR
   ↓
HIPÓTESE
   ↓
TESTE
   ↓
EVIDÊNCIA
   ↓
MUDANÇA DE PERSPECTIVA
   ↓
CORREÇÃO
   ↓
VALIDAÇÃO
   ↓
APRENDIZADO
```

Mas bugs são apenas um caso particular. O mesmo princípio deve ser usado para decisões, arquitetura, pesquisa, planejamento e execução.

---

## 27. Regra de continuidade autônoma

Quando o próximo passo for claramente determinado pelo objetivo, pelas evidências e pelo estado real do sistema, executar sem interromper o fluxo apenas para pedir autorização sobre detalhes operacionais.

Parar e pedir decisão humana quando houver:

- escolha de produto ou direção estratégica que não possa ser inferida com segurança;
- autorização necessária;
- custo ou risco relevante não autorizado;
- acesso externo inexistente;
- informação essencial que só o usuário possui;
- conflito entre objetivos;
- decisão irreversível ou de alto impacto.

A autonomia operacional não elimina a agência humana. Ela reduz interrupções desnecessárias e devolve ao usuário as decisões que realmente são dele.

---

## 28. Critério final de qualidade

Uma etapa não deve ser considerada concluída apenas porque uma tarefa foi executada.

Ela está suficientemente concluída quando, proporcionalmente ao risco:

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

O objetivo do método é maximizar valor e aprendizado por ciclo, não maximizar quantidade de tarefas executadas.

---

## 29. Aplicação ao Projeto Absoluto

Este método passa a orientar o trabalho do Cérebro, do Sistema e das futuras áreas do Projeto Absoluto.

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

O método também deve evoluir. Se a experiência mostrar que uma regra está inadequada, ela deve ser tratada como hipótese do próprio sistema de trabalho: observar, testar, avaliar, registrar e atualizar.
