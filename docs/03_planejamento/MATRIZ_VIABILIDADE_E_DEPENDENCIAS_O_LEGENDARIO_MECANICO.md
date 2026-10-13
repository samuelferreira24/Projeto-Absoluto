# Matriz de viabilidade, dependências e lacunas — O Lendário Mecânico

**Projeto-pai:** Projeto Absoluto  
**Estado:** método preparado; nenhuma avaliação abrangente concluída  
**Versão:** 0.1 — 2026-10-11

## Objetivo
Converter comparações entre ficção e realidade em requisitos, dependências e gargalos explícitos. O catálogo mestre contém fichas por candidato; esta matriz destaca dependências e decisões relevantes, sem duplicar o catálogo.

## Categorias de viabilidade
- **A — Disponível:** função relevante disponível, com evidência adequada ao escopo declarado.
- **B — Reproduzível/adaptável:** componentes e técnicas existentes permitem realizar a função útil com adaptações.
- **C — Exige desenvolvimento:** requer engenharia, integração ou validação adicional.
- **D — Pesquisa avançada:** persistem obstáculos técnicos ou científicos substanciais.
- **E — Sem caminho conhecido:** não foi identificado caminho demonstrado para a versão especificada.

Declarar versão, requisito funcional, escopo, data e confiança. Uma versão simplificada pode ter categoria diferente da versão ficcional completa. E não significa impossível para sempre.

## Dimensões separadas
Maturidade científica; componentes; integração; materiais e fabricação; energia e calor; sensores e controle; software/dados; infraestrutura; custo inicial e recorrente; manutenção e confiabilidade; segurança/ética/legislação; escalabilidade; dependência de fornecedores e recursos. Não esconder risco crítico em uma média ou pontuação agregada.

## Registro de gargalo
Cada GAP-0001 deve indicar: capacidade relacionada; requisito; estado real sustentado pelas evidências; diferença; tipo (ciência, engenharia, integração, custo, infraestrutura, segurança ou legal); dependências; evidências; alternativas; critério de saída; custo/recursos e origem da estimativa; confiança; próximo passo; estado (aberto, em estudo, mitigado, resolvido ou arquivado).

## Grafo de dependências
Usar relações explícitas: requer (indispensável); facilita (ajuda mas pode ser substituído); alternativa a (rota diferente); bloqueado por (gargalo); validado por (teste/evidência que sustenta parte específica). Não presumir necessidade técnica só porque duas tecnologias aparecem juntas na narrativa.

## Método
1. Definir a função mínima útil.
2. Separar versão mínima e versão ficcional completa.
3. Dividir em subsistemas.
4. Marcar componentes existentes, adaptáveis e ausentes.
5. Identificar gargalos dominantes e ciclos de dependência.
6. Buscar arquiteturas alternativas.
7. Definir o menor teste que reduza a incerteza principal.
8. Atualizar classificação com evidências.

## Estado inicial e critério de saída
Não há classificações finais nesta matriz. O relatório-piloto é exploratório e não deve ser convertido automaticamente em avaliação madura. Antes de priorizar, exigir função clara, fonte textual consultada, dependências mapeadas, evidências favoráveis e contrárias, gargalos e riscos explícitos, alternativa considerada e confiança declarada. Pronta para priorização não significa autorização para construir.