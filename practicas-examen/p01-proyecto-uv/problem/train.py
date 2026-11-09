"""Prototipo de entrenamiento del modelo de cancelacion de reservas.

Viene de un notebook. Funciona si lo ejecutas desde la carpeta donde esta el
CSV, pero todavia no es un proyecto: no tiene entorno, ni dependencias
declaradas, ni rutas fiables, ni resultados reproducibles.
"""
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERICAS = [
    "antelacion_dias",
    "noches",
    "adultos",
    "ninos",
    "precio_noche",
    "cancelaciones_previas",
    "peticiones_especiales",
]
CATEGORICAS = ["canal"]
VARIABLES = NUMERICAS + CATEGORICAS
OBJETIVO = "cancelada"

# TODO 1 (rutas): estas rutas dependen de la carpeta desde la que ejecutes el
#   script. Define RAIZ como la carpeta raiz del proyecto a partir de __file__
#   (investiga pathlib.Path(__file__).resolve().parents) y construye:
#     RUTA_DATOS  -> RAIZ / data / raw / reservas_hotel.csv
#     RUTA_MODELO -> RAIZ / models / modelo.joblib
#   Comprobacion: tests/test_train.py::test_rutas_relativas_a_la_raiz
RUTA_DATOS = "reservas_hotel.csv"
RUTA_MODELO = "modelo.joblib"

# TODO 2 (reproducibilidad): sin semilla, cada entrenamiento da una metrica
#   distinta. Fija SEMILLA a un entero y usala en train_test_split.
#   Comprobacion: tests/test_train.py::test_entrenamiento_reproducible
SEMILLA = None


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
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
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
    # TODO 3: crea la carpeta de destino si no existe (Path.mkdir con parents
    #   y exist_ok) antes de guardar.
    #   Comprobacion: tests/test_train.py::test_guardar_modelo
    joblib.dump(modelo, ruta)
    return ruta


def main():
    modelo, metricas = entrenar()
    ruta = guardar_modelo(modelo)
    print("Metricas:", metricas)
    print("Modelo guardado en", ruta)


if __name__ == "__main__":
    main()
