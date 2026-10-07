# Experimento 06 — Primeiro protótipo executável

Este é o primeiro protótipo que deixa de ser apenas um seletor e executa um ciclo completo em sandbox:

OBJETIVO → ESTADO → MODO → EXECUTOR → RESULTADO → NOVO ESTADO → NOVA DECISÃO

Foram mantidas duas implementações:

- A: controlador por estado;
- B: transições em grafo.

O executor é determinístico e não produz efeitos externos. Isso permite testar a lógica sem colocar o ABS real em risco.

## Cenários

1. execução simples;
2. falha seguida de recuperação;
3. falha de verificação seguida de recuperação;
4. mudança de estado durante execução;
5. descoberta de capacidade;
6. autorização;
7. pesquisa;
8. paralelização.

## Critério de avanço

O protótipo é considerado válido como protótipo experimental quando:

- consegue completar a missão em sandbox;
- muda de molde depois de falha;
- reage a mudança de estado;
- não confunde descoberta/autorização com execução;
- mantém o objetivo enquanto troca o modo;
- permite duas implementações diferentes do mesmo contrato.

## Limites

Ainda não é integração no ABS. Não usa ferramentas externas, não executa IA real, não altera banco real e não tem rollback de efeitos externos.

## Estado

Candidato a primeiro protótipo arquitetural executável. A existência de A e B é intencional: não há necessidade de escolher uma única forma antes de testar mais profundamente.
