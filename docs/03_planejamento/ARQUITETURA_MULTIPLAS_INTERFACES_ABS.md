# ARQUITETURA DE MÚLTIPLAS INTERFACES — ABS

## 1. Objetivo

O ABS não deve depender de uma única interface.

A interface própria do ABS continua sendo uma frente estratégica de longo prazo, mas a V1 pode utilizar interfaces prontas de terceiros quando elas acelerarem o uso do sistema.

O princípio é:

```
IMPERADOR
    ↓
MÚLTIPLAS INTERFACES
    ↓
API / GATEWAY ABS
    ↓
ABS CORE
    ↓
CAPACIDADES / IAs / FERRAMENTAS
```

As interfaces são portas de entrada diferentes para o mesmo ABS. Elas não devem criar sistemas concorrentes nem duplicar a lógica central.

---

## 2. Princípio arquitetural

### Interface não é o ABS

Uma interface pode mudar, ser substituída, desaparecer ou ser utilizada apenas para uma função específica sem exigir reconstrução do núcleo.

Regra:

```
Interface → contrato/API ABS → ABS
```

e não:

```
Interface → lógica própria espalhada → dependência estrutural
```

Quando tecnicamente possível, terceiros entram por uma camada controlada pelo ABS.

---

## 3. Modelo de conjunto de interfaces

O ABS poderá utilizar simultaneamente interfaces diferentes, cada uma especializada em uma área.

| Área | Interface candidata | Função |
|---|---|---|
| Conversa / operação geral | Open WebUI | Porta de entrada geral para IA, ferramentas e conhecimento |
| Multi-IA / agentes | LibreChat | Conversas com múltiplos provedores, agentes e endpoints |
| Conhecimento / documentos | AnythingLLM | Bases documentais, RAG e conhecimento especializado |
| Workflows / agentes | Dify | Construção e operação de fluxos, agentes e automações |
| Experiência de conversa | LobeChat | Interface de interação com múltiplos modelos/provedores |
| IA local / experimentação | Jan | Ambiente complementar para modelos locais |
| Interface leve / customização | Chatbot UI e equivalentes | Entrada simples ou base para experiências específicas |
| Controle central | Interface própria ABS | Sala de comando do Imperador e integração nativa do ABS |

Esta tabela é um mapa de candidatos, não uma decisão de instalação.

---

## 4. Especialização por função

### 4.1 Conversa e operação geral

Uma interface como Open WebUI pode funcionar como uma porta de entrada ampla para conversar com o ABS e explorar capacidades disponíveis.

Objetivo:

- conversar;
- selecionar modelos;
- acessar conhecimento;
- utilizar ferramentas;
- testar capacidades;
- operar o ABS pelo navegador.

### 4.2 Multi-IA e agentes

LibreChat pode funcionar como uma bancada para múltiplos provedores, endpoints compatíveis e agentes.

Objetivo:

- testar diferentes motores;
- utilizar endpoints do ABS;
- comparar comportamentos sem alterar o núcleo;
- explorar agentes e integrações.

### 4.3 Conhecimento e documentos

AnythingLLM pode ser avaliado como camada/interface especializada para documentos e bases de conhecimento.

Objetivo:

- documentos;
- coleções de conhecimento;
- RAG;
- consulta especializada.

A memória oficial do ABS continua sendo responsabilidade do próprio ABS. Uma ferramenta externa não deve se tornar automaticamente a memória central.

### 4.4 Workflows e agentes

Dify pode ser avaliado como bancada de construção de workflows e agentes.

Objetivo:

- fluxos de várias etapas;
- processamento;
- agentes;
- automações;
- experimentação de processos.

O ABS continua sendo a autoridade arquitetural; Dify, quando usado, é uma capacidade auxiliar.

### 4.5 Interface de experiência

LobeChat e interfaces semelhantes podem ser avaliadas principalmente pela experiência de interação.

Objetivo:

- conversa;
- acesso móvel/web;
- múltiplos modelos;
- experiências alternativas.

### 4.6 IA local

Jan e outras ferramentas locais podem ser utilizadas para experimentação, teste e operação de modelos locais.

O ABS não deve depender da existência de Jan para operar sua IA local atual.

Atualmente a cadeia local já existente é:

```
llama.cpp → Qwen → ABS local-ai → ABS
```

### 4.7 Interface própria

A interface própria do ABS deve evoluir separadamente.

Ela não precisa tentar reproduzir imediatamente tudo o que ferramentas maduras de terceiros já fazem.

Seu papel de longo prazo é fornecer:

- comando do Imperador;
- visão do sistema;
- trabalhos;
- objetivos;
- capacidades;
- IAs;
- ferramentas;
- estado;
- memória;
- proveniência;
- autorização;
- execução;
- múltiplos canais;
- expansão futura.

---

## 5. Arquitetura de integração

Modelo-alvo:

```
                         IMPERADOR
                             │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
     Interface A        Interface B        Interface C
     conversa           agentes            documentos
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ↓
                    API / GATEWAY ABS
                             ↓
                         ABS CORE
                             ↓
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
             IA          FERRAMENTAS      DADOS
              ↓              ↓              ↓
          local/cloud      Termux/API     Cérebro
                             ↓
                         EXECUÇÃO
                             ↓
                       VERIFICAÇÃO
                             ↓
                     MEMÓRIA / LOGS
```

O ponto central é o ABS, não qualquer interface individual.

---

## 6. Critérios de avaliação

Antes de instalar uma interface, avaliar:

1. Compatibilidade com Android/Termux ou acesso por navegador.
2. Consumo de RAM e CPU.
3. Facilidade de implantação.
4. Compatibilidade com API OpenAI.
5. Compatibilidade com o Gateway ABS.
6. Suporte a múltiplos modelos.
7. Agentes.
8. Ferramentas.
9. MCP e integrações.
10. Arquivos.
11. RAG/conhecimento.
12. Uso offline/local, quando aplicável.
13. Experiência em tela pequena.
14. Facilidade de substituição.
15. Licença e restrições.
16. Manutenção do projeto.
17. Capacidade de rodar no celular ou ser deslocada para outro nó.
18. Possibilidade de coexistir com outras interfaces.

Nenhuma interface deve ser escolhida apenas por aparência.

---

## 7. Estratégia de implantação

### Fase A — levantamento

Mapear interfaces e suas capacidades.

**Não instalar todas.**

### Fase B — seleção experimental

Escolher um pequeno conjunto de interfaces que cubra funções diferentes.

Exemplo de categorias para teste:

- uma interface geral;
- uma multi-IA/agentes;
- uma de conhecimento/documentos;
- uma de workflows/agentes.

### Fase C — integração

Conectar as selecionadas ao Gateway/API ABS.

A interface deve consumir o ABS, não substituir o ABS.

### Fase D — avaliação real

Usar no celular e medir:

- consumo;
- velocidade;
- estabilidade;
- facilidade;
- capacidades;
- limitações;
- integração;
- manutenção.

### Fase E — consolidação

Manter somente as interfaces que tenham função real.

Interfaces redundantes podem ser removidas sem afetar o núcleo.

### Fase F — interface própria

Continuar construindo a interface própria ABS com base nas necessidades observadas no uso real.

---

## 8. Relação com terceiros

Terceiros são permitidos e desejáveis quando aceleram a construção.

Porém:

```
TERCEIRO = capacidade auxiliar
ABS = autoridade arquitetural
```

Uma interface externa pode ser substituída sem alterar:

- Work;
- Capability;
- Authorization;
- Adapter;
- Execution;
- Verification;
- Persistence;
- Provenance;
- Core.

---

## 9. Redundância

Múltiplas interfaces também podem funcionar como redundância de acesso.

Exemplo:

```
Interface própria
      ↓
Gateway ABS
      ↓
ABS

Open WebUI
      ↓
Gateway ABS
      ↓
ABS

LibreChat
      ↓
Gateway ABS
      ↓
ABS
```

Se uma interface for retirada, as demais continuam podendo acessar o mesmo sistema.

Isso evita transformar a interface em ponto único de falha.

---

## 10. Relação com o planejamento curto, médio e longo prazo

### Curto prazo

Usar interfaces prontas para acelerar a operação do ABS.

Prioridade:

**funcionar → testar → aprender.**

### Médio prazo

Criar uma arquitetura de múltiplas portas de entrada e contratos estáveis.

Prioridade:

**modularidade → substituição → redundância.**

### Longo prazo

Aumentar a capacidade da interface própria sem perder a possibilidade de utilizar interfaces externas quando forem úteis.

Prioridade:

**controle → liberdade → expansão.**

---

## 11. Regra permanente

O ABS não deve perguntar:

> “Qual é a interface definitiva?”

A pergunta correta é:

> “Quais interfaces são úteis para cada função, e como todas podem acessar o mesmo ABS sem prender sua arquitetura?”

A interface própria pode se tornar a principal experiência do Imperador, mas não precisa ser a única.

---

## 12. Estado do planejamento

**Status: planejamento aprovado para investigação e experimentação.**

Este documento não determina que todas as interfaces serão instaladas.

Próximo passo:

**auditar tecnicamente as candidatas, separar por função e selecionar um conjunto mínimo para testes no ambiente real do ABS.**

Este planejamento complementa:

`docs/03_planejamento/PLANO_ABS_V1_CURTO_MEDIO_LONGO_PRAZO.md`

e deve ser tratado como parte da estratégia de evolução do ABS.
