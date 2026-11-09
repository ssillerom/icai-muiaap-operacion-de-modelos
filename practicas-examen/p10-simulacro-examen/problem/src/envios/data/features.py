"""Variables del modelo y preparacion de la fila (HECHO)."""
import pandas as pd

NUMERICAS = ["distancia_km", "peso_kg", "dias_prometidos", "envios_en_cola", "es_internacional"]
CATEGORICAS = ["transportista"]
# Orden exacto de columnas con el que se entreno el modelo
VARIABLES = NUMERICAS + CATEGORICAS


def preparar_fila(datos: dict) -> pd.DataFrame:
    """DataFrame de una fila con las columnas en el orden de VARIABLES."""
    return pd.DataFrame([[datos[v] for v in VARIABLES]], columns=VARIABLES)
