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

## Próximas integrações

1. Git/GitHub e PRs como eventos.
2. runtime ABS como fonte de recursos/capacidades/nós.
3. testes/CI como evidência.
4. avaliador automático de caminhos.
5. projeções adicionais para mapas existentes.
6. pacote de orientação para nova IA.
7. integração no daemon de atualização.
