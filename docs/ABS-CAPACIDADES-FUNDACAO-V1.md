# ABS — Fundação de Capacidades V1

## Estado

Esta etapa executa a decisão atual do Projeto Absoluto de tratar **capacidades como requisito primário** e a interface como camada de acesso.

A V1 não deve começar por um design de interface. Primeiro deve existir uma base capaz de:

1. receber uma intenção;
2. representar um trabalho persistente;
3. selecionar/usar uma capacidade;
4. executar;
5. acompanhar estado e eventos;
6. registrar resultado e proveniência;
7. permitir continuação, interrupção e substituição;
8. devolver controle ao Imperador.

## Ordem de construção

```
Imperador
  ↓
Comando / intenção
  ↓
Núcleo de trabalho
  ↓
Orquestração
  ↓
Adaptadores de capacidades
  ↓
Execução
  ↓
Eventos / estado
  ↓
Memória / proveniência
  ↓
Controle / aprovação
  ↓
Interface
```

## Primeira capacidade externa prioritária

**Codex** é a primeira integração de referência para validar a arquitetura de capacidades.

A documentação oficial atual da OpenAI descreve:

- **Codex SDK**: integração programática para iniciar, continuar e retomar threads e automatizar trabalhos.
- **Codex App Server**: integração profunda de produto, com autenticação, histórico, aprovações e eventos em streaming; usa JSON-RPC e suporta threads, retomada, fork, interrupção e execução de comandos.

O App Server é atualmente descrito como experimental/não suportado para cargas de produção. Portanto, deve ser tratado como **adaptador de capacidade experimental**, não como identidade ou fundamento permanente do ABS.

## Abstração obrigatória

O ABS não deve depender diretamente de APIs específicas de uma única IA.

Criar uma fronteira conceitual:

```
Capability
├── identidade
├── tipo
├── capacidades oferecidas
├── modo de conexão
├── autenticação
├── permissões
├── entrada
├── execução
├── eventos
├── saída
├── interrupção
├── recuperação
└── proveniência
```

Codex, Claude, Gemini ou qualquer outra capacidade devem poder implementar essa fronteira por adaptadores diferentes.

## Trabalho persistente

O objeto central de continuidade deve ser o **trabalho**, não a conversa de uma IA.

Modelo inicial:

```
WORK
├── id
├── objetivo
├── contexto
├── estado
├── capacidade atual
├── histórico de capacidades
├── entradas
├── eventos
├── artefatos
├── testes
├── resultados
├── problemas
├── decisões
├── proveniência
└── próximo passo
```

Uma capacidade pode executar um trabalho e depois ser substituída por outra sem apagar o estado do trabalho.

## Regra de substituição

```
WORK
 ↓
Codex A
 ↓
estado persistido
 ↓
Codex B / outra capacidade
 ↓
continuação
```

A implementação deve provar essa possibilidade antes de assumir que ela funciona.

## Interface

A interface entra depois da fundação de capacidades.

Ela deve consumir o mesmo modelo de trabalho e capacidade usado pelo núcleo.

Isso permite futuramente:

- texto;
- voz;
- toque;
- web;
- Android;
- 3D;
- AR/MR/XR;
- outras interfaces.

Nenhuma dessas formas deve alterar a identidade do trabalho ou da capacidade.

## O que construir agora

### P0 — Fundação

- modelo de trabalho;
- registro de capacidades;
- adaptador de capacidade;
- ciclo de execução;
- estado/eventos;
- proveniência;
- controle básico;
- teste de continuidade.

### P1 — Primeiro adaptador

Implementar um adaptador real para Codex usando a integração oficialmente suportada que melhor corresponda ao primeiro caso de uso.

Antes de fixar App Server ou SDK como base, testar ambos conceitualmente e escolher conforme a necessidade real.

### P2 — Segunda capacidade

Adicionar uma segunda capacidade independente para provar que o núcleo não foi acoplado ao Codex.

### P3 — Interface

Somente após P0/P1/P2 funcionarem, construir a primeira interface de acesso.

## Critério de sucesso da etapa

A etapa estará validada quando for possível demonstrar:

> O Imperador cria um trabalho → ABS seleciona uma capacidade → a capacidade executa → o ABS registra estado/eventos/resultado → o trabalho pode ser retomado → outra capacidade pode assumir quando suportado → o Imperador permanece no controle.

## Não decidir agora

Não decidir prematuramente:

- arquitetura definitiva do ABS;
- IA definitiva;
- modelo definitivo;
- Android como identidade;
- interface definitiva;
- 3D como interface principal;
- arquitetura de produção do App Server;
- infraestrutura definitiva.

## Próxima ação técnica

Construir primeiro um **vertical slice mínimo de capacidade**, não uma interface completa:

```
comando
→ work
→ capability registry
→ adapter
→ execução
→ evento
→ resultado
→ persistência
→ retomada
```

Depois testar com uma segunda capacidade.

## Princípio

> **Não construir a porta antes de construir o mecanismo que a porta precisa abrir.**

A interface continuará sendo importante, mas nesta etapa ela é consequência das capacidades que o ABS realmente possuir.
