"""Variables del modelo y preparacion de la entrada."""
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
# Orden exacto de columnas con el que se entreno el modelo
VARIABLES = NUMERICAS + CATEGORICAS


def validar_campos(datos: dict) -> None:
    """Lanza ValueError si faltan variables o sobran campos."""
    faltan = [v for v in VARIABLES if v not in datos]
    sobran = [c for c in datos if c not in VARIABLES]
    if faltan:
        raise ValueError(f"Faltan variables: {faltan}")
    if sobran:
        raise ValueError(f"Campos no reconocidos: {sobran}")


def preparar_fila(datos: dict) -> pd.DataFrame:
    """Devuelve un DataFrame de una fila con las columnas en el orden de VARIABLES."""
    validar_campos(datos)
    return pd.DataFrame([[datos[v] for v in VARIABLES]], columns=VARIABLES)
