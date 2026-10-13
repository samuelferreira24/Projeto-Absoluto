# Comando operacional — Passagem 1 em lotes contínuos

**Projeto:** O Lendário Mecânico  
**Branch obrigatória:** `pesquisa/lendario-mecanico-base`  
**Estado:** protocolo operacional de execução assistida; não é um binário nem uma workflow de GitHub Actions autónoma.

## Comando de trabalho

Usar esta diretiva ao retomar a pesquisa:

```text
EXECUTAR_PASSAGEM_1_CONTINUA
  --obra="The Legendary Mechanic"
  --edicao="WebNovel, tradução inglesa"
  --inicio=33
  --fim=42
  --lote=10
  --qc-interno=5
  --persistencia=github
  --branch="pesquisa/lendario-mecanico-base"
  --handoff=obrigatorio
  --sem-merge=true
  --sem-avancar-se-fonte-incompleta=true
```

Os números de início/fim são parâmetros de exemplo para a próxima execução a partir do estado registado. O comando é uma **diretiva operacional padronizada para o assistente**, não um comando de terminal executável.

## Procedimento obrigatório

1. Ler o handoff, o método canónico, o mapa de cobertura e a síntese do último lote. Verificar o estado atual da branch antes de criar conteúdo.
2. Confirmar o URL e o título de cada capítulo através da navegação da edição de trabalho; não adivinhar URLs nem saltar capítulos.
3. Ler sequencialmente cada corpo narrativo acessível. Para cada capítulo, criar nota individual com acontecimentos, causalidade, objetivos, personagens/conhecimento, regras ficcionais, ligações, incertezas e limites de acesso.
4. Distinguir texto narrativo de comentários, recomendações, navegação e módulos auxiliares da página. Só marcar truncamento quando houver evidência de interrupção do corpo narrativo ou quando o seu limite não puder ser verificado.
5. Trabalhar em **um lote operacional de até 10 capítulos**, mas dividi-lo em dois sublotes de até cinco. Depois de cada sublote, verificar cobertura, cronologia, nomes, contagem de personagens/eventos, causalidade e consistência com os capítulos anteriores.
6. Quando a continuação revelar erro ou omissão anterior, atualizar a nota antiga retrospetivamente e registar a razão da correção; não esconder discrepâncias da tradução.
7. No fim do lote de até 10, criar síntese narrativa integrada, auditoria cruzada, atualizar mapa de cobertura e handoff com o próximo capítulo exato.
8. Só continuar para o lote seguinte se os capítulos do lote atual tiverem corpo visível verificado, notas individuais, QC documentado e persistência confirmada no GitHub.
9. Se uma página não abrir, houver paywall, limite de acesso, capítulo ausente ou texto incompleto, registar o bloqueio e continuar apenas até ao limite seguro; nunca inventar conteúdo nem declarar leitura integral sem evidência.
10. Não executar Passagem 2, não fundir o PR e não alterar a branch principal como parte desta diretiva.

## O que é automatizado e o que não é

- **Pode ser padronizado/automatizado:** navegação sequencial a partir de links confirmados, estrutura dos registos, validações de cobertura, verificação de ficheiros existentes, criação/atualização de documentos, mapa e handoff.
- **Continua a exigir leitura e julgamento do modelo:** interpretação narrativa, distinção entre facto e hipótese, detecção de contradições e síntese. Um runner não transforma, por si só, uma página da Webnovel numa leitura semanticamente validada; isso exige uma implementação explícita de aquisição permitida, análise e QC.
- **Não usar scraping para contornar paywall, autenticação ou mecanismos de proteção.** Em caso de falha, marcar o capítulo como bloqueado e preservar a rastreabilidade.

## Critério de sucesso

Um lote só está concluído quando:
- todos os capítulos previstos têm estado explícito (lido, parcial, bloqueado ou pendente);
- cada capítulo efetivamente lido tem nota individual;
- os dois sublotes foram verificados quanto a consistência;
- discrepâncias e questões abertas foram preservadas;
- a síntese, o mapa e o handoff foram atualizados;
- os commits/ficheiros foram confirmados no GitHub.

## Estado de arranque registado

O handoff da pesquisa indica capítulo 32 como último capítulo com nota individual criada. Antes da execução, verificar novamente a branch e a nota; o próximo capítulo esperado é o 33. Não presumir que capítulos 33–42 já foram lidos.
