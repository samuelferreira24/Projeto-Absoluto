# Relatório — Experimento 02

## Pergunta

A família de moldes continua válida quando saímos de exemplos simples e introduzimos estado incompleto, autorização, capacidade inexistente, restrições, falhas, verificação e mudança de estado?

## Ataques

O experimento 01 tinha uma simplificação perigosa: quando as restrições eliminavam todos os moldes especializados, o seletor retornava DIRECT. Isso pode ser incorreto se DIRECT não possuir capacidade suficiente para cumprir o objetivo.

O experimento 02 transforma esse ponto em teste adversarial. O comportamento esperado passa a ser BLOCKED/DISCOVER/WAIT_AUTH/OBSERVE quando não existe execução segura ou suficiente.

Também foram atacados:

- contexto incompleto;
- autorização pendente;
- capacidade ausente;
- composição de critérios;
- orçamento de complexidade;
- falha do executor;
- falha de verificação;
- mudança de estado durante a missão;
- sucesso semântico;
- independência entre recurso e molde;
- override explícito do Imperador.

## Resultado esperado dos dois protótipos

### Protótipo A — Controlador Adaptativo

Separação explícita entre:

ESTADO → CONTROLE → SELEÇÃO DE MODO → EXECUÇÃO → EVENTO → NOVA DECISÃO

### Protótipo B — Grafo de Moldes

Representação como:

ESTADO → NÓ/MOLDE → TRANSIÇÃO → NOVO ESTADO

Ambos devem suportar composição e replanejamento sem transformar todos os problemas em AGENT/MULTIAGENT.

## Critério de aprovação

Os protótipos não precisam produzir a mesma implementação interna. Precisam preservar os mesmos invariantes comportamentais.

## Interpretação

Se ambos passarem, teremos duas famílias de implementação candidatas, e não uma arquitetura oficial. A próxima etapa é colocar as duas contra o runtime real do ABS em modo adaptador/simulação, sem alterar o núcleo.

Se uma falhar, o erro deve ser usado para corrigir o contrato, não para esconder a diferença.

## Limitações

Ainda não é prova de produção. Os executores são simulados; não há ainda execução real de ferramentas/IA, concorrência real, persistência de plano, rollback de efeitos externos ou avaliação semântica por domínio.

## Próxima barreira

Experimento 03: integração em modo sombra com o ABS real. O protótipo recebe missões reais, observa o que o ABS atual faria e produz uma decisão/plan sem executar nenhuma ação externa. Isso permite medir divergências sem risco para main.
