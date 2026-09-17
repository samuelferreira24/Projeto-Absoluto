# Arquitetura da Fundação — V0.2

## 1. Finalidade

Esta especificação amplia a fundação V0.1 para permitir que o Projeto Absoluto continue sua construção, operação, auditoria e evolução com diferentes IAs, ferramentas, plataformas e componentes, sem transferir a identidade ou o conhecimento de construção para qualquer fornecedor.

A V0.2 define a arquitetura que a base deve suportar. A implementação pode ocorrer incrementalmente conforme os ciclos reais exigirem cada capacidade.

## 2. Princípio estrutural

> O Projeto Absoluto é maior que qualquer IA, automação, software, plataforma ou componente tecnológico. Esses elementos são engrenagens que podem ser substituídas, combinadas ou ampliadas.

A fundação deve preservar a continuidade do Projeto mesmo quando um agente, modelo, conta, ferramenta, plataforma ou implementação for substituído.

## 3. Modelo geral

```text
PROJETO ABSOLUTO
       │
       ├── IDENTIDADE E GOVERNANÇA
       │
       ├── VISÃO / OBJETIVOS
       │
       ├── MAPA DA CONSTRUÇÃO
       │      ├── requisitos
       │      ├── capacidades
       │      ├── componentes
       │      ├── dependências
       │      ├── interfaces
       │      └── critérios de conclusão
       │
       ├── ESTADO DO SISTEMA
       │      ├── progresso
       │      ├── problemas
       │      ├── riscos
       │      ├── decisões pendentes
       │      └── próxima ação
       │
       ├── CÉREBRO
       │      ├── fontes
       │      ├── conhecimento
       │      ├── experiência
       │      ├── evidências
       │      ├── decisões
       │      └── aprendizados
       │
       ├── AGENTES / RECURSOS
       │      ├── identidade
       │      ├── capacidades
       │      ├── permissões
       │      └── contratos
       │
       ├── EXECUÇÃO
       │
       ├── OBSERVABILIDADE E PROVENIÊNCIA
       │
       ├── VERIFICAÇÃO / VALIDAÇÃO
       │
       ├── RISCO / SEGURANÇA / RECUPERAÇÃO
       │
       └── EVOLUÇÃO
              │
              └─────────────── ciclo contínuo
```

## 4. Identidade e continuidade

A identidade lógica de objetos e componentes não deve depender de nomes de arquivos, URLs, contas, repositórios, provedores de IA ou bancos específicos.

A arquitetura deverá permitir identificar pelo menos:

- Projeto;
- componente;
- requisito;
- capacidade;
- agente/recurso;
- sessão/execução;
- evento;
- decisão;
- evidência;
- versão.

## 5. Estado global

O estado global deve ser reconstruível a partir de registros versionados e eventos. Deve representar, quando aplicável:

- versão da arquitetura;
- componentes ativos;
- capacidades disponíveis;
- itens em construção;
- problemas abertos;
- riscos relevantes;
- decisões pendentes;
- integrações ativas;
- agentes disponíveis;
- última validação;
- próxima ação prioritária.

O estado é uma fotografia derivada; não substitui histórico ou evidências.

## 6. Mapa da construção

O mapa deve representar a construção em unidades que possam ser transferidas entre agentes.

Cada unidade deverá poder responder:

- o que é;
- por que existe;
- qual objetivo atende;
- de que depende;
- o que depende dela;
- qual contrato possui;
- o que já foi implementado;
- o que foi testado;
- qual evidência existe;
- quais problemas existem;
- qual é a próxima ação;
- qual é o critério de conclusão.

O mapa é um modelo operacional e versionado, não uma autoridade absoluta. A realidade observada e as evidências podem revelar divergência entre mapa e sistema.

## 7. Rastreabilidade

A fundação deve suportar a cadeia:

```text
OBJETIVO
  ↓
REQUISITO
  ↓
CAPACIDADE
  ↓
COMPONENTE
  ↓
IMPLEMENTAÇÃO
  ↓
TESTE
  ↓
EVIDÊNCIA
  ↓
VALIDAÇÃO
```

Isso permite verificar por que determinado componente existe e se uma necessidade foi realmente atendida.

## 8. Dependências e interfaces

Dependências estruturais devem ser distintas de relações de conhecimento.

Interfaces devem possuir contratos explícitos sempre que houver integração relevante:

```text
ENTRADA
  ↓
CONTRATO
  ↓
PROCESSAMENTO
  ↓
SAÍDA
  ↓
VALIDAÇÃO
```

O contrato deve registrar, conforme o caso, entradas, saídas, garantias, pré-condições, pós-condições, limites, erros e ações proibidas.

## 9. Agentes e recursos

O registro de agentes deve permitir que uma tarefa seja entregue a diferentes recursos sem alterar a identidade do Projeto.

Informações previstas:

- identidade;
- tipo;
- modelo/provedor, quando aplicável;
- capacidades;
- ferramentas;
- ambiente;
- permissões;
- limites;
- custo, quando mensurável;
- histórico de execução;
- evidências de desempenho;
- estado de disponibilidade.

Um agente não é a autoridade do Projeto apenas por produzir uma resposta.

## 10. Autonomia e governança

A arquitetura deve separar capacidade técnica de autorização.

Exemplo de níveis:

- observar;
- pesquisar/analisar;
- executar ações reversíveis;
- delegar;
- modificar sistemas autorizados;
- propor decisões estratégicas;
- executar ação de alto impacto somente após autorização exigida.

As regras exatas devem ser configuráveis e evolutivas. Ações irreversíveis, de alto impacto ou fora das permissões não devem ser executadas apenas por inferência de um agente.

## 11. Observabilidade

A execução deve poder ser reconstruída por uma cadeia semelhante a:

```text
EVENTO → DECISÃO → AÇÃO → AGENTE → FERRAMENTA → RESULTADO → VALIDAÇÃO
```

Eventos relevantes devem possuir correlação e causalidade suficientes para detectar duplicação, ciclos, falhas, desvios e origem de resultados.

## 12. Evidência e proveniência

Resultados importantes devem registrar origem e contexto suficientes para permitir auditoria. O sistema deve distinguir:

- observado diretamente;
- informado por fonte externa;
- derivado por processamento;
- inferido;
- hipótese;
- validado por teste.

Nenhuma interpretação deve substituir a fonte original.

## 13. Mudanças e versões

Mudanças relevantes devem preservar:

- versão anterior;
- versão nova;
- motivo;
- origem da mudança;
- agente/recurso responsável;
- áreas afetadas;
- evidências;
- validação;
- possibilidade de recuperação, quando aplicável.

## 14. Divergência e drift

A base deverá permitir comparar:

```text
MAPA
DOCS
CÓDIGO
TESTES
ESTADO REAL
```

Quando houver divergência relevante:

```text
DETECTAR
  ↓
REGISTRAR
  ↓
ANALISAR
  ↓
DECIDIR
  ↓
CORRIGIR
  ↓
VALIDAR
  ↓
ATUALIZAR O MAPA
```

## 15. Segurança e recuperação

A evolução da base deve prever mecanismos para preservar continuidade diante de erro humano, erro de IA, corrupção, mudança de plataforma ou alteração estrutural.

Capacidades arquiteturais previstas:

- versionamento;
- cópias/backup;
- checkpoints;
- recuperação;
- rollback quando tecnicamente possível;
- isolamento de ações de risco;
- auditoria.

## 16. Evolução

O sistema deve transformar experiência em melhoria:

```text
EXECUTAR
  ↓
OBSERVAR
  ↓
AVALIAR
  ↓
APRENDER
  ↓
PROPOR MELHORIA
  ↓
TESTAR
  ↓
INCORPORAR
  ↓
ATUALIZAR A BASE
```

A própria arquitetura deve ser tratada como objeto evolutivo.

## 17. Implementação incremental

A V0.2 não exige implementar todas as capacidades simultaneamente.

Ordem arquitetural sugerida:

1. identidade e estado;
2. mapa da construção;
3. rastreabilidade de requisitos/capacidades/componentes;
4. contratos e interfaces;
5. registro de agentes e permissões;
6. eventos e observabilidade;
7. evidências e mudanças;
8. divergência/drift;
9. recuperação;
10. evolução automatizada.

Cada camada deve ser implementada somente quando houver contrato, teste e critério de validação suficientes.

## 18. Critério de continuidade

Uma nova IA ou colaborador deve conseguir continuar a construção sem depender do histórico privado de uma conversa anterior, desde que tenha acesso aos artefatos necessários do Projeto.

O pacote mínimo de continuidade deve incluir:

- visão;
- arquitetura;
- mapa da construção;
- estado atual;
- decisões;
- contratos;
- código;
- testes;
- problemas conhecidos;
- evidências;
- próxima ação.

## 19. Regra final

O Projeto Absoluto deve ser capaz de mudar de IA, modelo, conta, plataforma, ferramenta ou implementação sem perder sua identidade, conhecimento de construção, histórico, proveniência ou capacidade de continuar evoluindo.
