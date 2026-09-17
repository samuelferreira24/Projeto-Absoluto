# Contrato de Adaptadores de Coleta V0.1

## Finalidade

Permitir que qualquer chat, IA, plataforma, ferramenta ou sistema participe da memória do Projeto sem criar uma integração direta com todas as outras fontes.

## Regra N x N

Não conectar:

```text
ChatGPT <-> Claude <-> Gemini <-> GitHub <-> ferramenta <-> ...
```

Conectar cada fonte somente ao **barramento de coleta do Projeto**:

```text
ChatGPT ─┐
Claude ──┤
Gemini ──┤
GitHub ──┤
MCP ─────┤──> COLETA DO PROJETO ──> CÉREBRO
API ─────┤
Arquivo ─┤
Humano ──┘
```

Isso reduz acoplamento, facilita substituição de plataformas e preserva a identidade do Projeto.

## Responsabilidade do adaptador

O adaptador deve somente:

1. ler a fonte autorizada;
2. identificar a origem;
3. preservar o identificador externo;
4. capturar contexto disponível;
5. converter para o envelope padrão;
6. enviar ao barramento de coleta;
7. registrar falhas de transmissão quando aplicável.

O adaptador **não decide sozinho** o significado final do conhecimento.

## Envelope

```json
{
  "source_type": "CHATGPT",
  "source_id": "id-externo",
  "occurred_at": "2026-09-17T12:00:00+00:00",
  "content": "conteúdo original",
  "title": "contexto opcional",
  "actor": "agente-ou-humano",
  "conversation_id": "conversa",
  "session_id": "sessão",
  "event_type": "descoberta",
  "metadata": {},
  "raw": {}
}
```

O Cérebro calcula/valida a idempotência e preserva a proveniência.

## Como uma nova plataforma entra

```text
NOVA PLATAFORMA
      |
      v
ADAPTADOR
      |
      v
ENVELOPE PADRÃO
      |
      v
BARRAMENTO DE COLETA
      |
      v
CÉREBRO
```

Não é necessário alterar o restante da arquitetura para cada nova IA.

## Mecanismos de transporte

Um adaptador pode usar:

- webhook;
- HTTP/API;
- `repository_dispatch` do GitHub;
- MCP;
- fila/event bus;
- arquivo/exportação;
- mecanismo nativo da plataforma;
- outro transporte futuro.

O transporte pode mudar sem mudar o modelo de memória.

## Plataformas sem API adequada

Quando uma plataforma não oferece uma forma autorizada de leitura/integração, o Projeto não deve simular acesso nem violar controles da plataforma.

Usar, nessa ordem, quando disponíveis:

1. API oficial;
2. webhook oficial;
3. exportação oficial;
4. conector autorizado;
5. MCP/integração intermediária autorizada;
6. entrada manual temporária.

## Organização posterior

A coleta é deliberadamente separada da organização profunda:

```text
ADAPTADOR
  ↓
CAPTURA BRUTA
  ↓
IDEMPOTÊNCIA
  ↓
MEMÓRIA INICIAL
  ↓
AGENTE ORGANIZADOR
  ↓
RELAÇÕES
  ↓
ENTENDIMENTO
  ↓
APRENDIZADO
  ↓
SABEDORIA
```

Assim, diferentes IAs podem participar da organização sem alterar a fonte original.

## Futuro

O barramento deve poder receber fontes ainda inexistentes hoje. Portanto, `source_type` é extensível e a arquitetura não depende de uma lista fechada de fornecedores.
