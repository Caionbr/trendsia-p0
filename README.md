# trendsia-p0: triagem de mensagens de clientes com LLM

Repositório do **projeto P0** da formação [TrendsIA](https://softexcps.org.br/trendsia/), uma formação em Agentes de Inteligência Artificial baseada em projetos (PBL). A formação faz parte do programa TrendsIT, do Núcleo Softex Campinas, com coordenação do Softex e iniciativa do Ministério da Ciência, Tecnologia e Inovação (MCTI).

> **Status:** nível **Básico** concluído. Os níveis Intermediário e Avançado estão em desenvolvimento.

## O problema

Uma startup de impressão 3D em fase inicial (action figures e peças sob encomenda) recebe mensagens de clientes pelo WhatsApp e pelo Instagram. Uma única pessoa cuida do atendimento. Num dia normal chegam de 5 a 20 mensagens, e em datas como o Dia das Crianças e o Natal esse número sobe para 40 a 60. As mensagens dos dois canais se misturam, e uma reclamação pode ficar esperando atrás de vários "bom dia".

Este programa **classifica cada mensagem por tipo e urgência** e sugere uma ação, para que o atendente saiba o que responder primeiro.

- **Público:** quem atende sozinho os clientes de um pequeno negócio.
- **Entrada:** o texto de uma mensagem de cliente.
- **Saída:** categoria, urgência, um resumo curto e uma ação sugerida.

| Categoria | Quando | Urgência típica |
|---|---|---|
| `reclamacao` | produto quebrado, danificado, faltando parte ou outro problema no pedido | **alta** |
| `encomenda` | pedido de produção de uma peça | media |
| `orcamento` | pergunta sobre preço | media |
| `frete_entrega` | custo, prazo ou área de entrega | media |
| `saudacao` | apenas cumprimento | baixa |
| `outro` | elogios, parcerias, spam e o que não se encaixa nas anteriores | baixa |

O sistema **nunca promete reembolso**. Nas reclamações, ele apenas sugere analisar o caso. A decisão é do atendente.

### Por que usar um LLM e não regras fixas

Clientes escrevem de modo informal, com gírias, abreviações, erros de digitação, emojis e mais de uma intenção na mesma mensagem. Uma regra por palavras-chave não pega casos como estes:

- "chegou faltando o braço do boneco" é uma reclamação urgente, mas não contém "quebrado" nem "danificado";
- "Faz quanto pra mandar pra Manaus?" é uma pergunta sobre frete, mas não contém a palavra "frete".

Um modelo de linguagem interpreta a intenção da mensagem, não só as palavras.

## Como funciona

```
mensagem (terminal) → monta o prompt → POST /api/chat (Ollama) → JSON → resultado no terminal
```

1. O programa lê a configuração (endereço do LLM, modelo e tempo limite) do arquivo `.env`.
2. Recebe a mensagem como argumento do comando ou pede que ela seja digitada.
3. Envia ao LLM, por **API REST**, as instruções de classificação e a mensagem, pedindo a resposta em JSON.
4. Converte o JSON da resposta e mostra os quatro campos no terminal.

### LLM utilizado

O projeto usa o **[Ollama](https://ollama.com)** rodando **no próprio computador**, com o modelo **`qwen3.5:9b-q4_K_M`**, da família Qwen.

- É gratuito e não usa chave de API. Não há credencial para configurar nem para vazar.
- Funciona sem internet depois que o modelo é baixado.
- Usa a mesma API do LLM institucional da formação, que também é um servidor Ollama. Para trocar de um para o outro, basta mudar `LLM_URL` e `LLM_MODEL` no `.env`, sem alterar o código.

## Estrutura do repositório

```
trendsia-p0/
├── README.md             # este arquivo
├── pyproject.toml        # descreve o pacote "triagem" (permite "python -m triagem")
├── requirements.txt      # dependências Python, com versões fixas
├── .env.example          # modelo das variáveis de ambiente
├── .gitignore            # arquivos que não devem ser versionados (inclui .env e .venv)
├── src/
│   └── triagem/
│       ├── __init__.py
│       └── __main__.py   # programa principal
├── tests/                # casos de teste (a partir do nível Avançado)
├── evidencias/           # registros de execução e avaliações
└── docs/
    ├── relatorio.md      # relatório principal do projeto
    └── uso-de-ia.md      # declaração de uso de ferramentas de IA
```

## Requisitos

- **Python 3.12** ou mais novo ([python.org](https://www.python.org/downloads/)). No Windows, marque **"Add python.exe to PATH"** durante a instalação.
- **Git** ([git-scm.com](https://git-scm.com/downloads)).
- **Ollama** ([ollama.com/download](https://ollama.com/download)).
- Cerca de **7 GB de espaço livre** em disco para o modelo e **pelo menos 8 GB de RAM livres** para rodá-lo.

## Instalação

Os comandos abaixo são para o **PowerShell no Windows**. Os equivalentes para Linux e macOS aparecem logo depois de cada bloco.

### 1. Instalar o Ollama e baixar o modelo

Instale o Ollama pelo site ou pelo terminal:

```powershell
winget install --id Ollama.Ollama -e
```

Em um terminal novo, baixe o modelo (cerca de 6,6 GB):

```powershell
ollama pull qwen3.5:9b-q4_K_M
```

Para confirmar que o servidor está no ar, rode o comando abaixo. A resposta esperada é `Ollama is running`:

```powershell
Invoke-RestMethod http://localhost:11434
```

> Linux: `curl -fsSL https://ollama.com/install.sh | sh` instala o Ollama, e `curl http://localhost:11434` confere o servidor. O `ollama pull` é igual.

### 2. Clonar o repositório

```powershell
git clone https://github.com/Caionbr/trendsia-p0.git
cd trendsia-p0
```

### 3. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

O início da linha do terminal passa a mostrar `(.venv)`.

> Linux/macOS: `python3 -m venv .venv` e `source .venv/bin/activate`.

### 4. Instalar as dependências e o programa

```powershell
pip install -r requirements.txt
pip install -e .
```

O primeiro comando instala as bibliotecas `requests` e `python-dotenv`. O segundo instala o próprio programa (o pacote `triagem`) no ambiente virtual.

## Configuração

Copie o arquivo de modelo para criar o seu `.env`:

```powershell
Copy-Item .env.example .env
```

> Linux/macOS: `cp .env.example .env`.

Os valores do modelo já funcionam com a instalação acima:

| Variável | Valor padrão | Para que serve |
|---|---|---|
| `LLM_URL` | `http://localhost:11434` | endereço do servidor Ollama |
| `LLM_MODEL` | `qwen3.5:9b-q4_K_M` | modelo usado. Precisa aparecer em `ollama list` |
| `LLM_TIMEOUT` | `120` | tempo máximo de espera pela resposta, em segundos |

O `.env` é local e está no `.gitignore`, então **nunca vai para o repositório**.

## Execução

Com o ambiente virtual ativo (`(.venv)` no início da linha), passe a mensagem entre aspas:

```powershell
python -m triagem "chegou faltando o braço do boneco"
```

Ou rode sem a mensagem e digite-a quando o programa pedir:

```powershell
python -m triagem
```

### Exemplo de saída

```
Categoria:     reclamacao
Urgência:      alta
Resumo:        Cliente reportou peça entregue incompleta, faltando o braço da action figure.
Ação sugerida: Aguardar envio de foto do pacote e peça; analisar caso para orientar sobre reposição ou troca.
```

O texto do resumo e da ação muda a cada execução. A categoria e a urgência tendem a se manter.

**Tempo de resposta:** num computador sem GPU dedicada, a primeira execução leva cerca de 1 minuto, porque o modelo é carregado na memória. As seguintes levam em torno de 30 segundos.

## Resultados

Nas 12 mensagens fictícias do conjunto de exemplos, a **categoria acertou em 11 de 12** e a **urgência em 12 de 12**. A tabela completa e os casos difíceis estão em [evidencias/avaliacao-basico.md](evidencias/avaliacao-basico.md).

## Testes

Os testes automatizados (com resposta simulada do LLM, sem chamá-lo de verdade) entram no nível Avançado e ficarão em [tests/](tests/).

## Limitações conhecidas

- **Erros em mensagens ambíguas:** comentários curtos ou com avaliação mista ("Eh bom", "Ja vi melhor, pelo preco eh ok") podem ser classificados de forma errada, e o resumo pode afirmar algo que o cliente não disse.
- **Categorias incompletas:** não existe categoria para "status do pedido" ("ainda não recebi atualização"). Essas mensagens caem em `outro`, às vezes com uma urgência fora do critério.
- **Qualidade do texto:** o modelo local às vezes produz palavras erradas no resumo e na ação ("prazos médicos", "complimentos").
- **Regra do reembolso:** apesar da instrução, a ação sugerida pode mencionar "reembolso parcial". O atendente deve sempre revisar a sugestão.
- **Desempenho:** a resposta leva dezenas de segundos sem GPU.
- **Tratamento de erros:** no nível Básico, falhas como Ollama desligado, tempo esgotado ou resposta fora do formato aparecem como erro técnico do Python. Mensagens claras para esses casos fazem parte do nível Intermediário.
- O programa só classifica: ele **não** responde ao cliente, não se integra ao WhatsApp ou ao Instagram e não guarda histórico.

## Níveis de entrega e versões

O projeto é entregue em três níveis. Cada nível é marcado por uma **tag** no repositório:

| Nível | Tag | Status |
|---|---|---|
| Básico | `p0-basico` | concluído |
| Intermediário | `p0-intermediario` | pendente |
| Avançado (versão final entregue) | `p0-avancado` | pendente |

## Documentação

- **Relatório principal:** [docs/relatorio.md](docs/relatorio.md)
- **Uso de IA no desenvolvimento:** [docs/uso-de-ia.md](docs/uso-de-ia.md)
- **Avaliação do nível Básico:** [evidencias/avaliacao-basico.md](evidencias/avaliacao-basico.md)
o.md)
- **Uso de IA no desenvolvimento:** [docs/uso-de-ia.md](docs/uso-de-ia.md)
- **Vídeo de apresentação:** (link a definir)

## Autor

- [Caionbr](https://github.com/Caionbr)
