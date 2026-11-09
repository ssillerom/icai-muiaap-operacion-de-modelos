"""Entrenamiento del modelo (HECHO). Uso: uv run entrenar"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from reservas.config import RUTA_DATOS, RUTA_MODELO, SEMILLA
from reservas.data.features import CATEGORICAS, NUMERICAS, VARIABLES

OBJETIVO = "cancelada"


def cargar_datos(ruta=RUTA_DATOS) -> pd.DataFrame:
    datos = pd.read_csv(ruta)
    faltan = [c for c in VARIABLES + [OBJETIVO] if c not in datos.columns]
    if faltan:
        raise ValueError(f"Faltan columnas en el dataset: {faltan}")
    return datos


def construir_modelo() -> Pipeline:
    preprocesado = ColumnTransformer(
        [
            ("num", StandardScaler(), NUMERICAS),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAS),
        ]
    )
    return Pipeline(
        [("preprocesado", preprocesado), ("clasificador", LogisticRegression(max_iter=1000))]
    )


def entrenar(ruta=RUTA_DATOS):
    """Entrena el modelo y devuelve (modelo, metricas)."""
    datos = cargar_datos(ruta)
    X = datos[VARIABLES]
    y = datos[OBJETIVO]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEMILLA, stratify=y
    )
    modelo = construir_modelo()
    modelo.fit(X_train, y_train)
    predicciones = modelo.predict(X_test)
    metricas = {
        "filas": len(datos),
        "accuracy": round(accuracy_score(y_test, predicciones), 4),
        "f1": round(f1_score(y_test, predicciones), 4),
    }
    return modelo, metricas


def guardar_modelo(modelo, ruta=RUTA_MODELO):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta)
    return ruta


def main():
    modelo, metricas = entrenar()
    ruta = guardar_modelo(modelo)
    print("Metricas:", metricas)
    print("Modelo guardado en", ruta)


if __name__ == "__main__":
    main()
