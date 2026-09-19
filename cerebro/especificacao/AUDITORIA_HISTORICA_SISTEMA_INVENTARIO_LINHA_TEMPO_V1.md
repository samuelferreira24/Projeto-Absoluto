# AUDITORIA HISTÓRICA — INVENTÁRIO E LINHA DO TEMPO V1
## Sistema antigo → Mini-Cérebro → Projeto Absoluto
## 2026-09-19

> Documento complementar e não destrutivo. O repositório histórico não foi alterado.

## 1. INVENTÁRIO REAL DA RAIZ

A árvore `main` do repositório `samuelferreira24/Sistema` retornou 31 itens e não está truncada.

### Documentação
- COMO-USAR.md
- MEMORIA.md
- NATIVO.md
- P1-SISTEMA-PROPRIO.md
- TERMUX-PASSO-A-PASSO.md

### Núcleo Python
- base.py
- coletor.py
- especialistas.py
- executor.py
- governanca.py
- jetro.py
- orquestrador.py
- ponte.py
- semente.py

### Operação/Shell
- arranque.sh
- ligar.sh
- motor.sh
- rodar-coleta.sh
- rish

### Estado/configuração/web
- index.html
- manifest.json
- sw.js
- capacitor.config.json
- package.json
- build-android.yml

### Memória/sementes
- semente-nucleo.json
- semente-operacao.json

### Recursos Android
- rish_shizuku.dex

### Arquivos auxiliares
- .gitignore
- icon-192.png
- icon-512.png

### Artefato adicional
- sistema-absoluto.zip

## 2. CONSTATAÇÃO IMPORTANTE

A raiz atual contém muito mais que uma aplicação.

Ela contém simultaneamente:

1. documentação conceitual;
2. memória;
3. coleta de conhecimento;
4. busca/indexação;
5. orquestração;
6. especialistas;
7. execução controlada;
8. governança;
9. ponte de comunicação;
10. automação Android/Termux;
11. interface web/PWA;
12. empacotamento Android;
13. sementes de conhecimento;
14. integração experimental com Shizuku;
15. um ZIP do sistema.

Portanto, o enquadramento como “aplicativo antigo” é insuficiente. O repositório é um registro de várias camadas de experimentação.

## 3. HISTÓRICO GIT

A consulta ao histórico atual retornou 31 commits entre 2026-08-28 e 2026-09-08.

O histórico contém principalmente mensagens genéricas `Add files via upload`, portanto a mensagem de commit, isoladamente, não explica a evolução conceitual.

Isso muda a estratégia da auditoria:

**não podemos reconstruir a história apenas pelas mensagens dos commits.**

Precisamos cruzar:
- árvore de cada etapa;
- alterações de arquivos;
- conteúdo dos documentos;
- código;
- sementes;
- ZIP;
- datas.

## 4. LINHA DO TEMPO INICIAL

### 28/08
Primeiros commits disponíveis no histórico atual.

### 29/08
Grande sequência de uploads e uma atualização via app.
O projeto já apresenta evolução de múltiplas partes.

### 03–05/09
Nova sequência intensa de alterações/upload.
A arquitetura e os componentes foram sendo acumulados.

### 08/09
Três uploads finais no histórico atual, chegando à árvore que hoje contém 31 itens.

Esta linha do tempo é somente a camada factual disponível pelo Git. A interpretação do que mudou em cada ponto ainda precisa ser reconstruída por comparação de árvores/arquivos.

## 5. DESCOBERTA SOBRE O CONECTOR

Foi possível obter diretamente a árvore Git recursiva completa da branch `main`.

Ela retornou:

- `truncated: false`
- 31 itens
- SHA da árvore atual.

Isso é diferente do code search.

Portanto:

**o conector consegue acessar a estrutura do repositório mesmo quando o índice de busca de código não está disponível.**

Essa descoberta abre uma estratégia melhor para o Mini-Cérebro:
**usar Git como fonte primária de inventário e busca estrutural, sem depender exclusivamente do code search.**

## 6. CONSEQUÊNCIA ARQUITETURAL

O Mini-Cérebro não precisa depender de:

`GitHub code search → resultado`.

Pode trabalhar com:

`Git repository → tree → blobs → index próprio`.

Assim ele cria seu próprio índice sobre a fonte histórica.

## 7. ANTECEDENTES JÁ IDENTIFICADOS

O inventário confirma a existência de antecedentes para:

### Memória
`MEMORIA.md`, `semente-nucleo.json`, `semente-operacao.json`, `semente.py`

### Conhecimento/coleta
`coletor.py`, `base.py`

### Inteligência/orquestração
`orquestrador.py`, `especialistas.py`, `jetro.py`

### Execução/governança
`executor.py`, `governanca.py`

### Comunicação
`ponte.py`

### Continuidade Android
`arranque.sh`, `ligar.sh`, `rodar-coleta.sh`, `rish`

### Interface/plataforma
`index.html`, `manifest.json`, `sw.js`, Capacitor e workflow Android.

## 8. HIPÓTESE DE HERANÇA

O Mini-Cérebro provavelmente não deverá ser construído como uma peça completamente nova.

Há pelo menos quatro patrimônios a investigar:

**A — patrimônio de dados**
base/memória/indexação.

**B — patrimônio de ingestão**
coleta/normalização/proveniência.

**C — patrimônio de raciocínio operacional**
orquestração/especialistas/governança.

**D — patrimônio de integração**
ponte/Termux/Shizuku/Android.

Cada patrimônio precisa de auditoria própria antes de qualquer reutilização.

## 9. PRÓXIMA OPERAÇÃO

A próxima etapa da auditoria deve ser uma comparação histórica de árvores.

Objetivo:

`commit → árvore → arquivos adicionados/removidos/modificados → mudança de arquitetura`.

Depois:

`mudança técnica → mudança conceitual → decisão/hipótese → resultado`.

## 10. REGRA

Não interpretar “upload” como uma decisão arquitetural.

A decisão deve ser inferida somente quando houver evidência documental, código, mudança estrutural ou combinação verificável dessas fontes.

## STATUS

**Fase 0: inventário estrutural concluída.**

**Fase 0.5: linha do tempo factual iniciada.**

**Próximo passo: reconstrução das mudanças entre versões e recuperação dos relatórios/conclusões escondidos na evolução do repositório.**
