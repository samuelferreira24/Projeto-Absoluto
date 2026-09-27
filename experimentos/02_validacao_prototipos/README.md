# Experimento 02 — Validação de protótipos alternativos

Objetivo: atacar a hipótese da família de moldes com missões mais próximas do ABS real e verificar se duas arquiteturas diferentes conseguem preservar os mesmos invariantes.

Este experimento é isolado, não oficial e não altera main.

## Protótipos

- A — Controlador Adaptativo: separa estado, decisão, modo de execução e transição.
- B — Grafo de Moldes: representa moldes como nós composáveis com transições condicionais.

Nenhum é considerado vencedor. O objetivo é verificar se ambos conseguem satisfazer o mesmo contrato.

## Invariantes

1. Objetivo permanece externo ao molde.
2. Contexto/estado influencia a estratégia.
3. Recurso não define estratégia.
4. Complexidade deve ser proporcional.
5. Composição precisa preservar ordem/dependência.
6. Falha pode provocar troca de molde.
7. Contexto pode mudar durante a missão.
8. Resultado não equivale automaticamente a sucesso semântico.
9. Falta de capacidade não deve virar DIRECT silenciosamente.
10. Autorização é transição de controle, não molde.
11. Descoberta/aquisição pode ser necessária antes da execução.
12. Imperador pode sobrescrever seleção dentro da autoridade permitida.

## Critério

Um protótipo passa se tratar corretamente os casos sem criar uma regra específica para cada missão.
