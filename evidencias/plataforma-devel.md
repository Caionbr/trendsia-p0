# Execução na plataforma Devel (LLM institucional)

- **Código:** o mesmo do nível Básico, acrescido da variável `LLM_VERIFY_SSL`
- **Imagem Docker:** `python:3.12-slim` com o pacote `triagem` instalado, com 198 MB (o limite da plataforma é 1024 MB)
- **LLM:** o servidor Ollama interno da plataforma, com o modelo `qwen3.5:9b-q4_K_M`, o mesmo usado localmente

## Configuração no portal

| Campo | Valor |
|---|---|
| Porta do container | `8080` (exigida pelo portal; o programa não escuta nenhuma porta) |
| `LLM_URL` | o endereço do LLM interno informado no guia da plataforma |
| `LLM_MODEL` | `qwen3.5:9b-q4_K_M` |
| `LLM_TIMEOUT` | `300` |
| `ESPERA_LLM` | `120` |
| `LLM_VERIFY_SSL` | `false` |
| `MENSAGEM` | `chegou faltando o braço do boneco` |

## Constatações

1. **O LLM interno só é alcançável de dentro da plataforma.** O programa precisa rodar num container lá, e não no computador local.
2. **O servidor usa um certificado HTTPS autoassinado.** Com a verificação padrão do `requests`, a chamada é recusada com `SSLError: CERTIFICATE_VERIFY_FAILED: self-signed certificate`. Por isso foi criada a variável `LLM_VERIFY_SSL`, que vale `true` por padrão e é definida como `false` apenas na plataforma.
3. **Sem terminal interativo:** a mensagem vem da variável `MENSAGEM`, e a saída aparece em **Logs**.
4. **O LLM liga junto com o container:** o portal indica "indisponível" até um container ser iniciado. O `ESPERA_LLM=120` faz o programa esperar antes de chamar o LLM.

## Resultado (Logs)

```
InsecureRequestWarning: Unverified HTTPS request is being made to host '<LLM interno>'. Adding certificate verification is strongly advised.
Categoria:     reclamacao
Urgência:      alta
Resumo:        Cliente relata falta de parte (braço) na peça recebida.
Ação sugerida: Aguardar envio do número do pedido para localizar a ocorrência e solicitar ao cliente fotos da embalagem e da peça para análise.
```

- **Classificação:** correta, e igual à da execução local.
- **Tempo de resposta:** cerca de 102 s entre o envio da requisição e a resposta. Foi a primeira chamada depois de iniciar, então o tempo inclui o carregamento do modelo.
- O aviso `InsecureRequestWarning` é esperado com `LLM_VERIFY_SSL=false` e foi mantido de propósito, para deixar visível que a verificação está desligada.

## Nível Intermediário na plataforma

A mesma imagem, montada com o código do nível Intermediário e com a mesma configuração do portal. A mensagem usada foi `Tem código de rastreio do meu pedido?`.

| Teste | Configuração alterada | Resultado nos Logs |
|---|---|---|
| Funcionamento | nenhuma | `status_pedido` / `media`, resposta cerca de 100 s depois do fim da espera (o LLM ainda estava terminando de ligar) |
| Certificado | `LLM_VERIFY_SSL=true` | `Erro: Não foi possível verificar o certificado HTTPS do servidor do LLM. Se for um servidor interno com certificado autoassinado, defina LLM_VERIFY_SSL=false.` |
| Sem espera, LLM já ligado | `ESPERA_LLM=0`, com o LLM disponível | `status_pedido` / `media` em **cerca de 2 s** |
| Sem espera, LLM desligado | `ESPERA_LLM=0`, com o LLM indisponível | `Erro: O servidor do LLM está com problemas (HTTP 502). Tente novamente em alguns minutos.` |
| Mensagem vazia | `MENSAGEM=` | `Erro: A mensagem está vazia. Informe o texto do cliente: [...] na plataforma Devel, na variável MENSAGEM.` |

### Constatações

- **Com o LLM ligado, a plataforma responde em cerca de 2 s**, contra 30 a 75 s no computador local sem GPU. Os cerca de 100 s das outras execuções correspondem ao tempo de o LLM ficar pronto.
- **Enquanto o LLM liga, a plataforma devolve HTTP 502** (Bad Gateway), e não uma falha de conexão. O programa trata esse caso como serviço indisponível. É isso que justifica o `ESPERA_LLM`.
- Todos os erros aparecem nos Logs como **uma única linha**, sem traceback.
