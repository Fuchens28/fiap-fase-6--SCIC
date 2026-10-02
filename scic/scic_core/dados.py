"""Leitura, limpeza e consulta da base operacional do SCIC."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from scic_core.catalogo import MODULOS

COLUNAS_ESPERADAS = [
    "ciclo",
    "modulo_id",
    "nome_modulo",
    "tipo_modulo",
    "latencia_observada_ms",
    "latencia_estimada_ms",
    "tensao_v",
    "corrente_a",
    "potencia_w",
    "qualidade_sinal",
    "carga_enlace",
    "status",
    "prioridade",
    "peso_prioridade",
    "codigo_sensor_dec",
    "mensagem_alerta",
]


class RepositorioDados:
    """Carrega o CSV da colônia e expõe consultas simples em DataFrame."""

    def __init__(self, caminho_csv: Path) -> None:
        self.caminho_csv = Path(caminho_csv)
        self.df: pd.DataFrame | None = None

    def carregar(self) -> pd.DataFrame:
        if not self.caminho_csv.exists():
            raise FileNotFoundError(
                f"Arquivo de dados nao encontrado: {self.caminho_csv}"
            )
        df = pd.read_csv(self.caminho_csv)
        faltando = [c for c in COLUNAS_ESPERADAS if c not in df.columns]
        if faltando:
            raise ValueError(f"Colunas ausentes no CSV: {faltando}")

        df = df.copy()
        df["modulo_id"] = df["modulo_id"].astype(str).str.upper().str.strip()
        df["status"] = df["status"].astype(str).str.lower().str.strip()
        numericas = [
            "ciclo",
            "latencia_observada_ms",
            "latencia_estimada_ms",
            "tensao_v",
            "corrente_a",
            "potencia_w",
            "qualidade_sinal",
            "carga_enlace",
            "peso_prioridade",
            "codigo_sensor_dec",
        ]
        for coluna in numericas:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        df = df.dropna(subset=["modulo_id", "latencia_observada_ms", "ciclo"])
        self.df = df.reset_index(drop=True)
        return self.df

    def exigir_carregado(self) -> pd.DataFrame:
        if self.df is None:
            raise RuntimeError("Carregue os dados antes de consultar (opcao 1).")
        return self.df

    def cadastrar_registro(self, registro: dict) -> pd.DataFrame:
        df = self.exigir_carregado()
        novo = pd.DataFrame([registro])
        self.df = pd.concat([df, novo], ignore_index=True)
        self.df.to_csv(self.caminho_csv, index=False)
        return self.df

    def consultar(self, modulo_id: str | None = None, status: str | None = None) -> pd.DataFrame:
        df = self.exigir_carregado()
        filtro = df
        if modulo_id:
            filtro = filtro[filtro["modulo_id"] == modulo_id.upper()]
        if status:
            filtro = filtro[filtro["status"] == status.lower()]
        return filtro

    def resumo_modulos(self) -> pd.DataFrame:
        df = self.exigir_carregado()
        agrupado = (
            df.groupby(["modulo_id", "nome_modulo", "tipo_modulo", "prioridade"], as_index=False)
            .agg(
                ciclos=("ciclo", "count"),
                latencia_media=("latencia_observada_ms", "mean"),
                latencia_max=("latencia_observada_ms", "max"),
                potencia_media=("potencia_w", "mean"),
                qualidade_media=("qualidade_sinal", "mean"),
            )
            .sort_values("modulo_id")
        )
        return agrupado

    def nomes_para_trie(self) -> list[str]:
        nomes = [info["nome"] for info in MODULOS.values()]
        ids = list(MODULOS.keys())
        return nomes + ids
