# CONTRATO DE PROVA DA CONTINUIDADE

A camada de conhecimento só pode afirmar o que consegue sustentar.

## Níveis

- **observed**: estrutura encontrada no repositório.
- **tested**: teste automatizado passou.
- **operational**: execução real foi comprovada.
- **degraded**: existia evidência anterior, mas a evidência atual indica falha.
- **unavailable**: não há caminho utilizável no estado atual.
- **historical**: pertence ao histórico, não ao estado atual.
- **hypothetical**: possibilidade ainda não comprovada.

## Regra

Código + documentação != capacidade comprovada.

Cada promoção de estado deve registrar:
- fonte;
- timestamp;
- revisão;
- teste ou execução;
- resultado;
- proveniência.

## Continuidade

Se uma conversa terminar, uma nova IA deve conseguir reconstruir o estado a partir destas evidências sem confiar em lembranças da conversa anterior.
