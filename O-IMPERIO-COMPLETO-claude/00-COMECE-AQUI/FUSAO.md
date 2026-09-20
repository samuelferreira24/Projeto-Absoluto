# REGISTRO DA FUSÃO

Duas conversas do projeto O IMPÉRIO, reunidas em 10 de setembro de 2026.

| Fonte | Período | Assunto |
|---|---|---|
| **Correção de bugs** | 04–08 set | app, Ponte, coleta mundial, planta do sistema |
| **Cliente e migração** | 25 ago–10 set | Pinheiro, planilha, interface, saída da plataforma |

---

## COMO OS CONFLITOS FORAM RESOLVIDOS

**23 arquivos existiam nos dois pacotes.** 13 eram idênticos. Os outros 10
exigiram decisão.

### O caso crítico: `index.html`

As duas conversas alteraram o aplicativo em **04 de setembro**. Meu pacote tinha
325 KB; o outro, 463 KB.

**Não aceitei o maior por ser maior.** Verifiquei função por função se o trabalho
da frente "cliente" sobreviveu na versão da frente "bugs":

| Verificação | Resultado |
|---|---|
| 18 funções da reforma de interface | **todas presentes** |
| menu lateral, temas, logo, streaming | presentes |
| tela de projeto, folha de ações, markdown | presentes |
| Ponte, coleta 33 fontes, varredura, oficina | **só na versão "bugs"** |

**Conclusão:** a versão "bugs" é a versão "cliente" mais o trabalho dela. Vence
sem perda.

### `coletor.py` — 20 KB contra 38 KB

Mesma verificação. Nenhuma função do meu pacote sumiu, e o outro acrescenta
GDELT, OpenAlex e 23 fontes a mais.

**Vence a versão "bugs".**

### Os ícones

Meu pacote tinha 690 bytes e 2,2 KB — eram marcadores. O outro tem 23 KB e 61 KB,
imagens reais.

**Vence a versão "bugs".**

### Os três documentos de organização

`DECISOES-REJEITADAS`, `LINHA-DO-TEMPO` e `LEIA-PRIMEIRO` existiam nos dois, com
conteúdo diferente e **ambos válidos** — cada conversa registrou o que viveu.

**Não escolhi um.** Foram mesclados em duas partes, com a origem marcada. Os
originais estão em `05-historico/originais/`, intactos.

---

## O QUE CADA CONVERSA TROUXE DE ÚNICO

### Da frente "correção de bugs"
- A Ponte — Termux virou serviço comandado pelo app
- Coleta mundial: 33 fontes em 13 domínios, com GDELT e OpenAlex
- Memória em quatro camadas
- Varredura que executa em vez de contar
- A Oficina — app lê e conserta o próprio código
- `PLANTA-DO-SISTEMA.md` — MAPE-K e OODA, a Fábrica, os Espaços

### Da frente "cliente e migração"
- Todo o trabalho com a Pinheiro Negócios
- `FECHAMENTO_V3.xlsx` e o questionário de 40 perguntas
- `O-IMPERIO.md` — o documento unificado do projeto
- A reforma da interface
- A auditoria do ecossistema e o caminho de saída da plataforma

---

## O QUE AINDA PRECISA DE ATENÇÃO

⚠ **Dois documentos de planejamento coexistem.** `PLANTA-DO-SISTEMA.md` (frente
bugs) e `O-IMPERIO.md` (frente cliente) tratam do mesmo assunto com escopos
diferentes — a Planta é do Sistema, o e-book é do Império inteiro.

O e-book já incorporou a maior parte da Planta, mas **não tudo**. A Planta tem
detalhe de arquitetura que o e-book resume. Os dois ficam, e a conciliação é
trabalho para depois.

⚠ **O e-book não menciona a Ponte, a coleta de 33 fontes nem a Oficina** na
versão que tinha, porque foram produzidas na outra conversa. Precisa ser
atualizado com isso.

⚠ **A migração tem dois caminhos documentados.** `INSTALAR-NO-TERMUX.md` é o
caminho antigo. `PARA-OPENHANDS-CLOUD.md` é a decisão atual. O primeiro fica
como referência do que existe hoje no aparelho.
