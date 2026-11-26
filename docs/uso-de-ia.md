# Declaração de uso de IA

Este documento registra, de forma resumida, o uso de ferramentas de Inteligência Artificial no desenvolvimento do projeto P0, conforme a política de uso de IA da formação TrendsIA.

## Compromisso de autoria

A IA foi usada como **apoio**: explicar conceitos, propor código e documentação e revisar. Todo conteúdo sugerido foi **revisado, testado e aprovado pelo autor**, que define o comportamento do sistema e é capaz de explicar cada parte do projeto.

## Ferramentas utilizadas

| Ferramenta | Modelo | Finalidade |
|---|---|---|
| Claude Code (extensão do VS Code) | Claude Opus 5.5 (Anthropic) | Apoio à configuração do ambiente, ao código, à documentação e ao aprendizado de Git, Python e Docker |

> O **Ollama com o modelo Qwen** não é ferramenta de apoio: é o LLM que o próprio programa chama, ou seja, faz parte do produto.

## Registro de uso

### 1. Estrutura do repositório e README inicial

- **Tarefa:** propor a estrutura de pastas e uma primeira versão do README.
- **Verificação:** conferência com as regras da formação e revisão do texto pelo autor.

### 2. Ambiente e LLM local

- **Tarefa:** instalar o Ollama, identificar a tag do modelo Qwen equivalente à do LLM institucional e baixá-lo.
- **Verificação:** servidor respondendo em `http://localhost:11434` e modelo listado em `ollama list`.

### 3. Código do nível Básico

- **Tarefa:** codesenvolver o programa (configuração, entrada, prompt, chamada à API `/api/chat` e saída) e os arquivos de configuração. O problema, as categorias, os critérios de urgência e as regras do prompt foram definidos pelo autor.
- **Verificação:** execução com as 12 mensagens do conjunto de exemplos e com casos extras ([evidencias/avaliacao-basico.md](../evidencias/avaliacao-basico.md)).

### 4. Execução na plataforma Devel

- **Tarefa:** explicar Docker e certificados HTTPS, escrever o `Dockerfile` e o `.dockerignore` e tornar configurável a verificação do certificado (`LLM_VERIFY_SSL`).
- **Verificação:** teste da imagem com o Ollama local e execução na plataforma ([evidencias/plataforma-devel.md](../evidencias/plataforma-devel.md)).

### 5. Documentação

- **Tarefa:** atualizar o README e organizar em tabelas os resultados dos testes feitos pelo autor.
- **Verificação:** leitura completa pelo autor e conferência dos comandos no Windows.
