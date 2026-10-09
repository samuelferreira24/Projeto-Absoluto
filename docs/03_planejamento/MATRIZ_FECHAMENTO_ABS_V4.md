# Matriz de Fechamento V4 — Capacidades, Dependências e Evidências

**Estado:** plano de execução derivado dos registros atuais; atualizar somente após evidência.  
**Fonte-base:** `continuidade/07_conhecimento/closure_registry.json` e `capability_registry.json`.  
**Regra:** esta matriz não muda nenhum status. “Etapa V4” indica prioridade de trabalho, não uma versão do produto.

## 1. Ordem de fechamento por dependência

| Ordem | IDs | Capacidade/lacuna | Trabalho principal | Depende de |
|---|---|---|---|---|
| 0 | transversal | Baseline e segurança da mudança | Registrar SHA/deploy/recursos, testes, backups e rollback | Nenhuma |
| 1 | 07 | Cérebro | Fechar missão → Work → capacidade → resultado → estado do Cérebro | Runtime e contratos existentes |
| 1 | 25 | Validação | Critérios de sucesso e verificação end-to-end, além de invariantes estruturais | Ciclo vertical |
| 1 | 34 | Registro de agentes | Integrar registry existente ao runtime, estado durável e teste end-to-end | Contratos de capability/identidade |
| 1 | 44 | Idempotência | Integrar mecanismo existente com Work, adaptadores e resultados incertos | Persistência e contrato de execução |
| 1 | 45 | Filas/processamento futuro | Fila recuperável ou contrato durável equivalente, leases e reconciliação | Work persistido e máquina de estados |
| 1 | 48 | Execução contínua | Retomar trabalho após reinício, com checkpoint e parada controlada | Fila/estado durável |
| 1 | 46 | Monitoramento | Estado contínuo, alertas e registro de eventos/health | Contratos de estado e execução |
| 1 | 27 | Auditoria | Trilha de autorização, ações, efeitos, resultado e evidência | Proveniência e eventos |
| 2 | 35 | Multi-IA | Seleção por capacidade/política, fallback, limites e testes por motor | Catálogo e contratos de modelo |
| 2 | 38 | Supervisão | Supervisão com escopo, critérios, limites e escalonamento | Execução e verificação |
| 2 | 39 | Meta-supervisão | Limites da supervisão, tratamento de desacordo e escalonamento humano | Supervisão |
| 2 | 40 | Auditoria independente | Caminho de verificação separado do executor em tarefas apropriadas | Critérios de sucesso e evidências |
| 2 | 52 | Outras plataformas | Adicionar integrações através de adaptadores e testes de contrato | Gateway de ferramentas e segurança |
| 2 | 58 | Interoperabilidade | Contratos comprovados entre ferramentas, agentes, nós e serviços | Contratos versionados |
| 2 | 64 | Detecção de conflitos | Integrar mecanismo existente a instruções, recursos, estado e autorização | Estado canônico e política |
| 3 | 09 | Memória temporal | Persistência temporal recuperável integrada ao ciclo operacional | Eventos, Work e proveniência |
| 3 | 15 | Experiência | Registro estruturado de experiência reutilizável | Resultado verificado |
| 3 | 16 | Aprendizado | Demonstrar mudança de comportamento avaliada, versionada e reversível | Experiência + avaliação offline |
| 3 | 17 | Sabedoria operacional | Derivar regras/heurísticas com fonte, validade e prova | Aprendizado validado |
| 3 | 13 | Pesquisa contínua | Pesquisa programada/reativa com fontes, resultados e atualização de estado | Ferramentas web + agendamento + memória |
| 3 | 26 | Observabilidade | Painel consolidado de runtime, modelos, recursos, custos e erros | Instrumentação e eventos |
| 3 | 28 | Evolução arquitetural | Mudanças controladas com CI, autorização, rollback e histórico | Update manager + evidências |
| 4 | 65 | Red team independente | Desafios repetíveis, achados, correções e regressões | Superfície de execução estabilizada |
| 4 | 67 | Novas capacidades | Pipeline descoberta → especificação → implementação → teste → registro | Registry e governança |
| 4 | 68 | Novos recursos | Descoberta → avaliação → registro → autorização → integração | Identidade de recurso e política |
| 4 | 69 | Sistemas derivados | Criar e registrar sistemas derivados com dependências e proveniência | Catálogo de sistemas/capacidades |
| 4 | 70 | Escala | Testar carga, concorrência, nós e preservação de controle | Durabilidade, observabilidade e nó registry |

## 2. Capacidades planejadas que precisam entrar no desenho, sem fingir que já existem

| ID | Capacidade | Tratamento na V4 |
|---|---|---|
| 47 | Detecção de oportunidades | Pipeline de sinais/observações → hipótese → avaliação de valor/risco → proposta ao Imperador; sem executar oportunidade automaticamente |
| 49 | Operação 24/7 | Disponibilidade de serviços, agendamento, fila persistente, monitoramento, recuperação e escalonamento; não equivale a manter uma aba aberta |
| 71 | Capacidades ainda desconhecidas | Arquitetura aberta, descoberta controlada e integração sob contratos; não pode ser “implementada” como catálogo fechado |
| 72 | Oportunidades descobertas durante a construção | Captura de descobertas e triagem rastreável durante a execução do plano, sem alterar escopo/autoridade silenciosamente |

## 3. Fechamento das relações semânticas

Estas relações são dependências transversais, não um projeto separado de reorganização documental.

| Relação | Estado no registro | Fechamento V4 |
|---|---|---|
| Decisão → evidência | Parcialmente registrada | ID de evidência específica ligado à decisão e seu estado |
| Evidência → implementação | Parcialmente registrada | Referência concreta a arquivo/commit/teste/resultado |
| Implementação → resultado | Parcialmente registrada | Resultado operacional ou teste vinculado à implementação |
| Resultado → decisão substituta | Não registrada | Relação explícita quando uma decisão for substituída |
| Pesquisa → evidência | Parcialmente registrada | Evidências específicas, não só documento amplo |
| Artefato → decisão/capacidade/componente | Não registrada | Relação de propriedade/produção e finalidade |
| Agente → modelo/política/ferramenta/responsabilidade | Não registrada | Identidade operacional, escopo e capacidades |
| Recurso externo → ambiente/nó/serviço | Parcialmente registrada | Recurso observado, origem e localização |
| Ambiente externo → estado atual | Não registrada | Observação com timestamp, saúde e fonte |

## 4. Ordem de dependência real

Não iniciar a partir da lista de produtos. A ordem técnica é:

1. **Ciclo vertical e contratos:** Cérebro, Work, capability, autorização, resultado, verificação e retorno.
2. **Durabilidade:** estados, fila, leases, idempotência, checkpoint e reconciliação.
3. **Política e catálogo:** identidade, permissões, modelos, ferramentas, agentes, custos e capacidades.
4. **Multi-IA e ferramentas:** cada adaptador validado ponta a ponta; browser, HTTP, GitHub, Codex e outros.
5. **Memória e aprendizado:** proveniência semântica, memória temporal, experiência e promoção reversível de aprendizado.
6. **Operação 24/7:** monitoramento, agendamento, notificações, recuperação e backup restaurável.
7. **Construção segura:** sandbox, CI, deploy/rollback e red team.
8. **Pesquisa/oportunidades e expansão:** descoberta de novas capacidades, recursos, sistemas derivados e escala.

A ordem pode ser ajustada somente quando uma dependência real ou evidência de risco justificar. Não se abre uma versão nova para cada etapa.

## 5. Evidência mínima para cada capacidade

Uma capacidade só muda de status quando o registro aponta para:
- implementação identificável;
- contrato de entrada/saída;
- integração no runtime correto;
- teste automatizado e/ou evidência operacional;
- comportamento em falha relevante;
- autorização e escopo;
- persistência/proveniência quando necessária;
- recuperação quando necessária;
- link para commit/teste/resultado;
- confirmação de que o teste não foi apenas simulado quando a alegação é operacional.

**“Existe código” ≠ “está integrado”. “Passou unit test” ≠ “está operacional”. “Está disponível” ≠ “foi validado ponta a ponta”.**

## 6. Regras para manter a matriz viva

- Atualizar após cada mudança material de status.
- Não modificar registros de status automaticamente com base em nomes de arquivos.
- Preservar histórico da evidência que justificou transição.
- Não marcar as 72 capacidades como fechadas; o catálogo é mais amplo que o estado atual.
- Não duplicar o `closure_registry.json`: este documento é a projeção de planejamento legível; o registry é a fonte estruturada de status.
