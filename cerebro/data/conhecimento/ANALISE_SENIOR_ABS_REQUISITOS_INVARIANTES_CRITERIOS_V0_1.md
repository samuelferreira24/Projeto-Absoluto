# ANÁLISE SÊNIOR — ABS: REQUISITOS, INVARIANTES E CRITÉRIOS DE EXISTÊNCIA DE CAPACIDADES V0.1

Data: 2026-09-18
Status: pesquisa/análise; não normativa; aberta a revisão
Branch: base-cerebro-v0.1

## 1. Objetivo
Dar o passo seguinte ao mapa de 26 capacidades: descobrir quais propriedades são mais fundamentais, quais dependem de outras e como distinguir uma capacidade real de uma promessa ou aparência de capacidade.

## 2. Descoberta principal: capacidades podem ser organizadas em camadas
Uma organização preliminar, sem transformar isso em arquitetura fixa:

CAMADA A — IDENTIDADE E COMANDO
- identidade/continuidade;
- autoridade do Imperador;
- autorização;
- integridade;
- rastreabilidade.

CAMADA B — ESTADO E CONHECIMENTO
- percepção;
- estado atual;
- memória;
- conhecimento;
- histórico;
- contexto.

CAMADA C — INTELIGÊNCIA OPERACIONAL
- raciocínio;
- planejamento;
- decisão;
- verificação;
- avaliação de alternativas.

CAMADA D — CAPACIDADE DE AÇÃO
- ferramentas;
- execução;
- coordenação;
- aquisição de recursos;
- composição de capacidades.

CAMADA E — CONTINUIDADE E EVOLUÇÃO
- aprendizagem;
- adaptação;
- substituição;
- reconfiguração;
- recuperação;
- escala;
- reconstrução;
- evolução.

Essas camadas são uma forma de análise, não uma proposta de arquitetura definitiva.

## 3. O que parece ser mais fundamental
Três grupos aparecem como candidatos a fundamentos transversais:

### 3.1 Controle
Sem uma relação clara entre Imperador, comando, autorização e execução, a capacidade técnica não estabelece que o sistema esteja sob controle do Imperador.

Pesquisas atuais do NIST sobre agentes estão tratando identidade, autorização, auditoria, não-repúdio e controle de acesso como problemas específicos para agentes. Isso reforça a importância da separação entre capacidade e autoridade. citeturn1search0turn1search4

### 3.2 Continuidade
Se o ABS pode trocar componentes, localização, infraestrutura, modelos e meios, precisa existir alguma forma de continuidade de estado e identidade.

Pesquisas recentes sobre agentes de longa duração tratam explicitamente continuidade de estado como problema próprio, diferente de simplesmente armazenar histórico. citeturn1academia12turn1academia15

### 3.3 Capacidade de transformação
O ABS precisa conseguir transformar recursos disponíveis em capacidade operacional para uma missão.

Isso conecta aquisição, composição, execução, substituição e evolução.

## 4. Nova distinção: recurso, capacidade e autoridade
Esses três conceitos não devem ser misturados.

RECURSO = algo que pode ser utilizado.
CAPACIDADE = aquilo que o sistema consegue realizar.
AUTORIDADE = aquilo que o sistema está autorizado a determinar ou executar.

Exemplo:
- um servidor é recurso;
- executar código é capacidade;
- autorização para executar determinado código é autoridade.

Essa separação permite que o ABS troque recursos sem perder sua definição de capacidade ou sua cadeia de comando.

## 5. Nova distinção: capacidade declarada versus capacidade demonstrada
Uma capacidade só deve ser considerada estabelecida quando houver evidência de que ela pode ser exercida dentro de condições conhecidas.

Para análise do ABS, quatro estados são mais úteis:
- DECLARADA — afirma-se que a capacidade existe, mas não há demonstração suficiente;
- EXPERIMENTAL — existe demonstração limitada ou em ambiente controlado;
- OPERACIONAL — funciona de forma repetível dentro de condições definidas;
- RESILIENTE — continua funcionando ou pode ser recuperada diante de mudanças/falhas relevantes.

Essa classificação não é um ranking de valor. É um estado epistemológico/operacional.

## 6. Critério geral para provar uma capacidade
Uma capacidade pode ser descrita por cinco elementos:

1. ENTRADA — o que a capacidade recebe;
2. TRANSFORMAÇÃO — o que o sistema faz;
3. SAÍDA — qual resultado produz;
4. CONDIÇÕES — em quais condições funciona;
5. EVIDÊNCIA — como sabemos que funcionou.

Exemplo abstrato:
Capacidade: substituir um componente.
Entrada: componente indisponível + alternativa válida.
Transformação: localizar, validar, configurar e ativar alternativa.
Saída: serviço restaurado.
Condições: alternativa compatível e recursos suficientes.
Evidência: teste operacional + registro da substituição.

Isso permite começar a testar capacidades sem definir antecipadamente toda a arquitetura do ABS.

## 7. Dependências entre capacidades
Algumas capacidades parecem depender de outras.

Exemplo:
comando → interpretação → estado/conhecimento → planejamento → decisão → autorização → execução → observação → verificação → aprendizado.

Mas essa é apenas uma cadeia possível.

Uma missão simples pode não precisar de aprendizagem. Uma missão física pode exigir sensores. Uma missão de aquisição pode exigir identidade, autorização, pagamento e verificação. Uma missão distribuída pode exigir coordenação e recuperação.

Portanto, o mapa deve representar dependências condicionais, não um pipeline universal.

## 8. Descoberta importante sobre o “primeiro ABS”
Não é necessário implementar as 26 capacidades para iniciar o ABS.

Também não é correto concluir que uma capacidade isolada seja o ABS.

Uma hipótese operacional mais adequada é:

**o primeiro ABS deve ser a menor combinação de capacidades que permita ao sistema receber uma determinação do Imperador, agir sobre um ambiente real, registrar o resultado e manter continuidade suficiente para continuar a missão.**

Isso ainda é hipótese de trabalho.

## 9. Núcleo mínimo hipotético
Sem fechar arquitetura, um núcleo mínimo de capacidades poderia exigir:

1. comando;
2. identidade/continuidade;
3. estado/memória;
4. raciocínio/planejamento;
5. execução;
6. observação de resultado;
7. registro/proveniência;
8. controle/autorização.

Aprendizagem, aquisição de capacidades, substituição, escala e reconstrução podem inicialmente existir de maneira limitada e evoluir depois.

Não há evidência suficiente para afirmar que esta composição seja a única possível.

## 10. Controle deve ser verificável
A frase “o Imperador controla o ABS” precisa futuramente deixar de ser apenas uma afirmação conceitual e ganhar significado operacional.

Perguntas técnicas:
- como o comando legítimo é identificado?
- como uma ordem é autenticada?
- como uma ação é autorizada?
- como um componente subordinado recebe somente os privilégios necessários?
- como uma autorização pode ser revogada?
- como ações são registradas?
- como detectar tentativa de alteração da cadeia de autoridade?
- como manter controle quando componentes são substituídos?

O NIST atualmente enfatiza identidade, autorização granular, credenciais, auditoria e não-repúdio para agentes, e destaca riscos de privilégios excessivos e credenciais de longa duração. citeturn1search3turn1search8

## 11. Continuidade também precisa ser verificável
“O ABS continua sendo o mesmo” não pode depender somente do nome ou de uma etiqueta.

Será necessário pesquisar quais elementos poderiam formar uma continuidade verificável:
- identidade;
- estado autorizado;
- patrimônio de conhecimento;
- histórico/proveniência;
- configuração aceita;
- cadeia de autoridade;
- relações com componentes;
- versão/linhagem;
- mecanismos de recuperação.

Pesquisas recentes sobre memória persistente e continuidade de agentes mostram que manter informação histórica não é necessariamente suficiente para preservar estado operacional e autoridade. citeturn1academia12turn1academia15

## 12. Segurança não deve ficar somente dentro da inteligência
Uma conclusão importante da pesquisa externa é que segurança de agentes não pode depender exclusivamente do comportamento do modelo.

NIST destaca riscos que surgem da combinação entre modelos e sistemas de software, incluindo prompt injection, modelos comprometidos, ações inseguras e specification gaming, além da necessidade de restringir e monitorar acesso. citeturn0search3turn1search7

Para o ABS, isso reforça um princípio já presente na pesquisa anterior:

**o componente inteligente não deve ser a única camada responsável por proteger o sistema.**

## 13. Interoperabilidade como capacidade estratégica
NIST lançou em 2026 uma iniciativa específica para padrões de agentes com foco em interoperabilidade, protocolos abertos, identidade e segurança. citeturn1search10

Isso é relevante para o ABS porque reforça a direção de não depender de um único modelo, fornecedor ou protocolo.

Interoperabilidade, porém, deve ser tratada como capacidade do sistema, não como obrigação de adotar um padrão específico.

## 14. Mapa de lacunas conceitual
Comparando a visão atual com o que já existe no Cérebro, surgem quatro classes:

A — JÁ EXPERIMENTADO
- memória/conhecimento;
- execução;
- portas/ferramentas;
- orquestração;
- experiência/aprendizado;
- proveniência;
- controle parcial.

B — PARCIALMENTE EXISTENTE
- recuperação;
- persistência de estado operacional;
- substituição ampla de componentes;
- fallback;
- coordenação de múltiplos cérebros;
- continuidade operacional.

C — AINDA NÃO DEMONSTRADO COMO CAPACIDADE DO ABS
- aquisição geral de capacidades;
- reconstrução;
- mobilidade/reconfiguração independente de infraestrutura;
- continuidade sob substituição extrema;
- controle independente do meio;
- utilização heterogênea de recursos externos em escala.

D — AINDA CONCEITUAL
- evolução estrutural ampla;
- capacidade de operar através de futuros paradigmas tecnológicos;
- eventual desenvolvimento de inteligência geral por composição/evolução;
- formas avançadas de interface direta com o Imperador.

Essa classificação é inferência baseada no histórico do projeto, não uma auditoria completa do código atual.

## 15. Próximo teste conceitual
Antes de construir algo grande, cada capacidade fundamental deveria responder:

“Se eu remover o componente atual e fornecer outro meio, a capacidade continua existindo?”

Se sim, estamos provavelmente tratando uma capacidade.
Se não, talvez estejamos descrevendo uma implementação específica.

Esse teste é especialmente importante para:
- modelo;
- servidor;
- banco de dados;
- console;
- ferramenta;
- provedor;
- linguagem;
- rede;
- hardware.

## 16. Próximo passo recomendado
O próximo trabalho não precisa ser outra pesquisa ampla.

Deve ser uma **auditoria de capacidades do que já existe**:

CAPACIDADE DESEJADA
↓
IMPLEMENTAÇÃO ATUAL
↓
EVIDÊNCIA DISPONÍVEL
↓
LIMITAÇÃO
↓
LACUNA
↓
PRÓXIMO EXPERIMENTO

Isso finalmente conecta a expansão da visão com a construção real.

## 17. Conclusão
A pesquisa indica que o ABS pode avançar sem escolher ainda sua forma definitiva.

O que precisa começar a ser definido não é “qual arquitetura será o ABS?”, mas:

**quais capacidades precisam permanecer disponíveis para que qualquer arquitetura utilizada continue servindo ao ABS.**

A partir daqui, o projeto pode sair do modo predominantemente exploratório e entrar em um ciclo de descoberta experimental: definir uma capacidade, verificar o que já existe, identificar a lacuna, construir o menor experimento possível e aprender com o resultado.

## 18. Fontes externas principais
- NIST AI Agent Standards Initiative (2026): interoperabilidade, protocolos, identidade e segurança. citeturn1search10
- NIST Software and AI Agent Identity and Authorization (2026): identidade, autorização, auditoria e não-repúdio. citeturn1search0turn1search4
- NIST AI Agent Security RFI analysis (2026): ameaças específicas de agentes e necessidade de adaptar práticas de segurança. citeturn1search7
- NIST Agentic AI emerging threats and mitigations (2026): escopo de ferramentas, sandboxing, autorização, isolamento de memória, telemetria e proveniência. citeturn1search16
- NIST IR 8587 (2026): proteção de tokens, verificação, ciclo de vida e controle de acesso. citeturn1search8
- LiveMem (2026): continuidade de estado em agentes de longa duração. citeturn1academia12
- Beyond Memory (2026): continuidade como linhagem autorizada de estado. citeturn1academia15
- Taxonomy of Cognitive Capability Gaps (2026): estado persistente, autonomia orientada a objetivos, automonitoramento, interação ambiental, aprendizagem e adaptação. citeturn0academia13

## 19. Estado epistemológico
Fato/evidência: literatura e documentos externos sobre agentes, segurança, identidade, memória e continuidade.
Inferência: aplicação desses conceitos ao problema do ABS.
Hipótese: núcleo mínimo e invariantes de continuidade.
Não estabelecido: arquitetura final, conjunto definitivo de invariantes e definição operacional completa de controle pelo Imperador.
Não normativo: esta pesquisa não fecha decisões futuras.