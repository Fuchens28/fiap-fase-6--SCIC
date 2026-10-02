"""Modelo linear de previsão de latência e métricas de performance."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split


FEATURES = [
    "carga_enlace",
    "qualidade_sinal",
    "potencia_w",
    "peso_prioridade",
    "tensao_v",
]


@dataclass
class ResultadoModelo:
    mae: float
    mse: float
    rmse: float
    r2: float
    aic: float
    bic: float
    n_treino: int
    n_teste: int
    coeficientes: dict
    intercepto: float
    y_teste: np.ndarray
    y_pred: np.ndarray
    melhor_alpha: float | None
    interpretacao: str


def _aic_bic(n: int, mse: float, k: int) -> tuple[float, float]:
    mse_seguro = max(mse, 1e-12)
    aic = n * np.log(mse_seguro) + 2 * k
    bic = n * np.log(mse_seguro) + k * np.log(n)
    return float(aic), float(bic)


def _interpretar(mae: float, rmse: float, r2: float) -> str:
    razao = rmse / mae if mae > 1e-9 else float("inf")
    partes = [
        f"MAE = {mae:.3f} ms: em média, a previsão erra {mae:.2f} ms.",
        f"RMSE = {rmse:.3f} ms: na mesma unidade da latência, mas penaliza erros grandes.",
        f"R² = {r2:.3f}: fração da variação da latência explicada pelo modelo.",
    ]
    if r2 >= 0.85:
        partes.append(
            "R² alto não significa modelo perfeito: ele só diz que o ajuste "
            "explica bem a variação do conjunto de teste."
        )
    if razao > 1.4:
        partes.append(
            "RMSE bem maior que o MAE indica alguns registros com erro "
            "desproporcional (picos de latência), não um erro uniforme."
        )
    else:
        partes.append("MAE e RMSE próximos sugerem erros relativamente homogêneos.")
    partes.append("Um único número não basta: as quatro métricas devem ser lidas juntas.")
    return " ".join(partes)


def treinar_modelo(df: pd.DataFrame, random_state: int = 42) -> ResultadoModelo:
    dados = df.dropna(subset=FEATURES + ["latencia_observada_ms"]).copy()
    x = dados[FEATURES]
    y = dados["latencia_observada_ms"]

    x_treino, x_teste, y_treino, y_teste = train_test_split(
        x, y, test_size=0.30, random_state=random_state
    )

    linear = LinearRegression()
    linear.fit(x_treino, y_treino)
    pred_linear = linear.predict(x_teste)

    busca = GridSearchCV(
        Ridge(random_state=random_state),
        param_grid={"alpha": [0.01, 0.1, 1.0, 10.0]},
        scoring="neg_mean_squared_error",
        cv=3,
    )
    busca.fit(x_treino, y_treino)
    pred_ridge = busca.best_estimator_.predict(x_teste)

    mse_linear = mean_squared_error(y_teste, pred_linear)
    mse_ridge = mean_squared_error(y_teste, pred_ridge)
    usar_ridge = mse_ridge < mse_linear
    modelo = busca.best_estimator_ if usar_ridge else linear
    y_pred = pred_ridge if usar_ridge else pred_linear

    mae = float(mean_absolute_error(y_teste, y_pred))
    mse = float(mean_squared_error(y_teste, y_pred))
    rmse = float(np.sqrt(mse))
    r2 = float(r2_score(y_teste, y_pred))
    k = len(FEATURES) + 1
    aic, bic = _aic_bic(len(y_teste), mse, k)

    coeficientes = {
        nome: float(valor) for nome, valor in zip(FEATURES, modelo.coef_)
    }

    return ResultadoModelo(
        mae=mae,
        mse=mse,
        rmse=rmse,
        r2=r2,
        aic=aic,
        bic=bic,
        n_treino=len(y_treino),
        n_teste=len(y_teste),
        coeficientes=coeficientes,
        intercepto=float(modelo.intercept_),
        y_teste=np.asarray(y_teste, dtype=float),
        y_pred=np.asarray(y_pred, dtype=float),
        melhor_alpha=float(busca.best_params_["alpha"]) if usar_ridge else None,
        interpretacao=_interpretar(mae, rmse, r2),
    )
