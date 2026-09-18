# INVENTÁRIO DE PORTAS ABERTAS V0.1

## Objetivo

Registrar, sem fechar a arquitetura do Projeto Absoluto, as principais classes de portas tecnológicas que já podem ser investigadas ou conectadas ao Cérebro e à futura Sala de Comando.

Este documento é um inventário vivo. Não define a arquitetura final.

## 1. Princípio

O Projeto Absoluto não deve depender de uma única IA, interface, sistema operacional, dispositivo, agente, API ou plataforma.

Uma capacidade deve ser tratada como capacidade. O provedor que a executa deve poder ser substituído quando tecnicamente possível.

## 2. Agentes de programação

### OpenAI — Codex

Situação verificada em setembro de 2026:

- existe SDK oficial do Codex;
- existe Codex App Server;
- o SDK permite incorporar o Codex a aplicações e fluxos próprios;
- o App Server foi criado para integrações profundas, incluindo autenticação, histórico, aprovações e eventos em streaming;
- o App Server usa JSON-RPC e pode operar por stdio, WebSocket experimental ou socket Unix;
- o Codex pode ser usado com autenticação via ChatGPT ou API;
- há modos de sandbox, incluindo leitura, escrita no workspace e acesso mais amplo ao sistema de arquivos.

Implicação para o Projeto:

Sala de Comando/Cérebro → Codex → ambiente de desenvolvimento → resultado → Cérebro.

Fonte: documentação oficial do Codex.

## 3. Agentes de programação externos

### Anthropic — Claude Code

Situação verificada:

- possui CLI;
- pode executar tarefas de forma não interativa;
- suporta retomada de sessões;
- suporta MCP;
- permite definir ferramentas permitidas/negadas;
- pode ser incorporado por SDK/fluxos programáticos.

Implicação:

Claude Code deve ser tratado como um possível agente de execução de engenharia, não como dependência exclusiva do Projeto.

### Google — Jules

Situação verificada:

- agente de programação integrado ao GitHub;
- trabalha com repositórios e branches;
- pode criar alterações e PRs;
- executa testes em ambiente virtual;
- possui acesso por CLI;
- possui API para construção de fluxos próprios;
- possui suporte a MCP em expansão.

Implicação:

Jules é outra possível porta para execução de engenharia.

## 4. Modelos e APIs

Manter portas abertas para:

- OpenAI API;
- Anthropic API;
- Google/Gemini;
- OpenRouter;
- Groq;
- modelos locais;
- novos provedores.

O Cérebro atual já possui um contrato abstrato de modelo (ModeloEstruturado) e um OrquestradorModelos, o que é uma base adequada para manter provedores substituíveis.

## 5. MCP

MCP é uma porta de integração importante.

A documentação atual da OpenAI confirma que MCP pode conectar modelos a ferramentas e contexto de terceiros.

O ChatGPT e o Codex podem usar servidores MCP em diferentes ambientes compatíveis.

Implicação:

MCP deve ser tratado como uma camada de interoperabilidade, não como uma implementação específica do Projeto.

## 6. ChatGPT como porta

O Apps SDK/MCP Apps permite que sistemas próprios exponham ferramentas e, opcionalmente, interfaces ao ChatGPT.

Isso permite pensar no ChatGPT como uma possível porta de entrada para o Projeto Absoluto.

A arquitetura deve continuar funcionando fora do ChatGPT.

## 7. Sala de Comando

A Sala de Comando não deve ser definida como um aplicativo.

Uma aplicação pode ser uma interface.

Outras portas possíveis:

- navegador;
- celular;
- computador;
- terminal;
- ChatGPT;
- outros clientes MCP;
- APIs;
- futuras interfaces.

A capacidade de comando deve permanecer separada da interface que a apresenta.

## 8. Celular e Android

Objetivo futuro possível:

não apenas controlar aplicativos Android, mas investigar a possibilidade de modificar o próprio sistema operacional.

AOSP fornece caminho oficial para estudar e construir variantes do Android e componentes do sistema.

Portas de investigação:

- AOSP;
- serviços do sistema;
- launcher;
- APIs;
- Accessibility;
- runtime;
- componentes do sistema;
- builds próprias;
- dispositivos desbloqueáveis;
- integração profunda entre agente e sistema.

Limite atual:

isto é uma linha de pesquisa, não uma capacidade já implementada no Projeto.

## 9. Ambientes

Manter abertas as portas para:

- celular;
- computador;
- servidores;
- nuvem;
- Termux;
- navegadores;
- sistemas operacionais modificados;
- dispositivos futuros;
- ambientes físicos.

## 10. Histórico que não deve ser perdido

O antigo repositório Sistema já contém evidências de uma arquitetura anterior com:

- múltiplos motores;
- biblioteca;
- pesquisa;
- memória;
- Termux;
- execução;
- especialistas;
- módulos;
- mecanismos de treinamento/exportação;
- tentativa de auto-reparo.

O app antigo não deve ser tratado automaticamente como sistema final nem como projeto descartável.

Ele é patrimônio histórico e fonte de capacidades que podem ser reaproveitadas.

## 11. Estado atual do Cérebro

Na branch base-cerebro-v0.1 já existem:

- memória persistente;
- proveniência;
- ingestão;
- continuidade;
- contexto operacional;
- grafo de tarefas;
- agendamento adaptativo;
- execução controlada;
- controle de agentes;
- telemetria;
- orquestração;
- detecção de sinergia;
- inventário de capacidades;
- contrato abstrato de modelos;
- adaptador inicial OpenRouter.

O próximo trabalho deve conectar capacidades reais progressivamente, sem transformar a base em dependência de um único provedor.

## 12. Próximo passo concreto

Antes de construir uma Sala de Comando completa, consolidar uma camada mínima de portas/capacidades externas no Cérebro.

Essa camada deverá permitir que o Cérebro saiba:

- qual capacidade existe;
- qual agente/provedor pode fornecê-la;
- onde ela está disponível;
- quais ferramentas utiliza;
- quais permissões exige;
- qual ambiente alcança;
- como é chamada;
- como retorna resultado;
- quais limites possui;
- como pode ser substituída.

Não implementar todos os agentes agora.

Primeiro criar o contrato que permita adicioná-los posteriormente.

## 13. Critério de evolução

Uma nova tecnologia não deve exigir reconstrução do Cérebro.

Ideal:

NOVA TECNOLOGIA
→ registrar capacidade
→ adaptar contrato
→ testar
→ disponibilizar
→ usar quando apropriado.

## 14. Estado deste documento

Este inventário registra o conhecimento disponível neste ciclo.

Ele deve ser atualizado quando:

- uma nova porta for descoberta;
- uma integração for implementada;
- uma capacidade for testada;
- uma limitação for descoberta;
- uma tecnologia deixar de existir;
- uma alternativa melhor surgir.

Não é uma lista fechada.
