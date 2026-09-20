# ABS — Fundação de Capacidades V1

## Estado

A fundação mantém a regra central do Projeto Absoluto: **capacidades primeiro; interface depois**.

A V1 fornece:

1. intenção;
2. trabalho persistente;
3. registro de capacidades;
4. execução;
5. estado e eventos;
6. resultado e proveniência;
7. continuidade;
8. controle do Imperador.

## Ordem de construção

```
Imperador
  ↓
Comando / intenção
  ↓
Work persistente
  ↓
Orquestração
  ↓
Adaptador de capacidade
  ↓
Execução
  ↓
Eventos / estado
  ↓
Memória / proveniência
  ↓
Controle
  ↓
Interface
```

## Codex CLI

O primeiro adaptador real é o **Codex CLI local**.

O ABS não importa o SDK Python do Codex. Ele chama o executável `codex` disponível no ambiente e consome sua saída JSONL. O modo não interativo `codex exec --json` fornece eventos estruturados, incluindo o identificador da thread e mensagens do agente. Uma sessão pode ser retomada com `codex exec resume <SESSION_ID>`.

O adaptador registra o identificador da sessão no `Work`, permitindo:

```
WORK
 ↓
Codex CLI
 ↓
thread_id persistido
 ↓
Codex CLI resume
 ↓
continuação do trabalho
```

## Segurança e sandbox

O adaptador usa por padrão:

```
sandbox = read-only
approval = never
```

Isso mantém a primeira integração em modo de baixo impacto. Para operações que precisam editar o workspace, o ABS pode receber explicitamente:

```
ABS_CODEX_SANDBOX=workspace-write
```

O ambiente Android/Termux usado atualmente apresentou incompatibilidade do sandbox Linux do Codex com `proot/bwrap`. Nesse ambiente, a execução com acesso elevado só deve ser habilitada explicitamente e para um workspace controlado.

O bypass completo fica separado atrás de:

```
ABS_CODEX_DANGEROUSLY_BYPASS=1
```

e nunca é ativado por padrão.

## Configuração

Variáveis opcionais:

- `ABS_CODEX_COMMAND`: executável do Codex; padrão `codex`.
- `ABS_CODEX_SANDBOX`: modo de sandbox.
- `ABS_CODEX_APPROVAL`: política de aprovação.
- `ABS_CODEX_TIMEOUT`: timeout em segundos; padrão 900.
- `ABS_CODEX_DANGEROUSLY_BYPASS`: habilita explicitamente o bypass completo.

A autenticação permanece fora do repositório, no ambiente local do Codex. Nunca registrar tokens ou `~/.codex/auth.json` no projeto.

## Critério de sucesso

```
Imperador cria trabalho
→ ABS seleciona Codex
→ Codex executa
→ ABS recebe resultado
→ ABS registra sessão/proveniência
→ trabalho pode ser retomado
→ outra capacidade pode assumir posteriormente
```

## Próxima etapa

Com a ponte Codex CLI validada, o próximo passo é usar essa capacidade para avançar a construção do próprio ABS, mantendo a interface como camada de acesso ao núcleo.

A interface não define o ABS. Ela expõe as capacidades que o núcleo realmente possui.
