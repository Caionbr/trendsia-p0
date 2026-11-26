"""Ponto de entrada: python -m triagem "mensagem do cliente".

Este arquivo só organiza o fluxo. Cada etapa fica no seu próprio módulo:
configuração → entrada → prompt → chamada ao LLM → validação → saída.
"""

import sys

from triagem.cliente_llm import chamar_llm
from triagem.config import carregar_config
from triagem.entrada import obter_mensagem
from triagem.erros import TriagemErro
from triagem.parser import Classificacao, interpretar_resposta
from triagem.prompt import montar_mensagens
from triagem.saida import mostrar_erro, mostrar_resultado


def executar(argumentos: list[str]) -> None:
    """Executa o fluxo completo de triagem de uma mensagem."""
    config = carregar_config()
    mensagem = obter_mensagem(argumentos)
    mensagens = montar_mensagens(mensagem)
    # O esquema JSON da Classificacao faz o Ollama gerar apenas respostas nesse formato
    texto = chamar_llm(config, mensagens, formato=Classificacao.model_json_schema())
    classificacao = interpretar_resposta(texto)
    mostrar_resultado(classificacao)


def main() -> None:
    try:
        executar(sys.argv[1:])
    except TriagemErro as erro:
        mostrar_erro(erro)
        sys.exit(1)
    except KeyboardInterrupt:
        mostrar_erro("execução interrompida pelo usuário.")
        sys.exit(130)


if __name__ == "__main__":
    main()
