# ÍNDICE DE ARQUITETURA E ACERVO V0.1

Data: 2026-09-17
Branch de construção: `base-cerebro-v0.1`

## 1. Finalidade

Este índice resolve um problema diferente do mapa mestre: ele informa **onde cada tipo de conhecimento deve viver e qual documento deve ser usado como referência**, sem apagar materiais históricos.

## 2. Hierarquia documental

```text
PROJETO ABSOLUTO
│
├── DIREÇÃO / VISÃO
│   └── MAPA_MESTRE_PROJETO_ABSOLUTO_V0_2.md
│
├── ARQUITETURA DO CÉREBRO
│   ├── ARQUITETURA_FUNDACAO_V0_2.md
│   ├── ESTRUTURA_ATUAL_V0_2.md
│   └── contratos específicos
│
├── MÉTODO
│   ├── METODO_TRABALHO_V0_1.md
│   ├── PROTOCOLO_OTIMIZACAO_CONTINUA_V0_1.md
│   └── documentos de pesquisa/metodologia
│
├── MEMÓRIA / APRENDIZADO
│   ├── memoria/*.jsonl / *.json
│   ├── MEMORIA_DE_APRENDIZADO_E_CONSTRUCAO_V0_1.md
│   ├── CICLO_PERMANENTE_DE_APRENDIZADO_V0_1.md
│   └── MODELO_EXPERIENCIA_APLICACAO_SABEDORIA_V0_1.md
│
├── EXECUÇÃO / CONTINUIDADE
│   ├── contratos de runtime
│   ├── continuidade entre chats
│   └── mapas de execução
│
├── ORQUESTRAÇÃO / MULTIPLICADORES
│   ├── COMPOSICAO_ORQUESTRACAO_MULTIPLICADORES_V0_1.md
│   ├── AGENDAMENTO_ADAPTATIVO_V0_2.md
│   ├── ORQUESTRACAO_EXECUCAO_CONTINUA_V0_2.md
│   └── documentos anteriores preservados como histórico
│
└── ACERVO HISTÓRICO
    ├── documentos-base
    ├── relatórios
    ├── transcrições
    ├── MHT/MHTML
    └── conteúdo legado ainda não reconciliado
```

## 3. Classificação dos principais itens

| Item | Classificação | Uso |
|---|---|---|
| `cerebro/especificacao/MAPA_MESTRE_PROJETO_ABSOLUTO_V0_2.md` | CANÔNICO_ATUAL | quadro mestre do Projeto |
| `cerebro/ESTRUTURA_ATUAL_V0_2.md` | CANÔNICO_ATUAL | fotografia física do Cérebro |
| `cerebro/especificacao/ARQUITETURA_FUNDACAO_V0_2.md` | CANÔNICO_ATUAL | fundação arquitetural |
| `cerebro/especificacao/AGENDAMENTO_ADAPTATIVO_V0_2.md` | CANÔNICO_ATUAL | agendamento adaptativo atual |
| `cerebro/especificacao/ORQUESTRACAO_EXECUCAO_CONTINUA_V0_2.md` | CANÔNICO_ATUAL | orquestração/runtime evolutivo |
| `cerebro/especificacao/COMPOSICAO_ORQUESTRACAO_MULTIPLICADORES_V0_1.md` | CANÔNICO_ATUAL / BASE | composição e multiplicadores |
| `cerebro/especificacao/CONTINUIDADE_ENTRE_CHATS_V0_2.md` | CANÔNICO_ATUAL | continuidade |
| `cerebro/especificacao/PESQUISA_RETENCAO_EVOLUCAO_CONHECIMENTO_V0_1.md` | ATIVO | pesquisa/retensão |
| `cerebro/especificacao/MECANISMO_DESCOBERTA_E_REAVALIACAO_V0_1.md` | ATIVO | descoberta e reavaliação |
| `cerebro/memoria/` | ATIVO | memória persistida |
| `Projeto_Absoluto_MEMORIA_IA_V10_ATUALIZADO.docx` | FONTE_BRUTA | referência histórica primária |
| `Projeto_Absoluto_EBOOK_HUMANO_V10_ATUALIZADO.docx` | FONTE_BRUTA | referência histórica primária |
| `Pesquisa_Representacao_Armazenamento_Informacao_IA_Projeto_Absoluto_v1.docx` | FONTE_BRUTA | pesquisa histórica primária |
| `Transcricao_Conversa.txt` | FONTE_BRUTA / HISTÓRICO | reconstrução histórica |
| `Relatorio_Diagnostico_Completo_da_Conversa.docx` | FONTE_BRUTA / HISTÓRICO | diagnóstico histórico |
| relatórios de contribuição | FONTE_BRUTA / HISTÓRICO | patrimônio das contas |
| `Visao_Geral.md` | HISTÓRICO | visão anterior; não normativa |
| `cerebro/ESTRUTURA_ATUAL_V0_1.md` | HISTÓRICO | fotografia anterior |
| `orquestracao_adaptativa.py` | EXPERIMENTAL / EM RECONCILIAÇÃO | implementação paralela não integrada |
| `automacao/.gitkeep` | MIGRAÇÃO_PENDENTE | contém texto, não é placeholder puro |
| `comercial/.gitkeep` | MIGRAÇÃO_PENDENTE | contém texto, não é placeholder puro |
| `docs/.gitkeep` | MIGRAÇÃO_PENDENTE | contém texto, não é placeholder puro |
| `metas_pessoais/.gitkeep` | MIGRAÇÃO_PENDENTE | contém texto, não é placeholder puro |

## 4. Regra para documentos concorrentes

Não existe “documento mais novo = apagar documento antigo”.

O documento novo recebe a função de referência atual; o antigo permanece como histórico quando possuir valor para compreender decisões, erros, mudanças de entendimento ou origem de conceitos.

## 5. Regra para código concorrente

Quando duas implementações têm responsabilidades semelhantes:

1. identificar as diferenças;
2. registrar a finalidade de cada uma;
3. determinar qual está integrada ao fluxo principal;
4. preservar a outra como experimental/histórica;
5. só então decidir consolidação, substituição ou remoção.

## 6. Regra para fontes históricas

Fonte original permanece intacta. Derivações devem apontar para a fonte. Resumos e interpretações não substituem o original.

## 7. Regra para memória

Conhecimento relevante descoberto durante a construção deve receber registro persistente apropriado, com contexto, proveniência e relação com o restante do Cérebro.

## 8. Regra para estado atual

Snapshots de estado são fotografias temporais. Não devem ser usados para reescrever ou apagar o passado. O Git permanece como histórico de alterações da construção, enquanto o Cérebro deve registrar o significado das alterações.

## 9. Pendências documentais prioritárias

- extrair e reconciliar os documentos binários-base;
- extrair e classificar os MHT/MHTML;
- migrar com preservação o conteúdo dos `.gitkeep` não vazios;
- marcar explicitamente documentos históricos/legados;
- consolidar a autoridade entre especificações de agendamento/orquestração;
- registrar a relação entre `agendador.py` e `orquestracao_adaptativa.py`;
- persistir estado do grafo, sinergias e decisões de orquestração;
- integrar experiência de execução à memória permanente.

## 10. Regra final

> **Organizar significa tornar encontrável, contextualizado, relacionado e corretamente classificado — não apagar aquilo que ainda não foi compreendido.**
