"""Obtenção e validação da mensagem do cliente."""

from triagem.erros import EntradaInvalida


def obter_mensagem(argumentos: list[str]) -> str:
    """Usa os argumentos do terminal; se não houver, pede a mensagem ao usuário."""
    if argumentos:
        mensagem = " ".join(argumentos)
    else:
        try:
            mensagem = input("Mensagem do cliente: ")
        except EOFError:
            # Sem terminal para digitar (ex.: dentro de um container): trata como vazia
            mensagem = ""
    return validar_mensagem(mensagem)


def validar_mensagem(mensagem: str) -> str:
    """Remove espaços das pontas e recusa mensagem vazia."""
    mensagem = mensagem.strip()
    if not mensagem:
        raise EntradaInvalida(
            "A mensagem está vazia. Informe o texto do cliente: no terminal, entre aspas "
            '(python -m triagem "texto"); na plataforma Devel, na variável MENSAGEM.'
        )
    return mensagem
