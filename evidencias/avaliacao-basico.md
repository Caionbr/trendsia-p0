# Avaliação do nível Básico: 12 exemplos e casos extras

- **Data:** 16/11/2026
- **Modelo:** `qwen3.5:9b-q4_K_M` (Ollama 0.40.16), rodando localmente na CPU (Windows, 20 GB de RAM)
- **Prompt:** versão 1, em `src/triagem/__main__.py` (`PROMPT_SISTEMA`), com `"format": "json"` e `"think": false`
- **Tempo de resposta (medido em 2 execuções):** 76 s na primeira chamada, que inclui carregar o modelo na memória, e 33 s com o modelo já carregado

## Conjunto de 12 exemplos (mensagens fictícias)

| # | Mensagem | Esperado | Obtido | Categoria | Urgência |
|---|---|---|---|---|---|
| 1 | Gostaria de encomendar uma action figure do meu personagem de RPG | encomenda / media | encomenda / media | ✅ | ✅ |
| 2 | quanto fica pra imprimir essa peça? te mando o arquivo stl | orcamento / media | orcamento / media | ✅ | ✅ |
| 3 | Quanto custa o frete pra Fortaleza? | frete_entrega / media | frete_entrega / media | ✅ | ✅ |
| 4 | Vcs entregam p todo o Brasil? | frete_entrega / media | frete_entrega / media | ✅ | ✅ |
| 5 | Boa noite! | saudacao / baixa | saudacao / baixa | ✅ | ✅ |
| 6 | O produto chegou quebrado, a base veio rachada 😡 | reclamacao / alta | reclamacao / alta | ✅ | ✅ |
| 7 | chegou faltando o braço do boneco | reclamacao / alta | reclamacao / alta | ✅ | ✅ |
| 8 | Bom dia! Queria saber o valor de um chaveiro personalizado | orcamento / media | orcamento / media | ✅ | ✅ |
| 9 | Oi, tudo bem? Meu pedido chegou todo amassado, como faço? | reclamacao / alta | reclamacao / alta | ✅ | ✅ |
| 10 | Faz quanto pra mandar pra Manaus? | frete_entrega / media | frete_entrega / media | ✅ | ✅ |
| 11 | Quero 10 miniaturas iguais pra lembrancinha de aniversário | encomenda / media | encomenda / media | ✅ | ✅ |
| 12 | Adorei o trabalho de vcs, parabéns! | outro / baixa | saudacao / baixa | ❌ | ✅ |

**Resultado:** categoria correta em 11 de 12 (92%) e urgência correta em 12 de 12 (100%).

## Casos extras (escritos para provocar erros)

| Mensagem | Obtido | Análise |
|---|---|---|
| Parabéns, meu produto chegou todo quebrado... | reclamacao / alta | Correto: o modelo entendeu a ironia. |
| Produto de ótima, qualidade! Porém faltou enviar a base. | reclamacao / alta | Classificação correta, mas a ação sugere "reembolso parcial", o que viola a regra de nunca sugerir reembolso diretamente. |
| Boa noite, ainda não recebi atualização do meu pedido | outro / media | Não existe categoria para "status do pedido" (lacuna da taxonomia). A combinação `outro` + `media` contraria o critério de urgência. |
| N gosteui do produto | reclamacao / alta | Discutível: é insatisfação, não um dano. |
| Eh bom | saudacao / baixa | Errado: é um comentário sobre o produto, não um cumprimento. |
| Ja vi melhor, pelo preco eh ok | orcamento / media | Errado, e o resumo inventa que "o cliente aprovou o preço". |

## Outras observações

- **Erros de português no texto gerado:** "prazos médicos", "acabe final", "complimentos", "defeituosidade", "ação personalizada" (no lugar de "action figure") e um `}` sobrando no fim de uma ação sugerida.
- **Vazamento da instrução:** em uma mensagem de orçamento, a ação sugerida incluiu "lembrando não prometer reembolso", repetindo uma regra do prompt sem que ela se aplicasse.
- O modelo acerta bem as mensagens diretas, mas erra comentários curtos, ambíguos ou com avaliação mista sobre o produto.

## Próximos ajustes possíveis (Etapa 3 / nível Intermediário)

- Decidir se haverá uma categoria para status ou atraso de pedido.
- Dizer de forma explícita no prompt que elogios e comentários sobre o produto são `outro`.
- Reforçar no prompt que a ação nunca menciona reembolso, só "análise do caso".
- Validar a resposta com pydantic, rejeitando combinações inválidas de categoria e urgência.
