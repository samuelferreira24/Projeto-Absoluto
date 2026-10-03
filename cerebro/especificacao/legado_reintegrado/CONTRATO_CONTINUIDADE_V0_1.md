# Contrato de Continuidade da Construção — V0.1

## Finalidade

Garantir que uma nova IA, colaborador, ferramenta ou plataforma possa assumir uma parte da construção sem depender de memória privada de uma conversa anterior.

## Entrada mínima

O agente que assume uma tarefa deve receber acesso a:

1. visão e objetivos relevantes;
2. arquitetura vigente;
3. mapa da construção;
4. estado atual;
5. decisões relevantes;
6. contratos das interfaces envolvidas;
7. código e documentação pertinentes;
8. testes existentes;
9. problemas conhecidos;
10. evidências disponíveis;
11. próxima ação registrada.

## Protocolo de execução

```text
LER ESTADO
  ↓
CONFIRMAR CONTEXTO
  ↓
INSPECIONAR ARTEFATOS
  ↓
IDENTIFICAR CONTRATO
  ↓
EXECUTAR MENOR AÇÃO ÚTIL
  ↓
TESTAR
  ↓
VALIDAR
  ↓
REGISTRAR RESULTADO
  ↓
ATUALIZAR ESTADO
  ↓
ATUALIZAR MAPA
```

## Registro de transferência

Toda transferência relevante deve preservar:

- tarefa;
- objetivo;
- estado recebido;
- trabalho realizado;
- arquivos/componentes afetados;
- testes executados;
- resultados;
- evidências;
- decisões tomadas;
- problemas encontrados;
- hipóteses ainda abertas;
- riscos;
- dependências;
- alterações que não devem ser feitas sem revisão;
- próxima ação;
- condição de conclusão.

## Regra de autoridade

O agente que executa uma tarefa não passa a ser proprietário da identidade ou do conhecimento do Projeto. Suas contribuições entram no sistema por meio de registros, evidências, decisões, histórico e artefatos versionados.

## Regra de divergência

Se o agente encontrar diferença entre estado, mapa, documentação, código, testes ou realidade observada, não deve ocultar a diferença para manter aparência de consistência. Deve registrá-la como divergência e iniciar o fluxo de análise e correção apropriado.

## Regra de encerramento

Uma tarefa só deve ser considerada concluída quando seu critério de conclusão estiver atendido e houver verificação suficiente. Quando a validação real não for possível, o estado deve indicar explicitamente a limitação.

## Resultado esperado

A construção deve permanecer transferível entre IAs e ferramentas sem perder contexto, rastreabilidade, histórico, proveniência ou capacidade de continuar.


## Aplicação prática — arquitetura de preservação de contexto — 2026-10-03

O contrato acima continua válido e passa a ser interpretado através da pesquisa `docs/00_governanca/PESQUISA_PRESERVACAO_CONTEXTO_CONTINUIDADE_V1.md`.

A transferência não deve depender de um único handoff. O encerramento de uma tarefa relevante deve preservar, conforme o que mudou:

1. **conhecimento** — entendimento novo que deve sobreviver à sessão;
2. **decisão** — decisão efetivamente tomada pela autoridade competente;
3. **pesquisa/evidência** — descoberta, fonte, teste ou observação que sustenta uma afirmação;
4. **estado** — situação operacional atual;
5. **artefatos** — código, arquivos e resultados produzidos;
6. **checkpoint** — estado recuperável de trabalho interrompido;
7. **handoff** — ponte curta para a próxima sessão;
8. **proveniência** — origem, revisão, temporalidade e relação com a fonte.

### Regra operacional

**Não atualizar apenas o handoff quando uma sessão produzir uma mudança de outra categoria.**

O registro deve ir para a camada correspondente, e o handoff deve apontar para ela.

### Recuperação

A nova IA deve recuperar contexto nesta ordem, adaptando ao objetivo da tarefa:

intenção → navegação → estado → decisões → evidências/pesquisa → fontes profundas → artefatos → execução

O handoff acelera essa entrada, mas não substitui nenhuma fonte canônica.

### Verificação

O Project Knowledge deve registrar as camadas de continuidade observáveis e sua proveniência. A automação pode detectar presença, hash, estado técnico e relações derivadas, mas não pode promover automaticamente interpretação de IA a decisão humana.

### Critério de transferência

Uma transferência é adequada quando outra IA consegue iniciar a tarefa sem acesso à conversa anterior e sem precisar reconstruir o Projeto a partir de um único resumo.
