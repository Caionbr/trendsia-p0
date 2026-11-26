# Erros tratados no nível Intermediário: saídas reais

Cada situação foi provocada de propósito. Em todos os casos o programa mostra só a mensagem (sem o traceback do Python) e termina com **código de saída 1**.

Os casos de credencial (401/403), servidor com defeito (500) e resposta fora do formato não acontecem com o Ollama local, que não usa autenticação e responde sempre no formato pedido. Eles foram provocados com um **servidor simulado** que imita a API `/api/chat` do Ollama e responde com o código ou o conteúdo de cada caso. Esse servidor foi usado só para o teste e não faz parte do repositório.

| # | Situação | Como foi provocada | Saída |
|---|---|---|---|
| 1 | Mensagem vazia | `python -m triagem "   "` | `Erro: A mensagem está vazia. Informe o texto do cliente: no terminal, entre aspas (python -m triagem "texto"); na plataforma Devel, na variável MENSAGEM.` |
| 2 | Configuração ausente | `LLM_MODEL` vazio | `Erro: A variável LLM_MODEL não está definida. Copie o .env.example para .env e preencha os valores.` |
| 3 | URL inválida | `LLM_URL=localhost:11434` | `Erro: LLM_URL deve começar com http:// ou https://.` |
| 4 | Tempo limite inválido | `LLM_TIMEOUT=abc` | `Erro: LLM_TIMEOUT deve ser um número de segundos maior que zero (ex.: 300).` |
| 5 | Verificação SSL inválida | `LLM_VERIFY_SSL=talvez` | `Erro: LLM_VERIFY_SSL deve ser true ou false.` |
| 6 | Serviço indisponível | `LLM_URL=http://localhost:11999` (nada escutando) | `Erro: Não foi possível conectar ao LLM. Verifique se o Ollama está em execução e se LLM_URL está correto.` |
| 7 | Modelo não encontrado (HTTP 404) | `LLM_MODEL=modelo-que-nao-existe` no Ollama real | `Erro: O servidor não encontrou o modelo ou o endereço (HTTP 404). Confira LLM_MODEL (o modelo precisa aparecer em 'ollama list') e LLM_URL.` |
| 8 | Tempo esgotado | `LLM_TIMEOUT=1` no Ollama real | `Erro: O LLM não respondeu dentro do limite de 1 s. Tente de novo ou aumente LLM_TIMEOUT.` |
| 9 | Credencial inválida (HTTP 401) | servidor simulado, com `LLM_API_KEY` preenchida | `Erro: O servidor do LLM recusou o acesso (HTTP 401). Verifique a chave em LLM_API_KEY.` |
| 10 | Acesso negado (HTTP 403) | servidor simulado | `Erro: O servidor do LLM recusou o acesso (HTTP 403). Verifique a chave em LLM_API_KEY.` |
| 11 | Servidor com defeito (HTTP 500) | servidor simulado | `Erro: O servidor do LLM está com problemas (HTTP 500). Tente novamente em alguns minutos.` |
| 12 | Resposta que não é do Ollama | servidor simulado devolvendo um JSON sem o campo `message` | `Erro: O servidor respondeu num formato inesperado (não parece uma resposta do Ollama).` |
| 13 | Resposta que não é JSON | servidor simulado devolvendo texto livre | `Erro: O LLM respondeu fora do formato esperado (a resposta não é um JSON válido). Tente novamente.` |
| 14 | Categoria inexistente | servidor simulado devolvendo `"categoria": "elogio"` | `Erro: O LLM respondeu fora do formato esperado (campos com problema: categoria). Tente novamente.` |
| 15 | Certificado autoassinado | plataforma Devel com `LLM_VERIFY_SSL=true` | `Erro: Não foi possível verificar o certificado HTTPS do servidor do LLM. Se for um servidor interno com certificado autoassinado, defina LLM_VERIFY_SSL=false.` (no Básico, o mesmo caso gerava dezenas de linhas de traceback) |
| 16 | LLM ainda ligando (HTTP 502) | plataforma Devel com `ESPERA_LLM=0`, antes de o LLM ficar disponível | `Erro: O servidor do LLM está com problemas (HTTP 502). Tente novamente em alguns minutos.` |
| 17 | Mensagem vazia na plataforma | plataforma Devel com `MENSAGEM=` | `Erro: A mensagem está vazia. Informe o texto do cliente: no terminal, entre aspas (python -m triagem "texto"); na plataforma Devel, na variável MENSAGEM.` |

As mensagens de erro nunca repetem o texto do cliente nem o conteúdo da resposta do LLM.
