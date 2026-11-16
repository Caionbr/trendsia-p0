"""Triagem de mensagens de clientes com um LLM (nível Básico do P0).

Uso:
    python -m triagem "texto da mensagem"
    python -m triagem            (o programa pede a mensagem)
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv

PROMPT_SISTEMA = """Você faz a triagem de mensagens de clientes de uma pequena empresa de impressão 3D \
(action figures e peças sob encomenda). Classifique a mensagem do cliente.

Categorias (escolha exatamente uma):
- encomenda: o cliente quer fazer um pedido ou produzir uma peça.
- orcamento: pergunta sobre o preço de uma peça ou projeto.
- frete_entrega: dúvida sobre custo do frete, prazo ou área de entrega.
- reclamacao: produto quebrado, danificado, com defeito, faltando parte ou outro problema no pedido.
- saudacao: apenas um cumprimento, sem nenhum pedido.
- outro: nenhuma das anteriores (parcerias, elogios, spam).

Urgência (escolha exatamente uma):
- alta: peça quebrada, danificada ou outro problema com um pedido entregue.
- media: oportunidade de venda (encomenda, orçamento, frete ou entrega).
- baixa: não exige ação imediata (saudação, elogio, outros).

Se a mensagem tiver várias intenções, classifique pela intenção principal; a de maior urgência prevalece.
Nunca prometa reembolso: no máximo, sugira analisar o caso.

Responda somente com um objeto JSON, sem texto fora dele, neste formato:
{"categoria": "...", "urgencia": "...", "resumo": "uma frase curta", "acao_sugerida": "o que o atendente deve fazer"}"""


def carregar_config():
    """Lê a configuração do arquivo .env e devolve (url, modelo, timeout)."""
    load_dotenv()
    url = os.getenv("LLM_URL")
    modelo = os.getenv("LLM_MODEL")
    timeout = float(os.getenv("LLM_TIMEOUT", "120"))
    if not url or not modelo:
        sys.exit("Erro: defina LLM_URL e LLM_MODEL no arquivo .env (veja o .env.example).")
    return url.rstrip("/"), modelo, timeout


def ler_mensagem():
    """Pega a mensagem dos argumentos do terminal ou pede para a pessoa digitar."""
    if len(sys.argv) > 1:
        mensagem = " ".join(sys.argv[1:])
    else:
        mensagem = input("Mensagem do cliente: ")
    mensagem = mensagem.strip()
    if not mensagem:
        sys.exit("Erro: a mensagem está vazia.")
    return mensagem


def chamar_llm(url, modelo, timeout, mensagem):
    """Envia a mensagem para a API do Ollama e devolve o texto da resposta."""
    corpo = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": PROMPT_SISTEMA},
            {"role": "user", "content": mensagem},
        ],
        "stream": False,
        "format": "json",
        "think": False,
    }
    resposta = requests.post(f"{url}/api/chat", json=corpo, timeout=timeout)
    resposta.raise_for_status()
    return resposta.json()["message"]["content"]


def interpretar_resposta(texto):
    """Converte o texto JSON devolvido pelo LLM em um dicionário Python."""
    return json.loads(texto)


def mostrar_resultado(resultado):
    """Imprime a classificação de forma legível no terminal."""
    print(f"Categoria:     {resultado.get('categoria')}")
    print(f"Urgência:      {resultado.get('urgencia')}")
    print(f"Resumo:        {resultado.get('resumo')}")
    print(f"Ação sugerida: {resultado.get('acao_sugerida')}")


def main():
    url, modelo, timeout = carregar_config()
    mensagem = ler_mensagem()
    texto = chamar_llm(url, modelo, timeout, mensagem)
    resultado = interpretar_resposta(texto)
    mostrar_resultado(resultado)


if __name__ == "__main__":
    main()
