"""SCIC — Sistema de Comunicação Interplanetária da Colônia.

Protótipo acadêmico da Fase 6 da Aurora Siger (FIAP).
"""

__all__ = ["AplicacaoSCIC"]


def __getattr__(name: str):
    if name == "AplicacaoSCIC":
        from scic_core.aplicacao import AplicacaoSCIC

        return AplicacaoSCIC
    raise AttributeError(name)
