# Fechamento — ABS V1 Core

## Estado

A V1 Core do ABS está fechada como base operacional de software.

### Evidências

- Navegação de Conhecimento Verificável standalone: fechada.
- Integração nativa da navegação ao ABS: fechada.
- AI Layer: seleção por capacidades, modo offline e fallback entre inteligências.
- Orchestrator: execução, autorização, verificação e proveniência.
- Data Layer: persistência operacional e memória de trabalho/conversa.
- Aceitação end-to-end: conversa → navegação → inteligência → execução → verificação → Data Layer/proveniência.
- CI final: ABS Core e Project Knowledge Tests verdes.
- Suíte final: 163 testes passando.

## Limite desta etapa

Este fechamento não significa que o ABS esteja "completo". Significa que o núcleo necessário para entrar na operação contínua possui um ciclo verificável.

A partir daqui, novas melhorias de núcleo só entram quando um uso real revelar um gargalo.

## Próximo estágio

**Operação real e infraestrutura persistente.**

Prioridade imediata:
1. VPS/Coolify operacional.
2. ambiente de desenvolvimento remoto pelo celular.
3. serviços persistentes necessários.
4. deploy do ABS.
5. aceitação operacional no VPS.


## Plano operacional detalhado — ambiente de trabalho na VPS

A prioridade de construir um ambiente de desenvolvimento remoto pelo celular foi detalhada em:

- `docs/03_planejamento/PLANO_AMBIENTE_TRABALHO_VPS_ANDROID.md`

A ordem definida é: (1) construir e validar o ambiente de trabalho operável pelo Android; (2) continuar a construção do ABS nesse ambiente; (3) delegar ao ABS, gradualmente e sob limites verificáveis, a operação da infraestrutura. A auditoria do estado real precede instalações ou substituições.
