"""Comunicação com o LLM (servidor Ollama) pela API REST /api/chat.

Este é o único módulo que faz chamadas de rede. Cada falha técnica do requests
é traduzida para um erro do programa, com uma mensagem clara.
"""

import requests

from triagem.config import Config
from triagem.erros import (
    CredencialInvalida,
    FalhaComunicacao,
    LLMIndisponivel,
    RespostaInesperada,
    TempoEsgotado,
)


def chamar_llm(config: Config, mensagens: list[dict], formato: dict | str = "json") -> str:
    """Envia as mensagens ao LLM e devolve o texto da resposta (o conteúdo gerado pelo modelo)."""
    corpo = {
        "model": config.modelo,
        "messages": mensagens,
        "stream": False,
        "format": formato,  # pede a saída em JSON (ou no formato do esquema informado)
        "think": False,  # desliga o "raciocínio" visível do modelo
    }
    cabecalhos = {}
    if config.api_key:
        cabecalhos["Authorization"] = f"Bearer {config.api_key}"

    try:
        resposta = requests.post(
            f"{config.url}/api/chat",
            json=corpo,
            headers=cabecalhos,
            timeout=config.timeout,
            verify=config.verificar_ssl,
        )
    # A ordem importa: SSLError é um tipo de ConnectionError, então precisa vir antes
    except requests.exceptions.SSLError as erro:
        raise FalhaComunicacao(
            "Não foi possível verificar o certificado HTTPS do servidor do LLM. Se for um servidor "
            "interno com certificado autoassinado, defina LLM_VERIFY_SSL=false."
        ) from erro
    except requests.exceptions.ConnectionError as erro:
        raise LLMIndisponivel(
            "Não foi possível conectar ao LLM. Verifique se o Ollama está em execução "
            "e se LLM_URL está correto."
        ) from erro
    except requests.exceptions.Timeout as erro:
        raise TempoEsgotado(
            f"O LLM não respondeu dentro do limite de {config.timeout:g} s. "
            "Tente de novo ou aumente LLM_TIMEOUT."
        ) from erro
    except requests.exceptions.RequestException as erro:
        raise FalhaComunicacao("Falha na comunicação com o LLM. Verifique o valor de LLM_URL.") from erro

    verificar_status(resposta.status_code)

    try:
        return resposta.json()["message"]["content"]
    except (ValueError, KeyError, TypeError) as erro:
        raise RespostaInesperada(
            "O servidor respondeu num formato inesperado (não parece uma resposta do Ollama)."
        ) from erro


def verificar_status(codigo: int) -> None:
    """Traduz o código de status HTTP em um erro do programa, quando não for 200 (sucesso)."""
    if codigo == 200:
        return
    if codigo in (401, 403):
        raise CredencialInvalida(
            f"O servidor do LLM recusou o acesso (HTTP {codigo}). Verifique a chave em LLM_API_KEY."
        )
    if codigo == 404:
        raise FalhaComunicacao(
            "O servidor não encontrou o modelo ou o endereço (HTTP 404). "
            "Confira LLM_MODEL (o modelo precisa aparecer em 'ollama list') e LLM_URL."
        )
    if codigo >= 500:
        raise LLMIndisponivel(
            f"O servidor do LLM está com problemas (HTTP {codigo}). Tente novamente em alguns minutos."
        )
    raise FalhaComunicacao(f"O servidor do LLM respondeu com um erro inesperado (HTTP {codigo}).")
