# RECONSTRUÇÃO CAUSAL — EVIDÊNCIA DE COMMITS V2
## Sistema → Mini-Cérebro / Projeto Absoluto
## 2026-09-19

Esta camada adiciona evidência temporal e de diffs à reconstrução causal. Ela não substitui os registros anteriores.

## 1. EVIDÊNCIA E-004 — EXECUTOR + GOVERNANÇA

A comparação entre os commits `25bce60e` e `5788d863` mostra uma mudança concentrada:

- COMO-USAR.md: +69
- coletor.py: +26/-2
- executor.py: novo, +576
- governanca.py: novo, +676
- index.html: +673/-64
- motor.sh: +53/-3
- orquestrador.py: +32/-1

Isto é evidência forte de que executor e governança não eram pequenos ajustes isolados: foram introduzidos durante uma expansão importante do sistema.

### Leitura causal permitida
A coincidência temporal entre executor, governança, alterações do orquestrador, coleta e interface sustenta a interpretação de que o projeto estava tentando transformar a aplicação de uma casca de interação em um sistema com capacidade operacional e controle.

### O que NÃO pode ser concluído
O diff não prova que essa expansão foi a causa do abandono posterior nem que a arquitetura falhou por ser grande.

---

## 2. EVIDÊNCIA E-013 — PONTE / INTEGRAÇÃO

A comparação `37da0c8f → a6f22a49` mostra:

- coletor.py: +154/-12
- index.html: +364/-22
- ponte.py: +13

A ponte já existia antes desse intervalo e recebeu ajustes enquanto coleta e interface também evoluíam.

### Descoberta
A ponte não surgiu isoladamente: ela evoluiu junto com a necessidade de conectar capacidades de coleta, interface e operação.

### Hipótese a preservar
A ponte pode ter sido resposta ao crescimento do sistema e ao aumento da distância entre casca e núcleo.

Ainda não há evidência suficiente para afirmar que essa foi a única motivação.

---

## 3. EVIDÊNCIA E-010 — CONTINUIDADE

A comparação `a6f22a49 → b4daddfb` mostra a criação de:

`arranque.sh` — +55 linhas.

Isso confirma um passo explícito dedicado ao arranque/continuidade.

### Descoberta
Continuidade não era apenas uma propriedade implícita do app. Foi criada uma camada própria para inicialização.

### Relação ABS
Isso reforça a separação atual:
**existir no aparelho ≠ permanecer operacional no aparelho.**

---

## 4. EVIDÊNCIA E-014 — SHIZUKU/RISH

A comparação `ef1a4e21 → 025d5245` mostra:

- index.html: +103/-113
- rish: novo, +25
- rish_shizuku.dex: adicionado

Portanto, RISH/Shizuku entrou no histórico como uma camada técnica explícita, acompanhada de uma reorganização relevante da interface.

### Descoberta
O projeto estava explorando uma fronteira entre aplicação e acesso Android mais profundo.

### Limitação
O diff comprova a introdução do mecanismo, mas não comprova sozinho:
- nível de privilégio efetivamente obtido;
- estabilidade;
- quais operações foram realmente executadas;
- se o mecanismo resolveu o problema que motivou sua inclusão.

---

## 5. EVIDÊNCIA E-002 / E-015 — MOTOR E MEMÓRIA

No commit `5788d863`, a documentação `COMO-USAR.md` registra explicitamente:

- memória exportável;
- importação em outro aparelho;
- troca de fornecedor sem afetar a memória;
- motor como peça substituível;
- memória como patrimônio do usuário.

Também registra que a sincronização entre dispositivos seria uma etapa futura.

### Descoberta
A separação motor/memória não é uma interpretação posterior nossa; está documentada pelo próprio sistema histórico.

### Relação ABS
Convergência direta com o princípio atual de componentes substituíveis.

---

## 6. EVIDÊNCIA E-006 — ORQUESTRAÇÃO

Na mesma transição `25bce60e → 5788d863`:

- orquestrador.py recebeu +32/-1;
- governança foi criada;
- executor foi criado;
- interface recebeu grande expansão.

Isso indica que a orquestração foi desenvolvida dentro de um contexto maior de operacionalização.

### Descoberta
O histórico não mostra “orquestrador isolado”.
Mostra uma tentativa de formar uma cadeia:

```
motor
 ↓
orquestração
 ↓
execução
 ↓
governança
 ↓
interface
```

Mas isso ainda é uma reconstrução histórica, não arquitetura aprovada para o ABS.

---

## 7. EVIDÊNCIA E-009 — CRESCIMENTO DA INTERFACE

A comparação `5788d863 → 29f11596` mostra:

`index.html`: +912/-260 = 1172 mudanças.

Isso demonstra uma expansão muito grande da casca em uma única transição.

### Importante
Isso não permite concluir que “a interface era o problema”.

Permite afirmar apenas:

> A interface tornou-se uma parte de alta velocidade de mudança e grande volume de código durante a evolução do sistema.

Essa distinção deve ser preservada.

---

## 8. PADRÃO HISTÓRICO MAIS IMPORTANTE

Os commits fornecem evidência de uma dinâmica:

```
CAPACIDADE
   ↓
NOVA NECESSIDADE
   ↓
NOVA CAMADA
   ↓
MAIS CAPACIDADE
   ↓
NOVA COMPLEXIDADE
   ↓
NOVA CAMADA
```

Exemplos observados:

memória → motor → coleta → orquestração → execução → governança → ponte → continuidade → Android/RISH → interface expandida.

### Interpretação
O sistema não parece ter sido desenvolvido como uma arquitetura totalmente definida desde o início.

Ele foi descobrindo a arquitetura enquanto encontrava limitações.

Isso é compatível com o método atual do Projeto Absoluto de:

**mapear → pesquisar → descobrir → testar → adaptar → construir.**

Mas essa compatibilidade é uma interpretação, não uma afirmação histórica do repositório.

---

## 9. NOVA MATRIZ DE CAUSALIDADE

| Experimento | Evidência | Estado causal |
|---|---|---|
| Memória independente | documentação + estrutura | forte |
| Motor substituível | documentação | forte |
| Execução protegida | executor.py + governança | forte |
| Governança | governanca.py + diff | forte |
| Orquestração | orquestrador.py + evolução | forte |
| Ponte | ponte.py + evolução | forte |
| Continuidade | arranque.sh | forte |
| Shizuku/RISH | rish + dex | forte para introdução; fraca para resultado |
| Motor local | documentação | forte para hipótese; insuficiente para resultado |
| Busca/proveniência | base/coletor | forte |
| Interface como gargalo | grandes diffs | NÃO comprovado |
| Causa do abandono | histórico atual | NÃO comprovado |

---

## 10. PRINCIPAL CORREÇÃO DE INTERPRETAÇÃO

Não devemos contar a história assim:

```
APP
 ↓
ficou grande
 ↓
não funcionou
 ↓
abandonado
```

A evidência disponível é mais compatível com:

```
problemas encontrados
 ↓
novas capacidades
 ↓
novas camadas
 ↓
novas necessidades
 ↓
expansão do sistema
 ↓
experimentação de integração
 ↓
aumento de complexidade
 ↓
resultado final ainda a reconstruir
```

A causa do resultado final permanece em aberto.

---

## 11. PRÓXIMA LACUNA

Agora que os principais pontos temporais estão identificados, a próxima recuperação deve procurar evidência de RESULTADO, não apenas de IMPLEMENTAÇÃO:

- logs;
- mensagens/documentação de teste;
- arquivos de estado;
- relatórios;
- registros de erro;
- commits imediatamente posteriores às grandes implementações;
- alterações que claramente revertam ou limitem uma capacidade;
- versões compactadas;
- artefatos de build;
- scripts usados em produção/teste.

Objetivo:

**descobrir o que realmente funcionou.**

Não basta saber que uma capacidade foi criada.

Precisamos saber se ela:
1. foi executada;
2. funcionou;
3. falhou;
4. foi corrigida;
5. voltou a funcionar;
6. foi abandonada;
7. foi substituída.

## Estado

**RECUPERAÇÃO → EVIDÊNCIA TEMPORAL → RESULTADOS OPERACIONAIS**

A próxima etapa é reconstruir os resultados reais de cada grande experimento.
