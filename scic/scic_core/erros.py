"""Indicadores de comunicação, erros numéricos e simulação de Euler."""

from __future__ import annotations

import numpy as np
import pandas as pd


LIMITE_ERRO_RELATIVO_ACEITAVEL = 0.12
LIMITE_ERRO_RELATIVO_CRITICO = 0.25


def erro_absoluto(observado: np.ndarray, estimado: np.ndarray) -> np.ndarray:
    """|valor observado - valor estimado|."""
    return np.abs(observado - estimado)


def erro_relativo(observado: np.ndarray, estimado: np.ndarray) -> np.ndarray:
    """Erro absoluto dividido pelo valor de referência (latência observada).

    Quando o observado é zero, devolve NaN para evitar divisão inválida.
    """
    abs_err = erro_absoluto(observado, estimado)
    referencia = np.where(np.abs(observado) > 1e-12, observado, np.nan)
    return abs_err / np.abs(referencia)


def classificar_erro(relativo: float) -> str:
    if np.isnan(relativo):
        return "indefinido"
    if relativo <= LIMITE_ERRO_RELATIVO_ACEITAVEL:
        return "aceitavel"
    if relativo <= LIMITE_ERRO_RELATIVO_CRITICO:
        return "atencao"
    return "preocupante"


def analisar_erros(df: pd.DataFrame) -> pd.DataFrame:
    saida = df.copy()
    obs = saida["latencia_observada_ms"].to_numpy(dtype=float)
    est = saida["latencia_estimada_ms"].to_numpy(dtype=float)
    saida["erro_absoluto_ms"] = erro_absoluto(obs, est)
    saida["erro_relativo"] = erro_relativo(obs, est)
    saida["classificacao_erro"] = [classificar_erro(v) for v in saida["erro_relativo"]]
    return saida


def indicadores_comunicacao(df: pd.DataFrame) -> dict:
    erros = analisar_erros(df)
    potencia_calc = df["tensao_v"] * df["corrente_a"]
    diferenca_potencia = np.abs(df["potencia_w"] - potencia_calc)

    return {
        "n_registros": int(len(df)),
        "latencia_media_ms": float(df["latencia_observada_ms"].mean()),
        "latencia_mediana_ms": float(df["latencia_observada_ms"].median()),
        "potencia_media_w": float(df["potencia_w"].mean()),
        "qualidade_media": float(df["qualidade_sinal"].mean()),
        "erro_abs_medio_ms": float(erros["erro_absoluto_ms"].mean()),
        "erro_rel_medio": float(erros["erro_relativo"].mean()),
        "registros_preocupantes": int((erros["classificacao_erro"] == "preocupante").sum()),
        "registros_em_alerta": int((df["status"] == "alerta").sum()),
        "max_dif_potencia_w": float(diferenca_potencia.max()),
        "erros": erros,
    }


def euler_latencia(
    latencia_inicial: float,
    latencia_equilibrio: float,
    passos: int = 8,
    h: float = 1.0,
    k: float = 0.35,
) -> list[float]:
    """Simula a evolução da latência pelo método de Euler.

    Modelo simples: dL/dt = -k * (L - L_eq)
    Aproximação: L_{n+1} = L_n + h * f(L_n)
    """
    valores = [float(latencia_inicial)]
    atual = float(latencia_inicial)
    for _ in range(passos):
        derivada = -k * (atual - latencia_equilibrio)
        atual = atual + h * derivada
        valores.append(float(atual))
    return valores


def nota_ponto_flutuante() -> str:
    return (
        "O computador representa números reais em ponto flutuante, então "
        "0.1 + 0.2 pode não ser exatamente 0.3. No SCIC isso aparece em "
        "potências calculadas (P = V * I) e em erros relativos: diferenças "
        "da ordem de 1e-12 não são falha operacional, são arredondamento."
    )
