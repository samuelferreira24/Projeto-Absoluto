# PESQUISA — PRESERVAÇÃO DE CONTEXTO, CONHECIMENTO E CONTINUIDADE
## Projeto Absoluto — referência arquitetural para não depender de uma única conversa

**Data:** 2026-10-03  
**Status:** pesquisa de referência  
**Finalidade:** definir, com base em pesquisa externa e no conhecimento já acumulado no Projeto, como preservar de forma profissional aquilo que uma IA entende, aprende, decide, observa e precisa transmitir para outra IA ou sessão.

---

## 1. Pergunta da pesquisa

Como preservar o contexto de um projeto complexo de modo que uma nova IA consiga continuar sem depender da conversa anterior, sem reduzir conhecimento a um único handoff, sem confundir decisões com hipóteses, sem confundir estado atual com histórico e mantendo pesquisas, evidências, artefatos e trabalho em andamento recuperáveis?

A pergunta correta não é apenas onde guardar o texto da conversa. É:

> Como construir uma memória operacional e um sistema de continuidade que preserve significado, estado, evidência e capacidade de retomada sem transformar tudo em um único documento gigante?

## 2. Resultado central

A pesquisa converge para uma conclusão importante:

> **Handoff é uma camada de transferência, não a memória inteira do projeto.**

Uma arquitetura profissional precisa distinguir funcionalmente:

1. visão e conhecimento estável;
2. decisões;
3. pesquisa e evidências;
4. estado atual;
5. memória de experiências;
6. histórico;
7. artefatos de trabalho;
8. checkpoints e estado recuperável;
9. sessão/conversa;
10. handoff;
11. índices e mapas de recuperação;
12. proveniência e temporalidade.

Essas camadas podem compartilhar infraestrutura, mas não devem ser tratadas como a mesma coisa.

## 3. Evidência externa

### OpenAI
A documentação atual de agentes separa sessão, turnos, configuração, conversa, trabalho salvo, estado, arquivos/artefatos, ambientes, ferramentas e handoffs. A documentação também diferencia sessões da Agents API, sessões do SDK, conversas e ambientes.

A pesquisa de context engineering mostra que mesmo uma janela grande não significa que seja desejável carregar todo o histórico. O problema passa a ser selecionar, recuperar, comprimir e manter o contexto adequado.

Fontes principais:
- OpenAI Agents documentation.
- OpenAI Agents API Sessions.
- OpenAI Cookbook — Context Engineering / Session Memory.

### Microsoft Agent Framework
A documentação atual separa sessões, histórico, context providers, memória/persistência, armazenamento, estado de agente, estado de workflow e checkpoints.

Checkpoints são tratados como estado recuperável de execução e podem registrar estado de executores, mensagens pendentes, requests/responses e estado compartilhado. O framework também suporta reidratação de sessões e armazenamento externo.

Isso demonstra uma distinção essencial:

**conhecimento permanente != estado operacional necessário para continuar um trabalho.**

Fontes principais:
- Microsoft Agent Framework — Conversations & Memory.
- Microsoft Agent Framework — Memory & Persistence.
- Microsoft Agent Framework — Workflow Checkpoints.
- Microsoft Agent Framework — Storage / Self-hosting.

### Segurança
A documentação de checkpoints trata o armazenamento persistente como fronteira de confiança. Isso reforça que estado não deve ser considerado apenas texto: integridade, origem, autorização e proteção do armazenamento fazem parte da continuidade.

## 4. O que já havia sido descoberto no Projeto

O Projeto Absoluto já havia chegado a conclusões compatíveis com a pesquisa externa.

### Visão × memória × estado

**VISÃO** = o que o Projeto é, por que existe, princípios, conceitos, direção e significado.

**MEMÓRIA** = o que foi aprendido por experiências, pesquisas, erros, resultados e descobertas.

**ESTADO** = o que está acontecendo agora: tarefas, trabalhos em andamento, decisões recentes, resultados pendentes e próximos movimentos.

### Arquivo não é memória inteira

O arquivo pode ser uma fonte profunda da visão sem precisar ser colocado integralmente em cada contexto. O futuro sistema deve conseguir recuperar somente o necessário.

### Memória não é simples armazenamento de texto

O Projeto já registrou a possibilidade de uma progressão:

~~~text
EVIDÊNCIA → FRAGMENTO → FATO → CONCEITO → EPISÓDIO → EXPERIÊNCIA → PROCEDIMENTO → PRINCÍPIO → SABEDORIA
~~~

Isto é um modelo de evolução do conhecimento, não um pipeline rígido.

### Arquivo × Sistema

O arquivo pode crescer. O Sistema pode aprender. Ambos podem evoluir. Nenhum deles é a própria visão.

### Repositório como memória externa

O Projeto já adotou a ideia de que o repositório deve funcionar como memória externa verificável, enquanto documentos menores funcionam como mapas para o material profundo.

## 5. Por que somente um handoff é insuficiente

Um handoff é excelente para transferência imediata, mas sozinho cria riscos:

- **compressão:** conhecimento pode desaparecer no resumo;
- **mistura:** decisão, hipótese, pesquisa e estado podem ficar no mesmo texto;
- **desatualização:** o estado muda e o handoff envelhece;
- **perda de proveniência:** uma afirmação pode sobreviver sem a fonte;
- **duplicação:** o handoff passa a competir com estado, decisões e pesquisas;
- **falsa completude:** um documento chamado completo pode parecer substituir as fontes originais.

Portanto:

> **Handoff deve ser ponte, não fonte universal.**

## 6. Arquitetura de preservação recomendada

~~~text
                    PROJETO ABSOLUTO
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       VISÃO          CONHECIMENTO       PRINCÍPIOS
          │                │                │
          └────────────────┼────────────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
             PESQUISA            DECISÕES
                 │                   │
                 └─────────┬─────────┘
                           │
                    EVIDÊNCIAS / FONTES
                           │
              ┌────────────┴────────────┐
              │                         │
          ESTADO ATUAL             HISTÓRICO
              │                         │
         MEMÓRIA + ARTEFATOS + CHECKPOINT
              │                         │
              └────────────┬────────────┘
                           │
                        HANDOFF
                           │
                      NOVA IA / SESSÃO
~~~

O fluxo de recuperação deve ser:

**nova sessão → mapa → estado → decisões → evidências → fontes profundas → trabalho**

e não:

**nova sessão → ler um handoff gigante → confiar nele**.

## 7. Função de cada camada

| Camada | Pergunta |
|---|---|
| Visão | O que é o Projeto e por que existe? |
| Princípios | Quais fundamentos orientam o Projeto? |
| Conhecimento | O que foi aprendido/consolidado? |
| Decisões | O que foi decidido e por quem? |
| Pesquisa | O que foi investigado? |
| Evidência | O que sustenta uma afirmação? |
| Estado | O que existe/agora está acontecendo? |
| Memória | O que experiências anteriores ensinaram? |
| Histórico | O que aconteceu antes? |
| Artefatos | O que foi produzido para realizar o trabalho? |
| Checkpoint | De onde uma execução pode ser retomada? |
| Handoff | O que a próxima sessão precisa saber para começar? |
| Índice/mapa | Onde encontrar cada coisa? |
| Proveniência | De onde veio, quando e como foi registrado? |

## 8. Autoridade

As camadas não têm a mesma autoridade.

Para saber **o que existe hoje**:
**código + testes + CI + evidência operacional**.

Para saber **o que foi decidido**:
**registro autorizado da decisão do Imperador**.

Para saber **o que foi pesquisado**:
**pesquisa + fontes + evidências**.

Para saber **o que aconteceu historicamente**:
**registro histórico preservado**.

Para saber **como continuar uma tarefa interrompida**:
**estado/checkpoint + artefatos + handoff**.

Uma resposta de IA não vira conhecimento confiável automaticamente.

## 9. Temporalidade e proveniência

Guardar informação significa preservar:

**conteúdo + origem + período + status + relação com o presente**.

Uma informação pode ser atual, histórica, superada, experimental, provisória, hipótese ou pendente de validação.

Para informações importantes, deve ser possível responder:

- de onde veio;
- quem registrou;
- quando;
- qual fonte sustenta;
- se foi observado ou inferido;
- se foi testado;
- qual versão existia;
- se foi posteriormente corrigido.

Especialmente:

**IA disse X** não deve automaticamente virar **Projeto sabe X**.

## 10. Contexto deve ser recuperado, não despejado

O objetivo futuro não é mandar todos os documentos para toda IA.

~~~text
INTENÇÃO DA NOVA TAREFA
        ↓
IDENTIFICAR CONTEXTO NECESSÁRIO
        ↓
CONSULTAR MAPA
        ↓
RECUPERAR ESTADO
        ↓
RECUPERAR DECISÕES RELEVANTES
        ↓
RECUPERAR EVIDÊNCIAS/FONTES
        ↓
RECUPERAR HISTÓRICO SOMENTE SE NECESSÁRIO
        ↓
EXECUTAR
        ↓
REGISTRAR NOVO RESULTADO
~~~

## 11. O que uma sessão relevante precisa preservar

Quando uma sessão produzir qualquer um destes elementos, ele deve ser persistido na camada apropriada:

- nova decisão;
- mudança de entendimento;
- correção;
- descoberta;
- pesquisa;
- evidência;
- resultado;
- erro;
- nova hipótese;
- alteração de arquitetura;
- alteração de estado;
- trabalho pendente;
- artefato novo;
- dependência nova;
- risco novo;
- próximo ponto de retomada.

Não basta gerar um resumo.

## 12. Protocolo profissional de fechamento

Conforme o caso, uma sessão deve produzir:

### A. Conhecimento
Registrar o que foi aprendido.

### B. Decisão
Registrar somente decisões efetivamente fechadas.

### C. Evidência
Registrar resultados verificáveis.

### D. Estado
Registrar o que agora existe e o que permanece pendente.

### E. Artefatos
Preservar código, arquivos, pesquisas e resultados relevantes.

### F. Checkpoint
Registrar o ponto exato de retomada quando houver trabalho interrompido.

### G. Handoff
Criar uma ponte curta para a próxima IA, apontando para as fontes acima.

### H. Navegação
Atualizar índices quando necessário para tornar as fontes recuperáveis.

## 13. Papel do handoff

O handoff ideal deve responder rapidamente:

1. onde estamos;
2. o que mudou;
3. quais decisões são relevantes;
4. quais evidências sustentam o estado;
5. o que está pendente;
6. onde estão as fontes;
7. qual é o próximo ponto de trabalho.

Ele não deve repetir integralmente pesquisas, código, histórico, documentos conceituais ou todos os artefatos. Deve referenciá-los.

## 14. Aplicação ao Projeto Absoluto

O Projeto já possui grande parte das camadas necessárias:

- `AGENTS.md` — regras;
- `00_IA_NAVEGACAO.md` — porta de entrada;
- `docs/00_GOVERNANCA_INFORMACAO.md` — autoridade/classificação;
- `docs/00_MODELO_PROJETO_ABSOLUTO.md` — modelo conceitual;
- `docs/02_arquitetura/` — arquitetura;
- `docs/03_planejamento/` — planejamento/pesquisa;
- `docs/90_fontes/` — fontes;
- `cerebro/` — conhecimento/mapas/estado;
- `continuidade/` — transferência e checkpoints;
- `project_knowledge.json` — conhecimento derivado;
- `MAPA_AUTO_ESTADO_PROJETO.md` — projeção do estado;
- `abs_core/` — implementação;
- `tests/` — verificação;
- `99_arquivo/` — patrimônio histórico;
- `mini-cerebro/` — recuperação/investigação histórica.

O problema identificado não é ausência absoluta dessas peças. É que o processo de preservação precisa tratá-las explicitamente como camadas de um sistema, em vez de concentrar o entendimento inteiro em um handoff.

## 15. Correção da operação de 2026-10-03

Foi criado:

`continuidade/05_handoffs/05_HANDOFF_ATUAL_COMPLETO_2026-10-03.md`

Esse arquivo continua válido como **handoff atual**.

Mas ele não deve ser considerado a preservação integral do conhecimento.

A preservação correta é:

**handoff + estado + conhecimento + decisões + pesquisas + evidências + histórico + artefatos + mapas + proveniência.**

Esta pesquisa passa a ser a referência explícita para essa interpretação.

## 16. O que não fazer

Não:

- criar um mega-handoff cada vez maior;
- copiar toda a conversa para um arquivo;
- substituir pesquisas originais por resumos;
- substituir decisões por interpretação da IA;
- transformar memória em regra;
- tratar histórico como estado atual;
- duplicar código apenas para documentação;
- carregar todo o repositório em toda sessão;
- usar um único arquivo como fonte universal;
- apagar patrimônio histórico para simplificar;
- fragmentar tudo antecipadamente.

## 17. Critério de sucesso

A preservação estará funcionando quando uma nova IA, sem acesso à conversa anterior, conseguir:

1. descobrir o que é o Projeto;
2. distinguir ABS geral de ABS em construção;
3. localizar o estado atual;
4. localizar decisões;
5. localizar pesquisas;
6. localizar evidências;
7. localizar arquitetura;
8. localizar planejamento;
9. distinguir atual/histórico/hipótese;
10. recuperar artefatos necessários;
11. entender o trabalho interrompido;
12. continuar sem reconstruir tudo manualmente.

O objetivo não é que a nova IA leia tudo.

O objetivo é que ela **saiba onde encontrar tudo o que precisa**.

## 18. Conclusão

> **O contexto do Projeto Absoluto deve ser preservado como um sistema de fontes relacionadas, não como um único handoff.**

A conversa é temporária.

O handoff é uma ponte.

O estado é operacional.

A memória registra aprendizado.

As decisões registram autoridade.

As pesquisas preservam descoberta.

As evidências sustentam afirmações.

Os artefatos preservam trabalho.

O histórico preserva trajetória.

Os mapas permitem recuperação.

O Project Knowledge pode funcionar como camada derivada de navegação/conhecimento.

O repositório preserva as fontes duráveis.

E o ABS futuro deverá ser capaz de operar esse conjunto sem depender de uma IA específica.

## 19. Fontes técnicas consultadas

- OpenAI — Agents documentation: sessões, estado, ferramentas, arquivos/artefatos, handoffs e ambientes.
- OpenAI — Agents API Sessions: continuidade de sessões e trabalho salvo.
- OpenAI Cookbook — Context Engineering / Session Memory: sessões, histórico, trimming, compressão e administração de contexto.
- Microsoft Agent Framework — Conversations & Memory: sessões, histórico, persistência e reidratação.
- Microsoft Agent Framework — Memory & Persistence: context providers, history providers e armazenamento.
- Microsoft Agent Framework — Workflow Checkpoints: checkpoint, persistência, retomada, reidratação e segurança do estado.
- Microsoft Agent Framework — Storage / Self-hosting: armazenamento de sessões e estado em infraestrutura da aplicação.

**Nota epistemológica:** essas fontes descrevem mecanismos técnicos de plataformas/frameworks. Elas não definem a arquitetura do Projeto Absoluto. Foram usadas como evidência comparativa para descobrir princípios de preservação de contexto e continuidade.
