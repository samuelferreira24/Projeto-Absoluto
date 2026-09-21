# Recursos e Conexões da Interface ABS V1

## 1. Princípio

A interface não se conecta a uma única ferramenta. Ela acessa um universo extensível de recursos.

ABS não é ChatGPT, Codex, GitHub, Claude, Gemini, navegador, API ou rede.

Esses elementos são recursos que podem ser conectados, substituídos, combinados ou removidos.

## 2. Formas de conexão

- CLI / Termux;
- API;
- navegador;
- Connector/Plugin administrado pela plataforma;
- token ou credencial;
- aplicativo instalado;
- serviço local;
- rede local;
- dispositivo remoto;
- protocolos futuros.

O mesmo serviço pode possuir vários caminhos.

## 3. Universo inicial

A V1 registra como classes de conexão:

- Codex via Termux/CLI;
- ChatGPT Connector;
- Claude API;
- Gemini API;
- IA local;
- Internet/HTTP;
- Browser Runtime;
- APIs externas;
- GitHub API;
- GitHub via Termux;
- rede local;
- dispositivo remoto;
- futuras tecnologias de rede.

O registro é aberto. A lista não é um limite do ABS.

## 4. Estado epistemológico

Registrar uma conexão não significa que ela já esteja operacional.

Estados:
- configured — credencial/configuração presente;
- available — caminho conhecido e disponível para integração;
- planned — contrato previsto, runtime ainda não validado;
- extensible — ponto de extensão para tecnologia futura.

Uma capacidade executável só deve ser marcada como operacional depois de implementação, teste e evidência.

## 5. IA externa

A arquitetura permite combinar Codex, Claude, Gemini, IA local, outras IAs e futuras IAs.

## 6. Internet e APIs

Internet e APIs são recursos de infraestrutura. A implementação de navegador real exige um runtime de navegador validado.

## 7. Controle de credenciais

Segredos não pertencem ao registro público de conexões. A V1 usa referências a variáveis de ambiente sem armazenar ou expor valores das chaves.

## 8. Multi-dispositivo

Dispositivos são recursos, não definições do ABS.

Próximo nível: descoberta, autenticação, seleção, despacho, execução, heartbeat e resultado.

O registro e heartbeat atuais não devem ser confundidos com execução distribuída já validada.

## 9. Evolução

Necessidade → pesquisa → meios de conexão → registro → adapter/contrato → teste → validação → integração.

## 10. Regra central

> A interface é a porta de acesso aos recursos; o ABS Core continua sendo o núcleo de orquestração.

A conexão é substituível. A capacidade é substituível. A interface é substituível. O ABS permanece acima desses meios.