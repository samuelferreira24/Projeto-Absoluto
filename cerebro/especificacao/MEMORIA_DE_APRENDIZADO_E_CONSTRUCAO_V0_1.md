# Memória de Aprendizado e Construção V0.1

## Princípio

Todo aprendizado relevante produzido durante a construção do Projeto Absoluto deve poder ser preservado como memória do projeto.

Isso inclui não apenas conhecimento final, mas também:

- descobertas;
- entendimentos;
- mudanças de entendimento;
- correções;
- erros e suas causas;
- decisões e motivos;
- progresso de construção;
- eventos de construção;
- resultados de experimentos;
- relações entre descobertas e decisões;
- evidências que sustentam o aprendizado.

## Regra de não perda

A construção não deve consumir aprendizado sem registrá-lo. Um resultado pode ser substituído; o aprendizado que levou à substituição permanece preservado, salvo remoção deliberada pelo responsável pelo projeto.

## Separação entre evidência e interpretação

A evidência original permanece intacta. O aprendizado é uma camada derivada, com origem, evidências, contexto, confiança e relações explicitadas.

## Mudança de entendimento

Quando um entendimento posterior contradizer ou substituir outro, o anterior não deve ser apagado. O novo registro deve apontar para o anterior por `supersede`, permitindo reconstruir a evolução do pensamento.

## Idempotência

O registro utiliza identidade determinística para evitar duplicação quando o mesmo aprendizado for processado mais de uma vez.

## Ciclo

```text
EXPERIÊNCIA / PESQUISA / CONSTRUÇÃO
              ↓
           RESULTADO
              ↓
         APRENDIZADO
              ↓
           REGISTRO
              ↓
            CÉREBRO
              ↓
      RECUPERAÇÃO / APLICAÇÃO
              ↓
        NOVA EXPERIÊNCIA
              ↺
```

## Consequência arquitetural

O sistema deve aprender enquanto é construído. A memória do processo de construção é parte da capacidade do próprio sistema, e não apenas documentação externa.
