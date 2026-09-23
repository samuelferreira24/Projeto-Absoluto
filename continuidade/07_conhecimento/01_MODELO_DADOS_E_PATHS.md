# MODELO DE DADOS — CONHECIMENTO DE CONSTRUÇÃO

## Entidades mínimas

- projeto
- componente
- capacidade
- recurso
- ferramenta
- nó
- caminho
- evidência
- decisão
- evento
- proveniência

## Caminho operacional

`PATH_ID → objetivo → origem → destino → pré-condições → recursos → ferramentas → operação → autorização → risco → teste → evidência → fallback → estado → última validação`

## Evidência

Evidência é obrigatória para promover um caminho de `observed` para um estado operacional.

A presença de um arquivo, classe ou documentação não prova execução.

## Expansão automática

A camada deve aceitar novos registros descobertos sem exigir que o Imperador redesenhe manualmente os mapas. A expansão automática é derivada do estado observável e permanece separada da autoridade humana.
