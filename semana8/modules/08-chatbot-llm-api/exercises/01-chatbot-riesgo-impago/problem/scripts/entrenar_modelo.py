# Genera datos sinteticos de solicitudes de prestamo y entrena el modelo.
# Uso: python entrenar_modelo.py   (crea models/modelo_impago.joblib)
import os
import random

import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Orden fijo de las variables que espera el modelo
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]


def generar_datos(n=3000, semilla=7):
    azar = random.Random(semilla)
    filas = []
    etiquetas = []
    for _ in range(n):
        edad = azar.randint(18, 75)
        ingresos = azar.randint(900, 6000)
        importe = azar.randint(1000, 40000)
        plazo = azar.choice([12, 24, 36, 48, 60, 72])
        antiguedad = azar.randint(0, min(40, edad - 18))
        impagos = azar.choice([0, 0, 0, 0, 1, 1, 2, 3])
        carga = (importe / plazo) / ingresos
        z = -3.0 + 7.0 * carga + 0.8 * impagos - 0.04 * antiguedad
        prob = 1 / (1 + np.exp(-z))
        filas.append([edad, ingresos, importe, plazo, antiguedad, impagos])
        etiquetas.append(1 if azar.random() < prob else 0)
    return np.array(filas), np.array(etiquetas)


if __name__ == "__main__":
    X, y = generar_datos()
    modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
    modelo.fit(X, y)
    os.makedirs("models", exist_ok=True)
    joblib.dump(modelo, "models/modelo_impago.joblib")
    print("Modelo guardado en models/modelo_impago.joblib")
    print("Variables, en este orden:", VARIABLES)
