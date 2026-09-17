# Contrato de Integração — V0.1

## Finalidade

Definir uma fronteira estável entre o Projeto Absoluto e qualquer IA, conta, plataforma, ferramenta ou sistema externo.

## Princípio central

Integrações devem adaptar recursos externos ao Projeto; o Projeto não deve adaptar sua identidade ao fornecedor.

## Entrada mínima

Toda solicitação integrada deve poder carregar, quando aplicável:

- `project_id`
- `agent_id`
- `session_id`
- `request_id`
- `correlation_id`
- objetivo
- contexto
- permissões concedidas
- nível de autonomia
- restrições
- evidências disponíveis

## Saída mínima

Toda operação relevante deve poder produzir:

- resultado;
- estado;
- evidência;
- eventos;
- problemas;
- decisões;
- custo/recursos quando mensurável;
- próxima ação;
- referência para reconstrução da execução.

## Adaptadores

Um adaptador é responsável por traduzir o contrato do Projeto para o protocolo específico de um fornecedor. O núcleo não deve depender da implementação interna do fornecedor.

## Falhas

Falhas de integração devem ser classificadas separadamente de falhas da tarefa. Timeout, indisponibilidade, autenticação, limite, formato incompatível e resposta inválida não devem ser confundidos com erro de domínio.

## Idempotência

Operações repetíveis devem carregar uma chave de idempotência. Reprocessamento não deve gerar efeitos duplicados quando a operação exigir unicidade.

## Segurança

O adaptador deve respeitar as permissões e o nível de autonomia concedidos. Ausência de permissão não pode ser interpretada como autorização implícita.

## Portabilidade

A remoção de um fornecedor não pode destruir identidade, histórico, decisões, evidências ou conhecimento do Projeto.

## Estado

Integração é um mecanismo de transporte e execução. A fonte de verdade do Projeto deve permanecer em estruturas sob controle do próprio Projeto, quando tecnicamente possível.
