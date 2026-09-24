# HANDOFF OPERACIONAL — SNAPSHOT DE 2026-09-22

> **Classificação:** snapshot histórico operacional. Este arquivo não é mais o ponto de continuidade vigente. Para o estado atual, use `continuidade/05_handoffs/04_HANDOFF_ARQUITETURA_PROJETO_ABSOLUTO_2026-09-23.md` e `continuidade/07_conhecimento/SESSAO_ATUAL.md`.


Data de referência: 2026-09-22
Repositório operacional: samuelferreira24/Projeto-Absoluto
Branch: main
Último estado remoto auditado: 3d1316d4b0f3ac2f23fd506b004b67a2d8466a2c

## 1. FINALIDADE

Este arquivo registra o estado operacional observado em 2026-09-22 para preservar histórico e contexto. Ele não deve ser usado como autoridade única sobre o estado atual.

Regra principal: não reconstruir componentes existentes antes de auditar o estado real, os testes e as integrações.

ABS não é uma tecnologia isolada. É um ecossistema sob controle do Imperador, formado por sistemas, subsistemas, capacidades, recursos e meios substituíveis.
V1 é uma fundação atual; não é o estado final do ABS.

## 2. ESTADO ATUAL CONFIRMADO

- ABS Core V1 existe em abs_core/.
- Há modelos de Work, persistência SQLite, eventos, provenance, sessões, capabilities e orquestração.
- Há API, servidor/local runtime e CLI.
- Existe adapter Codex.
- Existe GitHub Bridge.
- Existe continuidade e update manager.
- Existe daemon de atualização automática.
- Existe gate de testes antes de aplicar atualização.
- Existe rollback após falha de validação/restart/health.
- Existe Cérebro com implementação real.
- cerebro/ciclo_continuo.py existe no estado atual; uma auditoria anterior que o classificou como ausente estava incorreta.
- Existe cerebro/abs_core_executor.py, fazendo a ponte mínima Cérebro → ABS Core.
- Existe Mini-Cérebro como camada histórica/investigativa.
- Existe interface web evoluída para uma superfície de controle/visualização do ABS Pessoal.
- A interface atual foi efetivamente atualizada no dispositivo pelo usuário.

## 3. CONVERGÊNCIA CÉREBRO → ABS CORE

Existe uma ponte implementada em cerebro/abs_core_executor.py.
Fluxo: Missão do Cérebro → ABS Core Orchestrator → Work → Capability → resultado.

O próximo objetivo técnico continua sendo demonstrar o ciclo vertical completo e mínimo:
Cérebro → missão → ABS Core → Echo → resultado → Cérebro.

Depois disso, evoluir para capacidades mais complexas, como Codex.

A existência da ponte não deve ser confundida com um Cérebro plenamente fechado em ciclo de aprendizado.
Ainda precisam ser demonstrados de forma explícita os ciclos de estado → decisão → execução → observação → atualização → novo planejamento.

## 4. CODEX E GITHUB BRIDGE

Codex é uma capability do ABS, não o ABS.
O adapter Codex suporta execução via CLI, resume/thread, eventos JSON, resultado estruturado, sandbox, aprovação e timeout.

Existe evidência operacional real do smoke test:
GitHub Issue → Bridge → Work → Codex → resultado → GitHub.
Task: bridge-smoke-001.
Resultado: ABS_BRIDGE_OK.

Isso demonstra uma execução end-to-end de smoke test, mas não demonstra robustez completa contra duplicação, concorrência, timeout, queda, recuperação, indisponibilidade do GitHub/Codex ou execução parcial.

## 5. INTERFACE

A interface atual está em 20_interface/web/.
Estado confirmado:
- Service Worker abs-interface-v7;
- atualização explícita do Service Worker;
- updateViaCache: none;
- endpoints de atualização;
- mapa espacial do ABS;
- modos Explorar / Editar / Operar;
- painel fixo/contextual;
- workspace visual local;
- criação, edição, duplicação, remoção visual, redimensionamento, conexão e undo/redo;
- superfície de Inteligências;
- superfície de Cérebro/Missões/Recursos/Projetos/Evolução;
- chat baseado em Work;
- sala de inteligências;
- controles de atualização/rollback.

Princípio: mudança visual ≠ alteração real do ABS. Operações reais passam pela cadeia Core/Orchestrator/Capability e exigem autorização quando aplicável.

## 6. ATUALIZAÇÃO AUTÔNOMA

Existe abs_core/update_daemon.py e scripts Termux para instalação do serviço.
Fluxo: detectar → buscar → validar candidato → aplicar → reiniciar ABS → health check → sucesso.
Em falha: rollback → restart → health check.
Validação padrão: python -m pytest -q tests.
O daemon possui lock para impedir instâncias duplicadas.

Foi identificada uma deficiência de observabilidade: quando não havia atualização, o daemon não registrava o ciclo. Isso foi corrigido.

PR #57 — fix(update): make updater check cycles observable — foi integrado ao main.
Commits relevantes:
- f9bca6927a41cba990e870b31055419274ec87ac — logging dos ciclos;
- 698b7f957fbc45fcded4a36fc3563f5c442a2b6d — teste do logging;
- 58ebaa9326baa47bf119c6278d6ce0c79a03fae8 — preservação dos artefatos de bootstrap sem bloquear update;
- 3d1316d4b0f3ac2f23fd506b004b67a2d8466a2c — merge do PR #57.
CI do commit de teste 698b7f9 terminou com ABS Core — success — run #206.

## 7. BOOTSTRAP NO DISPOSITIVO

Antes da atualização automática, o dispositivo estava em e3f5d1a. Depois foi sincronizado manualmente até bdcfec2004f124e000df8f792669c35482137a21.
O serviço abs-updater foi instalado via runit e estava em execução.
Foram observados: daemon iniciado; lock funcionando; git fetch funcionando; update_manager.check() funcionando; ausência de atualização naquele momento.

Dois arquivos acidentais haviam sido criados no repositório por comandos malformados: 'git log --all --oneline --grep=ABS V1' e 'tatus --short'. O conteúdo foi preservado para análise e o mecanismo de atualização recebeu tratamento para não bloquear os artefatos preservados de bootstrap.

## 8. UPDATE MANAGER

abs_core/update_manager.py atualmente:
- consulta origin/main;
- detecta divergência;
- exige worktree sem alterações bloqueantes;
- registra rollback;
- aplica target;
- executa testes;
- reinicia o serviço ABS;
- verifica /health;
- faz rollback em falha;
- mantém estado em ~/.abs/update-state.json.
Health esperado: status == alive.

## 9. CÉREBRO

Arquivos importantes: cerebro/estado.py, cerebro/orquestrador.py, cerebro/runtime.py, cerebro/temporal.py, cerebro/ciclo_continuo.py e cerebro/abs_core_executor.py.
O Cérebro possui implementação real de estado, missão, ciclos, runtime, temporalidade e ponte para ABS Core.
Não classificar como apenas documentação.
Ao mesmo tempo, não classificar como Cérebro vivo completo sem evidência do ciclo fechado e contínuo.

## 10. MINI-CÉREBRO

O Mini-Cérebro preserva e investiga patrimônio histórico.
Funções incluem ingestão de arquivos/ZIP, diretórios, Git/commits, hashes, SQLite, FTS, classificação, claims, relações, evidências, busca, exportação e API local.
Ele não deve ser confundido com o Cérebro operacional.
Integração Mini-Cérebro → Cérebro → decisão → ABS ainda não deve ser tratada como totalmente operacional.

## 11. HISTÓRICO

Repositório histórico: samuelferreira24/Sistema.
Regra: código histórico ≠ capacidade atual comprovada.
Mas implementação histórica descartada ≠ descoberta histórica descartada.
O histórico deve ser consultado para recuperar decisões, experimentos, hipóteses, erros, soluções e descobertas quando a investigação atual exigir.

## 12. CONTINUIDADE HISTÓRICA VS ATUAL

Histórico possui mecanismos antigos de state/journal/checkpoints/heartbeat/lease/hash chain.
O ABS Core atual possui abs_core/continuity.py baseado em snapshot/manifest/hash.
Não assumir equivalência completa entre os dois sem auditoria específica.

## 13. MAPAS

Referências conhecidas:
- 00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md
- 01_TABULEIRO_72_CAPACIDADES_V0_1.md
- 02_QUADRO_PENDENCIAS_CONSTRUCAO_V0_1.md
- 03_PLANO_REDE_EVOLUTIVA_V0_1.md

Os mapas são instrumentos de governança e navegação, não substitutos do estado real do código.
Não interpretar o tabuleiro de 72 capacidades como prova de implementação das 72 capacidades.
Sempre convergir: mapa → capacidade → código → teste → integração → evidência.

## 14. CLASSIFICAÇÃO OBRIGATÓRIA

Para qualquer auditoria futura usar estados explícitos:
NÃO LOCALIZADO; ESPECIFICADO; IMPLEMENTADO; TESTADO; INTEGRADO; OPERACIONAL; OPERACIONALMENTE COMPROVADO; PARCIAL; EXPERIMENTAL; HISTÓRICO; HIPÓTESE; NÃO COMPROVADO.

## 15. O QUE NÃO DEVE SER RECONSTRUÍDO AGORA

Não reconstruir sem evidência: ABS Core; Codex adapter; GitHub Bridge; Cérebro; Mini-Cérebro; interface; continuidade; update manager; mapas.
Primeiro verificar se a necessidade já é atendida por algo existente.

## 16. LACUNAS REAIS PRIORITÁRIAS

A principal fronteira atual é integração, não criação indiscriminada de componentes.
Prioridade:
1. validar o baseline atual;
2. validar a ponte Cérebro → ABS Core;
3. executar/fortalecer o vertical slice com capability simples;
4. fechar retorno do resultado ao Cérebro;
5. testar persistência, autorização, erro e repetição;
6. depois testar Cérebro → ABS Core → Codex → Cérebro;
7. posteriormente investigar integração do Mini-Cérebro no ciclo vivo.

## 17. PRÓXIMO EXPERIMENTO RECOMENDADO

CÉREBRO → MISSÃO → ABS CORE → ECHO → RESULTADO → CÉREBRO.
Critérios: missão identificável; Work persistido; capability explícita; autorização explícita; resultado estruturado; provenance/eventos; atualização do estado do Cérebro; comportamento previsível em erro; repetição sem corromper o estado.
Depois: CÉREBRO → ABS CORE → CODEX → RESULTADO → CÉREBRO.

## 18. ARQUITETURA OPERACIONAL DE REFERÊNCIA

IMPERADOR → ABS PESSOAL → ABS — ECOSSISTEMA → sistemas → subsistemas → capacidades → recursos/infraestrutura.
Resiliência desejada: falha de componente ≠ falha do ecossistema.
Isso é objetivo de engenharia, não garantia absoluta de ausência de falhas.

## 19. ESTADO EPISTEMOLÓGICO

O projeto está em transição de construção isolada de componentes para convergência e integração de capacidades existentes.
A pergunta central passou de apenas 'o que construir?' para 'como provar que os componentes existentes funcionam como sistema?'.

## 20. REGRA PARA A PRÓXIMA IA

1. Ler o handoff vigente (`continuidade/05_handoffs/04_HANDOFF_ARQUITETURA_PROJETO_ABSOLUTO_2026-09-23.md`).
2. Verificar o estado real de main.
3. Verificar testes antes de modificar.
4. Auditar código relevante.
5. Preservar distinção entre fato e hipótese.
6. Consultar histórico quando necessário.
7. Evitar reconstrução.
8. Escolher o menor experimento que reduza a incerteza.
9. Registrar evidência.
10. Atualizar este handoff quando o estado mudar materialmente.

## 21. ESTADO DE ENCERRAMENTO DESTA SESSÃO

- interface atualizada e confirmada pelo usuário;
- updater recebeu observabilidade;
- correção passou na CI;
- PR #57 integrado;
- tratamento dos artefatos de bootstrap incorporado;
- estado do repositório reauditado;
- ponte Cérebro → ABS Core confirmada no código;
- ciclo_continuo.py confirmado existente;
- próximo foco: integração comprovável do Cérebro com ABS Core.

Não há necessidade de reconstruir o contexto conceitual do ABS a partir do zero. Este arquivo é o ponto de partida operacional para a próxima conversa.

## 22. FRASE DE CONTINUIDADE

O ABS está sendo construído agora, mas o ABS não termina agora.
A V1 é fundação. A construção continua por experimentos, evidências, integração, aprendizado e evolução.