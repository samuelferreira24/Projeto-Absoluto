# GOVERNANÇA DA INFORMAÇÃO — PROJETO ABSOLUTO

## 1. Objetivo
Este documento define como a informação do Projeto Absoluto deve ser organizada, classificada, recuperada e mantida.

A finalidade não é reduzir a quantidade de informação. É impedir que informação importante fique sem função, duplicada sem autoridade, misturada com histórico, confundida com estado atual ou presa a uma conversa.

## 2. Princípio central
Cada informação deve possuir:
**função → autoridade → temporalidade → origem → caminho de recuperação**

A organização física é consequência dessa classificação, não o contrário.

## 3. Fontes de autoridade

### O que existe agora
Prioridade:
1. código atual;
2. testes;
3. CI/resultados verificáveis;
4. runtime/evidência de execução;
5. documentação operacional;
6. especificações;
7. histórico.

Documentação nunca transforma hipótese em capacidade comprovada.

### O que foi decidido
Decisões do Imperador são autoridade sobre direção e princípios.
Uma decisão não deve ser inferida de código, documentação histórica ou sugestão de IA.

### O que o projeto sabe
O conhecimento estruturado deve ser persistido no mecanismo de Project Knowledge/Cérebro e ter proveniência.

### O que aconteceu
Histórico preservado é autoridade sobre o registro histórico daquilo que ocorreu, mas não sobre o estado operacional atual.

## 4. Classes de informação
| Classe | Pergunta |
|---|---|
| Estado | O que existe agora? |
| Conhecimento | O que sabemos? |
| Decisão | O que foi decidido? |
| Arquitetura | Como os componentes se relacionam? |
| Planejamento | Quais possibilidades/direções existem? |
| Operação | Como usar o que existe? |
| Evidência | O que foi observado/testado/executado? |
| Continuidade | O que uma nova sessão precisa recuperar? |
| Histórico | O que aconteceu antes? |
| Fonte | De onde veio a informação? |
| Referência | Qual é a descrição técnica estável? |
| Tutorial/How-to | Como realizar uma ação? |

## 5. Documentação
A documentação deve separar necessidades diferentes em vez de colocar tudo no mesmo documento.

Aplicação adaptada ao Projeto Absoluto:
- Tutorial → aprendizado guiado;
- How-to → execução de tarefa real;
- Referência → descrição técnica precisa;
- Explicação → contexto, motivos e relações.

Não criar quatro pastas vazias apenas para obedecer a um modelo. A classificação deve surgir do conteúdo real.

## 6. Continuidade
A pasta continuidade é infraestrutura de transferência entre sessões/IAs.
Ela não deve virar um segundo depósito geral de documentação.

Deve conter principalmente:
- checkpoints;
- contexto necessário para retomada;
- decisões necessárias à retomada;
- ponte para estado vivo;
- handoffs/projeções;
- contratos de continuidade.

Material que pertence estruturalmente a arquitetura, operação, referência ou planejamento deve permanecer em sua área própria.

## 7. Estado vivo
O estado estruturado produzido por Project Knowledge deve ser tratado como fonte canônica de estado derivado do repositório e das evidências que o mecanismo consegue observar.

MAPA_AUTO_ESTADO_PROJETO.md é uma projeção humana desse estado.

Handoffs não devem competir com o estado vivo. São checkpoints de contexto e devem apontar para as fontes canônicas.

## 8. Sessões
Uma sessão de IA é uma unidade temporária de trabalho.

Quando uma sessão produzir decisão, mudança de arquitetura, resultado, evidência, descoberta, pendência ou ponto de retomada que altere o estado do Projeto, isso deve ser persistido no repositório antes do encerramento/transferência.

A conversa não é armazenamento persistente do Projeto.

## 9. Histórico
Histórico nunca deve ser apagado apenas para simplificar a navegação.
Mas histórico também não deve aparecer como implementação atual.

Cada fonte histórica deve ser identificada por origem, período, versão, estado, relação com o presente e se foi superada ou continua válida.

## 10. Mapas
Mapas são instrumentos de navegação e planejamento.
Eles não são código, prova operacional, fila obrigatória ou substituto do estado vivo.
O mapa deve apontar para fontes verificáveis.

## 11. Reorganização física
Nenhum arquivo operacional deve ser movido apenas por estética.

Antes de mover:
1. localizar referências;
2. verificar imports;
3. verificar scripts;
4. verificar CI;
5. verificar entrypoints;
6. verificar documentação dependente;
7. criar migração reversível;
8. executar testes;
9. atualizar referências;
10. verificar continuidade.

Documentos podem ser reorganizados com menor risco, mas também devem preservar histórico e referências.

## 12. Regra contra duplicação
Dois documentos com o mesmo assunto não são automaticamente duplicados.

Comparar:
**função + autoridade + temporalidade + origem + público**

Só consolidar quando função e autoridade forem equivalentes.

Quando houver conteúdo histórico diferente, preservar a fonte e criar referência para a autoridade atual.

## 13. Regra de navegação
Uma IA nova deve conseguir responder:
1. Qual é o Projeto?
2. Qual é o estado atual?
3. Qual é a arquitetura atual?
4. Quais decisões são vinculantes?
5. Quais capacidades estão comprovadas?
6. Quais são as evidências?
7. O que é planejamento?
8. O que é histórico?
9. Qual é o ponto de retomada da sessão?

## 14. Arquitetura de informação
A estrutura não deve ser reorganizada para criar uma árvore artificialmente profunda.

Preferir:
- poucos níveis;
- nomes semânticos;
- índices claros;
- links entre fontes;
- uma autoridade por pergunta;
- projeções automáticas quando possível.

## 15. Fases da reorganização
### Fase 1 — Governança e navegação
Definir autoridade, taxonomia, índice mestre, portas de entrada e documentos derivados.

### Fase 2 — Classificação documental
Inventariar documentos, classificar função, detectar duplicação semântica e registrar relações, sem mover código.

### Fase 3 — Continuidade
Reduzir concorrência entre handoffs e ligar sessão → estado → evidência → decisão.

### Fase 4 — Migração documental
Mover somente documentos cuja função esteja comprovada, preservando referências.

### Fase 5 — Migração estrutural
Somente quando houver benefício operacional comprovado; código é protegido; testar após cada lote.

### Fase 6 — Automação
Gerar índices, validar links, detectar documentos órfãos e estado desatualizado, e atualizar projeções.

## 16. Critério profissional de conclusão
A reorganização só será concluída quando uma nova IA puder, sem depender da conversa anterior:
- localizar o estado atual;
- distinguir atual/histórico/hipótese;
- localizar decisões;
- localizar evidências;
- localizar arquitetura;
- localizar planejamento;
- localizar ponto de retomada;
- descobrir onde cada tipo de informação deve ser registrado.

**Organização concluída = recuperação confiável, não apenas pastas bonitas.**
