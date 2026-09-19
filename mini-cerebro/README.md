# Mini-Cérebro V1

Sistema histórico de recuperação e investigação do antigo Sistema Absoluto.

## Função
Preservar e investigar, sem modificar a fonte:
- arquivos e ZIPs;
- histórico Git;
- código e documentação;
- experimentos, falhas, decisões e descobertas;
- proveniência e evidências;
- memória bruta e memória derivada;
- relações entre ideia, decisão, implementação, experimento, resultado e correção.

## Princípios
1. A fonte original é somente leitura.
2. Nada é apagado para simplificar.
3. Fato, inferência, hipótese e interpretação permanecem separados.
4. Toda informação derivada aponta para uma fonte.
5. Conflitos são preservados até serem resolvidos.
6. O Mini-Cérebro não altera o repositório histórico.
7. O Mini-Cérebro não substitui o Cérebro ABS.
8. O motor/modelo de IA é substituível; a memória histórica é patrimônio.

## Operação
```
python -m mini_cerebro ingest --source /caminho/Sistema
python -m mini_cerebro ingest --source /caminho/sistema-absoluto.zip
python -m mini_cerebro search "memória interface"
python -m mini_cerebro evidence <id>
python -m mini_cerebro export
```

A implementação inicial usa somente biblioteca padrão Python e SQLite.
