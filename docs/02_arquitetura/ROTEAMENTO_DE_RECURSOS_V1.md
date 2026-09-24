# Roteamento de Recursos — V1

O ABS agora possui um contrato separado para **seleção de caminhos de recurso**.

Fluxo conceitual:

```
missão
↓
objetivo + capacidades necessárias + restrições
↓
ResourceRouter
↓
conexões candidatas
↓
classificação
↓
rota primária + alternativas
↓
adaptador de execução
```

## Princípios

- Um recurso pode possuir vários caminhos de conexão.
- Seleção não significa autenticação.
- Seleção não significa execução.
- Registrado não significa operacional.
- Uma conexão planejada não pode ser tratada como disponível.
- O caminho escolhido pode ser substituído sem alterar o objetivo da missão.
- Alternativas permanecem disponíveis para futura política de fallback.

Exemplo:

```
GitHub
├── github-api
├── github-termux
├── connector futuro
└── browser futuro
```

O mesmo modelo pode ser aplicado a:

- IA por API;
- IA local;
- CLI/Termux;
- navegador;
- APIs externas;
- dispositivos remotos;
- redes locais;
- novos transportes ainda desconhecidos.

## Próxima integração

A próxima camada é conectar:

```
Work
↓
capability
↓
ResourceRouter
↓
connection
↓
adapter
↓
resultado
```

Essa integração deve preservar autorização do Imperador, observabilidade, persistência, fallback e continuidade.
