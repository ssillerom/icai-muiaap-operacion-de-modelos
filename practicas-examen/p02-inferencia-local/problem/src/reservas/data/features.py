"""Variables del modelo y preparacion de la entrada (TU)."""
import pandas as pd

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
# Orden exacto de columnas con el que se entreno el modelo (HECHO, lo usa train.py)
VARIABLES = NUMERICAS + CATEGORICAS


def validar_campos(datos: dict) -> None:
    """Lanza ValueError si faltan variables o sobran campos."""
    # TODO: calcula que variables de VARIABLES no estan en `datos` y que claves
    #   de `datos` no estan en VARIABLES. Si hay alguna, lanza ValueError con un
    #   mensaje que incluya sus nombres (el usuario tiene que saber que corregir).
    #   Comprobacion: tests/test_features.py::test_validar_campos_*
    raise NotImplementedError("TODO: validar_campos")


def preparar_fila(datos: dict) -> pd.DataFrame:
    """Devuelve un DataFrame de una fila con las columnas en el orden de VARIABLES."""
    # TODO: valida los campos y construye un pd.DataFrame de UNA fila con
    #   columns=VARIABLES. El modelo se entreno con ese orden: un diccionario
    #   puede llegar desordenado y no debe importar.
    #   Comprobacion: tests/test_features.py::test_preparar_fila_*
    raise NotImplementedError("TODO: preparar_fila")
