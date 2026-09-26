# AUDITORIA TÉCNICA — CONJUNTO DE INTERFACES ABS

## Data
2026-09-25

## 1. Contexto real

Ambiente considerado: Android 10, ARM64, 4 GB de RAM, Termux, ABS no telefone, llama.cpp, Qwen2.5-0.5B-Instruct Q4_K_M, IA local em 127.0.0.1:8080, ABS Gateway OpenAI-compatible em 127.0.0.1:8788 e navegador Android.

Conclusão: não devemos instalar várias plataformas pesadas no telefone ao mesmo tempo. Interfaces pesadas podem ser executadas posteriormente em VPS/nó remoto, enquanto o telefone continua sendo ponto de comando.

## 2. Resultado

### A — candidatos para teste real

#### 1. Open WebUI — interface geral
Conecta APIs OpenAI-compatible, provedores locais e externos, possui conhecimento/RAG e suporte a MCP. A documentação oficial também oferece instalação por Python, além de Docker.
Avaliação: ALTA prioridade para teste.
Uso previsto: Android → Open WebUI → ABS Gateway → ABS.
Risco: medir consumo antes de manter no telefone.

#### 2. LibreChat — multi-IA e agentes
Suporta endpoints OpenAI-compatible personalizados, agentes, MCP, RAG, Code Interpreter e outras capacidades. Possui instalação Docker, npm e hospedagem remota.
Avaliação: ALTA prioridade para teste, preferencialmente fora do telefone se necessário.
Uso previsto: Android → LibreChat → ABS Gateway → ABS.
Risco: instalação completa pode envolver MongoDB e outros componentes.

#### 3. AnythingLLM — conhecimento e documentos
Trabalha com workspaces, múltiplos LLMs, provedores locais/cloud, agentes e documentos. Possui opções de self-hosting.
Avaliação: MÉDIA/ALTA prioridade como componente especializado.
Uso previsto: conhecimento/documentos, complementando o Cérebro sem substituir a memória oficial do ABS.

#### 4. Dify — workflows e agentes
Oferece workflows, agentes, RAG, gerenciamento de modelos e observabilidade. O repositório oficial informa requisito mínimo de 4 GiB de RAM e instalação por Docker Compose.
Avaliação: ALTA utilidade funcional, BAIXA prioridade para instalar no telefone.
Uso previsto: ferramenta auxiliar em VPS/nó remoto.

### B — complementares

LobeChat: baixa prioridade imediata; pode ser testado posteriormente para experiência de conversa.

Jan: não instalar agora. O ABS já possui a cadeia llama.cpp → Qwen → ABS local-ai. Jan permanece como reserva para experimentação local.

Chatbot UI: não priorizar agora. Pode servir como referência ou futura base de interface própria.

## 3. Conjunto inicial recomendado

O ABS não precisa de uma única interface.

1. Open WebUI — operação geral.
2. LibreChat — multi-IA/agentes.
3. AnythingLLM — conhecimento/documentos.
4. Dify — workflows/agentes.

Isso não significa instalar os quatro no telefone.

## 4. Ordem de experimentação

1. Open WebUI: primeira interface geral; testar Gateway ABS, celular e consumo.
2. LibreChat: testar multi-IA/agentes e endpoint ABS; preferencialmente em ambiente separado se necessário.
3. AnythingLLM: testar documentos/conhecimento e integração conceitual com o Cérebro.
4. Dify: testar workflows/agentes, preferencialmente em VPS/nó remoto.

## 5. Estratégia de nós

Telefone: Android + Termux + ABS Core + llama.cpp + Qwen + interface leve/teste.
Futuro nó remoto: LibreChat + Dify + AnythingLLM + outros serviços auxiliares.
Ambos acessam o mesmo ABS Gateway/API e o mesmo ABS Core.

## 6. Critério de aprovação

Uma interface somente entra no conjunto operacional se acessar o ABS por contrato estável, não exigir alteração estrutural, tiver utilidade real, desempenho aceitável e puder ser removida sem quebrar o ABS.

## 7. Resultado arquitetural

O ABS deve possuir múltiplas interfaces especializadas, não uma única interface obrigatória.

INTERFACE → API/GATEWAY ABS → ABS CORE → CAPACIDADES

O núcleo permanece independente das interfaces.

## 8. Próxima execução

Primeira experiência prática: Open WebUI → ABS Gateway → ABS → Qwen local.
Depois: LibreChat → ABS Gateway.
Posteriormente: AnythingLLM para conhecimento/documentos e Dify para workflows/agentes.

## 9. Restrição encontrada para o primeiro teste

A documentação atual do Open WebUI informa suporte Python 3.11 e 3.12 e recomenda 3.11; Python 3.13 ainda não é suportado. O ambiente conhecido do ABS usa Python 3.14.6.

Portanto, **não instalar Open WebUI diretamente no Python atual do Termux**.

As opções corretas são:

1. executar Open WebUI em um ambiente compatível separado;
2. usar um nó remoto/VPS quando disponível;
3. disponibilizar Python 3.11 isolado no Termux somente se isso for tecnicamente seguro e não criar conflito com o ABS;
4. manter a interface própria/uma interface leve como acesso imediato enquanto a implantação da interface geral é resolvida.

Esta restrição não elimina Open WebUI da arquitetura; apenas muda sua ordem de implantação.

## Status

AUDITORIA CONCLUÍDA.

A seleção é funcional e arquitetural; não é um ranking geral de qualidade.

**Próxima ação técnica:** resolver o ambiente de execução da primeira interface sem alterar o runtime Python do ABS.