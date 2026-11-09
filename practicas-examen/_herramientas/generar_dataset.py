"""Genera el dataset sintetico de reservas de hotel (SOLO PROFESOR).

Uso (desde practicas-examen/):
    uv run --with pandas --with numpy python _herramientas/generar_dataset.py

Escribe reservas_hotel.csv en las carpetas problem/ que lo necesitan. Las
soluciones se guardan fuera del repositorio: copia alli el CSV si lo regeneras.
El dataset es sintetico: la relacion entre variables y cancelacion es inventada
y solo sirve para practicar operacion de modelos.
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEMILLA = 42
N_FILAS = 2000
RAIZ = Path(__file__).resolve().parent.parent

DESTINOS = [
    RAIZ / "p01-proyecto-uv" / "problem",
] + [
    RAIZ / practica / carpeta / "data" / "raw"
    for practica in [
        "p02-inferencia-local",
        "p03-contratos-pydantic",
        "p04-artefacto-manifiesto",
        "p05-streamlit-local",
        "p06-fastapi",
        "p07-errores-docs",
        "p08-api-key",
        "p09-streamlit-api",
    ]
    for carpeta in ["problem"]
]


def generar(n: int = N_FILAS, semilla: int = SEMILLA) -> pd.DataFrame:
    rng = np.random.default_rng(semilla)
    antelacion = rng.integers(0, 366, n)
    noches = rng.integers(1, 15, n)
    adultos = rng.integers(1, 5, n)
    ninos = np.minimum(rng.integers(0, 3, n), 6 - adultos)
    precio = np.round(rng.uniform(40, 400, n), 2)
    canal = rng.choice(["web", "agencia", "telefono"], n, p=[0.6, 0.3, 0.1])
    cancel_prev = rng.choice([0, 0, 0, 0, 1, 1, 2, 3], n)
    peticiones = rng.integers(0, 4, n)

    efecto_canal = np.select(
        [canal == "agencia", canal == "web"], [0.8, 0.3], default=-0.4
    )
    z = (
        -2.2
        + 0.008 * antelacion
        + 0.9 * cancel_prev
        - 0.5 * peticiones
        + 0.003 * precio
        - 0.05 * noches
        + 0.1 * ninos
        + efecto_canal
    )
    prob = 1 / (1 + np.exp(-z))
    cancelada = (rng.random(n) < prob).astype(int)

    return pd.DataFrame(
        {
            "antelacion_dias": antelacion,
            "noches": noches,
            "adultos": adultos,
            "ninos": ninos,
            "precio_noche": precio,
            "canal": canal,
            "cancelaciones_previas": cancel_prev,
            "peticiones_especiales": peticiones,
            "cancelada": cancelada,
        }
    )


if __name__ == "__main__":
    datos = generar()
    for destino in DESTINOS:
        destino.mkdir(parents=True, exist_ok=True)
        datos.to_csv(destino / "reservas_hotel.csv", index=False)
        print("Escrito", destino / "reservas_hotel.csv")
    print(datos.describe(include="all").T)
    print("Tasa de cancelacion:", round(datos["cancelada"].mean(), 3))
