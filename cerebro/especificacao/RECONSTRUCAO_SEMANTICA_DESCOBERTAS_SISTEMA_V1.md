# RECONSTRUÇÃO SEMÂNTICA — DESCOBERTAS DO SISTEMA ANTIGO V1
## Sistema → Mini-Cérebro → ABS
## 2026-09-19

Esta etapa lê o conteúdo dos principais artefatos históricos para separar **descoberta** de **implementação**.

## 1. DESCOBERTA CENTRAL: A MEMÓRIA NÃO PERTENCE À CASCA

`MEMORIA.md` formula explicitamente que o dado deve poder sair inteiro sem depender do app.

A especificação define:
- formato de memória externo à interface;
- versões do formato;
- compatibilidade;
- migração;
- separação entre método/estado/princípio/decisão/calibragem/lição e CONTEXTO;
- CONTEXTO como dado bruto, nunca como ordem.

### Significado histórico
A ideia não era simplesmente “guardar memória”.

Era criar **independência entre memória e interface**.

Isso é diretamente relevante para o Mini-Cérebro e para o ABS atual.

### Herança conceitual possível
**Alta relevância.**

Não significa copiar o JSON V5. O princípio é mais importante que o formato específico:

> conhecimento/estado deve sobreviver à troca da casca.

## 2. DESCOBERTA: MOTOR É SUBSTITUÍVEL

A documentação estabelece que qualquer motor que aceite HTTP compatível pode ser usado.

As decisões e lições também registram:
- motor local;
- motores remotos;
- troca de motor;
- memória própria como fator de independência.

### Significado
A inteligência do sistema não deveria ficar presa a um fornecedor/modelo.

### Relação com ABS
Isso converge diretamente com a regra atual:

**próprio quando útil; emprestado quando melhor; substituível quando necessário.**

## 3. DESCOBERTA: EXECUÇÃO E AUTORIZAÇÃO SÃO DIFERENTES

`executor.py` possui uma camada de proteção para:
- snapshot antes de alteração;
- rollback;
- comandos proibidos;
- bloqueio de operações sensíveis;
- escalada para aprovação humana em ações de alto impacto.

A documentação registra explicitamente que uma capacidade disponível não implica autorização para a IA utilizá-la.

### Significado
O projeto antigo já havia encontrado uma distinção fundamental:

**“consegue fazer” ≠ “pode fazer”.**

### Relação com ABS
Alta relevância para o núcleo de autorização do ABS.

## 4. DESCOBERTA: CONTEXTO EXTERNO NÃO É INSTRUÇÃO

A memória define `CONTEXTO` como dado bruto e não confiável.

Conteúdo externo pode ser coletado, mas não deve virar comando.

### Significado
Isso é uma forma explícita de separação entre:
- conhecimento;
- instrução;
- autoridade.

### Relação com ABS
Alta relevância para Cérebro, coleta, ferramentas e futura ponte entre cérebros.

## 5. DESCOBERTA: COLETA PRECISA DE PROVENIÊNCIA

O coletor registra origem, domínio, fonte, data e sinais de conteúdo suspeito.

A base também diferencia fontes por nível e registra uso.

### Significado
O sistema não trata informação coletada como verdade simplesmente porque foi encontrada.

### Relação com Mini-Cérebro
Muito alta.

O Mini-Cérebro histórico precisa preservar:
**de onde veio → quando veio → qual versão → qual evidência → qual interpretação posterior.**

## 6. DESCOBERTA: BUSCA TEM MAIS DE UMA CAMADA

`base.py` combina:
1. busca textual;
2. busca semântica;
3. combinação ponderada pela qualidade da fonte.

Também registra consultas e utilização dos resultados.

### Significado
O projeto antigo já distinguia:
**armazenar informação ≠ conseguir recuperá-la.**

### Relação com Mini-Cérebro
Alta.

O Mini-Cérebro deve nascer como sistema de recuperação, não como simples pasta de arquivos.

## 7. DESCOBERTA: LACUNAS PODEM SER OBSERVADAS

A base registra buscas e quantos resultados foram encontrados.

O coletor e o tabuleiro também registram lacunas.

### Hipótese importante
O sistema estava começando a tratar **“não encontrei conhecimento suficiente”** como informação operacional.

Isso merece investigação adicional antes de ser incorporado ao ABS.

## 8. DESCOBERTA: ORQUESTRAÇÃO NÃO É UMA ÚNICA IA

`orquestrador.py`, `especialistas.py` e `jetro.py` experimentam divisão de trabalho.

O fluxo histórico inclui coleta, análise, especialistas, integração, filtro, decisão, registro e aprendizado.

### Significado
O sistema antigo investigava composição de capacidades.

### Cuidado
Não concluir que a arquitetura de múltiplos agentes deve ser usada pelo ABS.

A descoberta é mais abstrata:

> tarefas diferentes podem ser distribuídas entre capacidades especializadas e posteriormente integradas.

## 9. DESCOBERTA: PONTE É UMA CAPACIDADE PRÓPRIA

`ponte.py` cria uma interface local entre partes do sistema.

Isso demonstra uma preocupação recorrente:

**como fazer componentes independentes cooperarem sem fundi-los em uma única peça.**

### Relação com dois cérebros
Muito alta.

A ideia atual de Bridge entre Cérebro ABS e Mini-Cérebro possui um antecedente técnico claro.

Mas a ponte antiga deve ser tratada como experimento, não como contrato final.

## 10. DESCOBERTA: CONTINUIDADE NO ANDROID É UM PROBLEMA DISTINTO

`arranque.sh`, `rodar-coleta.sh`, Termux e P1 tratam da operação sem depender da interface aberta.

O documento P1 chama a interface de “cabine” e o sistema contínuo de “casa de máquinas”.

### Significado
O projeto já diferenciava:

**interface de uso ≠ sistema operacional subjacente.**

Essa distinção é muito importante para o ABS atual.

## 11. DESCOBERTA: O ANDROID ERA MEIO, NÃO INTELIGÊNCIA

`NATIVO.md` registra explicitamente que aumentar acesso ao Android muda acesso, não inteligência.

Isso converge fortemente com a investigação atual:

**controle do Android ≠ inteligência do ABS.**

Android pode ser território, infraestrutura ou camada integrada sem definir sozinho o que é o ABS.

## 12. DESCOBERTA: FALHAS DE PLATAFORMA E FALHAS DE ARQUITETURA DEVEM SER SEPARADAS

O material histórico contém várias decisões baseadas em limites reais de:
- RAM;
- motor local;
- Android;
- armazenamento;
- background;
- disponibilidade de APIs;
- ferramentas externas.

Isso mostra a necessidade de separar:

`falha do código`
`falha da arquitetura`
`limitação do recurso`
`limitação da plataforma`
`limitação do modelo`.

Esta separação deve entrar no Mini-Cérebro como dimensão histórica.

## 13. DESCOBERTA: CONSTRUÇÃO ANTES DA VALIDAÇÃO PODE INVERTER A ORDEM

As próprias LIÇÕES históricas registram que houve construção da ferramenta antes da validação do “Sistema Próprio”.

Isso não significa que a construção foi inútil.

Significa que o projeto identificou um problema de sequência:

**produto/casca pode avançar enquanto o núcleo operacional ainda não está comprovado.**

### Relação com ABS
Isso reforça a decisão atual de:
**mapear → pesquisar → validar → construir.**

## 14. O QUE O SISTEMA ANTIGO JÁ TINHA DESCOBERTO

Primeira lista consolidada:

| Descoberta | Relevância atual |
|---|---|
| Memória independente da interface | Alta |
| Motor substituível | Alta |
| Capacidade ≠ autorização | Alta |
| CONTEXTO externo ≠ comando | Alta |
| Proveniência da informação | Alta |
| Busca textual + semântica | Alta |
| Registro de lacunas | Média/Alta |
| Especialização/orquestração | Média/Alta |
| Ponte entre componentes | Alta |
| Interface ≠ sistema operacional | Alta |
| Android ≠ inteligência | Alta |
| Limitação de recurso ≠ falha de conceito | Alta |
| Validação antes de expansão | Alta |

## 15. O QUE AINDA NÃO DEVE SER HERDADO

Ainda não há evidência suficiente para declarar como arquitetura do ABS:

- PWA;
- Capacitor;
- formato JSON V5;
- Jetro;
- múltiplos agentes como arquitetura permanente;
- Shizuku;
- llama.cpp;
- n8n;
- VPS;
- interface atual;
- estrutura do antigo orquestrador.

Esses são **implementações ou experimentos históricos**.

## 16. PRIMEIRO MAPA DE HERANÇA

### Princípios
→ preservar e investigar.

### Descobertas
→ incorporar ao conhecimento do ABS após validação.

### Código
→ auditar antes de reutilizar.

### Falhas
→ preservar como conhecimento.

### Decisões antigas
→ manter como decisões históricas, não como ordens atuais.

### Hipóteses
→ reabrir quando ainda relevantes.

### Interface
→ tratar como casca substituível.

## 17. NOVA FUNÇÃO DO MINI-CÉREBRO

A partir desta auditoria, o Mini-Cérebro não é apenas:

**“buscador do repositório”.**

Ele precisa conseguir responder:

> O que já tentamos?

> Por que tentamos?

> O que descobrimos?

> O que falhou?

> O que funcionou?

> Em qual versão?

> Qual era a evidência?

> O que foi apenas hipótese?

> O que o ABS atual já incorporou?

> O que ainda não foi revisitado?

Essa é a função histórica que diferencia o Mini-Cérebro de um simples RAG.

## STATUS

**Fase 0.5 — reconstrução semântica: iniciada e primeira camada concluída.**

Próxima etapa:

**transformar essas descobertas em uma matriz de conhecimento histórico com evidência e relações entre elas.**

Somente depois disso começaremos a construir o Mini-Cérebro V0.
