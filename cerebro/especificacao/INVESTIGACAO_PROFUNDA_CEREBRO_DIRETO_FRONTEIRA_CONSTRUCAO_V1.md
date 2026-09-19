# INVESTIGAÇÃO PROFUNDA — CÉREBRO DIRETO E FRONTEIRA DE CONSTRUÇÃO
## 2026-09-19

## 1. NOVA EVIDÊNCIA

A Pull Request #1 do repositório Sistema permanece **aberta, draft e não mesclada**.

Título:
`feat: permitir comunicação direta com o Cérebro sem Termux`

Base:
`main @ 57d55daf`

Head:
`cerebro-direct-bridge @ 92196817`

A PR possui 3 commits e altera somente `index.html`, com 103 linhas adicionadas no estado final.

### Consequência histórica

A tentativa de ligação direta App ↔ Cérebro deve ser classificada como:

**IMPLEMENTADA EM BRANCH EXPERIMENTAL + ITERADA + NÃO INTEGRADA À MAIN.**

Não deve ser classificada como capacidade consolidada do Sistema.

---

## 2. O FLUXO REAL DO EXPERIMENTO

O código da PR mostra:

```
Cérebro
   │
   │ /v1/trabalho/proximo
   ▼
App
   │
   │ capacidade = inferencia
   ▼
chamarMotor(...)
   │
   ▼
resultado
   │
   │ POST /v1/trabalho/{id}/resultado
   ▼
Cérebro
```

O App:
- consulta trabalhos por polling;
- aceita inicialmente somente `inferencia`;
- usa o próprio motor para executar;
- devolve sucesso ou erro;
- mantém o canal opcional;
- continua funcionando se o Cérebro estiver indisponível.

---

## 3. O QUE O EXPERIMENTO RESOLVE

Ele separa duas coisas que antes estavam acopladas:

**Ponte Termux** ≠ **comunicação App ↔ Cérebro**.

A comunicação pode ocorrer diretamente entre App e um endpoint do Cérebro.

Isso é uma descoberta arquitetural importante.

---

## 4. O QUE O EXPERIMENTO NÃO RESOLVE

O App continua sendo o executor da capacidade.

Portanto:

```
Cérebro não ganhou automaticamente a capacidade de inferência.
Cérebro ganhou a capacidade de ENFILEIRAR/ORQUESTRAR trabalho.
App continuou fornecendo o motor.
```

Isto reforça uma distinção que já apareceu no histórico:

**orquestração ≠ inteligência do motor.**

---

## 5. NOVA DESCOBERTA SOBRE O TERMO “DOIS CÉREBROS”

O experimento histórico sugere uma topologia mais precisa:

```
CÉREBRO
  │
  ├── estado / trabalho / coordenação
  │
  ▼
ADAPTER
  │
  ▼
APP
  │
  ├── motor
  ├── interface
  └── capacidades locais
```

Portanto, a ponte entre cérebros não precisa significar sincronização total de memória.

Pode ser uma **interface de capacidade**.

Essa hipótese deve ser preservada para o futuro ABS, mas ainda não deve ser transformada em arquitetura definitiva.

---

## 6. PROBLEMA DE SEGURANÇA IDENTIFICADO

O código permite configurar endpoint e token por:
- query string;
- localStorage;
- chamada JavaScript.

Isso é conveniente para experimento, mas cria questões que precisam ser investigadas antes de qualquer reutilização:

- exposição do token em URL;
- persistência local do token;
- origem/CORS;
- autenticação real do servidor;
- replay;
- autorização de capacidades;
- identidade do App;
- identidade do Cérebro;
- escopo do token;
- execução de trabalhos não autorizados.

Não significa que o experimento esteja “errado”; significa que ele não pode ser promovido diretamente para núcleo de um sistema de controle sem uma camada de segurança revisada.

---

## 7. NOVA EVIDÊNCIA SOBRE A FORMA DE DESENVOLVIMENTO

A sequência histórica agora apresenta:

```
PONTE TERMUX
   ↓
PONTE LOCAL
   ↓
EXPERIMENTAÇÃO SHIZUKU
   ↓
ADAPTER DIRETO APP ↔ CÉREBRO
```

Isso mostra que o problema de integração foi atacado por múltiplas soluções, não por uma única arquitetura.

Isso é exatamente o tipo de patrimônio que o Mini-Cérebro precisa preservar:

**problema → tentativa A → limitações → tentativa B → tentativa C → descoberta.**

---

## 8. STATUS DA INVESTIGAÇÃO HISTÓRICA

A investigação já recuperou:

- árvore do repositório;
- histórico de commits;
- evolução de arquivos;
- memória;
- coleta;
- busca;
- motor;
- executor;
- governança;
- orquestração;
- ponte;
- continuidade;
- Termux;
- Android;
- Shizuku/RISH;
- interface;
- PWA/Capacitor;
- tentativa de motor local;
- tentativa de comunicação direta;
- branch experimental;
- PR;
- sequência de correções;
- publicação GitHub Pages.

A recuperação ainda não permite afirmar todos os resultados reais de execução.

---

## 9. FRONTEIRA ATUAL

Chegamos a uma mudança de fase.

A investigação histórica principal já não está procurando “mais componentes” indiscriminadamente.

Agora precisamos fechar três mapas:

### MAPA 1 — O que já foi descoberto
Conhecimento histórico.

### MAPA 2 — O que ainda não foi descoberto
Lacunas históricas.

### MAPA 3 — O que o ABS atual precisa
Necessidades atuais.

Somente a interseção dos três poderá definir o que merece construção.

---

## 10. PRÓXIMA INVESTIGAÇÃO

Antes de criar qualquer componente, investigar:

### A. Mini-Cérebro
- qual é a unidade mínima de conhecimento histórico;
- como preservar evidência;
- como preservar versões;
- como ligar código a experimento;
- como representar conflitos;
- como recuperar causalidade;
- como consultar Git;
- como evitar transformar inferência em fato.

### B. Dois Cérebros
- contrato de comunicação;
- capacidade vs mensagem;
- autenticação;
- autorização;
- identidade;
- fila;
- resultado;
- falha;
- indisponibilidade;
- recuperação;
- proveniência.

### C. ABS atual
- quais invariantes já foram definidos;
- quais capacidades são realmente necessárias;
- quais são apenas possibilidades futuras.

### D. Android atual
- quais portas estão disponíveis no Galaxy A17;
- quais exigem computador;
- quais exigem reset;
- quais exigem desbloqueio;
- quais são reversíveis;
- quais aumentam realmente a capacidade do ABS.

### E. Histórico
- continuar procurando evidência de execução real;
- recuperar artefatos binários/ZIP quando possível;
- comparar branches;
- fechar a causalidade do adapter direto.

---

## 11. REGRA

**Nenhum código novo do ABS ou Mini-Cérebro será criado nesta etapa.**

A investigação continua.

A fronteira de construção será atingida quando houver informação suficiente para responder:

> **O que construir primeiro, por que construir, qual capacidade isso cria, qual evidência sustenta a escolha, como testar, como reverter e como isso se conecta ao restante do ABS?**

Até lá, pesquisar.
