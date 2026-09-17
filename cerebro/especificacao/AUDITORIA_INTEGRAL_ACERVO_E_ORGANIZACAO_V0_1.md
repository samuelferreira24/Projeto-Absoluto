# AUDITORIA INTEGRAL DO ACERVO E DA ORGANIZAÇÃO V0.1

Data: 2026-09-17
Branch auditada: `base-cerebro-v0.1`
Commit auditado: `d1df8b310c401a768cd48b2da059b87d336da7a2`

## 1. Objetivo

Realizar uma varredura profissional do patrimônio técnico e documental disponível, procurando:

- conteúdo não preservado;
- conteúdo guardado no lugar errado;
- documentos duplicados ou concorrentes;
- documentação desatualizada em relação ao código;
- capacidades já construídas ainda marcadas como futuras;
- capacidades existentes sem persistência suficiente;
- histórico que precisa ser preservado antes de qualquer limpeza;
- responsabilidades duplicadas entre módulos;
- referências importantes sem proveniência ou contexto;
- riscos de perda de conhecimento durante a evolução.

A regra desta auditoria é **preservar antes de reorganizar**. Nenhum material histórico deve ser apagado apenas porque parece antigo, duplicado ou inadequado ao modelo atual.

## 2. Integridade da branch

A construção permanece em `base-cerebro-v0.1`. A `main` permanece separada.

A comparação atual mostra a branch de construção divergente da `main`; a `main` continua no commit-base `958476848b5111cdac02efa6206f2fb32f550624`. Não realizar merge automático como parte desta auditoria.

## 3. Inventário encontrado

O repositório contém atualmente quatro grandes classes de patrimônio:

1. **Fontes históricas e documentos-base** — DOCX, PDF, TXT e MHT/MHTML.
2. **Especificações do Projeto/Cérebro** — contratos, mapas, arquitetura, método, memória, continuidade, execução, economia, orquestração e evolução.
3. **Implementação do Cérebro** — ingestão, núcleo, semântica, memória, temporalidade, relações, aprendizagem, runtime, execução, recursos, grafo de tarefas, agendamento, composição e sinergia.
4. **Validação e operação** — testes, workflows, CLI, Docker e artefatos de continuidade.

## 4. Conteúdo encontrado fora do lugar

Foram encontrados quatro arquivos chamados `.gitkeep` que não são placeholders vazios: contêm conteúdo textual de conversas/consultoria.

Arquivos afetados:

- `automacao/.gitkeep`
- `comercial/.gitkeep`
- `docs/.gitkeep`
- `metas_pessoais/.gitkeep`

Isso é uma anomalia documental. `.gitkeep` deve ser usado somente para preservar diretórios vazios. O conteúdo existente é patrimônio histórico e **não deve ser apagado** até que seja extraído, classificado, relacionado e preservado em uma localização semântica adequada.

Estado: **PRESERVAR / MIGRAÇÃO PENDENTE**.

## 5. Possível duplicação de fonte MHT

`Conversaweb.mht` e `👔 Consultoria_ Projeto Comercial & Automação _ OpenHands Cloud (1).mht` apontam para o mesmo SHA de blob (`90ffe9418c265b7c346644b1ca0126e7e9a79e14`).

Isso indica que os dois nomes representam o mesmo conteúdo binário no estado atual do Git. Não remover nenhum dos nomes nesta auditoria. Primeiro registrar a equivalência e verificar sua função histórica; depois, se necessário, manter um original canônico e um registro de alias/legado.

Estado: **DUPLICIDADE CONFIRMADA / LIMPEZA ADIADA**.

## 6. Documentação de visão desatualizada

`Visao_Geral.md` descreve uma visão anterior centrada em plataforma integradora, metas pessoais, comercial e automação. O quadro atual do Projeto é mais amplo e explicitamente não reduz o Projeto a software, automação ou IA.

O arquivo deve permanecer como **documento histórico**, mas não deve funcionar como referência normativa da arquitetura atual.

A referência atual deve ser o mapa mestre evolutivo dentro de `cerebro/especificacao/`.

Estado: **LEGADO / NÃO NORMATIVO**.

## 7. Fotografia estrutural desatualizada

`cerebro/ESTRUTURA_ATUAL_V0_1.md` descreve diretórios lógicos como `esquemas/`, `ingestao/`, `registros/`, `relacoes/` e `historico/`, enquanto a implementação real está concentrada em módulos Python, `especificacao/`, `memoria/` e `tests/`.

A V0.1 deve ser preservada como fotografia histórica. Uma fotografia V0.2 deve representar a estrutura real atual sem apagar a anterior.

Estado: **VERSÃO HISTÓRICA / NOVA FOTOGRAFIA NECESSÁRIA**.

## 8. Especificações concorrentes de agendamento/orquestração

Existem várias especificações relacionadas a agendamento e orquestração, incluindo versões V0.1, V0.2 e documentos de controles/composição.

Isso não é necessariamente erro: parte desse conjunto registra evolução. O problema é não existir ainda uma classificação documental explícita entre:

- canônico atual;
- histórico;
- adendo;
- proposta experimental;
- superado.

A `AGENDAMENTO_ADAPTATIVO_V0_2.md` já declara explicitamente limitações da versão atual e deve ser tratada como referência da capacidade de agendamento V0.2, enquanto as versões anteriores permanecem como histórico.

Estado: **RECONCILIAÇÃO DOCUMENTAL NECESSÁRIA**.

## 9. Responsabilidades duplicadas na implementação

Foram encontradas duas camadas relacionadas à orquestração adaptativa:

- `cerebro/agendador.py` — integrado à fachada `Cerebro`, com planejamento, histórico, perfis de experiência, retry e replanejamento;
- `cerebro/orquestracao_adaptativa.py` — possui planejamento adaptativo e descoberta de sinergia, mas não aparece integrada à fachada principal atual.

A existência de ambas pode representar evolução experimental, mas a responsabilidade de cada uma precisa ser declarada. Não apagar a segunda antes de registrar sua finalidade e comparar sua lógica.

Estado: **DUPLICIDADE FUNCIONAL / CLASSIFICAÇÃO PENDENTE**.

## 10. Sinergia ainda não é memória durável

`cerebro/sinergia.py` já detecta ganhos de combinações e gera candidatos promissores, mas seu estado é mantido em memória do processo. A fachada instancia `DetectorSinergia()` sem caminho de persistência.

Consequência: uma nova execução pode perder os resultados de sinergia observados anteriormente.

Isso é especialmente importante porque o Projeto considera a descoberta de novas combinações um mecanismo multiplicador.

Estado: **LACUNA REAL DE PERSISTÊNCIA**.

## 11. Grafo de tarefas ainda é estado de processo

`GrafoTarefas` organiza dependências, prontidão, lotes paralelos e estados das tarefas, mas o grafo em si é criado em memória na inicialização do `Cerebro`.

O `AgendadorAdaptativo` persiste histórico e perfis, porém isso não equivale a persistir integralmente o estado estrutural do grafo.

Para continuidade real, é necessário preservar também:

- tarefas;
- dependências;
- estados;
- prioridades;
- recursos;
- parâmetros de execução;
- versões do grafo;
- alterações estruturais e seus motivos.

Estado: **LACUNA DE CONTINUIDADE/PERSISTÊNCIA**.

## 12. Aprendizado do agendamento ainda não chega automaticamente à memória do Cérebro

O agendador aprende perfis locais por tarefa e mantém histórico próprio. A especificação reconhece que essa experiência futuramente deve alimentar a memória permanente.

No estado atual, essa integração ainda não é automática.

Estado: **PLANEJADO, NÃO CONSOLIDADO**.

## 13. Descoberta de sinergias ainda é predominantemente pareada

`DetectorSinergia.combinações_promissoras()` gera combinações de duas capacidades. O modelo de resultados consegue representar conjuntos maiores, mas a geração de candidatos ainda não explora sistematicamente combinações de três ou mais fatores.

Isso não deve ser tratado como erro de V0.1/V0.2; é uma limitação conhecida que precisa permanecer registrada para a evolução do mecanismo multiplicador.

Estado: **LIMITAÇÃO CONHECIDA / PRÓXIMA EVOLUÇÃO**.

## 14. Recursos ainda precisam de semântica quantitativa mais forte

O agendamento atual trabalha principalmente com conjuntos de recursos e orçamento/custo/tempo. A própria especificação reconhece que capacidade quantitativa de recursos, custo de comunicação, caminho crítico e otimização multiobjetivo completa ainda não estão resolvidos.

Isso deve permanecer como pendência explícita, não como capacidade já concluída.

Estado: **PENDENTE**.

## 15. Referências fixas foram registradas corretamente

O princípio de referências fixas contextualizadas foi registrado na memória fundamental em 2026-09-17. Ele estabelece que uma referência fixa deve conservar princípio, contexto, significado, finalidade, evidências/proveniência, relações, limitações, condições de aplicação, confiança e histórico de mudanças de entendimento.

Isso corrige um risco importante: transformar uma frase antiga em regra sem contexto.

Estado: **REGISTRADO**.

## 16. Memória recuperada do chat foi preservada

`cerebro/memoria/recuperacao_chat_2026-09-17.json` contém uma recuperação estruturada de princípios, história, retenção, pesquisa, aprendizado, temporalidade, planejamento, múltiplas IAs, motores, coleta, portabilidade, composição, orquestração e progresso.

Esse arquivo deve ser tratado como **registro de recuperação**, não como substituto da fonte original nem como verdade completa do histórico interno.

A próxima atualização deve ser um novo registro de estado/contexto, não uma sobrescrita que elimine a fotografia histórica anterior.

## 17. Patrimônio histórico que não deve ser perdido

A auditoria confirma como patrimônio a preservar:

- os três documentos-base V10 e a pesquisa de representação/armazenamento;
- relatórios de contribuição;
- relatório diagnóstico;
- transcrição de conversa;
- arquivos MHT/MHTML;
- memória histórica do `Sistema`;
- `semente-nucleo.json` e demais sementes do Sistema;
- código e histórico do Sistema;
- código e histórico do Cérebro;
- decisões, correções, erros e mudanças de entendimento registradas no Git;
- especificações antigas, mesmo quando superadas.

O objetivo não é deixar tudo como referência ativa. O objetivo é garantir que nada seja perdido e que cada item possa receber uma classificação histórica adequada.

## 18. Regra documental profissional adotada

A partir desta auditoria, todo patrimônio deve receber uma das classificações:

`CANÔNICO_ATUAL` — referência normativa da arquitetura atual.

`ATIVO` — componente em uso/construção.

`ADENDO` — complementa um documento canônico.

`EXPERIMENTAL` — hipótese ou implementação em avaliação.

`HISTÓRICO` — preservado para entender a evolução.

`SUPERADO` — substituído por entendimento posterior, mas preservado.

`FONTE_BRUTA` — material original que não deve ser alterado.

`DERIVADO` — interpretação, resumo, índice ou análise produzida a partir de uma fonte.

`MIGRAÇÃO_PENDENTE` — conteúdo válido localizado em lugar inadequado e aguardando preservação sem perda.

## 19. Regra de ouro

> **Nenhum conteúdo será apagado para “organizar” antes de existir uma cópia preservada, uma classificação e uma referência de proveniência.**

Organização não pode produzir perda histórica.

## 20. Resultado da varredura

A varredura encontrou patrimônio bem preservado, mas também encontrou problemas reais de organização e continuidade:

1. placeholders contendo conteúdo;
2. fonte MHT duplicada por nome;
3. visão geral histórica não marcada como legado;
4. fotografia estrutural V0.1 divergente da implementação atual;
5. especificações concorrentes sem índice de autoridade documental;
6. duas camadas de orquestração adaptativa com responsabilidade sobreposta;
7. sinergias sem persistência;
8. grafo de tarefas sem persistência estrutural;
9. experiência do agendamento ainda não consolidada automaticamente na memória;
10. descoberta de combinações ainda limitada para além de pares.

Nenhum desses pontos justifica apagar o patrimônio. Eles definem o trabalho profissional de reconciliação que deve ser feito agora.

## 21. Próxima etapa recomendada pela própria auditoria

A próxima etapa não deve ser adicionar módulos aleatórios. Deve ser construir a **camada de governança documental e reconciliação do patrimônio**, contendo:

```text
ACERVO
  ↓
INVENTÁRIO
  ↓
CLASSIFICAÇÃO
  ↓
PROVENIÊNCIA
  ↓
CANONICIDADE
  ↓
RELAÇÕES
  ↓
LACUNAS
  ↓
PENDÊNCIAS
  ↓
CÉREBRO
```

Depois disso, a evolução técnica deve priorizar a persistência do grafo/agendamento/sinergia e a integração da experiência de orquestração à memória permanente.
