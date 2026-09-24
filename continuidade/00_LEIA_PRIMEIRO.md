# CONTINUIDADE — LEIA PRIMEIRO

## Função
`continuidade/` é a infraestrutura de transferência entre sessões e IAs.

Ela não é um segundo diretório geral de documentação.

## Ordem de leitura
1. `AGENTS.md`
2. `00_IA_NAVEGACAO.md`
3. `docs/00_GOVERNANCA_INFORMACAO.md`
4. `docs/00_MODELO_PROJETO_ABSOLUTO.md`
5. `continuidade/07_conhecimento/project_knowledge.json`
6. `continuidade/07_conhecimento/MAPA_AUTO_ESTADO_PROJETO.md`
7. `continuidade/07_conhecimento/SESSAO_ATUAL.md`
8. `cerebro/mapas/00_MAPA_MESTRE_PROJETO_ABSOLUTO_V1.md`
9. `continuidade/05_handoffs/01_HANDOFF_ATUAL_OPERACIONAL.md`
10. fonte específica conforme a pergunta.

## O que é continuidade
- checkpoint;
- handoff;
- decisão necessária à retomada;
- ponte para estado vivo;
- contexto de sessão;
- contratos de continuidade.

## O que não é continuidade
Material temático deve ficar na área funcional correspondente:
- operação → `docs/01_operacao/`;
- arquitetura → `docs/02_arquitetura/`;
- planejamento → `docs/03_planejamento/`;
- referência → `docs/04_referencia/`;
- fontes → `docs/90_fontes/`;
- auditoria → `docs/06_auditoria/`.

Por isso a antiga `continuidade/06_interface/` foi esvaziada e seus documentos foram classificados por função.

## Estado vivo
Project Knowledge é o estado estruturado derivado.
`MAPA_AUTO_ESTADO_PROJETO.md` é sua projeção legível.
Handoffs são checkpoints; não vencem o estado vivo automaticamente.
Snapshots antigos devem ser tratados como históricos.

## Regra de sessão
Uma sessão de IA que produzir decisão, descoberta, resultado, evidência, mudança de arquitetura, pendência ou ponto de retomada que altere o Projeto deve persistir isso antes de encerrar/transferir.

A conversa é temporária. O repositório é a continuidade.
