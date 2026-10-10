# VPS Direct Admin MCP

Serviço independente do ABS para permitir que um cliente MCP autenticado consulte o host, inspecione contêineres, leia logs e gerencie arquivos de trabalho autorizados.

- Endpoint: \`https://mcp.207.180.3.245.sslip.io/mcp\`
- Health check: \`/healthz\` (retorna apenas status genérico)
- Autenticação: \`Authorization: Bearer <VPS_MCP_API_KEY>\`
- Proxy: Traefik já existente, rede Docker \`coolify\`, HTTPS/Let's Encrypt.
- A chave fica em \`/opt/vps-mcp/api_token\` no host, permissão 0600. Nunca comitar nem imprimir a chave nos logs.
- Ferramentas sem execução arbitrária de shell. Alterações em contêineres ficam limitadas à lista permitida e aos contêineres \`vps-workload-*\`.
- O socket Docker dá alto privilégio ao serviço; manter o endpoint protegido, revisar ferramentas e rotacionar a chave se houver suspeita de exposição.
