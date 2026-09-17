# Persistência da Rede Evolutiva V0.1

## Objetivo

Dar ao tabuleiro/rede evolutiva um estado portátil e persistente, permitindo que o Cérebro preserve caminhos, relações, evidências e sinais entre sessões e entre diferentes agentes.

## Princípios

- A rede pertence ao Projeto, não a uma IA específica.
- Persistência não define uma ordem fixa de execução.
- Candidatos contextuais são sinais auxiliares; novos caminhos continuam permitidos.
- Relações devem preservar convergência, impulso, multiplicação de valor, questionamento, bloqueio e reutilização.
- O formato deve permanecer simples, versionável e substituível.
- O carregamento deve reconstruir uma rede semanticamente equivalente e validar referências.

## Estado persistido

O arquivo `rede_evolutiva.json` contém `schema_version`, nós e arestas. Cada nó preserva estado, potencial multiplicador, evidências e metadados. Cada aresta preserva origem, relação, destino, peso, evidência e metadados.

## Continuidade

A fachada `Cerebro` carrega a rede ao iniciar e grava a rede junto com o estado operacional quando `salvar_estado()` é chamado. Assim, a rede deixa de ser apenas uma estrutura transitória em memória.

## Limites atuais

Esta versão não implementa ainda sincronização distribuída, concorrência, consenso entre agentes, histórico temporal completo de cada mutação ou resolução automática de conflitos. Esses pontos permanecem caminhos de evolução.
