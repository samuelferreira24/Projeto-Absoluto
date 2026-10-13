# Auditoria de preparação da pesquisa — O Lendário Mecânico

**Data:** 2026-10-11  
**Escopo:** estrutura documental e critérios prévios à pesquisa sistemática  
**Estado:** preparação documental concluída como versão inicial; pesquisa factual abrangente ainda não iniciada  
**Branch:** pesquisa/lendario-mecanico-base  
**PR:** https://github.com/samuelferreira24/Projeto-Absoluto/pull/165

## 1. Objetivo da auditoria

Verificar se a frente de pesquisa tem estrutura suficiente para começar a coleta sistemática sem misturar contexto narrativo, extração ficcional, evidência científica, avaliação de viabilidade, experimentação e continuidade do Projeto Absoluto.

Esta auditoria verifica a presença e a função dos documentos. Não valida a veracidade integral das informações da novel, não confirma a leitura de capítulos e não representa revisão científica.

## 2. Artefatos preparados

| Artefato | Função | Estado |
|---|---|---|
| Plano mestre | Método, escopo, governança e fases | Presente; inclui portões de qualidade |
| Contexto da história e tecnologias | Introdução ao universo narrativo e conceitos iniciais | Presente; síntese inicial ainda precisa de validação capítulo a capítulo |
| Mapa de cobertura dos capítulos | Controle de edição, acesso, leitura e extração | Criado; ainda sem cobertura sistemática |
| Glossário e taxonomia | Normalização terminológica e classificação | Criado; sementes explicitamente provisórias |
| Catálogo mestre de tecnologias | Registro central de candidatos | Criado; contém apenas dois candidatos-piloto iniciais |
| Registro de fontes | Fontes textuais e técnicas iniciais, limites de acesso | Presente; algumas questões de edição permanecem abertas |
| Protocolo de evidências científicas | Busca, avaliação e registro de evidência | Criado; nenhuma revisão sistemática foi executada |
| Matriz de viabilidade e dependências | Requisitos, gargalos, alternativas e classificação | Criada; sem avaliação abrangente concluída |
| Protocolo de experimentos e validação | Critérios, registros e segurança | Criado; não registra experimento executado |
| Fila de oportunidades | Conversão da pesquisa em opções futuras | Criada; sem ranking final |
| Relatório-piloto | Teste exploratório do método em prótese e rover | Presente; não exaustivo |
| Índice de planejamento | Navegação entre artefatos | Atualizado |

## 3. Verificações realizadas

- Os sete novos documentos foram recuperados novamente do GitHub na branch de pesquisa e seus títulos/conteúdos estavam presentes.
- O índice e o plano mestre foram recuperados após atualização.
- O PR #165 foi verificado como aberto, em rascunho e não mergeado.
- O escopo continua documental: nenhum código, serviço ou runtime do ABS foi alterado por esta preparação.
- A discrepância de contagem entre catálogos permanece declarada como não resolvida.
- As entradas iniciais são identificadas como provisórias; não há alegação de cobertura integral, revisão sistemática ou experimento físico concluído.

## 4. Portões antes de ampliar a pesquisa

### Portão A — Corpus e edição
- [ ] Confirmar a URL canônica da edição chinesa e registrar o limite de acesso.
- [ ] Estabelecer a edição de trabalho e inventariar os capítulos listados.
- [ ] Investigar a diferença entre as contagens das edições sem inventar correspondências.

### Portão B — Contexto narrativo
- [ ] Começar a cobertura por capítulos efetivamente consultados.
- [ ] Mapear arcos, eventos e termos com referências específicas.
- [ ] Separar afirmações textuais, inferências e dúvidas.

### Portão C — Extração técnica
- [ ] Usar o esquema do catálogo e os IDs estáveis.
- [ ] Registrar requisitos, limitações, falhas e condições de funcionamento.
- [ ] Rever duplicações e divergências de tradução.

### Portão D — Evidência e viabilidade
- [ ] Pesquisar fontes reais para perguntas técnicas específicas.
- [ ] Registrar limitações e evidências contrárias.
- [ ] Mapear dependências, gargalos, alternativas e riscos.
- [ ] Justificar cada classificação de viabilidade e confiança.

### Portão E — Prototipagem
- [ ] Definir hipótese, métricas, critério de sucesso e critério de interrupção.
- [ ] Avaliar riscos, recursos e autorizações antes de executar.
- [ ] Só declarar resultados após preservar evidências do teste.

## 5. Riscos residuais

1. **Acesso ao corpus:** páginas podem limitar acesso; registrar o que foi efetivamente consultado e não contornar controles de acesso.
2. **Divergência entre edições:** títulos, divisão e contagens podem variar; a correspondência permanece uma questão aberta.
3. **Tradução:** termos podem mudar de sentido; não normalizar equivalências sem fonte.
4. **Viés de seleção:** começar por tecnologias interessantes pode ocultar métodos, infraestrutura e limitações menos chamativos.
5. **Excesso de confiança:** fontes promocionais, patentes, simulações e protótipos têm limites distintos.
6. **Confusão de estado:** planos e fichas vazias não são resultados, implementações nem capacidades validadas.
7. **Direitos autorais:** usar notas próprias e referências, sem reproduzir capítulos ou traduções extensas.

## 6. Conclusão

A estrutura documental inicial está preparada para começar a fase factual de modo rastreável. Isso não significa que a pesquisa científica ou a leitura sistemática da obra já tenha começado ou terminado. O próximo passo operacional é validar o corpus e iniciar o mapa de cobertura com capítulos realmente consultados. Manter todas as alterações nesta branch até revisão; não fazer merge automático para main e não modificar o ABS sem uma relação técnica demonstrada e uma decisão apropriada.
