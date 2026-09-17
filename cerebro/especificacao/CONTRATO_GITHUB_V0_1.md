# Contrato Operacional GitHub — V0.1

## Finalidade

Definir uma fronteira estável entre o Projeto Absoluto e o GitHub. O GitHub fornece execução, versionamento e evidências operacionais; a identidade, o estado e o conhecimento de construção pertencem ao Projeto.

## Princípio

```text
PROJETO ABSOLUTO
      ↕
CONTRATO GITHUB
      ↕
REPOSITÓRIO / BRANCH / COMMIT / PR / ACTIONS / CHECKS / ARTEFATOS
```

Nenhum componente do Projeto deve depender de uma sessão específica de chat para interpretar o estado do GitHub.

## Unidade de comunicação

Toda execução relevante deve poder ser correlacionada por:

- `repository`;
- `ref` (branch/tag/ref);
- `commit`;
- `workflow`;
- `run_id`;
- `correlation_id`;
- `idempotency_key`;
- `observed_at`.

## Ciclo operacional

```text
OBJETIVO
  ↓
ESTADO ATUAL
  ↓
ALTERAÇÃO
  ↓
COMMIT
  ↓
ACTIONS
  ↓
CHECKS / LOGS / ARTEFATOS
  ↓
INTERPRETAÇÃO
  ↓
CORREÇÃO, SE NECESSÁRIA
  ↓
NOVA VALIDAÇÃO
  ↓
EVIDÊNCIA
  ↓
ATUALIZAÇÃO DO ESTADO
```

## Estados da execução

- `EM_VALIDACAO_CI`: execução ainda não terminou;
- `VALIDADO_CI`: execução terminou com conclusão de sucesso;
- `FALHOU_CI`: execução terminou com falha, cancelamento ou timeout;
- `ESTADO_DESCONHECIDO_CI`: payload insuficiente ou estado não reconhecido.

`VALIDADO_CI` significa apenas que a validação automatizada representada pela execução passou. Não significa que todo o Projeto ou toda a arquitetura esteja validada.

## Evidências

Para uma falha, preservar sempre que disponível:

- commit;
- run;
- job;
- etapa que falhou;
- logs;
- arquivos/componentes afetados;
- hipótese de causa;
- correção aplicada;
- nova execução;
- resultado final.

## Idempotência e ciclos

Operações repetíveis devem usar uma chave de idempotência derivada de repositório, ref e operação. O mecanismo deve evitar processar duas vezes o mesmo evento quando isso não produzir benefício.

Eventos devem possuir correlação suficiente para detectar ciclos como:

```text
A → B → A → B → ...
```

## Permissões

O acesso deve seguir o princípio do menor privilégio. Leitura de estado deve ser separada de ações de escrita, execução, rerun, merge e outras operações de maior impacto.

## Segurança de mudança

A camada não deve realizar merge ou ações irreversíveis apenas porque uma validação passou. Essas operações continuam sujeitas às regras de autorização do Projeto.

## Limite da integração

O GitHub é uma infraestrutura operacional do Projeto. Não é a fonte única da identidade, do conhecimento, da memória ou do mapa da construção.

O contrato deve permanecer utilizável caso o Projeto troque GitHub por outra infraestrutura no futuro.
