# Governança do Limite de Execução — V0.2

## Descoberta

A auditoria do ciclo encontrou uma inconsistência: a política de autonomia limitava níveis de ação, mas o worker ainda poderia executar um comando externo arbitrário quando recebia a política padrão.

Pesquisa atual sobre agentes de longa duração reforça a necessidade de separar capacidade, autorização, escopo técnico, execução, observabilidade e intervenção.

## Correção

A fronteira passa a ser:

CAPACIDADE → AÇÃO PROPOSTA → AUTORIZAÇÃO → ESCOPO TÉCNICO → EXECUÇÃO → RESULTADO → AUDITORIA

O executor externo agora exige um allowlist explícito de executáveis. Sem allowlist, a execução externa é bloqueada por padrão.

O escopo pode restringir:
- executáveis;
- diretório de trabalho;
- variáveis de ambiente;
- tempo máximo de execução;
- shell desabilitado.

## Limite atual

Ainda não existe sandbox completo de sistema operacional, isolamento de filesystem, política de rede, quotas de CPU/memória, aprovação humana persistida ou prova criptográfica de que um executor permaneceu dentro do escopo.

Esses mecanismos continuam sendo requisitos antes de ampliar autonomia para ações de alto impacto.

## Princípio

> A autorização lógica não substitui o limite técnico. O Projeto Absoluto só deve ampliar autonomia quando ambos evoluírem juntos.
