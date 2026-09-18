from __future__ import annotations

from typing import Any


# Conhecimento inicial consolidado a partir da história do Projeto Absoluto,
# do aplicativo Sistema e da arquitetura atual do Cérebro.
# Isto é conhecimento de referência, não uma regra rígida.
CONHECIMENTOS_FUNDAMENTAIS: tuple[dict[str, Any], ...] = (
    {
        "id": "pa-001",
        "tipo": "principio",
        "titulo": "Ferramentas são peças, não o sistema",
        "conteudo": "ChatGPT, outros modelos, App, Cérebro, GitHub, Termux, APIs, computadores, celulares e servidores são peças substituíveis. O Projeto Absoluto não deve ficar preso a uma delas.",
        "origem": "historia_projeto",
        "status": "fundamental",
    },
    {
        "id": "pa-002",
        "tipo": "principio",
        "titulo": "Usar a ferramenta certa",
        "conteudo": "Eu não preciso saber tudo. Preciso saber usar a ferramenta certa.",
        "origem": "historia_projeto",
        "status": "fundamental",
    },
    {
        "id": "pa-003",
        "tipo": "aprendizado",
        "titulo": "O aplicativo existente funciona",
        "conteudo": "O Sistema já teve funcionamento real de conversa, motores de IA, memória, biblioteca, busca, Termux, APIs/modelos, módulos e outras capacidades. Falhas ou limitações específicas não devem ser transformadas em diagnóstico de que o aplicativo inteiro é quebrado.",
        "origem": "historico_app",
        "status": "verificado_historicamente",
    },
    {
        "id": "pa-004",
        "tipo": "aprendizado",
        "titulo": "Pesquisar o passado antes de inventar novamente",
        "conteudo": "Antes de criar uma capacidade nova, procurar no aplicativo, Cérebro, arquivos, commits e histórico. Uma ideia aparentemente nova pode já existir parcialmente.",
        "origem": "historico_app",
        "status": "fundamental",
    },
    {
        "id": "pa-005",
        "tipo": "arquitetura",
        "titulo": "O Cérebro deve permanecer aberto",
        "conteudo": "A arquitetura atual pode operar com um Cérebro, mas não deve ser desenhada de forma que impeça futuros múltiplos Cérebro, nós, ambientes ou provedores.",
        "origem": "arquitetura_cerebro",
        "status": "direcao",
    },
    {
        "id": "pa-006",
        "tipo": "arquitetura",
        "titulo": "Capacidades abstratas",
        "conteudo": "O Cérebro deve solicitar capacidades como inferencia, armazenamento, camera, computacao ou comunicacao, sem depender diretamente de um fornecedor ou tecnologia específica.",
        "origem": "arquitetura_cerebro",
        "status": "direcao",
    },
    {
        "id": "pa-007",
        "tipo": "arquitetura",
        "titulo": "Internet não é requisito universal",
        "conteudo": "A comunicação entre nós deve poder utilizar diferentes meios conforme o contexto. Internet é uma opção de transporte, não o fundamento obrigatório da rede.",
        "origem": "pesquisa_comunicacao",
        "status": "direcao",
    },
    {
        "id": "pa-008",
        "tipo": "arquitetura",
        "titulo": "Múltiplos meios de comunicação",
        "conteudo": "Bluetooth, BLE, Bluetooth Mesh, Wi-Fi, Wi-Fi Direct, Wi-Fi Aware, NFC, USB, Ethernet, celular, rádio e outros meios podem ser tratados como transportes possíveis.",
        "origem": "pesquisa_comunicacao",
        "status": "conhecimento_tecnico",
    },
    {
        "id": "pa-009",
        "tipo": "arquitetura",
        "titulo": "Um nó pode ser ponte",
        "conteudo": "Um dispositivo pode alcançar outro dispositivo por meio de um nó intermediário. A arquitetura deve permitir relay, múltiplos saltos e caminhos alternativos quando tecnicamente viável.",
        "origem": "pesquisa_comunicacao",
        "status": "direcao",
    },
    {
        "id": "pa-010",
        "tipo": "arquitetura",
        "titulo": "Comunicação adaptativa",
        "conteudo": "A escolha do transporte deve considerar disponibilidade, alcance, latência, largura de banda, energia, custo, segurança e necessidade de infraestrutura.",
        "origem": "pesquisa_comunicacao",
        "status": "direcao",
    },
    {
        "id": "pa-011",
        "tipo": "arquitetura",
        "titulo": "Offline e sincronização posterior",
        "conteudo": "Um nó não precisa estar permanentemente conectado. Tarefas, dados e resultados podem ser mantidos localmente e sincronizados quando outro caminho estiver disponível.",
        "origem": "arquitetura_rede",
        "status": "direcao",
    },
    {
        "id": "pa-012",
        "tipo": "historico",
        "titulo": "A ideia de malha já existia no App",
        "conteudo": "O aplicativo Sistema possui estado e interface relacionados à Malha e uma estrutura de matriz de posições, especialistas, alternativas e recursos. Portanto, a investigação atual de rede distribuída recupera uma linha histórica existente.",
        "origem": "Sistema/index.html",
        "status": "verificado_no_codigo",
    },
    {
        "id": "pa-013",
        "tipo": "historico",
        "titulo": "O App já tinha sincronização de aparelhos como objetivo",
        "conteudo": "O código do aplicativo contém explicitamente o objetivo de sincronizar dois aparelhos por nuvem cifrada.",
        "origem": "Sistema/index.html",
        "status": "verificado_no_codigo",
    },
    {
        "id": "pa-014",
        "tipo": "historico",
        "titulo": "O App já possuía uma camada de nuvem",
        "conteudo": "O aplicativo possui subida e download de estado por Gist privado com criptografia, além de cópia local e exportação.",
        "origem": "Sistema/index.html",
        "status": "verificado_no_codigo",
    },
    {
        "id": "pa-015",
        "tipo": "aprendizado",
        "titulo": "Nuvem pessoal não precisa significar servidor único",
        "conteudo": "Uma evolução possível é distribuir memória, armazenamento, computação e outras capacidades entre aparelhos, mantendo o Cérebro como camada de coordenação.",
        "origem": "sintese_projeto",
        "status": "hipotese",
    },
    {
        "id": "pa-016",
        "tipo": "arquitetura",
        "titulo": "Termux é uma ponte, não uma obrigação",
        "conteudo": "Termux pode fornecer capacidades locais no Android, mas a comunicação direta App-Cérebro pode existir sem Termux. As duas portas podem coexistir.",
        "origem": "arquitetura_cerebro_app",
        "status": "direcao",
    },
    {
        "id": "pa-017",
        "tipo": "aprendizado",
        "titulo": "Não declarar funcionamento sem teste",
        "conteudo": "Distinguir claramente o que existe no código, o que foi implementado, o que foi testado, o que foi verificado, o que permanece desconhecido e o que está bloqueado.",
        "origem": "comando_senior",
        "status": "fundamental",
    },
    {
        "id": "pa-018",
        "tipo": "principio",
        "titulo": "A BN serve à verdade, não à visão",
        "conteudo": "Acumular evidências, capacidades e aprendizados sem deixar que uma hipótese anterior force a interpretação dos fatos.",
        "origem": "historia_projeto",
        "status": "fundamental",
    },
    {
        "id": "pa-019",
        "tipo": "arquitetura",
        "titulo": "Portas substituíveis",
        "conteudo": "Uma capacidade deve poder ser fornecida por diferentes portas ou provedores. Se uma porta desaparecer, outra implementação deve poder assumir a capacidade.",
        "origem": "arquitetura_cerebro",
        "status": "direcao",
    },
    {
        "id": "pa-020",
        "tipo": "estrategia",
        "titulo": "Construir enquanto olha para passado, presente e futuro",
        "conteudo": "Cada avanço deve preservar o que já funciona, entender o estado presente e evitar bloquear possibilidades futuras.",
        "origem": "comando_mestre",
        "status": "fundamental",
    },
)


def conhecimento_fundamental() -> list[dict[str, Any]]:
    return [dict(item) for item in CONHECIMENTOS_FUNDAMENTAIS]


def buscar_conhecimento_fundamental(termo: str) -> list[dict[str, Any]]:
    termo = termo.strip().lower()
    if not termo:
        return conhecimento_fundamental()
    return [
        dict(item)
        for item in CONHECIMENTOS_FUNDAMENTAIS
        if termo in " ".join(str(v) for v in item.values()).lower()
    ]
