# Auditoria do canal de administração da VPS

**Data:** 2026-10-11  
**Escopo:** caminho atual GitHub comment → GitHub Actions → self-hosted runner → VPS.  
**Princípio:** observação antes de alteração; não parar runners nem serviços durante a migração.

## Estado verificado por execução real

- O workflow `.github/workflows/vps-admin-command.yml` respondeu a `/vps status`, `/vps services`, `/vps docker`, `/vps workspace` e `/vps mcp-smoke` enviados pelo proprietário ao issue histórico #121.
- `ssh.service`, `tailscaled.service`, `docker.service`, runner principal e runner reserva estavam `active/running` no momento da consulta.
- Host observado: `abs-vps-01`; 3 CPUs; RAM total ~5.7 GiB, disponível ~4.3 GiB; raiz 58 GiB, 46 GiB usados, 13 GiB disponíveis (79%).
- Docker estava ativo. Os contêineres `vps-mcp`, `code-server`, Coolify, banco, Redis, Sentinel e proxy estavam em execução; code-server, Coolify, Sentinel e proxy reportaram health `healthy`.
- O comando `/vps workspace` observou o checkout em `/home/absadmin/Projeto-Absoluto`, HEAD curto `6b487db`, e um arquivo não rastreado `:memory:`. Não foi removido: é necessário identificar sua origem e verificar se contém dados antes de limpar.
- O endpoint MCP aceitou inicialização autenticada (HTTP 200, sessão recebida). O smoke test das ferramentas também recebeu HTTP 200, mas o parser do workflow marcou falha porque pressupõe `structuredContent` ou texto JSON com formato específico. A falha do parser não prova falha da ferramenta; o resultado precisa ser interpretado com um parser compatível com respostas MCP textuais/estruturadas.
- O histórico do issue #121 tinha mais de 1.100 comentários e mistura comandos `/abs` e `/vps`, tornando difícil localizar as saídas recentes.

## Riscos e limitações identificados

1. O workflow atual aceita comentários `/vps ...` do proprietário em qualquer issue que não seja PR; a condição não limita o número do issue.
2. O job usa `runs-on: [self-hosted]`; o GitHub pode alocá-lo em qualquer runner self-hosted elegível. Ambos os serviços estavam ativos, mas o workflow não identifica explicitamente principal versus reserva.
3. O canal depende de um comentário GitHub como gatilho e da permissão do workflow para publicar a saída como comentário.
4. O smoke test tem lógica de interpretação frágil; seu status pode dar falso negativo.
5. O uso do disco em 79% merece monitoramento, mas não há base para apagar dados automaticamente.
6. O arquivo `:memory:` não rastreado no checkout precisa ser investigado, não apagado às cegas.

## Correções propostas neste branch

- Restringir o workflow a issues operacionais conhecidas (#121 legado e #162 novo), mantendo o caminho antigo durante a transição.
- Criar o issue #162 como canal dedicado a comandos `/vps`, sem misturá-los ao fluxo histórico `/abs`.
- Tornar o parser do smoke test tolerante a respostas MCP estruturadas ou textuais, diferenciando erro de execução de resposta válida em formato inesperado.
- Preservar o conjunto fechado de comandos: não introduzir shell arbitrário, não ler nem publicar variáveis de ambiente, e não alterar serviços da VPS.

## Plano de validação antes de encerrar a migração

1. Revisar este PR e integrar as mudanças somente depois da validação estática.
2. No issue #162, executar `/vps status`, `/vps services`, `/vps docker`, `/vps mcp-verify`, `/vps mcp-smoke` e `/vps workspace`.
3. Confirmar que o workflow responde apenas aos issues permitidos e ao proprietário autorizado.
4. Identificar a origem de `:memory:` e só então decidir se pode ser removido.
5. Depois de vários testes bem-sucedidos, considerar retirar #121 da allowlist. Não desligar os runners nem eliminar o caminho legado antes disso.

## Limite do que foi provado

Os testes confirmam que o fluxo por comentário consegue executar comandos allowlisted e devolver saídas reais. Não provam ainda a execução direta sem issue, o isolamento garantido entre runner principal e reserva, nem a saúde semântica das ferramentas MCP. Essas capacidades exigem testes específicos.
