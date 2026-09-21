# RECONSTRUÇÃO CAUSAL DOS EXPERIMENTOS — SISTEMA V1
## Fase seguinte da recuperação histórica
## 2026-09-19

Objetivo: reconstruir o que o Sistema antigo descobriu por meio da sequência problema → hipótese → implementação → resultado → limitação → correção → descoberta.

## Regra epistemológica

EVIDÊNCIA = aparece diretamente em arquivo, estrutura ou histórico Git.
INTERPRETAÇÃO = leitura causal sustentada por múltiplas evidências.
HIPÓTESE = explicação ainda não comprovada.
HERANÇA = princípio que merece ser levado ao Mini-Cérebro/ABS para nova avaliação.

## E-001 — MEMÓRIA INDEPENDENTE DA INTERFACE

Problema: a memória poderia ficar presa ao aplicativo/casca.

Hipótese: se os dados tiverem contrato próprio, a interface poderá ser substituída sem reconstruir o patrimônio.

Implementação: MEMORIA.md define formato JSON, versão, blocos tipados, projetos, arquivos, Império, tabuleiro, compatibilidade entre versões e leitura/escrita por diferentes cascas.

Evidência: o documento declara que o dado deve sair inteiro sem precisar do app e que outra PWA, app nativo, workflow ou script deve conseguir ler/escrever o mesmo formato.

Resultado: confirmado como decisão arquitetural histórica.

Descoberta: memória pode ser tratada como contrato independente da interface.

Herança: muito alta para Mini-Cérebro e ABS.

## E-002 — MOTOR SUBSTITUÍVEL

Problema: o modelo usado pelo sistema não deveria determinar sua identidade.

Hipótese: uma interface compatível permite trocar motores remotos e locais.

Implementação: contrato HTTP compatível com OpenAI em POST /v1/chat/completions; P1-SISTEMA-PROPRIO.md também descreve motor local e remoto.

Resultado: confirmado como princípio histórico.

Descoberta: motor é meio substituível; memória, estado e estrutura são patrimônio do sistema.

Herança: muito alta.

## E-003 — CONTEXTO EXTERNO NÃO É ORDEM

Problema: conteúdo vindo da Internet, coleta ou anexos poderia ser confundido com instrução.

Hipótese: separar contexto de método, estado e decisão reduz esse risco.

Implementação: a tag CONTEXTO é explicitamente tratada como dado bruto e nunca como ordem.

Resultado: confirmado no contrato histórico.

Descoberta: o sistema precisa distinguir conhecimento, contexto, instrução, decisão e autoridade.

Herança: muito alta.

## E-004 — EXECUÇÃO PROTEGIDA

Problema: uma IA capaz de executar comandos pode transformar erro lógico em dano.

Hipótese: segurança deve estar no executor, não apenas no prompt.

Implementação: executor.py contém cerca de uma pasta de trabalho, snapshots, rollback, comandos proibidos, timeout, diário, bloqueios para sistema, proteção de credenciais, bloqueio de publicação e escalada para ações sensíveis.

Resultado: implementação histórica comprovada.

Descoberta: capacidade técnica não significa autorização.

Herança: muito alta.

## E-005 — GOVERNANÇA DA MALHA

Problema: uma malha fixa pode deixar de cobrir assuntos novos ou acumular falhas.

Hipótese: o sistema pode detectar lacunas, auditar decisões, propor manutenção e transformar resultados em calibragens.

Implementação: governanca.py possui EXPANSOR, AUDITOR, MANUTENÇÃO e APRENDIZ; também há teto de especialistas, especialista não verificado inicialmente e escalada de decisões estruturais para Samuel.

Resultado: mecanismo comprovado; funcionamento confiável prolongado não comprovado apenas pelo código.

Descoberta: governança pode ser capacidade separada da execução.

Herança: alta, como experimento a reavaliar.

## E-006 — ORQUESTRAÇÃO / ESPECIALISTAS

Problema: um único motor pode não cobrir todos os tipos de trabalho.

Hipótese: especialização mais maestro pode aumentar cobertura.

Implementação: orquestrador.py, especialistas.py e jetro.py.

Resultado: experimento comprovado; superioridade da arquitetura não comprovada.

Descoberta: capacidades podem ser compostas por motores/agentes especializados.

Herança: reinvestigar, não copiar.

## E-007 — LACUNAS COMO DADO

Problema: o estado “não sabemos” normalmente desaparece.

Hipótese: uma lacuna pode virar objeto operacional.

Implementação: lacunas.json, lacunas-dado.json, contadores, exemplos e busca de fontes.

Resultado: implementação histórica comprovada.

Descoberta: ausência de conhecimento pode virar estado observável.

Herança: alta para Mini-Cérebro.

## E-008 — PROVENIÊNCIA E QUALIDADE DE FONTES

Problema: coletar muito conteúdo não significa construir conhecimento confiável.

Hipótese: a fonte precisa ser registrada e ponderada.

Implementação: base.py registra fonte, domínio, tier, data, suspeição, uso, URL e conteúdo; a coleta diferencia fontes primárias, especializadas e agregadoras.

Resultado: implementação comprovada.

Descoberta: recuperação de conhecimento precisa preservar origem.

Herança: muito alta para Mini-Cérebro.

## E-009 — BUSCA EM CAMADAS

Problema: busca literal não encontra necessariamente conhecimento semanticamente relacionado.

Hipótese: combinar busca textual e semântica aumenta recuperação.

Implementação: FTS5, embeddings, combinação, peso de fonte e registro das buscas.

Resultado: implementação comprovada.

Descoberta: armazenar não basta; recuperação é capacidade independente.

Herança: alta.

## E-010 — CONTINUIDADE FORA DA INTERFACE

Problema: o app só operava quando aberto.

Hipótese: Termux, processos, boot e scheduler poderiam manter operação.

Implementação: Termux, arranque.sh, rodar-coleta.sh, ponte, motor local e processos.

Resultado: tentativa comprovada; funcionamento contínuo confiável em todas as condições não comprovado.

Descoberta: interface e continuidade operacional são problemas diferentes.

Herança: alta, com revalidação no Android atual.

## E-011 — MOTOR LOCAL NO CELULAR

Problema: dependência de motor remoto e Internet.

Hipótese: modelo local pequeno pode oferecer autonomia operacional básica.

Implementação documentada: llama.cpp, Termux, modelo 1–3B, endpoint local e fallback local/remoto.

Resultado: proposta comprovada; os testes de desempenho real descritos precisam de evidência adicional.

Descoberta: celular pode ser primeiro ambiente computacional local.

Herança: reinvestigar.

## E-012 — PONTE

Problema: componentes distintos precisavam conversar sem depender diretamente da interface.

Hipótese: uma camada intermediária própria reduz acoplamento.

Implementação: ponte.py com HTTP local, autenticação, rotas, tarefas e comunicação app ↔ Termux.

Resultado: implementação comprovada.

Descoberta: integração/ponte é capacidade própria.

Herança: muito alta para Dois Cérebros.

## E-013 — ANDROID COMO MEIO OPERACIONAL

Problema: era necessário sair da simples interface web e alcançar recursos do aparelho.

Hipótese: Android, Termux e Capacitor poderiam formar ambiente operacional.

Implementação: PWA, Capacitor, workflow Android, Termux, RISH/Shizuku e scripts.

Resultado: experimentação comprovada.

Descoberta: acesso ao Android não cria inteligência por si só.

Herança: alta.

## E-014 — PRIVILÉGIO NÃO DEVE SER HERDADO AUTOMATICAMENTE

Problema: Shizuku/RISH pode elevar capacidade de execução.

Hipótese: executor deve continuar protegido mesmo em ambiente privilegiado.

Implementação: executor.py detecta ambiente privilegiado e remove elementos relacionados ao RISH do ambiente do executor.

Resultado: implementação comprovada.

Descoberta: capacidade disponível não deve virar autorização automática para a IA.

Herança: muito alta.

## E-015 — CASCA SUBSTITUÍVEL

Problema: a interface estava se tornando grande e complexa.

Hipótese: interface deve ser apenas casca.

Evidência: MEMORIA.md declara que interface, modos, ferramentas e visual são escolhas da casca.

Resultado: princípio explicitamente registrado.

Descoberta: identidade do sistema pode sobreviver à troca da interface.

Herança: muito alta.

## EVOLUÇÃO HISTÓRICA

A linha mais sustentada pelas evidências é:

INTERFACE
→ MEMÓRIA
→ MOTOR
→ COLETA
→ BUSCA
→ ORQUESTRAÇÃO
→ EXECUÇÃO
→ GOVERNANÇA
→ PONTE
→ CONTINUIDADE
→ ANDROID
→ PRIVILÉGIO

Leitura mais profunda:

problema
→ criação de capacidade
→ limitação encontrada
→ nova camada
→ nova capacidade
→ nova limitação
→ nova camada.

Isso é compatível com a evolução observada.

## DESCOBERTAS TRANSVERSAIS

T-001: o patrimônio mais importante não é necessariamente o código.

T-002: o sistema antigo produziu contratos e princípios que sobreviveram às interfaces.

T-003: várias separações descobertas historicamente convergem com o ABS atual:
memória ≠ interface;
motor ≠ sistema;
capacidade ≠ autorização;
Android ≠ inteligência;
contexto ≠ ordem;
execução ≠ governança;
conhecimento ≠ fonte;
ponte ≠ interface.

T-004: o crescimento adicionou camadas sucessivas, mas a confiabilidade operacional dessas camadas não foi demonstrada igualmente.

T-005: o maior patrimônio histórico é a cadeia causal entre problema e solução.

## O QUE AINDA NÃO PODE SER AFIRMADO

Ainda não é possível afirmar com segurança:
- causa única do abandono do aplicativo;
- principal gargalo;
- ganho líquido da orquestração;
- robustez da continuidade;
- estabilidade do motor local no hardware real;
- quais falhas eram bug versus limitação Android/modelo/recurso;
- quais decisões vieram de experiência prática versus planejamento.

Essas questões exigem evidência adicional de commits, logs, versões e artefatos.

## PRÓXIMA OPERAÇÃO

Fechar as lacunas causais:

COMMIT QUE INTRODUZIU
→ COMMIT QUE MODIFICOU
→ VERSÃO DO CÓDIGO
→ DOCUMENTAÇÃO
→ RESULTADO REGISTRADO
→ FALHA
→ CORREÇÃO
→ VERSÃO POSTERIOR.

Prioridade:
1. Memória
2. Executor
3. Governança
4. Ponte
5. Continuidade Android
6. Orquestrador
7. Coleta/Base
8. Motor local
9. Shizuku/RISH
10. Interface/Capacitor

Estado: recuperação histórica → reconstrução causal em andamento.

Nenhuma arquitetura do ABS foi alterada por esta reconstrução.
