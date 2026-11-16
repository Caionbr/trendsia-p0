# Declaração de uso de IA

Este documento registra o uso de ferramentas de Inteligência Artificial no desenvolvimento do projeto P0, conforme a política de uso de IA da formação TrendsIA.

## Compromisso de autoria

Ferramentas de IA são usadas como **apoio** ao desenvolvimento, para facilitar a escrita, a explicação de conceitos e a revisão. Todo conteúdo gerado ou sugerido por IA, seja código, teste ou documentação, é **revisado, corrigido e verificado pelo autor** antes de entrar no repositório. O autor mantém a autoria e a responsabilidade pelo que é entregue e é capaz de explicar cada parte do projeto.

Este registro inclui apenas as interações que influenciaram de forma significativa o trabalho. As conversas completas não são reproduzidas.

## Ferramentas utilizadas

| Ferramenta | Modelo | Finalidade |
|---|---|---|
| Claude Code (extensão do VS Code) | Claude Opus 5.5 (Anthropic) | Apoio à organização do repositório, à configuração do ambiente, à escrita do código e da documentação e ao aprendizado de Git e Python |

> O **Ollama com o modelo Qwen** não é ferramenta de apoio ao desenvolvimento: ele é o LLM que o próprio programa chama, ou seja, faz parte do produto (veja o [README](../README.md)).

## Registro de uso

### 1. Estrutura inicial do repositório

- **Tarefa delegada:** propor a estrutura de pastas e arquivos do repositório a partir das regras da formação (código-fonte, README, dependências, `.env.example`, `.gitignore`, testes, registros, relatório e declaração de uso de IA).
- **Resultado aproveitado:** a estrutura de pastas (`src/`, `tests/`, `evidencias/`, `docs/`) e os arquivos iniciais, criados vazios.
- **Correções, adaptações ou descartes:** a estrutura proposta foi revisada pelo autor e mantida.
- **Forma de verificação:** conferência, item por item, da estrutura contra a lista de artefatos exigidos pelas regras da formação.

### 2. Escrita do README

- **Tarefa delegada:** redigir uma primeira versão do `README.md` descrevendo o projeto P0, a partir das informações públicas da formação TrendsIA e do Guia do Aluno.
- **Resultado aproveitado:** a estrutura e o texto-base do README: descrição do projeto, estrutura do repositório, requisitos, instruções de execução, níveis de entrega e documentação.
- **Correções, adaptações ou descartes:** o texto foi revisado e ajustado pelo autor. A seção sobre a posição do P0 na trilha da formação foi removida por enquanto e poderá ser retomada depois.
- **Forma de verificação:** leitura completa do README e conferência das informações com o site da formação e o Guia do Aluno.

### 3. Ambiente de execução do LLM (Ollama)

- **Tarefa delegada:** instalar o Ollama no Windows pelo terminal (`winget`), conferir na biblioteca do Ollama qual tag do modelo Qwen corresponde à do LLM institucional e baixar o modelo.
- **Resultado aproveitado:** Ollama 0.40.16 instalado e o modelo `qwen3.5:9b-q4_K_M` (6,6 GB) baixado, a mesma tag usada na plataforma da formação.
- **Correções, adaptações ou descartes:** a escolha do Ollama local em vez da plataforma institucional foi decisão do autor. O modelo menor (`qwen3.5:4b-q4_K_M`) ficou como alternativa caso o de 9B fosse lento demais, o que não foi necessário.
- **Forma de verificação:** `ollama --version`, resposta `Ollama is running` em `http://localhost:11434` e o modelo listado em `ollama list`.

### 4. Arquivos de configuração e código do nível Básico

- **Tarefa delegada:** preencher o `.gitignore`, o `requirements.txt` e o `.env.example`, criar o `pyproject.toml` e codesenvolver o programa `src/triagem/__main__.py` (leitura da configuração, leitura da mensagem, prompt de classificação, chamada à API `/api/chat` com `requests` e exibição do resultado).
- **Resultado aproveitado:** o programa foi construído em conjunto. O autor definiu o comportamento: o problema, as categorias, os critérios de urgência, as regras do prompt, os campos da saída e a forma de execução pelo terminal. O assistente propôs a implementação em Python, explicada função por função. O autor revisou e testou o código antes de adotá-lo.
- **Correções, adaptações ou descartes:** as categorias, os critérios de urgência e a regra de nunca prometer reembolso que estão no prompt foram definidos pelo autor, na ficha do problema.
- **Forma de verificação:** execução do programa pelo autor com as 12 mensagens fictícias do conjunto de exemplos e com 6 mensagens extras escritas para provocar erros. Os resultados, incluindo erros e limitações, estão em [evidencias/avaliacao-basico.md](../evidencias/avaliacao-basico.md). O `git status` foi conferido para garantir que o `.env` e o `.venv` não são versionados.

### 5. README do nível Básico e registro da avaliação

- **Tarefa delegada:** atualizar o README com problema, público, justificativa do uso de LLM, funcionamento, instalação, configuração, execução, exemplo de saída e limitações; organizar em tabela os resultados dos testes feitos pelo autor.
- **Resultado aproveitado:** o README e o arquivo `evidencias/avaliacao-basico.md`.
- **Correções, adaptações ou descartes:** a parte inicial do README original foi mantida. As limitações listadas vêm dos erros observados pelo autor nos próprios testes.
- **Forma de verificação:** leitura completa pelo autor e conferência dos comandos de instalação no Windows.
