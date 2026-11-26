"""Leitura e validação da configuração.

Os valores vêm de variáveis de ambiente. Localmente, elas são lidas do arquivo
.env; na plataforma Devel, são definidas no portal. Nenhum valor fica no código.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from triagem.erros import ConfiguracaoInvalida


@dataclass(frozen=True)
class Config:
    """Configuração já validada. frozen=True impede que ela seja alterada depois."""

    url: str
    modelo: str
    timeout: float
    verificar_ssl: bool
    api_key: str | None


def carregar_config() -> Config:
    """Lê as variáveis de ambiente, valida cada uma e devolve um Config."""
    load_dotenv()
    return Config(
        url=_ler_url(),
        modelo=_ler_obrigatoria("LLM_MODEL"),
        timeout=_ler_timeout(),
        verificar_ssl=_ler_verificar_ssl(),
        api_key=os.getenv("LLM_API_KEY", "").strip() or None,
    )


def _ler_obrigatoria(nome: str) -> str:
    """Devolve o valor de uma variável que não pode faltar."""
    valor = os.getenv(nome, "").strip()
    if not valor:
        raise ConfiguracaoInvalida(
            f"A variável {nome} não está definida. "
            "Copie o .env.example para .env e preencha os valores."
        )
    return valor


def _ler_url() -> str:
    url = _ler_obrigatoria("LLM_URL").rstrip("/")
    if not url.startswith(("http://", "https://")):
        raise ConfiguracaoInvalida("LLM_URL deve começar com http:// ou https://.")
    return url


def _ler_timeout() -> float:
    texto = os.getenv("LLM_TIMEOUT", "300").strip()
    try:
        timeout = float(texto)
    except ValueError:
        timeout = 0
    if timeout <= 0:
        raise ConfiguracaoInvalida("LLM_TIMEOUT deve ser um número de segundos maior que zero (ex.: 300).")
    return timeout


def _ler_verificar_ssl() -> bool:
    texto = os.getenv("LLM_VERIFY_SSL", "true").strip().lower()
    if texto not in ("true", "false"):
        raise ConfiguracaoInvalida("LLM_VERIFY_SSL deve ser true ou false.")
    return texto == "true"
