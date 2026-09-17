# CONTINUIDADE ENTRE CHATS V0.2

## Objetivo

O Cérebro deve permitir que o trabalho continue em outra conversa sem depender de o histórico daquela conversa permanecer disponível.

A continuidade deve preservar, no mínimo:

- contexto de trabalho;
- estado atual do sistema;
- objetivo atual;
- próximo passo;
- progresso;
- decisões e motivos;
- entendimentos;
- descobertas;
- erros e correções;
- aprendizados;
- tarefas e dependências;
- missões e estado operacional;
- relações relevantes;
- proveniência das informações.

## Princípio

> O chat é uma interface de trabalho. O Cérebro é a memória persistente do trabalho.

A troca de chat, conta, modelo ou plataforma não deve obrigar o Projeto a recomeçar do zero.

## Camadas

```text
CONVERSA ATUAL
     ↓
CAPTURA DO CONTEXTO
     ↓
CHECKPOINT
     ├── estado
     ├── memória
     ├── aprendizado
     ├── progresso
     ├── decisões
     ├── tarefas
     ├── runtime
     └── relações
     ↓
SNAPSHOT PORTÁTIL
     ↓
PROMPT DE RETOMADA
     ↓
NOVO CHAT / NOVO AGENTE
     ↓
VALIDAÇÃO DO ESTADO
     ↓
CONTINUAÇÃO
```

## Dois produtos diferentes

### 1. `continuidade.json`

É a representação estruturada e completa do estado conhecido pelo Cérebro.

Serve para máquinas, integrações, auditoria e reconstrução automática.

### 2. `RETOMAR_OUTRO_CHAT.md`

É uma representação humana/IA portátil, pronta para ser copiada para outra conversa.

Ela contém a instrução explícita de não recomeçar do zero e de consultar o repositório quando disponível.

## O que significa "o que a IA aprendeu"

Não se deve tentar exportar estados internos ocultos do modelo como se fossem memória persistente garantida.

O Projeto deve registrar explicitamente aquilo que precisa sobreviver à troca de sessão:

- fatos e evidências;
- entendimentos construídos;
- decisões;
- hipóteses;
- resultados;
- experiências;
- erros;
- correções;
- princípios descobertos;
- mudanças de entendimento;
- estratégias que funcionaram ou falharam;
- contexto necessário para interpretar esses registros.

Assim, outra instância de IA pode reconstruir o contexto de trabalho a partir de uma memória externa verificável.

## Checkpoint

O checkpoint é uma fotografia persistente do trabalho em determinado momento.

Ele deve ser criado:

- antes de encerrar uma sessão importante;
- depois de uma mudança estrutural relevante;
- antes de trocar de chat quando a continuidade for necessária;
- após uma decisão que altere a rota;
- após um aprendizado importante.

O checkpoint não substitui o histórico. Ele aponta para e incorpora o estado necessário para a retomada.

## Retomada

Ao receber um pacote de continuidade, a nova conversa deve:

1. identificar o Projeto e o snapshot;
2. reconstruir o objetivo e o ponto de parada;
3. ler aprendizados e decisões relevantes;
4. verificar tarefas abertas;
5. validar o estado atual dos arquivos quando houver acesso ao repositório;
6. detectar mudanças ocorridas depois do snapshot;
7. continuar a partir do ponto válido mais recente;
8. registrar novas descobertas, decisões, erros e progresso.

## Regra contra perda de contexto

Nenhuma compactação ou resumo deve apagar silenciosamente a memória original.

```text
RAW / HISTÓRICO
      ↓
CONHECIMENTO ESTRUTURADO
      ↓
SNAPSHOT DE CONTINUIDADE
      ↓
RESUMO PORTÁTIL
```

O resumo é uma camada de acesso rápido. A memória estruturada e as evidências continuam sendo a fonte de reconstrução.

## Evolução futura

A continuidade deverá evoluir para:

- snapshots incrementais;
- IDs de sessão e de cadeia de sessões;
- versionamento de contexto;
- comparação entre snapshots;
- resolução de conflitos entre sessões concorrentes;
- sincronização entre plataformas;
- recuperação automática;
- compactação sem perda semântica relevante;
- recuperação seletiva conforme o objetivo;
- proveniência por item;
- detecção de conhecimento obsoleto;
- retomada automática por agente.

## Critério de sucesso

Trocar de chat não pode significar perder o trabalho.

O resultado esperado é:

```text
CHAT A → CHECKPOINT → CHAT B → VALIDAR → CONTINUAR
```

sem exigir que o usuário reconte manualmente tudo o que já foi construído.
