import joblib

from app.config import MODEL_PATH
from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada

# Orden en el que el modelo espera las variables
VARIABLES = [
    "edad",
    "ingresos_mensuales",
    "importe_prestamo",
    "plazo_meses",
    "antiguedad_laboral_anios",
    "impagos_previos",
]

UMBRAL_APROBAR = 0.2
UMBRAL_REVISAR = 0.5

# Se carga una sola vez, al importar el modulo (no en cada peticion)
MODELO = joblib.load(MODEL_PATH)


def decidir(probabilidad: float) -> str:
    """Traduce la probabilidad de impago en una decision de negocio."""
    if probabilidad < UMBRAL_APROBAR:
        return "aprobar"
    if probabilidad < UMBRAL_REVISAR:
        return "revisar"
    return "rechazar"


def predecir(entrada: PrestamoEntrada) -> PrediccionSalida:
    """Ejecuta el modelo con una entrada ya validada y devuelve la salida validada."""
    fila = [getattr(entrada, variable) for variable in VARIABLES]
    probabilidad = float(MODELO.predict_proba([fila])[0][1])
    return PrediccionSalida(probabilidad_impago=probabilidad, decision=decidir(probabilidad))
