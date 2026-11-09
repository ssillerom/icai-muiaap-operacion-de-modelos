"""Variables del modelo y preparacion de la entrada (HECHO)."""
import pandas as pd

from reservas.schemas import ReservaEntrada

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


def preparar_fila(entrada: ReservaEntrada) -> pd.DataFrame:
    """Devuelve un DataFrame de una fila con las columnas en el orden de VARIABLES.

    Ya no hace falta validar_campos(): si `entrada` existe, Pydantic ha
    comprobado que estan todos los campos, que no sobra ninguno y que los
    valores son correctos.
    """
    datos = entrada.model_dump()
    return pd.DataFrame([[datos[v] for v in VARIABLES]], columns=VARIABLES)
