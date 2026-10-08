# Canal reserva do ABS VPS

O canal principal usa o runner `abs-vps-01`. Este canal reserva usa um segundo runner no mesmo VPS com a label `abs-vps-01-reserve`.

## Ativação única

No VPS, registrar um segundo runner com um token temporário de GitHub Actions:

```bash
cd ~/Projeto-Absoluto
RUNNER_TOKEN='TOKEN_TEMPORARIO' bash tools/vps/install-reserve-runner.sh
```

O token não deve ser salvo no repositório.

## Comandos

- `/abs-reserve status`
- `/abs-reserve restart-abs`
- `/abs-reserve v3-test`

A reserva é deliberadamente menor que o canal principal: ela existe para recuperação, diagnóstico e validação, não para substituir todas as funções do canal principal.
