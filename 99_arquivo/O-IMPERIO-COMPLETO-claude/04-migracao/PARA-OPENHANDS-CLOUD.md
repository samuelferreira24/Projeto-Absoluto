# MIGRAÇÃO — para o OpenHands Cloud

Passo a passo verificado contra a documentação oficial em setembro de 2026.

⚑ **Decisão tomada:** OpenHands Cloud, não VM própria. A conta Oracle deu
problema — e a loteria de capacidade do free tier não vale o tempo.

**O que isso elimina:** criar VM, instalar Docker, configurar portas, montar
túnel SSH. Os quatro primeiros passos da versão anterior desaparecem.

**O que isso adia:** o LiteLLM. Ele precisa rodar em algum lugar, e sem servidor
próprio fica para quando o PC chegar. A versão para VM está preservada na
segunda metade deste documento — quando houver máquina, ela volta a valer.

**Regra de ouro:** FAÇA → confira o RESULTADO ESPERADO → só então avance.
Se aparecer erro que você não entende, pare e pergunte. Não improvise.

---

## ANTES: por que VM e não o celular

| | Seu celular | O que o OpenHands pede |
|---|---|---|
| RAM | 3 GB | **4 GB mínimo**, e isso sem contar o modelo |
| Node.js | não tem | 22.12 ou superior |
| Docker | não roda bem | necessário para isolamento |

A VM resolve os três. E o celular continua sendo seu ponto de acesso — só o
trabalho pesado muda de lugar.

```
   celular (navegador)  ──►  VM (onde tudo roda)
   você comanda               agente, Docker, LiteLLM
```

---

## PASSO 1 — Criar a conta

**Fazer:** conta no OpenHands Cloud.

⚑ Novos usuários recebem **US$ 20 em crédito**. Isso cobre o teste inteiro sem
tirar dinheiro do bolso.

**Resultado esperado:** a interface abre no navegador do celular. Sem instalar
nada, sem terminal.

---

## PASSO 2 — Escolher como pagar o motor

Duas formas, e você pode começar por qualquer uma.

| Forma | Como funciona | Quando usar |
|---|---|---|
| **Crédito da OpenHands** | modelos a preço de custo, sem margem | para começar — o crédito grátis já cobre |
| **Chave própria (BYOK)** | você traz a chave, paga o fornecedor direto | quando quiser escolher o modelo |

**Fazer, para começar:** usar o crédito grátis. Não configure chave ainda.

**Fazer, quando o crédito acabar:** criar conta no OpenRouter, pôr US$ 10, e
cadastrar a chave em Settings.

⚑ **Por que OpenRouter e não uma chave direta:** com ele, trocar de modelo é
mudar um nome. Sem ele, trocar de fornecedor é trocar de chave e de endereço.

⚠ **O que eu confirmei e você precisa saber:** assinatura de consumidor —
Claude Pro, ChatGPT Plus — **não** conecta em cliente de terceiro. Os
fornecedores não permitem. Para usar sua conta é chave de API, cobrada
separado da assinatura.

**Resultado esperado:** você sabe de onde vem o dinheiro que paga cada tarefa.

---

## PASSO 3 — Proteger a chave

⚑ **Nunca** coloque chave em arquivo do projeto, em prompt, ou em documento.
Ela vai junto quando você versionar, e fica lá para sempre no histórico.

**Onde ela mora:** no campo de configuração da plataforma, que guarda cifrado.

**Resultado esperado:** `git log` do seu projeto não contém nenhuma chave.

---

## PASSO 4 — Definir o teto de gasto

Sem teto, um laço que não fecha consome crédito até acabar.

| Defesa | Onde |
|---|---|
| Crédito pré-pago | não recarregue automático — é a defesa que sempre funciona |
| Limite mensal | OpenRouter e Anthropic deixam definir na conta |
| Olhar o painel | consumo aparece em tempo real |

⚑ **A defesa que funciona é o crédito pré-pago.** Sem cartão recarregando
sozinho, o gasto para quando o crédito acaba — não importa o que qualquer
configuração diga.

**Resultado esperado:** você sabe quanto pode gastar no máximo neste mês.

---

## PASSO 5 — Levar a memória

### Fazer

```bash
mkdir -p ~/projects/imperio && cd ~/projects/imperio
git init
mkdir 10_PESQUISAS
```

Enviar o e-book do celular para a VM:

```bash
# no Termux, com o arquivo em Downloads
scp ~/storage/downloads/O-IMPERIO.md ubuntu@SEU_IP:~/projects/imperio/00_VISAO.md
```

Criar os arquivos restantes:

```bash
cd ~/projects/imperio
for f in 01_REQUISITOS 02_ARQUITETURA 03_DECISOES 04_ROADMAP \
         05_RISCOS 06_AUDITORIA 07_MELHORIAS 08_ESTADO_ATUAL 09_PROMPTS; do
  touch "$f.md"
done
git add -A && git commit -m "memória inicial do projeto"
```

**Resultado esperado:** o projeto tem memória própria, versionada, que não
depende de nenhuma conversa.

⚑ **Também levar:** as travas do `executor.py` (testadas) e os arquivos de memória
calibrada. O resto do código antigo fica onde está, como consulta.

---

## PASSO 6 — A primeira conversa: não construir

### Fazer

Abrir o Canvas, criar conversa no projeto, e deixar claro que a primeira missão é
**diagnóstico, pesquisa e planejamento** — não código.

O prompt inicial:

> Você é o primeiro agente do projeto Império. Leia o `00_VISAO.md` e todos os
> arquivos de contexto.
>
> **Não implemente código nesta etapa.**
>
> Sua missão: explicar o objetivo que entendeu; listar o que já está decidido;
> identificar lacunas e dependências; separar FATOS, HIPÓTESES e RECOMENDAÇÕES;
> registrar decisões e riscos nos arquivos apropriados; propor um plano em
> etapas; indicar o que precisa de aprovação humana.
>
> Regras: nunca ponha segredo em código ou documento. Mantenha tudo reversível e
> versionado. Se algo não puder ser confirmado, marque como pendência — não
> invente.
>
> Responda em: A) ENTENDIMENTO · B) DECIDIDO · C) PENDENTE · D) RISCOS ·
> E) PRÓXIMOS 10 PASSOS

**Resultado esperado:** um diagnóstico que você lê e corrige. Não avance só
porque a resposta parece convincente.

⚠ **Se ele começar a programar:** pare, diga que o portão não foi aprovado, e
mande voltar ao diagnóstico.

---

## CHECKLIST

Marque só o que estiver realmente feito.

- [ ] Conta criada, crédito grátis confirmado
- [ ] Forma de pagamento decidida — crédito ou chave própria
- [ ] **Nenhuma chave dentro de arquivo do projeto**
- [ ] Teto de gasto definido, e sem recarga automática
- [ ] Projeto criado com memória versionada
- [ ] E-book como `00_VISAO.md`
- [ ] Primeira conversa foi diagnóstico, sem código
- [ ] Diagnóstico lido e corrigido por você

---

## O QUE PODE DAR ERRADO

| Problema | Causa provável | O que fazer |
|---|---|---|
| Crédito acabou rápido | tarefa em laço | ver o painel de consumo; o teto de voltas está no Livro VI |
| Modelo não responde | chave inválida | conferir em Settings, não no projeto |
| Resposta ruim | modelo fraco para a tarefa | trocar de modelo custa uma linha |
| Limite de conversas | tier gratuito é limitado | é restrição do plano, não erro |

---

## CUSTO REAL

| Item | Mensal |
|---|---|
| OpenHands Cloud, tier gratuito | R$ 0 |
| Crédito inicial | **R$ 0** — US$ 20 de bônus |
| Recarga, quando acabar | a partir de US$ 10 (~R$ 55) |
| **Primeiro mês** | **R$ 0** |

Contra R$ 100 da assinatura atual, com limite de mensagem.
---

# ANEXO — o caminho com VM própria

⚠ **Isto não é o caminho atual.** Está preservado porque, quando o PC chegar,
volta a valer — e porque é o único jeito de rodar o LiteLLM, que resolve a
dependência de fornecedor único.

**Quando usar:** quando houver máquina própria, ou quando a conta Oracle for
aprovada.

## VM-1 — Criar a VM

### Onde

| Opção | Custo | Prós | Contras |
|---|---|---|---|
| **Oracle Always Free** | R$ 0 | 2 núcleos, 12 GB, permanente | aprovação difícil, ARM, capacidade some |
| **Hetzner CX22** | ~R$ 22/mês | confiável, x86, simples | custa |

⚠ **O que mudou em junho de 2026:** o Oracle cortou o tier ARM de 4 núcleos/24 GB
para **2 núcleos/12 GB**. Continua muito acima dos 3 GB do celular, mas não é mais
o que os tutoriais antigos prometem.

⚠ **O risco real do Oracle:** há relatos de contas aprovadas sendo encerradas sem
aviso. Para aprender e testar, serve. Para produção com cliente pagando, não
confie só nele.

### Fazer — Oracle

1. Criar conta em `cloud.oracle.com`
2. Escolher região com Ampere A1 — **a região não muda depois**
3. Compute → Instances → Create Instance
4. Imagem: **Ubuntu 24.04 (aarch64)** — o `aarch64` é obrigatório para ARM
5. Shape: `VM.Standard.A1.Flex` — 2 OCPU, 12 GB
6. Disco: 50 GB (o limite grátis é 200)
7. Adicionar sua chave SSH
8. Anotar o IP público

**Resultado esperado:** instância criada, com IP público anotado.

⚠ **Se der "Out of capacity":** é o erro mais comum do Oracle. Tente outra
zona de disponibilidade, ou tente de novo mais tarde. Não é erro seu.

---

## VM-2 — Preparar a VM

### Fazer

Do celular, pelo Termux:

```bash
ssh ubuntu@SEU_IP_PUBLICO
```

Depois de entrar:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential curl git
```

O `build-essential` é necessário porque em ARM algumas dependências precisam ser
compiladas.

### Instalar o Docker

```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

Saia e entre de novo no SSH para o grupo valer.

**Resultado esperado:**

```bash
docker run hello-world
```

Deve imprimir uma mensagem de boas-vindas sem pedir `sudo`.

---

## VM-3 — Subir o OpenHands

### Fazer

```bash
export PROJECTS_PATH="$HOME/projects"
mkdir -p "$PROJECTS_PATH" "$HOME/.openhands"

docker run -d --restart unless-stopped \
  --name openhands \
  -p 127.0.0.1:8000:8000 \
  -v "$HOME/.openhands:/home/openhands/.openhands" \
  -v "${PROJECTS_PATH}:/projects" \
  ghcr.io/openhands/agent-canvas:latest
```

⚑ **Repare no `127.0.0.1:8000:8000`** — e não `-p 8000:8000`. Isso prende o
serviço à própria máquina. Sem isso, qualquer pessoa na internet acha sua
instalação e usa seus créditos.

A documentação é explícita: trate agentes como não confiáveis, e revise antes de
expor a uma rede que você não controla.

**Resultado esperado:**

```bash
docker ps
curl -I http://127.0.0.1:8000
```

O container aparece rodando e o `curl` responde.

---

## VM-4 — Acessar do celular, com segurança

O serviço está preso à VM. Falta uma ponte segura entre ele e seu celular.

### A forma simples: túnel SSH

No Termux:

```bash
ssh -L 8000:127.0.0.1:8000 ubuntu@SEU_IP_PUBLICO
```

Deixe essa janela aberta. No navegador do celular:

```
http://localhost:8000
```

**Resultado esperado:** a tela do Agent Canvas abre no seu celular.

### A forma melhor: rede privada

Instalar Tailscale nos dois — VM e celular. Eles passam a se enxergar por uma
rede privada, sem porta aberta na internet e sem manter janela de SSH.

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

**Resultado esperado:** o celular acessa a VM pelo nome, de qualquer lugar, sem
túnel manual.

⚠ **Nunca** troque o `127.0.0.1:8000:8000` por `8000:8000` para "facilitar o
acesso". É o erro que expõe tudo.

---

## VM-5 — LiteLLM na frente

Sem isso, você troca a dependência de uma plataforma pela dependência de um
agregador.

### Fazer

```bash
mkdir -p ~/litellm && cd ~/litellm
```

Criar `config.yaml`:

```yaml
model_list:
  - model_name: trabalho          # o nome que você usa
    litellm_params:
      model: openrouter/deepseek/deepseek-chat
      api_key: os.environ/OPENROUTER_API_KEY
  - model_name: trabalho          # mesmo nome = rota alternativa
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY
  - model_name: dificil
    litellm_params:
      model: openrouter/anthropic/claude-sonnet-5
      api_key: os.environ/OPENROUTER_API_KEY

router_settings:
  routing_strategy: simple-shuffle
  num_retries: 3
  timeout: 120
  cooldown_time: 60      # o disjuntor: rota que falha sai por 60s
  allowed_fails: 3
```

Subir:

```bash
docker run -d --restart unless-stopped \
  --name litellm \
  -p 127.0.0.1:4000:4000 \
  -v ~/litellm/config.yaml:/app/config.yaml \
  -e OPENROUTER_API_KEY="sua-chave" \
  -e GROQ_API_KEY="sua-chave" \
  -e LITELLM_MASTER_KEY="sk-invente-uma-senha-longa-aqui" \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

⚑ **A `LITELLM_MASTER_KEY` não é opcional.** É ela que autentica quem pode usar o
proxy. Sem ela, qualquer processo que alcance a porta 4000 gasta seus créditos.
No OpenHands, você usa essa mesma chave no campo de chave de API.

**Resultado esperado:**

```bash
curl http://127.0.0.1:4000/health
```

Responde. E no OpenHands você aponta para `http://127.0.0.1:4000` como endereço
compatível com OpenAI.

⚑ **O que você ganhou:** dois nomes de modelo — `trabalho` e `dificil`. Trocar de
fornecedor é editar o `config.yaml`. O `cooldown_time` é o disjuntor que faltava.

### ⚠ A armadilha do limite de gasto — leia antes de confiar

A documentação do LiteLLM avisa: **`max_budget` não é um teto de gasto** nesse
tipo de instalação. Somar o gasto exige um banco de dados conectado; sem ele, o
total nunca é calculado e a checagem **nunca dispara**.

Um proxy configurado com `max_budget: 100` continua atendendo depois dos US$ 100,
sem erro e sem alerta. O único aviso é uma linha no registro, na hora que sobe.

**O que fazer, já que o teto não funciona sozinho:**

| Defesa | Como |
|---|---|
| Teto no fornecedor | OpenRouter e Anthropic deixam definir limite mensal na conta |
| Crédito pré-pago | só ponha US$ 10; sem cartão automático, o gasto para sozinho |
| Olhar o painel | o consumo aparece no painel do fornecedor |

⚑ **A defesa que funciona é o crédito pré-pago.** Se não há cartão para recarregar
sozinho, o gasto para quando o crédito acaba — não importa o que o proxy pense.

---

