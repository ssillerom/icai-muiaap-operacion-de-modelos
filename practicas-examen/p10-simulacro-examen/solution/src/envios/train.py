"""Entrenamiento del modelo con datos SINTETICOS (HECHO). Uso: uv run entrenar

Guarda en RUTA_MODELO un unico joblib con un diccionario (payload):
    {"modelo": Pipeline, "variables": [...], "version": "1.0.0"}
"""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from envios.config import RUTA_MODELO, SEMILLA, VERSION_MODELO
from envios.data.features import CATEGORICAS, NUMERICAS, VARIABLES


def generar_datos(n: int = 3000, semilla: int = SEMILLA) -> tuple[pd.DataFrame, np.ndarray]:
    """Envios inventados: la relacion con el retraso es ficticia."""
    rng = np.random.default_rng(semilla)
    internacional = rng.random(n) < 0.3
    distancia = np.where(internacional, rng.uniform(300, 5000, n), rng.uniform(1, 1500, n))
    peso = rng.uniform(0.1, 70, n)
    dias = rng.integers(1, 16, n)
    cola = rng.integers(0, 1001, n)
    transportista = rng.choice(["rapido", "estandar", "economico"], n, p=[0.3, 0.5, 0.2])
    efecto = np.select([transportista == "rapido", transportista == "economico"], [-0.8, 0.8], 0.0)
    z = (
        0.3
        + 0.0005 * distancia
        + 0.02 * peso
        - 0.3 * dias
        + 0.002 * cola
        + 0.6 * internacional
        + efecto
    )
    retraso = (rng.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    datos = pd.DataFrame(
        {
            "distancia_km": distancia.round(1),
            "peso_kg": peso.round(2),
            "dias_prometidos": dias,
            "envios_en_cola": cola,
            "es_internacional": internacional,
            "transportista": transportista,
        }
    )
    return datos[VARIABLES], retraso


def entrenar():
    X, y = generar_datos()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA, stratify=y
    )
    modelo = Pipeline(
        [
            (
                "preprocesado",
                ColumnTransformer(
                    [
                        ("num", StandardScaler(), NUMERICAS),
                        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
                    ]
                ),
            ),
            ("clasificador", LogisticRegression(max_iter=1000)),
        ]
    )
    modelo.fit(X_train, y_train)
    return modelo, {"f1": round(f1_score(y_test, modelo.predict(X_test)), 4)}


def guardar(modelo, ruta=RUTA_MODELO) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"modelo": modelo, "variables": VARIABLES, "version": VERSION_MODELO}, ruta)
    return ruta


def main():
    modelo, metricas = entrenar()
    print("Metricas:", metricas)
    print("Modelo guardado en", guardar(modelo))


if __name__ == "__main__":
    main()
