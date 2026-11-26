# trendsia-p0: triagem de mensagens de clientes com LLM

Repositório do **projeto P0** da formação [TrendsIA](https://softexcps.org.br/trendsia/), uma formação em Agentes de Inteligência Artificial baseada em projetos (PBL). A formação faz parte do programa TrendsIT, do Núcleo Softex Campinas, com coordenação do Softex e iniciativa do Ministério da Ciência, Tecnologia e Inovação (MCTI).

> **Status:** níveis **Básico** e **Intermediário** concluídos. O nível Avançado está em desenvolvimento.

## O problema

Uma startup de impressão 3D em fase inicial (action figures e peças sob encomenda) recebe mensagens de clientes pelo WhatsApp e pelo Instagram. Uma única pessoa cuida do atendimento. Num dia normal chegam de 5 a 20 mensagens, e em datas como o Dia das Crianças e o Natal esse número sobe para 40 a 60. As mensagens dos dois canais se misturam, e uma reclamação pode ficar esperando atrás de vários "bom dia".

Este programa **classifica cada mensagem por tipo e urgência** e sugere uma ação, para que o atendente saiba o que responder primeiro.

- **Público:** quem atende sozinho os clientes de um pequeno negócio.
- **Entrada:** o texto de uma mensagem de cliente.
- **Saída:** categoria, urgência, um resumo curto e uma ação sugerida.

| Categoria | Quando | Urgência típica |
|---|---|---|
| `reclamacao` | produto quebrado, danificado, faltando parte, outro problema no pedido ou insatisfação clara | **alta** |
| `orcamento` | pergunta sobre preço | **alta** |
| `encomenda` | pedido de produção de uma peça | media |
| `frete_entrega` | custo, prazo ou área de entrega, antes da compra | media |
| `status_pedido` | andamento, envio, rastreio ou atraso de um pedido já feito | media |
| `saudacao` | apenas cumprimento | baixa |
| `outro` | elogios, parcerias, spam e o que não se encaixa nas anteriores | baixa |

Quando a mensagem tem mais de uma intenção, prevalece a de maior urgência. O sistema **nunca promete reembolso**: nas reclamações, ele apenas sugere analisar o caso, e a decisão é do atendente.

### Por que usar um LLM e não regras fixas

Clientes escrevem de modo informal, com gírias, abreviações, erros de digitação, emojis e mais de uma intenção na mesma mensagem. Uma regra por palavras-chave não pega casos como estes:

- "chegou faltando o braço do boneco" é uma reclamação urgente, mas não contém "quebrado" nem "danificado";
- "Faz quanto pra mandar pra Manaus?" é uma pergunta sobre frete, mas não contém a palavra "frete".

Um modelo de linguagem interpreta a intenção da mensagem, não só as palavras.

## Como funciona

```
configuração → mensagem → prompt → POST /api/chat (Ollama) → validação do JSON → resultado
```

1. Lê e **valida** a configuração (endereço do LLM, modelo, tempo limite etc.) das variáveis de ambiente ou do arquivo `.env`.
2. Recebe a mensagem como argumento do comando ou pede que ela seja digitada. Mensagem vazia é recusada.
3. Envia ao LLM, por **API REST**, as instruções de classificação e a mensagem. O pedido inclui o **esquema JSON** da resposta, então o Ollama só gera respostas nesse formato.
4. **Valida** a resposta com [pydantic](https://docs.pydantic.dev): as categorias e urgências precisam ser as da tabela acima, e o resumo e a ação não podem vir vazios.
5. Mostra os quatro campos no terminal.

Qualquer falha (configuração, rede, tempo esgotado, resposta fora do formato) vira uma **mensagem clara em português**, sem o erro técnico do Python. Veja [Erros tratados](#erros-tratados).

### Organização do código

Cada responsabilidade fica num módulo próprio, em `src/triagem/`:

| Módulo | Responsabilidade |
|---|---|
| `config.py` | ler e validar as variáveis de ambiente |
| `entrada.py` | obter e validar a mensagem do cliente |
| `prompt.py` | instruções de classificação enviadas ao LLM |
| `cliente_llm.py` | chamada HTTP ao Ollama e tradução dos erros de rede e de status HTTP |
| `parser.py` | conversão e validação da resposta (modelo `Classificacao`, com pydantic) |
| `saida.py` | apresentação do resultado e dos erros |
| `erros.py` | os tipos de erro do programa |
| `__main__.py` | ponto de entrada: organiza o fluxo e captura os erros |

### LLM utilizado

O projeto usa o **[Ollama](https://ollama.com)** rodando **no próprio computador**, com o modelo **`qwen3.5:9b-q4_K_M`**, da família Qwen.

- É gratuito e não usa chave de API. Para servidores que exigem autenticação, existe a variável opcional `LLM_API_KEY`.
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
├── Dockerfile            # imagem para rodar na plataforma Devel (LLM institucional)
├── .dockerignore         # arquivos que nunca entram na imagem (inclui .env)
├── src/
│   └── triagem/
│       ├── __init__.py
│       ├── __main__.py   # ponto de entrada (python -m triagem)
│       ├── config.py
│       ├── entrada.py
│       ├── prompt.py
│       ├── cliente_llm.py
│       ├── parser.py
│       ├── saida.py
│       └── erros.py
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

O primeiro comando instala as bibliotecas `requests`, `python-dotenv` e `pydantic`. O segundo instala o próprio programa (o pacote `triagem`) no ambiente virtual.

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
| `LLM_TIMEOUT` | `300` | tempo máximo de espera pela resposta, em segundos. Numa CPU, a primeira chamada pode passar de 2 minutos |
| `LLM_VERIFY_SSL` | `true` | verificar o certificado HTTPS do servidor. Use `false` apenas em servidores internos com certificado autoassinado (veja a seção sobre a plataforma Devel). Não tem efeito no Ollama local |
| `LLM_API_KEY` | (vazio) | chave de acesso, enviada no cabeçalho `Authorization: Bearer`. Opcional: o Ollama local não usa chave |

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

**Tempo de resposta:** num computador sem GPU dedicada, a primeira execução pode levar mais de 2 minutos, porque o modelo é carregado na memória. As seguintes levam de 30 segundos a pouco mais de 1 minuto.

## Erros tratados

Em caso de falha, o programa mostra uma mensagem clara (na saída de erros) e termina com código de saída `1`.

| Situação | Mensagem mostrada (resumo) |
|---|---|
| Mensagem vazia | A mensagem está vazia. Informe o texto do cliente… |
| Variável ausente (`LLM_URL`, `LLM_MODEL`) | A variável … não está definida. Copie o .env.example para .env… |
| Valor inválido (`LLM_URL` sem `http`, `LLM_TIMEOUT` não numérico, `LLM_VERIFY_SSL` diferente de `true`/`false`) | indica qual variável corrigir |
| Ollama desligado ou endereço errado | Não foi possível conectar ao LLM. Verifique se o Ollama está em execução… |
| Servidor com defeito ou ainda ligando (HTTP 5xx, como o 502 da plataforma Devel antes de o LLM ficar pronto) | O servidor do LLM está com problemas… |
| Credencial inválida ou acesso negado (HTTP 401/403) | O servidor do LLM recusou o acesso… Verifique a chave em LLM_API_KEY |
| Modelo não encontrado (HTTP 404) | Confira LLM_MODEL (o modelo precisa aparecer em 'ollama list')… |
| Certificado HTTPS não verificável | …defina LLM_VERIFY_SSL=false (só em servidores internos) |
| Tempo esgotado | O LLM não respondeu em … segundos. Tente de novo ou aumente LLM_TIMEOUT |
| Resposta fora do formato (não é JSON, categoria inexistente, campo vazio) | O LLM respondeu fora do formato esperado… |

O Ollama local não usa autenticação, então o erro de credencial não ocorre com ele. Esse caso e a resposta fora do formato foram verificados com um servidor simulado. O HTTP 5xx e o certificado autoassinado também foram observados de verdade na plataforma Devel. A saída de cada caso está em [evidencias/erros-intermediario.md](evidencias/erros-intermediario.md).

## Execução na plataforma Devel (LLM institucional)

O programa também roda na plataforma Devel da formação, usando o LLM institucional, que é um servidor Ollama interno com o mesmo modelo `qwen3.5:9b-q4_K_M`. **O código é o mesmo**: só a configuração muda.

Esse LLM só é acessível **de dentro da plataforma**. Por isso o programa é enviado como uma **imagem Docker** e roda num container lá. Como não há terminal interativo, a mensagem vem da variável `MENSAGEM`, e o resultado aparece em **Logs**, no portal.

**Requisito adicional:** [Docker Desktop](https://www.docker.com/products/docker-desktop/), com o motor ("Engine") em execução.

### 1. Montar e testar a imagem

Na pasta do repositório, troque `<seu-id>` pelo identificador exigido pela plataforma, que é o seu e-mail sem caracteres especiais:

```powershell
docker build -t <seu-id>:latest .
```

Para testar a imagem antes de enviar, usando o Ollama local (`host.docker.internal` é o endereço do seu computador visto de dentro do container):

```powershell
docker run --rm -e LLM_URL=http://host.docker.internal:11434 -e LLM_MODEL=qwen3.5:9b-q4_K_M -e LLM_TIMEOUT=300 -e ESPERA_LLM=0 -e MENSAGEM="chegou faltando o braço do boneco" <seu-id>:latest
```

### 2. Exportar e enviar

```powershell
docker save --output <seu-id>.tar <seu-id>:latest
```

No portal, use **Enviar container** com:

- **Porta do container:** `8080`. O portal exige uma porta, mas o programa não escuta nenhuma.
- **Variáveis de ambiente:**
  ```
  LLM_URL=<endereço do LLM interno, informado no guia da plataforma>
  LLM_MODEL=qwen3.5:9b-q4_K_M
  LLM_TIMEOUT=300
  ESPERA_LLM=120
  LLM_VERIFY_SSL=false
  MENSAGEM=chegou faltando o braço do boneco
  ```
- **Arquivo:** o `<seu-id>.tar` gerado acima.

### 3. Executar

Clique em **Iniciar** logo depois de configurar: o LLM da plataforma só liga quando um container é iniciado, e o `ESPERA_LLM` faz o programa aguardar até ele ficar pronto. Depois de cerca de 3 minutos, abra **Logs**. O programa classifica a mensagem e o container termina. Para classificar outra mensagem, altere `MENSAGEM` e inicie de novo.

Com o LLM já ligado, a plataforma responde em cerca de 2 segundos, porque o servidor é bem mais rápido que um computador sem GPU. Resultados dos testes na plataforma: [evidencias/plataforma-devel.md](evidencias/plataforma-devel.md).

## Resultados

Avaliação com o modelo local, em 21 mensagens fictícias (os 12 exemplos, 6 casos difíceis e 3 casos de `status_pedido` e orçamento):

| Versão | Categoria correta | Urgência correta |
|---|---|---|
| Básico (12 exemplos) | 11 de 12 | 12 de 12 |
| Intermediário (12 exemplos) | **12 de 12** | **12 de 12** |
| Intermediário (todas as 21) | **20 de 21** | **21 de 21** |

No Intermediário, nenhuma ação sugerida mencionou reembolso. Detalhes em [evidencias/avaliacao-basico.md](evidencias/avaliacao-basico.md) e [evidencias/avaliacao-intermediario.md](evidencias/avaliacao-intermediario.md).

## Testes

Os testes automatizados (com resposta simulada do LLM, sem chamá-lo de verdade) entram no nível Avançado e ficarão em [tests/](tests/).

## Limitações conhecidas

- **Mensagens curtas e vagas:** comentários como "Eh bom" ainda podem ser tomados por cumprimento (`saudacao` em vez de `outro`). Como as duas categorias têm urgência baixa, o impacto na priorização é pequeno.
- **Qualidade do texto:** o modelo local às vezes produz palavras erradas ou frases estranhas no resumo e na ação (por exemplo, "orçemento").
- **Sugestões não são garantidas:** nos testes do Intermediário, nenhuma ação mencionou reembolso, mas o modelo não é infalível. O atendente deve sempre revisar a sugestão antes de responder ao cliente.
- **Desempenho:** sem GPU, cada resposta leva de 30 segundos a mais de 1 minuto, e a primeira pode passar de 2 minutos.
- **Validação de formato, não de conteúdo:** o pydantic garante que a resposta tem o formato certo, mas não que a classificação está correta. Uma mensagem pode ser classificada na categoria errada e ainda assim passar pela validação.
- O programa só classifica: ele **não** responde ao cliente, não se integra ao WhatsApp ou ao Instagram e não guarda histórico.

## Níveis de entrega e versões

O projeto é entregue em três níveis. Cada nível é marcado por uma **tag** no repositório:

| Nível | Tag | Status |
|---|---|---|
| Básico | `p0-basico` | concluído |
| Intermediário | `p0-intermediario` | concluído |
| Avançado (versão final entregue) | `p0-avancado` | pendente |

## Documentação

- **Relatório principal:** [docs/relatorio.md](docs/relatorio.md)
- **Uso de IA no desenvolvimento:** [docs/uso-de-ia.md](docs/uso-de-ia.md)
- **Avaliação do nível Básico:** [evidencias/avaliacao-basico.md](evidencias/avaliacao-basico.md)
- **Execução na plataforma Devel:** [evidencias/plataforma-devel.md](evidencias/plataforma-devel.md)
- **Avaliação do nível Intermediário:** [evidencias/avaliacao-intermediario.md](evidencias/avaliacao-intermediario.md)
- **Erros tratados (saídas reais):** [evidencias/erros-intermediario.md](evidencias/erros-intermediario.md)
- **Vídeo de apresentação:** (link a definir)

## Autor

- [Caionbr](https://github.com/Caionbr)
