# AUDITORIA DE PRÉ-CONSTRUÇÃO — FECHAMENTO DA INVESTIGAÇÃO V1
## Projeto Absoluto / Sistema histórico / Dois Cérebros
## 2026-09-19

## Objetivo

Determinar se a investigação já atingiu condições suficientes para começar construção.

Regra: nenhuma implementação nova do ABS é autorizada por este documento. Ele apenas registra evidência, lacunas e o que precisa ser conhecido antes da construção.

## 1. PATRIMÔNIO HISTÓRICO RECUPERADO

O repositório `samuelferreira24/Sistema` possui:
- 31 itens na árvore principal analisada;
- histórico principal de 31 commits entre 28/08/2026 e 08/09/2026;
- branch adicional `cerebro-direct-bridge`;
- uma Pull Request aberta relacionada à comunicação direta App ↔ Cérebro;
- 31 execuções de GitHub Pages registradas, com as execuções observadas concluídas com sucesso;
- nenhum release formal encontrado;
- nenhuma issue encontrada no repositório no levantamento atual.

A ausência de issues/releases não significa ausência de problemas; apenas significa que eles não foram registrados nesses mecanismos.

## 2. NOVA DESCOBERTA: O PROJETO CONTINUOU APÓS O HISTÓRICO PRINCIPAL

Depois do último commit da linha principal analisada, houve nova atividade em 18/09/2026 na branch:

`cerebro-direct-bridge`

Foram encontrados três commits:

1. `45afc93c`
   `feat(app): permitir comunicacao direta com cerebro sem termux`

2. `5c3d3613`
   `fix(app): corrigir normalizacao do endpoint do cerebro`

3. `92196817`
   `fix(app): remover caractere literal no adapter do cerebro`

Isso altera a reconstrução histórica: a comunicação entre App e Cérebro não é apenas um experimento antigo. Houve uma tentativa posterior, explícita, de remover a dependência da Ponte Termux.

## 3. O QUE ESSA NOVA TENTATIVA IMPLEMENTA

O adapter direto introduz:

```
App
 ↓ polling
Cérebro
 ↓ trabalho
App
 ↓ inferência usando motor do App
Cérebro
```

O fluxo utiliza:
- endpoint configurável;
- token `X-Cerebro-Token`;
- fila de trabalho;
- `/v1/trabalho/proximo`;
- `/v1/trabalho/{id}/resultado`;
- capacidade inicial aceita: `inferencia`;
- fallback para mensagem/prompt;
- tratamento de erro;
- possibilidade de iniciar/parar;
- persistência local da configuração.

A Ponte Termux permanece independente e opcional.

## 4. O QUE OS COMMITS DE CORREÇÃO REVELAM

A sequência:

```
feature
 ↓
correção de normalização do endpoint
 ↓
correção de caractere literal
```

é evidência direta de iteração real sobre o adapter.

Isso é mais forte do que simplesmente encontrar uma especificação.

Mas ainda não prova que o canal foi testado ponta a ponta com um Cérebro operacional.

## 5. GITHUB PAGES — O QUE FOI COMPROVADO

Foram encontradas execuções de Pages Build and Deployment associadas aos commits da linha principal, com conclusão `success`.

Isso comprova que o mecanismo de publicação do GitHub Pages conseguiu construir/publicar as versões correspondentes.

Não comprova:
- funcionamento de todas as funções do aplicativo;
- funcionamento do Termux;
- funcionamento do Cérebro;
- funcionamento do motor;
- integração ponta a ponta;
- uso real no telefone.

Portanto:

**deploy bem-sucedido ≠ sistema operacionalmente validado.**

## 6. ESTADO DOS EXPERIMENTOS

| Experimento | Construção | Documentação | Evidência de execução | Resultado ponta a ponta |
|---|---|---|---|---|
| Memória independente | ✓ | ✓ | parcial | não fechado |
| Motor substituível | ✓ | ✓ | parcial | não fechado |
| Coleta/proveniência | ✓ | ✓ | parcial | não fechado |
| Busca | ✓ | ✓ | parcial | não fechado |
| Executor protegido | ✓ | ✓ | parcial | não fechado |
| Governança | ✓ | ✓ | parcial | não fechado |
| Orquestração | ✓ | ✓ | parcial | não fechado |
| Ponte Termux | ✓ | ✓ | parcial | não fechado |
| Continuidade Android | ✓ | ✓ | parcial | não fechado |
| Shizuku/RISH | ✓ | ✓ | não comprovada | não fechado |
| Motor local | especificado | ✓ | não comprovada | não fechado |
| App ↔ Cérebro direto | ✓ | ✓ | iteração/fixes comprovados | não fechado |

## 7. O QUE JÁ PODE SER CONSIDERADO CONHECIMENTO HISTÓRICO FORTE

Há evidência suficiente para preservar como descobertas históricas:

1. memória deve sobreviver à interface;
2. motor é substituível;
3. capacidade não implica autorização;
4. execução precisa de proteção;
5. contexto externo não é instrução;
6. informação precisa de proveniência;
7. busca e armazenamento são problemas diferentes;
8. especialização/orquestração foi experimentada;
9. ponte é uma capacidade própria;
10. continuidade é diferente da interface;
11. Android é meio de acesso, não inteligência;
12. privilégios não devem ser confundidos com capacidade;
13. o sistema foi descobrindo camadas conforme encontrava necessidades;
14. comunicação direta App ↔ Cérebro foi posteriormente investigada sem Termux.

## 8. O QUE AINDA NÃO PODE SER AFIRMADO

Ainda não há evidência suficiente para afirmar:

- por que o sistema antigo deixou de ser usado;
- qual foi o principal gargalo;
- se a interface foi causa ou apenas consequência da complexidade;
- se a governança melhorou resultados;
- se múltiplos especialistas superaram uma única inteligência;
- se a continuidade Android era confiável;
- se Shizuku trouxe ganho operacional sustentável;
- se o motor local funcionou de forma estável;
- se a ponte Termux funcionou de ponta a ponta em uso prolongado;
- se o novo adapter direto App ↔ Cérebro chegou a operar ponta a ponta;
- qual componente realmente deve ser herdado pelo ABS V1.

## 9. INVESTIGAÇÕES EXTERNAS QUE AINDA PRECISAM FECHAR

Antes de construir, ainda precisam ser fechados:

### Android
- modelo/API exatos do aparelho;
- limites de execução em segundo plano;
- Device Owner;
- Accessibility;
- Notification Listener;
- VPN;
- ADB;
- Shizuku;
- serviços;
- Binder;
- privilégios;
- boot/init;
- system image;
- AOSP;
- SELinux;
- Verified Boot;
- DSU/GSI;
- limites específicos do Galaxy A17.

### Dois Cérebros
- contrato de mensagens;
- identidade das fontes;
- autoridade de cada cérebro;
- memória de origem vs memória derivada;
- conflitos;
- proveniência;
- recuperação;
- indisponibilidade de um cérebro;
- segurança do canal;
- sincronização sem duplicação destrutiva.

### ABS
- invariantes;
- identidade;
- continuidade;
- autorização do Imperador;
- estado;
- memória;
- execução;
- observação;
- aprendizagem;
- recuperação;
- substituição de componentes;
- migração entre ambientes.

### Motor de IA
- router;
- modelos externos;
- modelo local;
- contexto;
- memória;
- ferramentas;
- avaliação;
- verificação;
- custo;
- limites do Android;
- possibilidade de substituição.

### Histórico
- recuperar artefatos binários quando possível;
- investigar ZIPs;
- investigar versões antigas;
- reconstruir resultados reais;
- cruzar commits com documentação;
- separar intenção declarada de comportamento efetivamente implementado.

## 10. REGRA DE PARADA

A investigação só termina quando, para cada capacidade que possa entrar na primeira construção, houver:

```
NECESSIDADE
 ↓
HIPÓTESE
 ↓
OPÇÕES
 ↓
DEPENDÊNCIAS
 ↓
LIMITAÇÕES
 ↓
RISCOS
 ↓
CUSTO
 ↓
EVIDÊNCIA HISTÓRICA
 ↓
EVIDÊNCIA TÉCNICA ATUAL
 ↓
TESTE POSSÍVEL
 ↓
REVERSIBILIDADE
 ↓
DECISÃO
```

Somente então começa a construção.

## 11. ESTADO ATUAL

**AINDA NÃO É HORA DE CONSTRUIR.**

A investigação encontrou novo patrimônio histórico e abriu uma nova linha causal importante: o adapter direto App ↔ Cérebro de setembro de 2026.

A próxima investigação deve fechar primeiro essa linha e depois cruzar todos os resultados com a arquitetura atual do ABS.

Nenhum componente histórico deve ser incorporado automaticamente.

## 12. PRINCÍPIO DE PRESERVAÇÃO

O Sistema antigo permanece intacto.

O Projeto Absoluto recebe:
- evidências;
- reconstruções;
- descobertas;
- hipóteses;
- relações;
- resultados;
- lacunas.

Não recebe automaticamente o código antigo.

A decisão de construir será feita somente depois que a investigação demonstrar o que vale a pena construir.
