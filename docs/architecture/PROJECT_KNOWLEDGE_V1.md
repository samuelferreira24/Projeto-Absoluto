# PROJECT KNOWLEDGE V1

## Objetivo

Criar uma camada persistente de conhecimento do Projeto Absoluto que permita continuidade entre chats, IAs, ferramentas e futuras interfaces.

## Arquitetura

Projeto Absoluto
  |
  +-- autoridade humana
  |     +-- visão
  |     +-- princípios
  |     +-- decisões
  |
  +-- observação automática
        +-- Git/GitHub
        +-- código
        +-- testes/CI
        +-- runtime
        +-- recursos/nós
        +-- ferramentas
                |
                v
        conhecimento estruturado
                |
          +-----+-----+
          v     v     v
        estado paths evidências
          |     |     |
          +-----+-----+
                |
                v
            projeções
          +-- mapas
          +-- handoffs
          +-- orientação de IA

## Princípio de prova

Nenhuma capacidade é marcada como operacional apenas porque existe código. O estado deve ser sustentado por testes ou evidência operacional apropriada.

## Automação

A sincronização inicial deriva fatos da árvore do repositório e gera uma fonte JSON e um mapa Markdown.

O workflow de Project Knowledge atualiza automaticamente essas projeções após mudanças em main. Isso elimina a necessidade de uma auditoria manual para refletir cada mudança factual básica do repositório.

## Limites

A automação não altera visão, princípios ou decisões do Imperador.

A presença de arquivo ou classe é evidência de existência estrutural, não prova de funcionamento.

## Próximas integrações

1. Git/GitHub e PRs como eventos estruturados.
2. runtime ABS como fonte de recursos, capacidades e nós.
3. testes/CI como evidência de funcionamento.
4. avaliador automático de caminhos.
5. projeções adicionais dos mapas existentes.
6. pacote de orientação compacto para nova IA.
7. integração com o ciclo de atualização local do ABS.
