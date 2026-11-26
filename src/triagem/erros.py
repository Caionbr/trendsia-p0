"""Erros (exceções) próprios do programa de triagem.

Cada problema esperado vira uma exceção com uma mensagem clara em português.
Todas herdam de TriagemErro, então o __main__ consegue capturar qualquer uma
delas com um único "except TriagemErro".
"""


class TriagemErro(Exception):
    """Erro base: qualquer falha esperada do programa."""


class EntradaInvalida(TriagemErro):
    """A mensagem do cliente está vazia."""


class ConfiguracaoInvalida(TriagemErro):
    """Falta uma variável de configuração ou ela tem um valor inválido."""


class CredencialInvalida(TriagemErro):
    """O servidor do LLM recusou o acesso (HTTP 401 ou 403)."""


class LLMIndisponivel(TriagemErro):
    """Ninguém responde no endereço configurado, ou o servidor está com problema (HTTP 5xx)."""


class FalhaComunicacao(TriagemErro):
    """Outra falha ao falar com o LLM (certificado, endereço, modelo não encontrado)."""


class TempoEsgotado(TriagemErro):
    """O LLM não respondeu dentro de LLM_TIMEOUT segundos."""


class RespostaInesperada(TriagemErro):
    """O LLM respondeu, mas fora do formato esperado."""
