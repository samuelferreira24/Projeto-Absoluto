# MATRIZ DE CONHECIMENTO HISTÓRICO — SISTEMA → ABS V1
## 2026-09-19

Objetivo: registrar descobertas do Sistema antigo como conhecimento histórico, preservando a diferença entre **evidência**, **interpretação** e **herança ainda não validada**.

| ID | Experimento/descoberta | Evidência histórica | Resultado/observação | Tipo | Relação com ABS | Estado |
|---|---|---|---|---|---|---|
| H-001 | Memória independente da interface | `MEMORIA.md` define exportação independente e exige que o dado saia inteiro sem o app | Troca de PWA/app/workflow não deveria exigir reconstrução da memória | descoberta explícita | memória própria, continuidade e substituição de interface | CONFIRMADO NO HISTÓRICO |
| H-002 | Separação de tipos de memória | `MEMORIA.md` separa MÉTODO, ESTADO, ESTRUTURA, PRINCÍPIO, DECISÃO, CALIBRAGEM, LIÇÃO e CONTEXTO | Contexto externo é dado bruto e não ordem | descoberta explícita | Cérebro, proveniência, segurança epistemológica | CONFIRMADO NO HISTÓRICO |
| H-003 | Motor substituível | `MEMORIA.md` e sementes registram motor HTTP compatível, local/remoto e lição sobre dependência do fornecedor | Motor é meio; memória/arquitetura permanecem | descoberta explícita | regra próprio/emprestado/substituível | CONFIRMADO NO HISTÓRICO |
| H-004 | Capacidade separada de autorização | `executor.py`, documentação e sementes registram bloqueios, aprovação e operações proibidas | Sistema pode possuir capacidade sem conceder autoridade automática | descoberta explícita | autorização/controle do ABS | CONFIRMADO NO HISTÓRICO |
| H-005 | Execução com proteção | `executor.py` usa snapshot/rollback e bloqueia operações sensíveis | Execução foi tratada como domínio de risco | implementação + princípio | executor seguro do ABS | CONFIRMADO NO HISTÓRICO; arquitetura futura não definida |
| H-006 | Proveniência da informação | `coletor.py`/semente registram fonte, domínio, data e conteúdo suspeito | Informação externa é rastreável e pode ser neutralizada | implementação + descoberta | Mini-Cérebro histórico | CONFIRMADO NO HISTÓRICO |
| H-007 | Busca em múltiplas camadas | `base.py` implementa FTS5, vetores e combinação ponderada por fonte | Recuperação textual e semântica foram combinadas | implementação | mecanismo de recuperação do Mini-Cérebro | CONFIRMADO NO HISTÓRICO; implementação não herdada automaticamente |
| H-008 | Lacuna como dado operacional | `base.py` registra buscas/achados; sementes mencionam lacunas | Ausência de conhecimento pode ser registrada | hipótese/descoberta parcial | investigação histórica | REQUER VALIDAÇÃO |
| H-009 | Especialização/orquestração | `orquestrador.py`, `especialistas.py`, `jetro.py` | Fluxo distribui tarefas e integra resultados | experimento arquitetural | composição de capacidades | CONFIRMADO COMO EXPERIMENTO; não como arquitetura ABS |
| H-010 | Ponte entre componentes | `ponte.py` cria comunicação local | Componentes podem cooperar sem fusão | experimento + descoberta | Bridge dos dois cérebros | CONFIRMADO COMO ANTECEDENTE |
| H-011 | Continuidade separada da interface | `arranque.sh`, `rodar-coleta.sh`, Termux e P1 | Tentativa de executar sem interface aberta | experimento | continuidade operacional ABS | CONFIRMADO COMO EXPERIMENTO |
| H-012 | Android como meio de acesso | `NATIVO.md` afirma que mais acesso ao Android altera acesso, não inteligência | Controle de plataforma não equivale a inteligência | descoberta explícita | integração ABS + Android | CONFIRMADO NO HISTÓRICO |
| H-013 | Limitação precisa ser classificada | código/documentação registram limites de RAM, motor, Android, background e recursos | Nem toda falha é falha conceitual | descoberta metodológica | AV/diagnóstico | CONFIRMADO NO HISTÓRICO |
| H-014 | Validação antes de expansão | `P1-SISTEMA-PROPRIO.md` coloca motor local + validação antes de VPS/orquestração | O histórico reconhece risco de construir casca antes de provar núcleo | lição explícita | método atual mapear→pesquisar→validar→construir | CONFIRMADO NO HISTÓRICO |
| H-015 | Casca substituível | `MEMORIA.md` e lições distinguem app/interface de dado e regras | A mesma memória pode alimentar outra casca | descoberta explícita | identidade/continuidade do ABS | CONFIRMADO NO HISTÓRICO |
| H-016 | Motor local no celular como experimento | `P1-SISTEMA-PROPRIO.md` propõe llama.cpp + Termux e teste no hardware real | A proposta pretendia transformar uma hipótese em evidência no aparelho | plano/hipótese histórica | atual Android V0 | HISTÓRICO; não confundir proposta com teste atual |
| H-017 | Operação contínua em Android | `P1-SISTEMA-PROPRIO.md`/scripts propõem Termux scheduler e recuperação | Documento registra que Android pode matar processo sob pressão | hipótese + evidência declarada no histórico | continuidade ABS | REQUER REVALIDAÇÃO NO A17/Android 16 |
| H-018 | Separação Núcleo/Operação | `MEMORIA.md` e `semente-operacao.json` mantêm espaços separados | Dados e estados operacionais não precisam ser misturados | descoberta/estrutura | separação de domínios do Cérebro | CONFIRMADO NO HISTÓRICO |
| H-019 | Aprendizado por erros registrados | sementes contêm CALIBRAGEM/LIÇÃO com falhas e correções | erro vira material de aprendizagem | descoberta/estrutura | memória de experiência do ABS | CONFIRMADO NO HISTÓRICO |
| H-020 | Fonte primária sobre comentário | `semente-nucleo.json` registra a lição explicitamente | Qualidade da origem deve influenciar recuperação | lição explícita | AV/proveniência | CONFIRMADO NO HISTÓRICO |

## Relações descobertas

```
MEMÓRIA
   ├── independência da interface
   ├── tipos epistemológicos
   └── versionamento
        ↓
MINI-CÉREBRO

COLETA
   ├── proveniência
   ├── neutralização
   └── lacunas
        ↓
MINI-CÉREBRO

BASE
   ├── recuperação textual
   ├── recuperação semântica
   └── uso dos resultados
        ↓
MINI-CÉREBRO

EXECUTOR
   ├── capacidade
   ├── autorização
   ├── snapshot
   └── rollback
        ↓
ABS

PONTE
   ↓
DOIS CÉREBROS

CONTINUIDADE + ANDROID
   ↓
ABS COMO SISTEMA OPERACIONALMENTE VIVO
```

## Separação epistemológica

### Evidência direta
O arquivo/implementação histórica afirma ou implementa.

### Interpretação histórica
O que podemos concluir razoavelmente sobre o objetivo/descoberta.

### Hipótese
Ainda precisa ser testada.

### Herança
Uma ideia do histórico pode ser relevante para ABS, mas isso não significa que a implementação antiga deva ser reutilizada.

## Regra desta matriz

**Nenhuma linha “CONFIRMADA NO HISTÓRICO” significa “arquitetura aprovada para o ABS”.**

Ela significa apenas que existe evidência suficiente para dizer que aquele princípio/experimento realmente pertence ao histórico recuperado.

## Próximo passo

Reconstituir os experimentos individualmente, começando pelos quatro que têm maior ligação com o ABS atual:

1. MEMÓRIA
2. EXECUÇÃO/AUTORIZAÇÃO
3. PONTE
4. CONTINUIDADE ANDROID

Depois cruzar com os commits que introduziram/modificaram cada componente e registrar:
**problema → hipótese → implementação → teste → resultado → falha → correção → descoberta.**
