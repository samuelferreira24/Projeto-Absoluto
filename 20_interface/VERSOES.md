# Versionamento da Interface ABS

## Padrão

- **V1.0 — Centro de Controle:** primeira interface operacional, com painel de controle e rotas reais do ABS.
- **V1.1 — Ecossistema de Inteligências:** expansão para capacidades multimodais, ferramentas, voz e ecossistema de inteligências.
- **V1.2 — Experiência Espacial:** evolução para mapa espacial e navegação visual do ABS.
- **V1.3 — Interação e Construção:** edição visual, seleção, conexão, agrupamento, zoom e modos de interação do ambiente.

## Regra de nomenclatura

Os nomes históricos `V3` e `V4` não representam versões principais independentes. Foram normalizados para **V1.2** e **V1.3**.

A interface atual é **V1.3**.

Correções, ajustes de compatibilidade e Service Worker não criam automaticamente uma nova versão visual; permanecem dentro da versão funcional correspondente.

## Compatibilidade

A chave antiga de workspace `abs-workspace-v4` é migrada automaticamente para `abs-workspace-v1.3`, preservando o ambiente visual salvo anteriormente no navegador.
