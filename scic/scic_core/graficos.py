"""Gráficos gerados durante a execução do SCIC."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from scic_core.modelo import ResultadoModelo


def garantir_pasta(pasta: Path) -> Path:
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def grafico_latencia_por_modulo(df: pd.DataFrame, pasta: Path) -> Path:
    destino = pasta / "latencia_por_modulo.png"
    media = (
        df.groupby("modulo_id")["latencia_observada_ms"].mean().sort_values()
    )
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(media.index, media.values, color="#c45c26")
    ax.set_title("Latência média observada por módulo")
    ax.set_xlabel("Módulo")
    ax.set_ylabel("ms")
    fig.tight_layout()
    fig.savefig(destino, dpi=120)
    plt.close(fig)
    return destino


def grafico_erros(df_erros: pd.DataFrame, pasta: Path) -> Path:
    destino = pasta / "erros_latencia.png"
    amostra = df_erros.tail(40)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(range(len(amostra)), amostra["latencia_observada_ms"], label="Observada")
    ax.plot(range(len(amostra)), amostra["latencia_estimada_ms"], label="Estimada (baseline)")
    ax.set_title("Latência observada x estimada (últimos registros)")
    ax.set_xlabel("Registro")
    ax.set_ylabel("ms")
    ax.legend()
    fig.tight_layout()
    fig.savefig(destino, dpi=120)
    plt.close(fig)
    return destino


def grafico_modelo(resultado: ResultadoModelo, pasta: Path) -> Path:
    destino = pasta / "modelo_observado_previsto.png"
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(resultado.y_teste, resultado.y_pred, alpha=0.75, color="#c45c26")
    limite = [
        min(resultado.y_teste.min(), resultado.y_pred.min()),
        max(resultado.y_teste.max(), resultado.y_pred.max()),
    ]
    ax.plot(limite, limite, color="#333333", linestyle="--")
    ax.set_title("Modelo: latência observada x prevista")
    ax.set_xlabel("Observada (ms)")
    ax.set_ylabel("Prevista (ms)")
    fig.tight_layout()
    fig.savefig(destino, dpi=120)
    plt.close(fig)
    return destino


def grafico_euler(valores: list[float], pasta: Path) -> Path:
    destino = pasta / "euler_latencia.png"
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(range(len(valores)), valores, marker="o", color="#2f6f4e")
    ax.set_title("Simulação de Euler da latência de um enlace")
    ax.set_xlabel("Passo")
    ax.set_ylabel("Latência (ms)")
    fig.tight_layout()
    fig.savefig(destino, dpi=120)
    plt.close(fig)
    return destino
