# INTEGRAÇÃO DO CÉREBRO COM O CONHECIMENTO V0.1

Data: 2026-09-18
Branch: `base-cerebro-v0.1`

## 1. Resultado desta etapa

A integração passa a existir como uma camada explícita entre o acervo/memória já existente e a fachada operacional do Cérebro.

O objetivo não é transformar toda fonte em fato automaticamente. A arquitetura mantém a separação:

```
FONTE BRUTA
   ↓
INGESTÃO / PRESERVAÇÃO
   ↓
REGISTRO DE ORIGEM
   ↓
ESTRUTURAÇÃO EXPLÍCITA
   ↓
CONHECIMENTO VERSIONADO
   ↓
RELAÇÕES / RECUPERAÇÃO
   ↓
USO
   ↓
RESULTADO / EXPERIÊNCIA
   ↓
APRENDIZADO
   ↓
CONSOLIDAÇÃO
   ↓
CONHECIMENTO
```

## 2. O que já existia

Antes desta integração a base já possuía:

- preservação de fontes por hash;
- registros JSONL com proveniência;
- busca textual com validade temporal;
- relações entre registros;
- unidades semânticas com fato/hipótese/interpretação;
- aprendizado idempotente;
- consolidação de aprendizados;
- experiência, lição e sabedoria;
- histórico de execução e orquestração;
- persistência do grafo de tarefas;
- persistência de resultados de sinergia;
- continuidade e reconstrução histórica;
- eventos, causalidade e telemetria.

A lacuna principal era que essas capacidades estavam distribuídas em mecanismos diferentes e não havia uma unidade persistente de conhecimento que pudesse funcionar como fronteira comum entre elas.

## 3. O que foi integrado

Foi criada `cerebro/conhecimento.py`, com:

- tipos explícitos de conhecimento;
- fonte e evidência separadas;
- proveniência;
- contexto;
- confiança/incerteza;
- estado de validação;
- validade temporal;
- tempo de registro;
- supersessão;
- relações explícitas;
- versionamento;
- histórico append-only;
- recuperação híbrida simples;
- expansão de relações;
- importação idempotente dos aprendizados existentes;
- diagnóstico da base.

A fachada `Cerebro` agora expõe:

- `registrar_conhecimento()`;
- `buscar_conhecimento()`;
- `conhecimento_relacionado()`;
- `relacionar_conhecimento()`;
- `atualizar_conhecimento()`;
- `importar_aprendizados_para_conhecimento()`;
- `registrar_experiencia()`.

A consolidação de aprendizados continua preservando os arquivos anteriores e também projeta os aprendizados para a base de conhecimento.

## 4. Preservação e evolução

A base de conhecimento utiliza duas perspectivas:

1. estado atual por identificador;
2. histórico completo por identificador.

Uma atualização não substitui silenciosamente o passado. Cada versão é anexada ao histórico.

Conhecimento conflitante também não é resolvido automaticamente. A relação `CONTRADIZ` registra o conflito para posterior análise, preservando as duas origens.

Quando um entendimento é superado, a nova unidade pode apontar para a anterior com `supersedes` e `SUBSTITUI`, enquanto a unidade anterior permanece disponível como histórico.

## 5. Temporalidade

A camada suporta:

- `valid_from`;
- `valid_until`;
- `recorded_at`.

Isso separa o período em que algo é considerado válido do momento em que o Projeto registrou a informação.

A recuperação pode receber um instante de consulta e excluir conhecimento que não era válido naquele ponto.

## 6. Relação com as camadas existentes

A integração não substitui os componentes anteriores:

- `ingestao.py` continua preservando a fonte original;
- `nucleo.py` continua sendo o registro geral portátil;
- `semantica.py` continua fornecendo contratos semânticos;
- `temporal.py` continua fornecendo a semântica temporal;
- `aprendizado.py` continua registrando aprendizado idempotente;
- `sabedoria.py` continua separando experiência, lição e sabedoria;
- `agendador.py` continua aprendendo sobre execução;
- `grafo_tarefas.py` continua representando dependências de execução;
- `rede_evolutiva.py` continua representando caminhos e alavancas;
- `continuidade.py` continua tratando transferência de contexto;
- `servico.py` passa a conectar essas capacidades à camada de conhecimento.

## 7. Tipos de memória

A arquitetura do Projeto já prevê múltiplas formas de memória. A nova camada deve ser entendida como um tecido comum, e não como uma única “memória”.

No estado atual:

- **episódica**: experiências, eventos e histórico;
- **semântica**: fatos, hipóteses, interpretações e relações;
- **procedural**: procedimentos e padrões derivados;
- **relacional**: relações explícitas entre unidades;
- **histórica**: versões, supersessão e registros temporais;
- **de erros**: erros e correções;
- **de decisões**: decisões e contexto;
- **de proveniência**: fontes, evidências e transformação.

As fronteiras entre essas categorias permanecem evolutivas.

## 8. Pesquisa técnica considerada

A pesquisa atual reforça alguns princípios compatíveis com a arquitetura do Projeto:

- memória de agentes tende a funcionar melhor como ciclo de escrita, gerenciamento e leitura, em vez de simples armazenamento bruto;
- memória episódica, semântica e procedural podem coexistir;
- conhecimento em grafo é útil quando relações e consultas multi-hop são importantes;
- recuperação híbrida pode combinar lexical, semântica e travessia de relações;
- conhecimento temporal precisa representar mudanças explicitamente;
- proveniência é especialmente importante em memória compartilhada por múltiplos agentes;
- memória deve ser avaliada quanto a recuperação, custo, latência, contradições e qualidade da consolidação.

Esses princípios são coerentes com pesquisas recentes sobre memória de agentes, GraphRAG, memória temporal e memória com proveniência. A pesquisa não foi usada para copiar uma implementação externa.

## 9. O que ainda NÃO está concluído

Esta integração não deve ser confundida com uma arquitetura final.

Ainda faltam, entre outros:

1. embeddings e recuperação vetorial reais;
2. recuperação multi-hop orientada por objetivo;
3. roteamento automático entre memória episódica, semântica e procedural;
4. grafo de conhecimento persistente dedicado;
5. resolução de entidades;
6. política de conflito mais sofisticada;
7. consolidação seletiva assistida por modelos;
8. esquecimento seletivo com retenção auditável;
9. controle de acesso por agente;
10. autenticação/assinatura de escritas;
11. avaliação sistemática de memória;
12. ingestão multimodal;
13. sincronização distribuída multiwriter.

Essas lacunas são evolução posterior, não motivo para substituir a camada atual.

## 10. Princípio arquitetural

> O Cérebro não deve depender de uma única forma de armazenamento para possuir conhecimento.

O conhecimento deve ter uma representação canônica com proveniência e histórico, enquanto mecanismos especializados de recuperação, indexação, grafo ou vetores podem ser adicionados como projeções substituíveis.

Isso mantém a identidade do conhecimento independente da tecnologia usada para recuperá-lo.

## 11. Próximo ciclo técnico

A próxima evolução deve priorizar:

```
BASE CANÔNICA
   ↓
ÍNDICES DE RECUPERAÇÃO
   ↓
GRAFO / RELAÇÕES
   ↓
RECUPERAÇÃO HÍBRIDA
   ↓
USO PELO PLANEJAMENTO
   ↓
RESULTADO
   ↓
EXPERIÊNCIA
   ↓
CONSOLIDAÇÃO
```

A prioridade deve ser recalculada conforme os testes e o uso real revelarem gargalos.
