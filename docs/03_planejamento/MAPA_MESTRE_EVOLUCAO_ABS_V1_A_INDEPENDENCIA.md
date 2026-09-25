# MAPA MESTRE DE EVOLUÇÃO DO ABS
## Da primeira V1 operacional à independência progressiva

> Mapa de direção. Não é uma especificação técnica congelada. Seu objetivo é mostrar **para onde o ABS deve evoluir**, quais capacidades entram em cada etapa e quando faz sentido trocar peças de terceiros por capacidades próprias.

---

## 0. PRINCÍPIO DE EVOLUÇÃO

O ABS não precisa nascer completo.

A estratégia é:

**operar cedo → aprender com o uso → fortalecer o núcleo → criar camadas próprias → reduzir dependências críticas → substituir peças quando fizer sentido → ampliar a capacidade do sistema.**

Terceiros são permitidos como aceleradores.

O objetivo não é "possuir tudo" por princípio. O objetivo é **não ficar estruturalmente limitado por aquilo que o ABS usa**.

---

# FASE 1 — V1 OPERACIONAL HÍBRIDA

### Objetivo
Colocar o ABS para funcionar de verdade o mais cedo possível.

### Composição
**Próprio:**
- ABS Core
- API/contratos
- Work/Missão
- Capabilities
- Autorização
- Adaptadores
- Orquestração
- Persistência inicial
- Proveniência/logs
- Cérebro como camada de conhecimento
- Interface do Imperador

**Terceiros:**
- modelos de IA
- OpenRouter e/ou APIs diretas
- serviços externos necessários
- n8n quando acelerar automações
- VPS quando necessário

**Base:**
- Android
- Termux
- Internet

### Fluxo obrigatório
**Imperador → Interface → ABS → Cérebro/IA → Planejamento → Execução → Verificação → Memória → Resultado**

### Saída da fase
O ABS consegue receber e realizar missões reais, com controle humano e registro do que aconteceu.

---

# FASE 2 — V1 CONSOLIDADA

### Objetivo
Transformar a primeira operação em uma base confiável.

### Construir
- contratos estáveis;
- adaptadores mais fortes;
- tratamento de erros;
- timeout;
- retry controlado;
- idempotência;
- recuperação após interrupção;
- testes de integração;
- observabilidade;
- backups;
- continuidade;
- múltiplos motores;
- fallback;
- controle de custos;
- melhoria da interface.

### Regra
Nenhum terceiro deve ficar espalhado pelo núcleo.

Preferência:

**ABS → camada própria → terceiro**

e não:

**ABS → terceiro diretamente em vários pontos.**

### Saída da fase
O ABS continua funcionando mesmo quando um componente externo falha ou precisa ser trocado.

---

# FASE 3 — V2 MODULAR

### Objetivo
Fazer cada capacidade importante ser substituível.

### Camadas próprias
- AI Layer
- Data Layer
- Execution Layer
- Tool Layer
- Identity/Authorization Layer
- Automation Layer
- Storage Layer
- Interface Layer
- Network/Node Layer

### Resultado
Cada camada passa a ter um contrato próprio.

Exemplo:

**ABS → AI Layer → OpenRouter**

pode virar:

**ABS → AI Layer → API direta**

ou:

**ABS → AI Layer → modelo local**

sem reconstruir o ABS.

### Saída da fase
Fornecedor deixa de ser parte da arquitetura. Passa a ser apenas implementação.

---

# FASE 4 — SUBSTITUIÇÃO ESTRATÉGICA

### Objetivo
Começar a possuir internamente as capacidades que se tornaram estratégicas.

Não substituir tudo.

Substituir aquilo que apresentar combinação relevante de:

- dependência;
- custo;
- limitação;
- risco;
- falta de controle;
- necessidade de escala;
- necessidade de privacidade;
- dificuldade de evolução;
- importância estratégica.

### Possíveis substituições
- roteamento externo → roteamento próprio;
- automação externa → automação própria em áreas críticas;
- armazenamento externo → camada própria;
- serviços de integração → adaptadores próprios;
- ferramentas externas → ferramentas próprias quando necessário;
- modelos externos → modelos locais/próprios onde houver benefício real.

### Saída da fase
As peças estratégicas começam a ser controladas pelo ABS.

---

# FASE 5 — ABS COM CAPACIDADES PRÓPRIAS AMPLIADAS

### Objetivo
Ter uma parcela significativa da infraestrutura e das capacidades críticas sob controle próprio.

### Possíveis peças próprias
1. Núcleo
2. Orquestrador
3. Cérebro
4. Memória
5. Banco de dados/camada de dados
6. Sistema de arquivos
7. Roteador de motores
8. Integração de motores
9. AV/verificação
10. Planejamento
11. Execução
12. Ferramentas
13. Interface
14. API
15. Logs/monitoramento
16. Autenticação
17. Autorização
18. Backups/continuidade
19. Adaptadores
20. Motor(es) de IA próprios/local
21. Equivalente próprio ao roteamento externo
22. Automação própria
23. Infraestrutura própria ou controlada
24. Rede entre nós
25. Sistemas de execução remota

### Observação
"Próprio" não significa necessariamente desenvolvido do zero.

Pode significar:
- código próprio;
- serviço próprio;
- modelo local;
- infraestrutura controlada;
- componente open source incorporado e adaptado;
- sistema desenvolvido especificamente para o ABS.

O critério é **controle e substituibilidade**, não autoria absoluta de cada linha de código.

---

# FASE 6 — ABS INDEPENDENTE E REDUNDANTE

### Objetivo
Eliminar pontos únicos de dependência nas capacidades críticas.

### Características
- múltiplos motores;
- múltiplos provedores;
- múltiplos nós;
- múltiplos caminhos de acesso;
- backups;
- recuperação;
- redundância;
- ferramentas alternativas;
- execução local e remota;
- modelos externos e locais;
- capacidade de operar mesmo quando partes da infraestrutura falham.

### Princípio
Não criar uma nova dependência única enquanto elimina uma antiga.

---

# FASE 7 — ABS EXPANSÍVEL

### Objetivo
O ABS deixa de ser definido pelas peças que existem hoje.

Ele passa a ser uma arquitetura capaz de:

**descobrir → adquirir → integrar → testar → usar → substituir → criar → melhorar capacidades.**

Nesta etapa, novas tecnologias podem entrar sem obrigar o ABS a mudar sua identidade arquitetural.

---

# MAPA DE TRANSFORMAÇÃO DAS PEÇAS

| Peça/capacidade | V1 | Médio prazo | Longo prazo |
|---|---|---|---|
| Núcleo | Próprio | Consolidado | Próprio |
| Orquestração | Próprio + terceiros | Camada própria | Própria |
| Cérebro | Próprio + IA externa | Multi-motor | Maior independência |
| Memória | Local | Camada de dados robusta | Própria/controlada |
| Banco | SQLite | PostgreSQL/alternativas se necessário | Camada independente |
| IA | APIs/OpenRouter | Roteamento próprio | Local/própria quando justificar |
| Automação | n8n opcional | Adaptada ao ABS | Automação própria crítica |
| Execução | Termux + APIs | Local + VPS | Rede de nós |
| Interface | Web/mobile | Sala de comando | Múltiplas interfaces |
| Arquivos | filesystem | armazenamento estruturado | infraestrutura própria/controlada |
| Rede | Internet | nós remotos | rede redundante |
| Infraestrutura | celular | celular + VPS | infraestrutura distribuída |
| Verificação | testes/AV | verificação robusta | sistema próprio de AV |
| Backup | Git/local | múltiplos destinos | redundância completa |
| Autorização | própria | refinada | própria |
| Adaptadores | próprios | contratos estáveis | substituição contínua |

---

# CRITÉRIO PARA AVANÇAR DE FASE

Não avançar apenas porque passou tempo.

Avançar quando a fase anterior estiver suficientemente operacional e houver necessidade real.

### Gatilhos
**V1 → V1 consolidada**
quando o ciclo operacional funcionar e os principais problemas reais forem conhecidos.

**V1 consolidada → V2**
quando dependências e contratos começarem a limitar evolução.

**V2 → substituição estratégica**
quando existir uma peça externa que se tornou gargalo relevante.

**Substituição → capacidades próprias ampliadas**
quando possuir internamente trouxer vantagem concreta.

**Capacidades próprias → independência**
quando houver necessidade de redundância, escala ou autonomia.

---

# REGRA DE OURO

**Não construir tudo antes de operar.**

**Não depender estruturalmente de terceiros depois que eles se tornarem uma limitação.**

**Não substituir terceiros apenas por orgulho de ter algo próprio.**

A trajetória correta é:

**TERCEIROS PARA ACELERAR → CAMADAS PRÓPRIAS PARA CONTROLAR → SUBSTITUIÇÃO ONDE NECESSÁRIO → CAPACIDADES PRÓPRIAS PARA AMPLIAR → REDUNDÂNCIA PARA NÃO FICAR LIMITADO.**

---

# VISÃO FINAL

O objetivo não é chegar a uma versão "final".

O objetivo é criar um ABS que consiga continuar evoluindo.

**V1**
→ funciona.

**V1 consolidada**
→ funciona com confiabilidade.

**V2**
→ é modular.

**V3**
→ reduz dependências.

**V4**
→ possui capacidades estratégicas próprias.

**V5+**
→ é redundante, expansível e capaz de incorporar novas capacidades.

**Princípio permanente:**

> O ABS deve permanecer sob controle do Imperador, independentemente das tecnologias, fornecedores, modelos, dispositivos ou infraestruturas usados em cada etapa.
