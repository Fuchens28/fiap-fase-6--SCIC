"""Gera a base simulada dados_aurora_siger.csv (reprodutível)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from scic_core.catalogo import MODULOS

MENSAGENS = {
    "ativo": "Enlace nominal",
    "manutencao": "Janela de manutencao preventiva",
    "alerta": "Latencia acima do envelope operacional",
}


def gerar(caminho: Path, ciclos: int = 12, semente: int = 26) -> pd.DataFrame:
    rng = np.random.default_rng(semente)
    linhas = []
    for ciclo in range(1, ciclos + 1):
        for codigo, info in MODULOS.items():
            carga = float(np.clip(rng.normal(45, 18), 5, 98))
            qualidade = float(np.clip(rng.normal(82, 12), 35, 99))
            ruido_v = rng.normal(0, 0.15)
            ruido_i = rng.normal(0, 0.008)
            tensao = max(info["tensao_nominal_v"] + ruido_v, 5.0)
            corrente = max(info["corrente_nominal_a"] + ruido_i, 0.05)
            potencia = tensao * corrente

            latencia = (
                info["latencia_base_ms"]
                + 0.38 * carga
                + 0.22 * (100 - qualidade)
                + 0.08 * potencia
                + rng.normal(0, 2.2)
            )
            # Alguns picos para RMSE > MAE e alertas reais
            if rng.random() < 0.08:
                latencia += rng.uniform(18, 42)

            estimada = (
                info["latencia_base_ms"]
                + 0.30 * carga
                + 0.10 * (100 - qualidade)
            )
            if latencia > estimada * 1.28 or qualidade < 55:
                status = "alerta"
            elif rng.random() < 0.07:
                status = "manutencao"
            else:
                status = "ativo"

            linhas.append(
                {
                    "ciclo": ciclo,
                    "modulo_id": codigo,
                    "nome_modulo": info["nome"],
                    "tipo_modulo": info["tipo"],
                    "latencia_observada_ms": round(float(latencia), 3),
                    "latencia_estimada_ms": round(float(estimada), 3),
                    "tensao_v": round(float(tensao), 4),
                    "corrente_a": round(float(corrente), 4),
                    "potencia_w": round(float(potencia), 4),
                    "qualidade_sinal": round(float(qualidade), 2),
                    "carga_enlace": round(float(carga), 2),
                    "status": status,
                    "prioridade": info["prioridade"],
                    "peso_prioridade": info["peso_prioridade"],
                    "codigo_sensor_dec": info["codigo_sensor"],
                    "mensagem_alerta": MENSAGENS[status],
                }
            )
    df = pd.DataFrame(linhas)
    df.to_csv(caminho, index=False)
    return df


if __name__ == "__main__":
    destino = Path(__file__).resolve().parent.parent / "dados_aurora_siger.csv"
    tabela = gerar(destino)
    print(f"Gerado {len(tabela)} registros em {destino}")
