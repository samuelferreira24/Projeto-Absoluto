# PLANO DE EVOLUÇÃO — ABS V1
## Curto, médio e longo prazo

> Documento de referência estratégica para a evolução do ABS. Define a trajetória de uso de peças próprias e de terceiros sem transformar nenhuma tecnologia atual em dependência estrutural.

## 1. Princípio central

O ABS deve começar operando o quanto antes, usando terceiros quando isso acelerar a construção, mas mantendo sob controle próprio:

- arquitetura;
- contratos/interfaces;
- decisões;
- autorização;
- roteamento;
- execução;
- verificação;
- memória/proveniência;
- capacidade de substituição.

**Regra:** terceiro pode fornecer capacidade; o ABS deve controlar como essa capacidade entra e pode ser substituída.

---

## 2. Curto prazo — colocar o ABS para operar

### Objetivo
Fazer o ciclo operacional principal funcionar de ponta a ponta, prioritariamente pelo celular.

### Arquitetura
```
IMPERADOR
  ↓
INTERFACE ABS
  ↓
API ABS
  ↓
ABS CORE ↔ CÉREBRO
  ↓
ORQUESTRADOR
  ↓
CAMADA DE CAPACIDADES
  ↓
PRÓPRIAS + TERCEIROS
  ↓
EXECUÇÃO
  ↓
VERIFICAÇÃO
  ↓
MEMÓRIA / PROVENIÊNCIA
  ↓
RESULTADO
```

### Prioridades
1. Consolidar o ABS Core como camada própria.
2. Consolidar contratos de Work, Capability, Authorization, Adapter e Result.
3. Fazer a camada de IA aceitar múltiplos motores sem espalhar dependência de fornecedor pelo código.
4. Usar OpenRouter e/ou APIs diretas como aceleradores iniciais.
5. Integrar Cérebro → decisão → missão → ABS → execução → resultado → memória.
6. Validar recuperação, erros, timeout, duplicação e interrupção.
7. Manter SQLite/localidade simples enquanto atende a V1.
8. Melhorar a interface para funcionar como sala de comando, não apenas como tela visual.
9. Operar pelo Android/Termux/browser sem exigir computador.
10. Adicionar terceiros somente quando resolverem uma necessidade real.

### Terceiros aceitáveis nesta fase
- provedores de IA;
- OpenRouter;
- n8n, se acelerar automações;
- serviços de banco/remoto, se necessários;
- VPS, quando o celular deixar de ser suficiente;
- Tailscale/Cloudflare Tunnel quando houver necessidade real de acesso entre nós.

### Não construir agora
- IA própria completa;
- banco próprio distribuído;
- plataforma própria de automação geral;
- VPN própria;
- infraestrutura física;
- substitutos próprios de serviços que ainda não são gargalo.

### Critério de saída
O Imperador consegue dar uma missão pelo celular e o ABS consegue:

**entender → planejar → autorizar → executar → verificar → registrar → responder → continuar.**

---

## 3. Médio prazo — consolidar e reduzir dependências críticas

### Objetivo
Transformar o protótipo operacional em um sistema mais robusto, modular e substituível.

### Prioridades
1. Fortalecer a camada de adaptadores.
2. Separar definitivamente ABS de fornecedores externos.
3. Criar fallback entre motores de IA.
4. Aumentar observabilidade, testes e recuperação.
5. Evoluir persistência conforme a necessidade real.
6. Introduzir VPS/nós remotos quando houver carga ou disponibilidade que justifique.
7. Usar n8n como braço de automação, nunca como cérebro/arquitetura central.
8. Criar mecanismos melhores de backup, continuidade e restauração.
9. Ampliar ferramentas próprias.
10. Melhorar a interface de comando e os múltiplos canais de acesso.
11. Medir custo, latência, disponibilidade e dependência de cada terceiro.
12. Definir, com dados de uso, quais componentes merecem substituição.

### Estratégia de substituição
Para cada terceiro, avaliar continuamente:

**utilidade atual → custo → dependência → controle → risco → dificuldade de substituição → benefício de possuir internamente.**

Só substituir quando houver ganho concreto ou necessidade estratégica.

### Critério de saída
O ABS consegue trocar um fornecedor importante sem reconstruir seu núcleo.

---

## 4. Longo prazo — independência progressiva e expansão

### Objetivo
Aumentar a capacidade própria do ABS e reduzir dependências estruturais à medida que recursos e maturidade permitirem.

### Possíveis evoluções
- motores de IA próprios ou locais;
- roteamento próprio de modelos;
- memória/banco de dados mais independente;
- infraestrutura própria;
- múltiplos nós de execução;
- redundância de serviços e caminhos;
- automação própria mais avançada;
- capacidades próprias de navegação, ferramentas e integração;
- maior autonomia operacional sob autorização do Imperador;
- novas interfaces e dispositivos;
- integração mais profunda com Android e outros ambientes;
- substituição gradual de terceiros que se tornarem limitantes.

### Regra de longo prazo
Não existe obrigação de substituir tudo.

Um componente externo pode permanecer indefinidamente se continuar sendo a escolha adequada. Independência significa **ter capacidade de substituir**, não necessariamente substituir.

### Critério de maturidade
O ABS deve ser capaz de ampliar suas capacidades sem ficar preso à forma, fornecedor ou tecnologia usados na V1.

---

## 5. Trajetória resumida

| Horizonte | Foco | Terceiros | ABS próprio |
|---|---|---|---|
| Curto | Operar | Acelerar | Controlar arquitetura |
| Médio | Consolidar | Reduzir dependências críticas | Substituir onde fizer sentido |
| Longo | Expandir | Usar quando conveniente | Aumentar independência e capacidade |

## 6. Princípio de decisão

**Curto prazo:** velocidade e funcionamento.

**Médio prazo:** robustez, modularidade e redução de dependências críticas.

**Longo prazo:** capacidade própria, redundância e liberdade tecnológica.

A decisão sobre construir ou usar uma peça deve ser tomada pelo impacto no objetivo do ABS, e não por preferência automática por tecnologia própria ou de terceiros.

---

## 7. Regra operacional permanente

Toda peça importante deve, quando tecnicamente possível, entrar no ABS por uma camada própria de contrato/adaptação:

`ABS → camada própria → terceiro`

e não:

`ABS → terceiro espalhado pela arquitetura`

Isso preserva a capacidade de evolução do sistema.

---

## 8. Relação com o celular

O celular é o ponto de comando do Imperador na V1.

Ele não precisa executar fisicamente tudo. Pode comandar capacidades locais e remotas por uma única interface.

Assim, a evolução pode seguir:

**celular → celular + serviços externos → celular + nós remotos → rede de capacidades próprias e externas sob controle do ABS.**

---

## Status

**Planejamento de referência — não é congelamento da arquitetura.**

Este documento orienta decisões de curto, médio e longo prazo e deve ser revisado quando o uso real do ABS fornecer novos dados.
