# CAMADA DE CONHECIMENTO E CONTINUIDADE DO PROJETO

Esta camada existe para que uma nova IA ou novo chat possa reconstruir o Projeto Absoluto sem depender da memória de uma conversa.

## Regra principal

**Mudança observável → evento → conhecimento estruturado → projeções → próxima IA.**

O conhecimento do Projeto é maior que o ABS. O ABS é registrado como uma parte do Projeto.

## Fontes

- código e testes: estado observável;
- Git/GitHub: histórico e proveniência;
- runtime: recursos, capacidades e presença;
- documentos do Cérebro: contexto, mapas e histórico;
- decisões do Imperador: autoridade humana, preservadas separadamente.

## Automação

`abs_core.project_knowledge` faz uma varredura determinística do repositório e produz:
- `project_knowledge.json`: fonte estruturada observável;
- `MAPA_AUTO_ESTADO_PROJETO.md`: projeção legível.

A projeção não substitui os mapas existentes. Ela os complementa e pode crescer automaticamente conforme o repositório muda.

## Estados

Caminhos e capacidades devem evoluir para estados verificáveis como: `operational`, `partial`, `experimental`, `degraded`, `unavailable`, `historical`, `hypothetical`.

Nesta primeira vertical, `observed` significa apenas que a estrutura foi encontrada; não significa que uma execução real foi comprovada.

## Limite de autoridade

Automação pode atualizar fatos observáveis, evidências, estado técnico e relações derivadas.

Automação não pode alterar silenciosamente:
- visão do Projeto Absoluto;
- princípios;
- decisões do Imperador;
- arquitetura intencionalmente declarada como autoridade humana.

## Estado desta vertical

As integrações iniciais já estão implementadas nesta vertical:
- Git/revisão/branch/commit como proveniência observável;
- runtime como snapshot observável;
- testes como evidência;
- avaliador automático de paths;
- expansão automática de paths a partir de capacidades conhecidas;
- projeção automática de recursos, ferramentas, nós, paths, eventos e evidências.

Ainda não é uma integração completa com a API do GitHub para PRs/issues nem um fluxo de eventos em tempo real do daemon. Esses são níveis posteriores de automação.

## Próximas integrações

1. GitHub PRs/issues/workflows como eventos externos.
2. eventos reais do runtime ABS, em vez de somente snapshots.
3. promoção operacional baseada em execução real.
4. integração direta com o daemon de atualização.
5. descoberta/validação automática de novas ferramentas e caminhos.


## Regra adicional de continuidade — 2026-10-03

O conhecimento persistente não deve registrar apenas arquivos e capacidades observáveis. Quando o Imperador estabelece uma distinção conceitual necessária para orientar a construção, ela deve permanecer recuperável nas fontes canônicas.

Em particular:
- **ABS geral / Sistema Absoluto** = ecossistema aberto de capacidades e recursos;
- **ABS em construção** = operador/orquestrador desse ecossistema;
- **ABS V1** = primeira versão operacional do ABS em construção.

A finalidade da camada de conhecimento é permitir que uma nova IA reconstrua também o **entendimento operacional necessário para continuar o trabalho**, e não apenas uma fotografia dos arquivos existentes.


## Aplicação prática da arquitetura de preservação — 2026-10-03

A arquitetura deixou de ser somente documentação.

O `abs_core.project_knowledge` agora registra automaticamente as **camadas de continuidade** como fontes observáveis, incluindo:
- visão/princípios;
- decisões;
- pesquisa;
- contrato de evidência;
- estado derivado;
- estado de sessão;
- handoff;
- navegação;
- arquivo histórico.

Cada fonte registrada possui, quando disponível, **caminho, camada, autoridade, temporalidade, presença e hash SHA-256**. Isso cria uma ponte verificável entre a pesquisa de continuidade e o Project Knowledge.

A automação não promove interpretação para autoridade humana. Ela observa e indexa; decisões continuam sendo registradas na fonte de decisões e estado técnico continua sendo derivado de evidências.

Os testes agora verificam que essas camadas continuam presentes e expostas na projeção automática. Uma regressão que reduza novamente a continuidade a um único handoff deve falhar na validação.
