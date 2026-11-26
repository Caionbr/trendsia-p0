"""Apresentação do resultado e dos erros no terminal."""

import sys

from triagem.parser import Classificacao


def formatar_resultado(classificacao: Classificacao) -> str:
    """Monta o texto do resultado (separado da impressão para facilitar os testes)."""
    return "\n".join(
        [
            f"Categoria:     {classificacao.categoria}",
            f"Urgência:      {classificacao.urgencia}",
            f"Resumo:        {classificacao.resumo}",
            f"Ação sugerida: {classificacao.acao_sugerida}",
        ]
    )


def mostrar_resultado(classificacao: Classificacao) -> None:
    print(formatar_resultado(classificacao))


def mostrar_erro(erro: object) -> None:
    """Mostra a mensagem de erro na saída de erros (stderr), sem o traceback técnico."""
    print(f"Erro: {erro}", file=sys.stderr)
