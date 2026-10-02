"""Arquivo principal do Sistema de Comunicação Interplanetária da Colônia (SCIC).

Ponto de entrada pedido no enunciado da Fase 6.

Execucao:
    python codigo_fonte.py
"""

import sys

from scic_core.aplicacao import AplicacaoSCIC


def main() -> None:
    app = AplicacaoSCIC()
    if "--demo" in sys.argv:
        app.carregar_dados()
        app.demonstracao_completa()
        return
    app.executar()


if __name__ == "__main__":
    main()
