"""Dispositivos de E/S, bases numéricas e eletricidade básica."""

from __future__ import annotations


def converter_codigo(decimal: int) -> dict:
    return {
        "decimal": int(decimal),
        "binario": format(int(decimal), "b"),
        "hexadecimal": format(int(decimal), "X"),
        "hex_formatado": "0x" + format(int(decimal), "X"),
    }


def potencia_transmissor(tensao_v: float, corrente_a: float) -> dict:
    """Potência aproximada P = V * I e resistência equivalente R = V / I."""
    potencia = tensao_v * corrente_a
    resistencia = tensao_v / corrente_a if abs(corrente_a) > 1e-12 else float("inf")
    return {
        "tensao_v": tensao_v,
        "corrente_a": corrente_a,
        "potencia_w": potencia,
        "resistencia_ohm": resistencia,
    }


def texto_dispositivos() -> str:
    return """
Entrada (simulada no CSV, como se viesse de sensores):
  - medidores de latência do enlace de cada módulo;
  - sensores de tensão e corrente do transmissor;
  - teclado do operador no terminal do SCIC.

Saída:
  - terminal do Python (este menu);
  - relatório técnico e gráficos em graficos_ou_imagens/;
  - em um cenário real, um monitor no Centro de Controle.

Interfaces (apenas conceituais, sem hardware real):
  - rede local da colônia para telemetria;
  - USB / serial para bancada de manutenção;
  - rádio do enlace Terra-Marte para o módulo COM.

O código hexadecimal do sensor é o identificador que o barramento
entregaria à CPU; o SCIC converte para decimal e binário para auditoria.
""".strip()
