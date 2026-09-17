# Deploy do Runtime Persistente V0.1

## Objetivo

Definir como o runtime do Cérebro pode permanecer executando fora da interface de chat ou navegador.

## Arquitetura

```text
CHAT / APP / API
       │
       │ comando / evento
       ▼
  COLETA / DESPERTAR
       │
       ▼
RUNTIME PERSISTENTE
       │
       ├── Orquestrador
       ├── Cérebro
       ├── Estado
       ├── Runtime/lease
       └── Worker
       │
       ▼
AGENTE / EXECUTOR AUTORIZADO
       │
       ▼
RESULTADO + EVIDÊNCIA
       │
       ▼
CÉREBRO
```

## Requisito essencial

O runtime deve ser hospedado em infraestrutura que permaneça ativa quando o usuário fechar o navegador. A aba do ChatGPT não é o runtime.

## Pacote atual

- `cerebro/runtime.py`: estado, lease, heartbeat e recuperação.
- `cerebro/orquestrador.py`: missões e ciclos idempotentes.
- `cerebro/despertador.py`: pedidos persistentes e recuperação de pedidos abandonados.
- `cerebro/worker.py`: worker configurável para processamento contínuo.
- `Dockerfile.runtime`: imagem portátil.
- `docker-compose.runtime.yml`: reinício automático e volume persistente.

## Executor externo

O worker recebe um comando por `PROJETO_ABSOLUTO_EXECUTOR_CMD`. O executor deve:

1. receber JSON pela entrada padrão;
2. respeitar a missão e o caminho fornecidos;
3. agir somente dentro das permissões concedidas;
4. devolver JSON pela saída padrão;
5. usar mecanismos próprios de idempotência para efeitos externos;
6. registrar falhas de forma recuperável.

O worker não presume um provedor de IA. O executor pode futuramente ser um agente OpenAI, Claude, Gemini, modelo local, serviço próprio ou outro mecanismo compatível.

## Persistência

`cerebro/data` deve permanecer em armazenamento persistente. O container pode ser recriado sem perder o estado quando o volume persistente for mantido.

## Reinício e recuperação

Se o processo cair:

```text
queda
  ↓
estado persistente
  ↓
lease expira
  ↓
novo worker assume
  ↓
recupera trabalho elegível
  ↓
continua com idempotência
```

A recuperação não deve repetir cegamente efeitos externos. Cada integração deve declarar como evita duplicação ou como compensa uma ação parcialmente concluída.

## Segurança

Segredos não devem ser gravados no repositório nem no Cérebro. Tokens, chaves e credenciais devem ser fornecidos pelo mecanismo seguro da infraestrutura de hospedagem.

O executor externo é uma fronteira de confiança. Antes de permitir ações de escrita ou alto impacto, a política de autonomia deve ser aplicada.

## GitHub

GitHub pode disparar eventos, armazenar código, documentação, evidências e workflows. Ele não é requisito para que o runtime permaneça vivo.

O workflow de coleta existente pode servir como mecanismo auxiliar de despertar/eventos, mas uma execução 24/7 deve usar um runtime hospedado de forma persistente.

## Critério de validação

O deploy será considerado tecnicamente validado somente após demonstrar:

- iniciar fora do navegador;
- processar uma missão;
- persistir estado;
- interromper o processo deliberadamente;
- recuperar a execução;
- evitar duplicação do ciclo;
- registrar evidência;
- continuar após reinício;
- permitir trocar o executor sem perder o estado do Projeto.

## Estado

**EM_CONSTRUCAO** — o pacote de runtime e deploy está preparado; a hospedagem real ainda é uma etapa operacional dependente da infraestrutura escolhida.
