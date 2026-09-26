# MOLDE CANDIDATO ABS — V0

**Status:** CANDIDATO DE PESQUISA — NÃO É ARQUITETURA OFICIAL  
**Origem:** auditoria individual + auditoria cruzada das Pesquisas 01 e 02.  
**Objetivo:** transformar os mecanismos sobreviventes em uma hipótese arquitetural mínima e testável.

## 1. Princípio central

O ABS não deve ser definido como:
- um modelo;
- um agente único;
- uma interface;
- um framework;
- um workflow;
- um sistema multiagente;
- um fornecedor.

O ABS deve ser capaz de **controlar diferentes formas de execução sob uma autoridade comum**.

## 2. Núcleo conceitual

```
IMPERADOR
   ↓
AUTORIDADE / POLÍTICAS
   ↓
OBJETIVO
   ↓
ESTADO
   ↓
ESTRATÉGIA
   ↓
SELEÇÃO DA EXECUÇÃO
   ├── DIRETA
   ├── WORKFLOW
   ├── AGENTE
   └── MULTIAGENTE
   ↓
EXECUTOR
   ├── MODELO
   ├── FERRAMENTA
   └── AMBIENTE
   ↓
AÇÃO
   ↓
OBSERVAÇÃO / EVIDÊNCIA
   ↓
VERIFICAÇÃO
   ↓
ESTADO ATUALIZADO
   ├── CONCLUÍDO
   ├── REPLANEJAR
   ├── RECUPERAR
   ├── PEDIR AUTORIZAÇÃO
   └── UNKNOWN
```

## 3. O que é invariável

### I1 — Autoridade
A autoridade não pertence ao modelo.

### I2 — Identidade da execução
A execução deve continuar identificável mesmo quando estratégia, modelo ou executor mudam.

### I3 — Objetivo
O objetivo precisa existir como estado controlável fora do modelo.

### I4 — Estado
A continuidade não pode depender somente do contexto interno do LLM.

### I5 — Observação
A ação deve produzir observação/evidência.

### I6 — Verificação
O sistema precisa poder avaliar se o resultado satisfaz o objetivo.

### I7 — Recuperação
Falha deve possuir política própria, não apenas retry cego.

### I8 — Limites
Tempo, custo, ações e autonomia precisam de orçamento/política.

### I9 — Substituibilidade
Modelos, ferramentas, executores e interfaces devem poder ser trocados sem redefinir o objetivo.

## 4. O que é variável

- modelo;
- número de modelos;
- planner;
- workflow;
- agentes;
- número de agentes;
- ferramenta;
- estratégia;
- ambiente;
- memória;
- interface;
- nível de autonomia;
- paralelização;
- verificador.

## 5. Princípio de complexidade elástica

A arquitetura deve usar a menor estrutura suficiente para a tarefa.

Exemplo:

### Tarefa simples
```
objetivo → modelo/ferramenta → resultado → verificação
```

### Tarefa estruturada
```
objetivo → plano → workflow → execução → verificação
```

### Tarefa aberta
```
objetivo → agente → ferramentas → observação → replanning
```

### Tarefa complexa/paralelizável
```
objetivo → supervisor → especialistas → agregação → verificação
```

Não há obrigação de utilizar o caminho mais complexo.

## 6. Contexto

O contexto deve ser construído dinamicamente.

Não colocar automaticamente tudo que existe no sistema dentro do prompt.

Deve existir separação conceitual entre:
- estado;
- memória;
- histórico;
- evidência;
- contexto de trabalho;
- instruções;
- skills;
- ferramentas disponíveis.

## 7. Capacidades

Ferramentas devem ser tratadas como capacidades com contratos claros.

Cada capacidade deve possuir, conforme aplicável:
- identidade;
- escopo;
- entradas;
- saída;
- efeitos;
- riscos;
- autorização;
- custo;
- timeout;
- erros;
- evidência;
- verificação.

## 8. Estratégia

A estratégia não deve ser confundida com o objetivo.

O sistema deve poder trocar de estratégia quando:
- a estratégia falhar;
- o ambiente mudar;
- surgir nova informação;
- o custo exceder limite;
- o risco aumentar;
- uma capacidade desaparecer;
- o objetivo permanecer, mas o caminho deixar de ser válido.

## 9. Agentes e especialistas

Agentes especializados são recursos controlados.

Não recebem autoridade global automaticamente.

Quando delegados, devem receber contrato com:
- objetivo;
- escopo;
- restrições;
- recursos;
- orçamento;
- resultado esperado;
- evidências;
- autoridade concedida.

## 10. Verificação

Verificação deve ocorrer em pontos proporcionais ao risco.

Não é necessário verificar tudo da mesma maneira.

Para ações simples:
- verificação leve.

Para ações importantes:
- pré-verificação;
- execução;
- pós-verificação.

Para ações irreversíveis ou de alto risco:
- política de autorização humana pode ser necessária.

## 11. Recovery

Recovery deve distinguir:
- retry seguro;
- retry com mudança;
- replanejamento;
- troca de executor;
- troca de modelo;
- troca de ferramenta;
- rollback;
- intervenção humana;
- abandono.

Retry infinito é proibido como mecanismo de recuperação.

## 12. Control Plane

O Control Plane deve controlar:
- objetivos;
- estado;
- políticas;
- estratégia;
- orçamento;
- autorização;
- seleção de execução;
- eventos;
- recuperação;
- auditoria.

Ele não precisa executar cada microação.

## 13. Teste obrigatório antes de arquitetura oficial

Este molde ainda precisa ser implementado na menor forma possível e testado contra:

1. tarefa simples;
2. pesquisa;
3. pesquisa + execução;
4. programação;
5. tarefa longa;
6. falha de ferramenta;
7. modelo fraco;
8. troca de modelo;
9. múltiplos especialistas;
10. mudança de objetivo;
11. autorização humana;
12. recuperação;
13. contexto limitado;
14. ferramenta desconhecida;
15. estratégia errada;
16. execução concorrente;
17. corrupção de estado;
18. custo excedido;
19. tarefa nunca vista;
20. falha do próprio verificador.

## 14. Hipótese principal

> Um runtime de controle orientado por objetivos e estado, com estratégia adaptável e execução selecionável, pode conter agentes, workflows, modelos e ferramentas sem depender de nenhum deles como molde absoluto.

## 15. O que ainda não sabemos

- se o runtime será simples o suficiente;
- quanto overhead será criado;
- qual parte deve ser determinística;
- qual parte pode ser agentiva;
- como selecionar estratégias;
- como medir confiança;
- como evitar loops;
- como governar escala;
- como impedir crescimento excessivo de complexidade.

## 16. Regra

Este documento é um **molde candidato**.

Não autoriza:
- refatoração geral;
- implementação completa;
- escolha de framework;
- escolha de modelo;
- merge;
- alteração da arquitetura oficial.

A próxima etapa correta é **experimento mínimo controlado**, não construção total.
