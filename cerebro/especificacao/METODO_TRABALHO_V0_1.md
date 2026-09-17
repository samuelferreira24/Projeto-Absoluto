# Método de Trabalho V0.1 — Aprender com erros sem entrar em loops

## Objetivo

Definir como o Projeto Absoluto deve investigar, corrigir e evoluir problemas sem repetir indefinidamente a mesma estratégia nem criar componentes duplicados.

Este método transforma erros em informação sobre o próprio sistema e sobre a forma de trabalhar.

## 1. Princípio central

Um erro não é apenas um obstáculo. Ele também é uma evidência sobre a hipótese que estava sendo usada.

Quando uma solução falhar, não assumir automaticamente que é necessário tentar a mesma solução novamente. Perguntar:

- O que exatamente falhou?
- O erro aponta para qual hipótese incorreta?
- O problema pode estar em outra camada?
- Estou usando o lugar, módulo, interface ou mecanismo correto?
- Já existe algo no sistema que resolve parte ou todo o problema?
- O erro revela uma contradição entre o modelo mental e a estrutura real?

## 2. Mudar a perspectiva quando a evidência pedir

Depois de uma falha, considerar pelo menos estas perspectivas quando forem pertinentes:

1. **Código:** a implementação está errada?
2. **Estrutura:** estou trabalhando no arquivo/módulo/pacote correto?
3. **Integração:** componentes existentes estão sendo usados de forma incompatível?
4. **Contrato:** minha suposição sobre entrada, saída ou API está errada?
5. **Ambiente:** o problema depende do runner, dependência, versão ou configuração?
6. **Dados:** o teste ou dado usado realmente representa o problema?
7. **Arquitetura:** estou tentando resolver localmente algo que pertence a outra camada?
8. **Processo:** estou repetindo uma estratégia que já produziu evidência contra ela?

A mudança de perspectiva deve ser orientada pelo erro observado, não feita aleatoriamente.

## 3. Ciclo de investigação

```text
OBSERVAR
   ↓
REPRODUZIR
   ↓
FORMULAR HIPÓTESE
   ↓
TESTAR A HIPÓTESE
   ↓
OBTER EVIDÊNCIA
   ├── hipótese confirmada → corrigir
   └── hipótese refutada → mudar perspectiva
                         ↓
                    nova hipótese
   ↓
VALIDAR A CORREÇÃO
   ↓
REGISTRAR O APRENDIZADO
   ↓
CONTINUAR OU ENCERRAR
```

A reprodução confiável vem antes de uma correção sempre que for possível. Uma correção sem reprodução pode apenas mascarar o problema.

## 4. Regra de inspeção antes de criação

Antes de criar um arquivo, módulo, diretório, função ou mecanismo novo:

1. procurar o que já existe;
2. ler a interface existente;
3. identificar quem já usa aquele mecanismo;
4. verificar se a necessidade pode ser atendida por extensão ou correção;
5. somente criar algo novo se houver uma necessidade real não atendida.

Exemplo aprendido na base do Cérebro: já existia `cerebro/ingestao.py`. Criar `cerebro/ingestao/` sem verificar isso criou um conflito desnecessário. A solução correta foi voltar ao mecanismo existente e testá-lo.

## 5. Menor mudança capaz de testar a hipótese

Não alterar várias camadas simultaneamente quando uma mudança pequena pode fornecer a evidência necessária.

Preferir:

- um teste reproduzível;
- uma alteração pequena;
- uma execução real;
- uma leitura objetiva do resultado.

Isso reduz o espaço de busca quando algo falha.

## 6. O erro deve virar teste quando fizer sentido

Quando um bug for reproduzível e sua causa estiver suficientemente entendida, criar um teste que capture o comportamento esperado.

O teste deve permanecer como proteção contra regressão, desde que realmente agregue confiança.

## 7. Testes em camadas

Usar a menor camada capaz de detectar o problema:

```text
unidade → integração → sistema
```

Se um teste de nível superior encontrar um erro que poderia ser isolado em uma camada inferior, adicionar ou melhorar o teste inferior. Testes superiores continuam quando acrescentarem uma evidência diferente e relevante.

## 8. Critério de parada — evitar loops

Não continuar tentando indefinidamente.

Encerrar a linha de investigação quando ocorrer uma destas condições:

- a hipótese foi confirmada e a correção foi validada;
- a hipótese foi refutada e não há evidência nova que justifique repetir a mesma abordagem;
- a mesma estratégia falhou novamente sem mudança relevante de evidência;
- o problema depende de uma decisão ou recurso externo que o sistema não possui;
- o custo da investigação ultrapassou o valor esperado sem nova informação;
- existe informação suficiente para registrar o problema como questão aberta e avançar por outra frente.

Repetir uma tentativa só é justificável quando existe uma variável relevante nova.

## 9. Regra de mudança de estratégia

Se uma tentativa falhar, não fazer imediatamente uma segunda tentativa idêntica.

Antes da próxima tentativa, identificar pelo menos uma mudança:

- nova evidência;
- nova hipótese;
- nova perspectiva;
- menor escopo;
- mecanismo diferente;
- informação adicional sobre o ambiente.

Se nenhuma mudança puder ser apontada, a tentativa provavelmente é um loop.

## 10. Validação real

Sempre que houver mecanismo de execução disponível, validar no ambiente real apropriado.

Para o Projeto Absoluto, quando a alteração estiver no GitHub:

```text
alteração
   ↓
commit
   ↓
GitHub Actions
   ↓
execução real
   ↓
logs/resultado
   ↓
interpretação
```

Não considerar uma alteração validada apenas porque ela parece correta pela inspeção textual.

## 11. Aprendizado obrigatório

Uma correção importante deve produzir pelo menos um aprendizado reutilizável:

- o que aconteceu;
- por que a primeira hipótese estava errada ou incompleta;
- qual evidência resolveu o problema;
- qual regra deve evitar a repetição;
- qual teste ou mecanismo ficou responsável por detectar regressão.

O aprendizado pode alterar o planejamento e o próprio método de trabalho.

## 12. Histórico das tentativas

Não apagar uma tentativa importante apenas porque falhou.

Registrar, quando relevante:

```text
problema → hipótese → tentativa → resultado → interpretação → decisão
```

Isso evita repetir caminhos já descartados e transforma experiência em memória do sistema.

## 13. Aplicação ao Projeto Absoluto

Este método passa a orientar as próximas etapas do Cérebro e do Sistema.

Prioridades operacionais:

1. inspeção do estado real antes de criar;
2. reutilização antes de duplicação;
3. erro como evidência;
4. mudança de perspectiva quando necessário;
5. testes pequenos e reproduzíveis;
6. validação real;
7. registro de aprendizado;
8. critérios explícitos para parar.

O objetivo não é procurar soluções infinitamente. É maximizar aprendizado por ciclo e usar esse aprendizado para escolher melhor o próximo ciclo.
