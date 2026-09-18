# Procedimento — Registro de Entendimentos de IAs no Cérebro

**Versão:** V2  
**Finalidade:** preservar, identificar, organizar e permitir comparação entre entendimentos produzidos por diferentes IAs, contas e chats sobre o Projeto Absoluto.

## 1. Princípio

Cada contribuição de uma IA deve ser tratada como uma fonte independente, rastreável e revisável.

O Cérebro deve preservar não apenas a síntese final, mas também:
- a origem;
- o contexto;
- o caminho que levou ao entendimento, quando relevante;
- as distinções entre declaração, interpretação, inferência, evidência, hipótese e decisão;
- a evolução do entendimento.

Este procedimento não transforma o entendimento de uma IA em regra do Projeto. A contribuição é uma fonte secundária para raciocínio, pesquisa, comparação e descoberta.

## 2. Identificação da origem — antes da reconstrução

Antes de analisar o conteúdo, a IA deve montar uma **ficha de origem** da contribuição.

Deve tentar identificar, conforme realmente estiver disponível:
- plataforma/ambiente;
- conta;
- identificador da conta;
- chat/conversa;
- título do chat;
- identificador do chat;
- período/data da conversa;
- identificadores técnicos adicionais;
- escopo efetivamente analisado;
- data de produção do registro;
- identificador único da contribuição.

### 2.1 Regra contra identificadores inventados

**Nunca inventar, adivinhar ou inferir como fato um ID técnico.**

Se um identificador exato não estiver acessível, registrar:

`não_disponível`

e continuar usando os demais elementos verificáveis.

### 2.2 Rastreabilidade mesmo sem IDs técnicos

A ausência de um ID técnico não deve tornar a contribuição irreconhecível.

Quando IDs externos não estiverem disponíveis, a ficha deve preservar os identificadores contextuais que existirem, como:
- plataforma;
- conta identificável pelo ambiente;
- título da conversa;
- período;
- data de produção;
- escopo;
- identificador único interno da contribuição.

O **ID único da contribuição deve ser criado pelo próprio procedimento quando ainda não existir**, sem fingir que ele é um ID da conta ou do chat.

Esse ID identifica o **registro da contribuição**, não a conta nem o chat.

Quando possível, o índice deve manter separadamente:
- identificação técnica real;
- identificação contextual;
- identificação interna da contribuição.

Assim, `não_disponível` em um campo não impede a rastreabilidade do conjunto.

## 3. Identidade da contribuição

Cada registro deve possuir uma identidade própria e estável.

Formato recomendado:

`CIA-AAAA-MM-###`

ou outro formato equivalente adotado pelo Cérebro.

O identificador deve ser único dentro do acervo de contribuições.

Se já existir um mecanismo oficial de IDs no Cérebro, utilizá-lo em vez de criar outro mecanismo concorrente.

## 4. Reconstrução do caminho

A IA deve reconstruir o entendimento a partir da conversa e dos materiais que realmente consegue acessar.

Não deve procurar apenas ocorrências literais de palavras como "ABS" ou "AGI". Deve recuperar também conceitos relacionados e a evolução semântica da conversa.

Preservar, quando relevantes:
- estado inicial do entendimento;
- perguntas e objetivos;
- descobertas;
- interpretações iniciais;
- hipóteses;
- erros;
- correções feitas pelo usuário;
- correções feitas pela própria IA;
- mudanças de entendimento;
- pesquisas realizadas;
- evidências encontradas;
- conclusões;
- relações descobertas;
- caminhos abandonados;
- questões ainda abertas;
- entendimento atual.

Um erro histórico não deve ser apagado apenas porque uma conclusão posterior o corrigiu.

## 5. Separação epistemológica

Cada afirmação relevante deve ser distinguida, quando possível, como:
- declaração do usuário;
- entendimento da IA;
- inferência da IA;
- pesquisa externa;
- evidência;
- hipótese;
- decisão;
- questão aberta;
- erro;
- correção;
- descoberta;
- resultado.

A IA não deve transformar inferência em fato, hipótese em decisão ou sugestão em requisito.

## 6. Projeto Absoluto

A reconstrução deve considerar o contexto necessário para entender como aquela conta chegou ao seu entendimento do Projeto Absoluto, incluindo, quando realmente presentes na conversa:
- Imperador;
- Sistema;
- Império;
- Sistema Pessoal do Imperador;
- Cérebro;
- múltiplos cérebros;
- IA e múltiplas IAs;
- agentes;
- capacidades;
- composição;
- orquestração;
- Matriz de Jetro;
- delegação;
- hierarquia;
- autoridade;
- memória;
- conhecimento;
- continuidade;
- governança;
- evolução;
- segurança;
- recursos;
- substituição e resiliência;
- relação ABS × AGI.

Não preencher lacunas com suposições apenas porque determinado conceito aparece no procedimento. Registrar somente o que a conversa realmente sustenta.

## 7. AGI e conceitos relacionados

Quando AGI aparecer, reconstruir exatamente o papel discutido.

Não assumir automaticamente que:
- AGI = Projeto Absoluto;
- AGI = Sistema;
- AGI = Cérebro;
- AGI = Meta-Cérebro;
- AGI = agente;
- AGI = motor;
- AGI = coordenador.

Se uma dessas relações tiver sido discutida como hipótese, registrá-la como hipótese.

Se a relação não tiver sido discutida, registrar que ela permanece aberta.

## 8. Descoberta do Cérebro antes do registro

A IA que estiver executando o procedimento não deve presumir que já conhece a arquitetura do Cérebro.

Antes de gravar:
1. localizar o repositório acessível;
2. identificar branch;
3. examinar a estrutura relevante;
4. descobrir como o conhecimento é armazenado;
5. localizar mecanismos de proveniência, histórico, relações e estados;
6. localizar o procedimento vigente para contribuições de IAs;
7. localizar a área reservada para essas contribuições;
8. verificar como o índice deve ser mantido.

O registro deve se adaptar ao mecanismo existente do Cérebro, sem criar uma estrutura paralela desnecessária.

## 9. Área de armazenamento

A área destinada às contribuições de IAs é:

`cerebro/data/conhecimento/contribuicoes_ias/`

Cada contribuição deve permanecer separada das demais.

O índice da área deve permitir localizar, quando disponível:
- ID da contribuição;
- plataforma;
- conta;
- ID da conta;
- chat;
- ID do chat;
- título;
- período;
- data do registro;
- escopo;
- estado;
- relações relevantes;
- caminho do arquivo.

Campos não disponíveis devem permanecer explicitamente marcados, sem fabricação de dados.

## 10. Proveniência

A origem deve permanecer vinculada à contribuição mesmo quando o conteúdo for:
- relacionado a outro conhecimento;
- corrigido;
- ampliado;
- consolidado;
- incorporado a uma camada de conhecimento;
- superado.

Se uma contribuição for incorporada à camada de conhecimento, a proveniência deve apontar para o registro original.

## 11. Status e natureza

Uma contribuição de IA é, por padrão:

- **secundária**;
- **não normativa**;
- **aberta à revisão**;
- **não limitadora da arquitetura**.

Ela pode ser contestada, corrigida, ampliada, relacionada ou superada sem apagar sua existência histórica.

## 12. Comparação entre múltiplas IAs

O acervo deve permitir reunir várias contribuições **sem misturar suas origens**.

Posteriormente, o Cérebro deve poder investigar:
- quais IAs/contas contribuíram;
- de quais chats vieram;
- quais conceitos cada contribuição identificou;
- onde houve convergência;
- onde houve divergência;
- quais ideias surgiram independentemente;
- quais hipóteses apareceram em mais de uma contribuição;
- quais pontos possuem evidência;
- quais permanecem abertos;
- como os entendimentos evoluíram.

Convergência entre IAs não transforma automaticamente uma ideia em verdade, decisão ou regra.

## 13. Integridade histórica

Nunca substituir uma contribuição anterior simplesmente para "organizar".

Correções devem ser rastreáveis por atualização, novo registro ou relação de supersessão, conforme os mecanismos existentes no Cérebro.

O histórico deve continuar permitindo reconstruir a evolução do entendimento.

## 14. Validação antes de gravar

Antes de registrar, verificar:

- a origem foi investigada;
- nenhum ID foi inventado;
- campos indisponíveis estão explicitamente marcados;
- existe um ID único da contribuição;
- o escopo está claro;
- a contribuição não foi misturada com outra conta/chat;
- fatos, hipóteses, inferências e decisões foram distinguidos;
- erros e correções relevantes foram preservados;
- o entendimento atual não foi apresentado como especificação normativa;
- a proveniência está vinculada ao registro;
- o arquivo e o índice permitem localizar a contribuição.

## 15. Resultado esperado

O Cérebro passa a funcionar também como um **acervo comparável de entendimentos de IAs**, no qual cada contribuição possui identidade própria e origem rastreável.

Mesmo quando a plataforma não fornece IDs técnicos, o conjunto de informações contextuais e o ID interno da contribuição deve permitir distinguir uma contribuição de outra.

O objetivo não é criar um sistema rígido de rastreamento, mas preservar contexto suficiente para que múltiplas perspectivas possam ser reunidas, comparadas e posteriormente avaliadas sem perda de origem.

## 16. Evolução do procedimento

Este procedimento é aberto à evolução.

Se novas evidências ou necessidades do Cérebro demonstrarem solução melhor, ele pode ser corrigido, ampliado ou substituído, preservando-se o histórico da versão anterior.
