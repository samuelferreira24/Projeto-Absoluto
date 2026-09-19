# RECONSTRUÇÃO HISTÓRICA — EVOLUÇÃO TÉCNICA DO SISTEMA V1
## 2026-09-19

Fonte: histórico Git e comparações entre commits do repositório `samuelferreira24/Sistema`.

## 1. PRIMEIRA BASE OBSERVÁVEL

Commit `7c73aaa9` (28/08) já continha um conjunto expressivo de componentes:

- memória/documentação;
- base de dados/busca;
- coleta;
- especialistas;
- Jetro;
- orquestrador;
- motor;
- sementes de conhecimento;
- PWA/Android em desenvolvimento.

A primeira observação importante é que o sistema já nasceu como um conjunto de subsistemas, não como uma única interface.

## 2. PRIMEIRA EXPANSÃO

`7c73aaa9 → cfd4aafa`

Foram adicionados os documentos e componentes principais, totalizando na comparação:

- MEMORIA.md
- NATIVO.md
- P1-SISTEMA-PROPRIO.md
- base.py
- build-android.yml
- capacitor.config.json
- coletor.py
- especialistas.py
- jetro.py
- motor.sh
- orquestrador.py
- package.json
- sementes

Depois, `cfd4aafa → fade2401` modificou fortemente `index.html` e adicionou `sistema-absoluto.zip`.

Isso mostra uma passagem rápida de núcleo técnico para uma interface/produto operacional.

## 3. FOCO INICIAL DA INTERFACE

Entre `fade2401` e `5788d863`, a maior parte das mudanças ocorreu em `index.html`.

Foram várias expansões consecutivas da interface.

Isso é relevante porque indica uma forte tentativa de transformar capacidades internas em uma experiência unificada para uso humano.

Não é possível, somente pelas mensagens de commit, afirmar que a interface foi a causa das falhas posteriores. Isso exigirá análise dos conteúdos e resultados.

## 4. SURGIMENTO DA CAMADA DE EXECUÇÃO E GOVERNANÇA

No salto `25bce60e → 5788d863`, aparecem simultaneamente:

- `executor.py` — 576 linhas adicionadas;
- `governanca.py` — 676 linhas adicionadas;
- modificações no orquestrador;
- grande expansão da interface;
- expansão do motor;
- `COMO-USAR.md`.

Esse é um ponto histórico importante.

O projeto passou a tratar explicitamente de:

**execução + governança + coordenação + interface.**

Isso é mais profundo que “fazer um chatbot”.

## 5. EXECUÇÃO COMEÇA A GANHAR CONTROLE

No salto seguinte:

`5788d863 → 29f11596`

houve:

- grande modificação do executor;
- nova modificação do orquestrador;
- criação de `ligar.sh`;
- expansão da interface.

Isso sugere uma tentativa de transformar o sistema de uma coleção de funções em algo operacionalmente acionável.

A relação causal ainda não deve ser afirmada sem ler os patches/conteúdos.

## 6. PONTE ENTRE CAMADAS

Em:

`b21eb5c2 → 37da0c8f`

foram adicionados/modificados:

- `ponte.py`;
- Capacitor;
- workflow Android;
- coletor;
- interface.

Depois:

`9ee3334e → a6f22a49`

a ponte continuou sendo modificada.

A ponte, portanto, não apareceu como detalhe periférico. Ela surgiu durante a tentativa de conectar partes diferentes do sistema.

## 7. CONTINUIDADE

`a6f22a49 → b4daddfb`

adicionou `arranque.sh`.

Depois:

`919850fc`

adicionou:

- TERMUX-PASSO-A-PASSO.md;
- rodar-coleta.sh;
- grandes alterações no coletor;
- grandes alterações na ponte;
- grandes alterações na interface.

Isso mostra uma linha clara de investigação:

**sistema → Android/Termux → execução contínua → coleta automática → ponte.**

## 8. SHIZUKU

Em:

`ef1a4e21 → 025d5245`

aparecem:

- `rish`;
- `rish_shizuku.dex`;
- mudança importante na interface.

Portanto, a busca por acesso Android mais profundo também possui antecedente histórico explícito no projeto antigo.

Isso não significa que Shizuku seja a solução atual. Significa que já houve uma investigação/implementação nessa direção.

## 9. EVOLUÇÃO FINAL OBSERVÁVEL

Nos últimos commits, a maior concentração de alterações continua em:

- `index.html`;
- `ponte.py`;
- `coletor.py`.

A interface recebe mudanças muito grandes, enquanto a ponte também evolui.

Isso reforça uma hipótese histórica:

> o projeto tentou resolver simultaneamente a experiência do usuário, a execução, a comunicação entre componentes, a coleta e a integração Android.

Ainda não devemos concluir que essa combinação era arquiteturalmente errada. Precisamos primeiro recuperar os experimentos e os resultados.

## 10. PRIMEIRA GRANDE DESCOBERTA HISTÓRICA

A evolução não foi:

`app → falhou → novo projeto`.

A evidência disponível mostra algo mais parecido com:

`núcleo`
→ `memória`
→ `coleta`
→ `orquestração`
→ `execução`
→ `governança`
→ `ponte`
→ `continuidade`
→ `Android`
→ `Shizuku`
→ `interface`.

Ou seja, várias capacidades que hoje estamos redescobrindo no ABS já haviam sido investigadas no Sistema.

## 11. SEGUNDA GRANDE DESCOBERTA

O histórico também mostra que o antigo projeto tentou resolver um problema que hoje aparece no ABS:

**como transformar capacidades separadas em um sistema operacionalmente coordenado.**

Isso aparece, em momentos diferentes, no orquestrador, executor, governança e ponte.

Ainda não devemos importar suas arquiteturas. Primeiro precisamos recuperar o que cada uma ensinou.

## 12. O QUE AINDA NÃO SABEMOS

O Git confirma alterações, mas não confirma sozinho:

- por que cada alteração foi feita;
- o que funcionou;
- o que falhou;
- qual hipótese foi validada;
- qual hipótese foi abandonada;
- qual problema era de software;
- qual problema era da plataforma;
- qual problema era de arquitetura;
- por que o usuário deixou de usar a plataforma.

Esses pontos precisam ser reconstruídos pelos conteúdos dos arquivos, sementes, ZIP e patches.

## 13. PRÓXIMA FASE

Agora a auditoria deve mudar de:

**“o que mudou?”**

para:

**“o que cada mudança tentou resolver e o que aprendemos?”**

A prioridade será recuperar os patches/conteúdos dos pontos de maior transformação:

1. criação de memória/base/coleta/orquestração;
2. surgimento de executor/governança;
3. criação da ponte;
4. continuidade Android;
5. Shizuku;
6. interface integrada;
7. documentos de uso e sementes.

## REGRA DE PRESERVAÇÃO

Nenhuma conclusão histórica será apagada ou substituída porque o Sistema antigo não funcionou como produto.

O objetivo é recuperar:

**ideias + hipóteses + implementações + experimentos + falhas + descobertas + decisões + conhecimento.**

## STATUS

Fase 0 — inventário: CONCLUÍDA.

Fase 0.5 — evolução estrutural: CONCLUÍDA EM PRIMEIRA PASSAGEM.

Próxima: **reconstrução semântica dos principais experimentos.**
