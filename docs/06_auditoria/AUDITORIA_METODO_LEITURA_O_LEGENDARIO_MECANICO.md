# Auditoria do método e da qualidade de leitura — O Lendário Mecânico

**Data:** 2026-10-11  
**Projeto-pai:** Projeto Absoluto  
**Branch:** `pesquisa/lendario-mecanico-base`  
**Escopo:** auditoria metodológica após a primeira consulta sequencial dos capítulos 1–10.  
**Estado:** avaliação preliminar; não é certificação independente da leitura integral dos capítulos.

## 1. Veredito executivo

O método de passagens sucessivas é conceitualmente sólido: primeiro compreender a narrativa, depois extrair capacidades, avaliar evidências, decompor sistemas, projetar, testar e sintetizar. A separação reduz o risco de julgar prematuramente uma tecnologia ou de ler a obra apenas à procura de artefatos úteis.

A execução inicial, porém, ainda não provou profundidade suficiente. Os capítulos 1–10 foram consultados analiticamente em sequência, mas a integralidade de cada página não foi verificada linha a linha. A síntese preserva o arco principal e algumas conexões causais, mas é predominantemente cumulativa; não contém ainda um registro granular e verificável de cada capítulo, cena decisiva, mudança de objetivo, informação conhecida por cada personagem e evidência para cada conexão.

**Conclusão:** manter as passagens sucessivas; corrigir o protocolo de leitura e a validação de qualidade antes de avançar para novos capítulos. O lote de dez capítulos serviu como piloto de fluxo, não como prova de que dez é o tamanho ideal nem de que a leitura foi completa.

## 2. O que está funcionando

- Ordem de leitura narrativa preservada, sem começar pela extração técnica.
- Edição e URLs identificadas.
- Estados de cobertura honestos; consulta substancial não é rotulada como leitura integral.
- Síntese de cronologia, personagens, facções, regras ficcionais e questões abertas.
- Conexões causais iniciais registadas sem transformar hipóteses em factos.
- Handoff e memória persistente no repositório.

## 3. Lacunas e riscos identificados

1. **Granularidade insuficiente:** uma síntese de dez capítulos pode apagar cenas intermediárias, transições, diálogos decisivos, alterações de motivação e consequências imediatas.
2. **Rastreabilidade fraca em algumas conexões:** uma conexão precisa apontar para capítulos e acontecimentos concretos que sustentem cada elo, não apenas para o lote como um todo.
3. **Estado mental e informação dos personagens:** é necessário distinguir o que o personagem sabe, suspeita, deseja, oculta e interpreta incorretamente, sem confundir conhecimento do protagonista com verdade objetiva do mundo.
4. **Ponto de vista e confiabilidade:** previsão, interface, memória de jogador, fala de personagem e narração não são automaticamente evidência equivalente.
5. **Controle de omissões ausente:** ainda não há uma segunda verificação sistemática que compare a nota de cada capítulo com o texto realmente consultado.
6. **Tamanho fixo prematuro:** dez capítulos pode funcionar para alguns trechos e falhar em capítulos longos, densos ou com viradas importantes.
7. **Risco de falsa confiança:** abrir uma página ou consultar conteúdo substancial não prova que o capítulo inteiro foi lido.
8. **Resumo cumulativo sobrecarregado:** contexto acumulado é necessário, mas deve coexistir com notas individuais para que detalhes não desapareçam na compressão.

## 4. Revisão do tamanho dos lotes

O lote inicial de dez capítulos é aceitável como piloto operacional. Não há evidência suficiente para o declarar ideal.

**Novo procedimento adaptativo recomendado:**
- Usar lotes de **3 a 5 capítulos** durante a calibração de qualidade.
- Reduzir para 1–3 capítulos quando houver revelação importante, mudança de arco, capítulo excepcionalmente longo/denso, várias cenas simultâneas ou dificuldade de acesso.
- Só aumentar o lote depois de dois lotes consecutivos passarem pelo controle de qualidade sem perda de rastreabilidade ou detalhe relevante.
- O tamanho do lote nunca altera o critério de leitura: cada capítulo recebe seu próprio estado e registo.
- Reavaliar o tamanho com base em extensão, densidade narrativa, tempo de consulta, taxa de correções e omissões encontradas.

Esta é uma decisão operacional provisória, a validar empiricamente — não uma regra universal sobre a obra.

## 5. Ficha mínima obrigatória por capítulo

Cada capítulo consultado deve ter uma nota própria, ainda que breve, com:

1. Identificador, título, edição, URL e estado de acesso.
2. Acontecimentos em ordem narrativa, sem reduzir o capítulo a uma única frase.
3. Objetivo imediato do protagonista e alterações desse objetivo.
4. Ações, motivações, decisões e consequências dos personagens relevantes.
5. Informações novas sobre o mundo, organizações, regras ou capacidades.
6. Causa → decisão/ação → consequência, com referência ao capítulo.
7. Prenúncios, ambiguidades, contradições aparentes e perguntas abertas.
8. O que o leitor sabe, o que cada personagem sabe e o que ainda não se pode concluir.
9. Ligações com capítulos anteriores e hipóteses para verificar depois.
10. Cobertura real e limitações: texto completo consultado, parcial, indisponível ou ainda por verificar.

A nota deve ser uma paráfrase analítica original, sem copiar passagens extensas. Não se exige que todo capítulo tenha todos os campos preenchidos com conteúdo novo; exige-se que campos relevantes sejam considerados e que ausência de evidência seja explícita.

## 6. Estados de cobertura padronizados

- **Listado:** só se confirmou que o capítulo existe na lista.
- **Página aberta:** página acessada, sem confirmação suficiente de conteúdo narrativo.
- **Consulta parcial:** apenas parte do conteúdo foi consultada.
- **Consulta analítica substancial:** conteúdo narrativo relevante foi consultado, mas não há confirmação de integralidade.
- **Leitura completa verificada:** todo o texto acessível do capítulo foi percorrido e a nota foi comparada com o texto.
- **Revisado:** capítulo previamente registado foi relido para resolver omissões, dúvidas ou contexto posterior.

Não promover um estado com base apenas em título, resumo secundário, lembrança ou existência de uma nota.

## 7. Controle de qualidade ao fim de cada lote

Antes de avançar, verificar:

- [ ] Todos os capítulos do lote têm estados individuais honestos.
- [ ] A nota de cada capítulo separa acontecimentos observados de inferências.
- [ ] Motivações, objetivos e consequências não foram fundidos ou inventados.
- [ ] Conexões importantes têm referências de capítulo e classificação: explícita, inferência fundamentada ou hipótese aberta.
- [ ] Contradições aparentes e perguntas abertas foram mantidas, não resolvidas por suposição.
- [ ] O resumo cumulativo concorda com as notas individuais.
- [ ] Pelo menos uma verificação de omissões foi feita em relação ao texto acessível.
- [ ] Mapa de cobertura, fontes e handoff foram atualizados e relidos no GitHub.

Se uma verificação falhar, corrigir o lote antes de aumentar a cobertura.

## 8. Plano de recuperação para os capítulos 1–10

Não declarar os capítulos 1–10 integralmente lidos. Antes de prosseguir para o capítulo 11:

1. Reabrir as páginas dos capítulos 1–10 e verificar o acesso efetivo ao texto, sem contornar bloqueios.
2. Construir notas individuais por capítulo usando a ficha mínima.
3. Comparar as notas existentes com o conteúdo acessível; corrigir, complementar ou marcar as lacunas.
4. Reexaminar as conexões já propostas e indicar a evidência exata, confiança e estado.
5. Manter a síntese cumulativa como visão geral, sem substituir as notas por capítulo.
6. Atualizar o mapa de cobertura para refletir o estado real após a revisão.
7. Só então continuar do capítulo 11, em lotes adaptativos de 3–5 capítulos.

Se algum capítulo não puder ser consultado integralmente de forma autorizada, manter o estado parcial/substancial e seguir sem alegar cobertura completa.

## 9. Avaliação honesta da qualidade atual

**Demonstrado:** boa estrutura documental inicial, síntese do arco principal, continuidade e distinção explícita entre consulta substancial e leitura integral verificada.

**Ainda não demonstrado:** leitura integral dos dez capítulos; cobertura de todas as cenas e transições relevantes; interpretação profunda de cada personagem; deteção sistemática de omissões; completude do mapa de prenúncios e conexões.

Portanto, a avaliação atual é **promissora, mas não validada**. A qualidade deve ser medida pela rastreabilidade ao texto, capacidade de recuperar detalhes, correção após revisão e preservação de incerteza — não pela quantidade de capítulos processados nem pelo tamanho do resumo.

## 10. Relação com as passagens posteriores

Esta auditoria melhora a Passagem 1 e não autoriza antecipar a análise técnico-científica. Durante a leitura narrativa, tecnologias podem ser sinalizadas, mas não devem monopolizar a atenção. As Passagens 2–7 permanecem separadas e dependem de fontes e validações próprias. Nenhuma alteração de código, runtime ou arquitetura do ABS é implicada por esta revisão metodológica.

## 11. Próxima ação

A tarefa ativa passa a ser **auditar e completar as notas dos capítulos 1–10**, e não iniciar imediatamente o capítulo 11. Depois de verificar os documentos e as páginas, atualizar este registo e o handoff com o ponto real de retomada.


## 12. Proposta de decomposição interna da Passagem 1

**Estado desta seção:** decomposição agora formalizada no método canônico, versão 1.0, por orientação do usuário em 2026-10-11. Esta auditoria preserva a razão e o histórico da decisão.

A Passagem 1 é a base interpretativa das passagens posteriores. Recomenda-se organizá-la em quatro subfases complementares, evitando tanto a leitura superficial quanto quatro projetos redundantes:

### 1A — Leitura narrativa sequencial
Ler a edição de trabalho em ordem e criar notas individuais por capítulo. Priorizar cenas, acontecimentos, objetivos, decisões, consequências, informação nova, ponto de vista e dúvidas. Sinalizar elementos potencialmente relevantes sem iniciar ainda a extração técnica sistemática.

**Saída:** notas de capítulo com estado de acesso honesto e referência à fonte.

### 1B — Integração narrativa contínua
Após cada lote, integrar as notas à cronologia e aos mapas de personagens, relações, facções, conflitos, regras do universo e questões abertas. Nos finais de arcos, fazer uma revisão de arco mais ampla. Rastrear prenúncios e consequências através de capítulos, distinguindo facto explícito, inferência fundamentada e hipótese.

**Saída:** visão cumulativa conectada, sem substituir as notas individuais.

### 1C — Auditoria progressiva de compreensão
Verificar cada lote contra o texto acessível antes de avançar. Fazer revisões maiores nos finais de arcos e corrigir omissões ou interpretações frágeis. Não é necessário repetir uma auditoria total a cada lote; a verificação deve ser proporcional ao risco e à densidade. Manter lacunas explícitas quando a página ou o texto não puder ser consultado integralmente por meios autorizados.

**Saída:** cobertura e interpretações verificadas na medida documentada, com incerteza preservada.

### 1D — Síntese global após a cobertura narrativa
Quando os capítulos acessíveis da edição tiverem sido percorridos, consolidar a cronologia, os arcos, as transformações dos personagens, as facções, as regras do universo, os principais prenúncios/resoluções e as questões sem resposta. Revisitar interpretações antigas à luz de revelações posteriores. Não afirmar cobertura total onde houver lacunas.

**Saída:** síntese integrada da obra e relatório explícito de cobertura/limitações, preparando a Passagem 2.

## 13. Cadência recomendada

- Calibrar com lotes adaptativos de 3–5 capítulos; reduzir o lote quando houver densidade, mudança de arco ou dificuldade de acesso.
- Depois de cada lote: notas individuais, integração narrativa, verificação proporcional e atualização do repositório.
- Nos finais de arco: auditoria de continuidade mais ampla e revisão das hipóteses abertas.
- Aumentar o tamanho dos lotes apenas após dois lotes consecutivos passarem pelo controle de qualidade.
- Não transformar cada subfase numa releitura integral redundante. O processo é cumulativo; as revisões retornam ao texto quando houver risco, omissão, contradição ou contexto novo.
- O tamanho de lote é um parâmetro de execução, não uma meta de produtividade. A qualidade da cobertura tem prioridade sobre o número de capítulos processados.

## 14. Aplicação imediata

Antes de avançar, concluir a auditoria de consistência das notas 1–3 e da síntese cumulativa; depois continuar pelo capítulo 4. Os capítulos 4–10 precisam de reabertura e notas individuais antes de liberar o capítulo 11.

## 15. Estado de execução após formalização

Em 2026-10-11, as subfases 1A–1D e a cadência adaptativa foram incorporadas ao método canônico. As páginas oficiais dos capítulos 1–3 foram reabertas e as notas individuais atualizadas. A mensagem “Load failed, please RETRY” aparece depois do corpo narrativo e do link “next chapter”, na área auxiliar pós-capítulo; não interrompe o texto narrativo visível. Assim, os capítulos 1–3 passaram para o estado **leitura completa do corpo narrativo visível verificada**.

A auditoria dos capítulos 4–10 ainda está pendente. O capítulo 11 permanece bloqueado até que os capítulos 4–10 sejam reabertos, anotados e verificados.

## 16. Correção de diagnóstico: erro auxiliar da página

O diagnóstico inicial confundiu a falha de um módulo auxiliar da Webnovel com uma possível interrupção do corpo narrativo. A estrutura observada nas páginas 1–3 contradiz essa leitura: o corpo narrativo termina, depois surge o link para o capítulo seguinte e só então aparece “Load failed, please RETRY” junto de componentes auxiliares. A metodologia foi corrigida para exigir que se localize o erro na estrutura da página antes de rebaixar o estado de cobertura.

O protocolo agora está no método canônico, Passagem 0. O erro auxiliar não exige intervenção técnica na página da Webnovel; a correção necessária era metodológica e documental: classificar corretamente o componente que falhou, corrigir as notas e impedir que esse falso positivo bloqueie a leitura.
