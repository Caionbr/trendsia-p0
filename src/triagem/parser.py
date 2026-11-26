"""Conversão e validação da resposta do LLM com pydantic."""

from typing import Literal

from pydantic import BaseModel, Field, ValidationError

from triagem.erros import RespostaInesperada


class Classificacao(BaseModel):
    """Formato esperado da resposta. O pydantic recusa qualquer coisa fora dele."""

    categoria: Literal[
        "encomenda",
        "orcamento",
        "frete_entrega",
        "status_pedido",
        "reclamacao",
        "saudacao",
        "outro",
    ]
    urgencia: Literal["alta", "media", "baixa"]
    resumo: str = Field(min_length=1)
    acao_sugerida: str = Field(min_length=1)


def interpretar_resposta(texto: str) -> Classificacao:
    """Converte o texto JSON do LLM em uma Classificacao validada."""
    try:
        return Classificacao.model_validate_json(texto)
    except ValidationError as erro:
        raise RespostaInesperada(
            f"O LLM respondeu fora do formato esperado ({_descrever(erro)}). Tente novamente."
        ) from erro


def _descrever(erro: ValidationError) -> str:
    """Resume o problema sem copiar o texto da resposta (que pode conter dados do cliente)."""
    problemas = erro.errors()
    if any(p["type"] == "json_invalid" for p in problemas):
        return "a resposta não é um JSON válido"
    campos = sorted({str(p["loc"][0]) for p in problemas if p["loc"]})
    return "campos com problema: " + ", ".join(campos)
