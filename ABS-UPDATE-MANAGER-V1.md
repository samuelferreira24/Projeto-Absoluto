# ABS Update Manager V1

O ABS local não atualiza a si mesmo. A atualização é uma capacidade externa de continuidade.

## Fluxo

GitHub
→ Update Manager
→ valida estado local
→ baixa referência configurada
→ registra ponto de retorno
→ instala commit
→ reinicia pelo supervisor
→ verifica /health
→ mantém ou faz rollback

## Segurança operacional

- Atualização recusada se o repositório estiver sujo.
- O commit anterior é registrado em estado local.
- A instalação usa um ponto Git recuperável.
- O processo ABS é reiniciado pelo supervisor `sv`.
- O resultado só é considerado válido após `/health`.
- Falha no pós-update dispara rollback automático.
- Tokens e autenticação continuam fora do repositório.

## Configuração

- `ABS_REPO_DIR`
- `ABS_UPDATE_REMOTE` (default `origin`)
- `ABS_UPDATE_REF` (default `main`)
- `ABS_UPDATE_STATE` (default `~/.abs/update-state.json`)
- `ABS_UPDATE_HEALTH_URL` (default `http://127.0.0.1:8787/health`)
- `ABS_UPDATE_SERVICE` (default `abs`)
- `ABS_UPDATE_HEALTH_TIMEOUT` (default `30`)

## Comandos

    abs-update status
    abs-update check
    abs-update apply
    abs-update rollback

## Princípio

O supervisor mantém o processo vivo. O Update Manager controla a versão. O ABS executa trabalho. Cada camada tem uma função diferente.
