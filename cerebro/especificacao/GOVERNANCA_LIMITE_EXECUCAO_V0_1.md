# Governança do Limite de Execução — V0.1

## Descoberta

A capacidade técnica de executar uma ação não deve ser confundida com autorização para executá-la.

Pesquisa recente e práticas atuais de agentes reforçam a separação entre capacidade, autorização, execução e verificação/auditoria.

## Aplicação no Projeto Absoluto

CAPACIDADE → AÇÃO PROPOSTA → POLÍTICA / AUTORIZAÇÃO → EXECUÇÃO → RESULTADO → AUDITORIA

O ExecutorCerebro já possui uma fronteira de política. O worker agora também aplica essa fronteira ao executor externo, mantendo a política configurável.

## Limite V0.1

A política atual classifica a ação em níveis de autonomia, mas ainda não possui escopo por recurso/arquivo/destino, permissões por ferramenta, sandbox técnico, política de rede, aprovação humana persistida ou prova de que a ação permaneceu dentro do escopo autorizado.

Esses itens devem ser desenvolvidos antes de aumentar a autonomia operacional do sistema.

## Princípio

> O Projeto Absoluto pode ampliar sua autonomia de execução somente quando a autoridade, o escopo, a observabilidade e os mecanismos de intervenção evoluírem junto.