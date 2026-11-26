# Avaliação do nível Intermediário: exemplos, casos difíceis e casos novos

- **Modelo:** `qwen3.5:9b-q4_K_M` no Ollama local, rodando na CPU
- **Mudanças em relação ao Básico:**
  - nova categoria `status_pedido` (urgência média);
  - `orcamento` passou para urgência alta;
  - prompt reescrito, com regras para elogios e comentários, para não inventar fatos e para nunca propor reembolso;
  - o pedido inclui o esquema JSON da resposta (campo `format`), e a resposta é validada com pydantic.
- **Tempo de resposta:** média de 44 s por mensagem (mínimo 28 s, máximo 75 s), com o modelo já carregado.

## Resultado geral

| Grupo | Casos | Categoria correta | Urgência correta |
|---|---|---|---|
| Conjunto de 12 exemplos | 12 | **12** (Básico: 11) | **12** (Básico: 12) |
| Casos difíceis do Básico | 6 | **5** (Básico: 3) | **6** (Básico: 5) |
| Casos novos (`status_pedido` e orçamento) | 3 | 3 | 3 |
| **Total** | **21** | **20 (95%)** | **21 (100%)** |

No Básico, a comparação de urgência dos exemplos usava os critérios antigos (orçamento como média). Aqui, os valores esperados seguem os critérios atuais.

## Conjunto de 12 exemplos

| # | Mensagem | Esperado | Obtido | ✓ |
|---|---|---|---|---|
| 1 | Gostaria de encomendar uma action figure do meu personagem de RPG | encomenda / media | encomenda / media | ✅ |
| 2 | quanto fica pra imprimir essa peça? te mando o arquivo stl | orcamento / alta | orcamento / alta | ✅ |
| 3 | Quanto custa o frete pra Fortaleza? | frete_entrega / media | frete_entrega / media | ✅ |
| 4 | Vcs entregam p todo o Brasil? | frete_entrega / media | frete_entrega / media | ✅ |
| 5 | Boa noite! | saudacao / baixa | saudacao / baixa | ✅ |
| 6 | O produto chegou quebrado, a base veio rachada 😡 | reclamacao / alta | reclamacao / alta | ✅ |
| 7 | chegou faltando o braço do boneco | reclamacao / alta | reclamacao / alta | ✅ |
| 8 | Bom dia! Queria saber o valor de um chaveiro personalizado | orcamento / alta | orcamento / alta | ✅ |
| 9 | Oi, tudo bem? Meu pedido chegou todo amassado, como faço? | reclamacao / alta | reclamacao / alta | ✅ |
| 10 | Faz quanto pra mandar pra Manaus? | frete_entrega / media | frete_entrega / media | ✅ |
| 11 | Quero 10 miniaturas iguais pra lembrancinha de aniversário | encomenda / media | encomenda / media | ✅ |
| 12 | Adorei o trabalho de vcs, parabéns! | outro / baixa | outro / baixa | ✅ (no Básico: saudacao) |

## Casos difíceis do Básico

| Mensagem | Esperado | Obtido | ✓ | Comentário |
|---|---|---|---|---|
| Parabéns, meu produto chegou todo quebrado... | reclamacao / alta | reclamacao / alta | ✅ | continua entendendo a ironia |
| Produto de ótima, qualidade! Porém faltou enviar a base. | reclamacao / alta | reclamacao / alta | ✅ | a ação não fala mais em "reembolso parcial": pede fotos e o número do pedido |
| Boa noite, ainda não recebi atualização do meu pedido | status_pedido / media | status_pedido / media | ✅ | antes caía em `outro` / media |
| N gosteui do produto | reclamacao / alta | reclamacao / alta | ✅ | insatisfação clara conta como reclamação |
| Eh bom | outro / baixa | saudacao / baixa | ❌ | continua confundido com cumprimento |
| Ja vi melhor, pelo preco eh ok | outro / baixa | outro / baixa | ✅ | antes era `orcamento` e o resumo inventava que o preço tinha sido aprovado |

## Casos novos

| Mensagem | Esperado | Obtido | ✓ |
|---|---|---|---|
| Meu pedido já foi enviado? Comprei semana passada | status_pedido / media | status_pedido / media | ✅ |
| Tem código de rastreio do meu pedido? | status_pedido / media | status_pedido / media | ✅ |
| Oi! Quanto sai uma miniatura de 10 cm pintada? | orcamento / alta | orcamento / alta | ✅ |

## Qualidade do texto gerado

- **Reembolso:** nenhuma das 21 ações sugeridas menciona reembolso, troca ou compensação. Nas reclamações, todas pedem fotos e o número do pedido para análise.
- **Invenção de fatos:** o caso "Ja vi melhor" não inventa mais que o cliente aprovou o preço.
- **Português:** bem melhor que no Básico, mas ainda com deslizes ("orçemento"; "Peça ao atendente que solicite…" numa ação que já é dirigida ao atendente).

## Limitação que permanece

Mensagens muito curtas e vagas ("Eh bom") ainda podem ser tomadas como cumprimento. O impacto é pequeno, porque as duas categorias (`saudacao` e `outro`) têm urgência baixa.
