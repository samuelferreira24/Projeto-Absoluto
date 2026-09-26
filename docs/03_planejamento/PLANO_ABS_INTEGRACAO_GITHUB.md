# ABS — Acesso ao GitHub

## Objetivo

O GitHub deve ser um recurso do ABS, e não uma dependência direta da interface.

Fluxo alvo:

`IMPERADOR → Interface → ABS API/Core → roteamento → GitHub → resultado → verificação/proveniência`

## Caminhos

### 1. GitHub API — caminho principal preparado

- conexão: `github-api`
- capacidade executável: `github`
- autenticação opcional: `ABS_GITHUB_TOKEN`
- repositório padrão: `ABS_GITHUB_REPO`
- API padrão: `https://api.github.com`
- leitura pública funciona sem token.

### 2. GitHub via Termux — caminho alternativo

- conexão: `github-termux`
- permanece registrada como rota de Git/controle de versão.
- pode ser usada futuramente para operações locais do repositório.

### 3. GitHub App / Connector

O GitHub App conectado ao ChatGPT é uma rota do ambiente externo/host. Ele não entrega automaticamente suas credenciais ao processo local do ABS.

Por isso o ABS não deve depender desse conector para funcionar. O caminho local preparado é a API do GitHub, com possibilidade de autenticação própria posteriormente.

## Operações de leitura preparadas

A capacidade `github` suporta:

- `repository`: informações do repositório;
- `file`: leitura de arquivo;
- `directory`: listagem de diretório;
- `search`: busca de código.

As operações de escrita permanecem fora desta primeira etapa.

## Segurança

- token não é gravado no código;
- token, quando necessário, vem de variável de ambiente;
- operações continuam passando pelo contrato de autorização do Imperador;
- a interface não recebe diretamente credenciais do GitHub;
- a capacidade é substituível por outro adaptador no futuro.

## Estado

Esta etapa prepara a camada de recurso. O próximo passo é conectar essa capacidade ao ciclo conversacional/ferramentas do ABS para que uma interface possa pedir ao ABS para consultar o repositório sem conhecer o GitHub diretamente.
