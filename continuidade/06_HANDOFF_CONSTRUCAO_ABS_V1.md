# HANDOFF — CONSTRUÇÃO DO ABS — V1

**Data:** 2026-09-21  
**Repositório principal:** `samuelferreira24/Projeto-Absoluto`  
**Repositório histórico:** `samuelferreira24/Sistema`  
**Branch operacional:** `main`  
**Commit observado neste handoff:** `fb7a1bbd2436a229887e45d7be4ae24149ae1c28`

---

# 1. OBJETIVO DESTE HANDOFF

Este documento permite que outra IA continue a construção do ABS sem reconstruir o projeto do zero.

**Não comece novamente. Inspecione o código real, os testes e os documentos de continuidade antes de alterar a arquitetura.**

O projeto já possui uma fundação operacional V1. O trabalho agora é **continuar a construção/evolução do ABS a partir do que existe**, usando o patrimônio histórico como evidência e não como arquitetura obrigatória.

---

# 2. O QUE É O ABS

Definição de trabalho atual:

> ABS — ABSoluto Sistema é o sistema sob controle do Imperador, criado para realizar aquilo que ele determina, utilizando, adquirindo, combinando, criando, substituindo ou desenvolvendo quaisquer capacidades, estruturas, recursos e meios necessários para isso.

Não reduzir ABS a:

- IA;
- AGI;
- agente;
- multiagente;
- aplicativo;
- Android;
- Cérebro;
- Codex;
- uma arquitetura fixa;
- Marte.

A forma técnica pode mudar.

Invariantes centrais:

- continuidade;
- controle pelo Imperador;
- capacidade de adaptar/adquirir/substituir meios;
- memória/conhecimento não dependentes de uma interface específica.

Método de raciocínio do projeto:

**PP + BN + AV**
- Primeiros Princípios;
- Bola de Neve;
- Avalanche.

---

# 3. ESTADO REAL DA CONSTRUÇÃO

Existe um **ABS Core V1 operacional** em `abs_core/`.

A fundação atual cobre:

1. intenção/comando;
2. Work persistente;
3. registro de capacidades;
4. orquestração;
5. execução;
6. estado/eventos;
7. resultado;
8. proveniência;
9. sessões;
10. continuidade operacional;
11. servidor/local;
12. bridge;
13. integração com Codex CLI;
14. atualização/rollback.

Arquivos principais:

```
abs_core/
├── adapters.py
├── api.py
├── bridge.py
├── capabilities.py
├── cli.py
├── codex_adapter.py
├── continuity.py
├── local.py
├── models.py
├── orchestrator.py
├── server.py
├── store.py
└── update_manager.py
```

**Não reorganizar `abs_core/` por estética sem verificar imports, entrypoints, scripts e testes.**

---

# 4. CAPACIDADE CODex

O primeiro adaptador real é o **Codex CLI local**.

Modelo:

```
Imperador
  ↓
Work
  ↓
ABS Orchestrator
  ↓
Capability
  ↓
Codex CLI
  ↓
resultado
  ↓
sessão/proveniência persistidas
```

O ABS chama o executável `codex`; não depende do SDK Python do Codex.

A sessão/thread pode ser persistida e reutilizada.

Configuração relevante:

- `ABS_CODEX_COMMAND`
- `ABS_CODEX_SANDBOX`
- `ABS_CODEX_APPROVAL`
- `ABS_CODEX_TIMEOUT`
- `ABS_CODEX_DANGEROUSLY_BYPASS`

**Nunca colocar credenciais/tokens no repositório.**

No ambiente Android/Termux existe uma limitação conhecida de sandbox Linux do Codex relacionada a proot/bwrap. Qualquer elevação deve ser explícita e restrita a workspace controlado.

---

# 5. CONTROLE E SEGURANÇA JÁ EXISTENTES

O Orchestrator diferencia capacidade de teste de capacidade externa.

Capacidades não-testes exigem aprovação explícita:

```
approved=True
```

Caso contrário:

```
work.denied
reason=imperator_approval_required
```

Princípio histórico mantido:

**capacidade disponível ≠ capacidade autorizada.**

Não remover essa separação.

---

# 6. CONTINUIDADE

Existe:

`abs_core/continuity.py`

Ela fornece checkpoint verificável do SQLite por snapshot + SHA-256.

Existe também Update Manager:

`abs_core/update_manager.py`

Com:

- `status`
- `check`
- `apply`
- `rollback`

O update:

1. verifica estado limpo;
2. identifica target;
3. registra rollback;
4. atualiza;
5. reinicia serviço;
6. verifica health;
7. faz rollback se necessário.

Não transformar atualização automática em mecanismo sem validação.

---

# 7. TESTES EXISTENTES

Existem testes do ABS em:

```
tests/
├── test_codex_cli_adapter.py
├── test_continuity.py
├── test_local.py
├── test_update_manager.py
└── test_vertical_slice.py
```

O vertical slice já testa:

- criação;
- execução;
- persistência;
- resume;
- substituição de capacidade;
- aprovação;
- sessão/proveniência.

Também existem testes históricos em:

```
cerebro/tests/
mini-cerebro/tests/
```

**Antes de alterar o núcleo, execute os testes e estabeleça a linha de base.**

---

# 8. CÉREBRO ATUAL

`cerebro/` contém conhecimento, estado, especificações, mapas e testes.

Estrutura relevante:

```
cerebro/
├── 00_estado/
├── data/
├── especificacao/
├── mapas/
├── estado.py
├── orquestrador.py
├── runtime.py
├── temporal.py
└── tests/
```

Os mapas existentes não devem ser substituídos por um novo mapa apenas para reorganizar o pensamento.

Há:

- mapa mestre;
- tabuleiro de 72 capacidades;
- quadro de pendências;
- plano de rede evolutiva.

Eles são instrumentos de orientação, não substitutos do código verificável.

---

# 9. MECANISMO DE DESCOBERTA

Existe uma decisão arquitetural importante:

```
planejamento
→ execução
→ observação
→ descoberta
→ pesquisa
→ reavaliação
→ cérebro/quadro
→ novo planejamento
```

Isso é permanente.

O ABS não deve assumir que o plano inicial contém todas as capacidades necessárias.

**Não criar um travamento fixo de rastreamento.**

---

# 10. MINI-CÉREBRO

`mini-cerebro/` é separado do ABS Core.

Função:

**investigar e preservar o patrimônio histórico do Sistema antigo.**

Não é simplesmente o Cérebro do ABS.

Estrutura:

```
mini-cerebro/
├── mini_cerebro/
│   ├── core.py
│   ├── github_source.py
│   ├── schema.sql
│   └── server.py
├── investigacoes/
└── tests/
```

Capacidades existentes/previstas:

- ingestão;
- ZIP;
- preservação;
- SHA-256;
- SQLite/FTS5;
- Git;
- classificação;
- claims/evidências;
- relações;
- busca;
- exportação;
- API local;
- aquisição GitHub.

Regra:

**fonte ≠ derivação.**

Não substituir o arquivo histórico por resumo ou interpretação.

---

# 11. SISTEMA ANTIGO

Repositório:

`samuelferreira24/Sistema`

Ele é tratado como **laboratório histórico de P&D**, não como arquitetura final.

O ZIP histórico:

`sistema-absoluto.zip`

Foi localizado e preservado.

Há reconstruções históricas sobre:

- memória independente da interface;
- busca;
- coleta;
- proveniência;
- executor protegido;
- governança;
- especialistas;
- orquestração;
- ponte;
- continuidade Android;
- Shizuku/RISH;
- PWA/Capacitor;
- motor substituível;
- motor local.

Mas:

**código histórico ≠ capacidade atual comprovada.**

**documentação histórica ≠ resultado operacional comprovado.**

---

# 12. DOIS CÉREBROS

Modelo provisório:

```
Imperador
   ↓
Cérebro ABS
   ↓
Ponte
   ↓
Mini-Cérebro
   ↓
patrimônio histórico
```

O Mini-Cérebro fornece:

- evidências;
- documentos;
- experimentos;
- falhas;
- descobertas;
- lacunas.

O ABS decide o que incorporar.

Não sincronizar cegamente todo o patrimônio histórico.

Se a ponte falhar:

- ABS continua;
- Mini-Cérebro continua.

---

# 13. DOCUMENTOS DE CONTINUIDADE — LEITURA PRIORITÁRIA

Antes de modificar arquitetura, ler:

1. `continuidade/00_LEIA_PRIMEIRO.md`
2. `continuidade/01_ESTADO_ATUAL_PROJETO.md`
3. `continuidade/02_MODELO_ABS_E_PRINCIPIOS.md`
4. `continuidade/03_HISTORICO_SISTEMA_ANTIGO_E_MINI_CEREBRO.md`
5. `continuidade/04_PONTO_EXATO_DE_PARADA.md`
6. `continuidade/05_DECISOES_CORRECOES_E_REGRAS.md`

Depois:

- `cerebro/00_estado/`
- `cerebro/especificacao/`
- `cerebro/mapas/`
- `docs/02_arquitetura/`
- `docs/04_referencia/`

Há uma transferência anterior dizendo que a construção definitiva ainda não deveria começar. **Esse registro é histórico do ponto anterior. O estado atual do repositório já possui ABS Core V1. Portanto, a IA deve reconciliar o documento com o código real, e não voltar artificialmente à estaca zero.**

---

# 14. O QUE JÁ FOI VALIDADO OPERACIONALMENTE

Registros anteriores indicam que a V1 já passou por verificações envolvendo:

- health local;
- execução/persistência;
- integração com Codex;
- bridge GitHub → Termux → ABS → Codex → GitHub;
- execução local;
- SQLite;
- continuidade Android;
- serviço Termux;
- Update Manager.

**Mesmo assim, a IA deve confirmar o estado atual executando os testes e inspeções atuais. Não confiar somente neste texto.**

---

# 15. PRÓXIMO TRABALHO DA IA

Não começar uma nova arquitetura.

Executar esta sequência:

### Fase A — Baseline
1. verificar branch/commit;
2. executar testes;
3. verificar health;
4. verificar serviço;
5. verificar Codex CLI;
6. verificar estado do Update Manager.

### Fase B — Auditoria do núcleo
Inspecionar:

- modelos;
- store;
- capabilities;
- orchestrator;
- Codex adapter;
- API/local;
- bridge;
- continuity;
- update manager.

Pergunta central:

> **Qual é a menor capacidade que falta para o ABS passar de fundação V1 para um sistema realmente capaz de conduzir a própria construção de forma controlada?**

### Fase C — Cruzamento com Cérebro
Comparar o núcleo atual com:

- mapa mestre;
- tabuleiro de 72 capacidades;
- pendências;
- especificações;
- mecanismo de descoberta.

Identificar lacunas reais, não inventadas.

### Fase D — Mini-Cérebro
Continuar a investigação histórica somente onde ela puder responder uma lacuna real do ABS.

Fluxo:

```
lacuna
→ pergunta
→ Mini-Cérebro
→ evidência
→ avaliação
→ decisão
→ implementação
→ teste
```

### Fase E — Construção incremental
Implementar a próxima capacidade real somente depois de:

- definir a necessidade;
- verificar alternativas;
- avaliar dependências;
- definir teste;
- implementar;
- testar;
- registrar resultado;
- atualizar conhecimento/estado.

---

# 16. REGRAS QUE NÃO DEVEM SER QUEBRADAS

1. Não apagar patrimônio histórico.
2. Não reescrever história para combinar com arquitetura atual.
3. Não transformar hipótese em fato.
4. Não transformar código em capacidade comprovada sem teste.
5. Não transformar documentação em prova operacional.
6. Não confundir capacidade com autorização.
7. Não tornar uma interface a identidade do ABS.
8. Não tornar Android a identidade do ABS.
9. Não tornar Codex a identidade do ABS.
10. Não tornar Cérebro a identidade do ABS.
11. Não assumir que uma arquitetura antiga é a arquitetura final.
12. Não criar travamentos fixos desnecessários.
13. Preservar substituibilidade de capacidades.
14. Manter continuidade.
15. Manter controle do Imperador.
16. Fazer mudanças pequenas, testáveis e reversíveis.
17. Verificar código real antes de contradizer documentos.
18. Quando houver conflito entre documentação histórica e comportamento atual, registrar o conflito e investigar.

---

# 17. CRITÉRIO DE TRABALHO SENIOR

Não perguntar:

> “Qual arquitetura parece mais bonita?”

Perguntar:

> “Qual capacidade falta, qual evidência temos, quais alternativas existem, qual é o menor experimento que reduz a incerteza e qual implementação deixa o sistema mais capaz sem retirar controle e continuidade?”

O objetivo não é produzir mais documentação.

O objetivo é:

**descobrir → decidir → construir → testar → aprender → continuar.**

---

# 18. PONTO DE PARTIDA

Comece pelo estado real do repositório `main`.

Não recrie:

- ABS Core;
- Mini-Cérebro;
- mapas;
- continuidade;
- histórico;
- integração Codex.

Eles já existem.

**A próxima IA deve primeiro validar o que existe e depois continuar a construção.**
