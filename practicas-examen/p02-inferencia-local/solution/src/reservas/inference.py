"""Inferencia: de un diccionario de datos a una prediccion."""
from reservas.data.features import preparar_fila
from reservas.model.cargador import cargar_modelo

UMBRAL_MEDIO = 0.3
UMBRAL_ALTO = 0.6


def clasificar_riesgo(probabilidad: float) -> str:
    """Devuelve "bajo" si p < 0.3, "medio" si p < 0.6 y "alto" en el resto."""
    if probabilidad < UMBRAL_MEDIO:
        return "bajo"
    if probabilidad < UMBRAL_ALTO:
        return "medio"
    return "alto"


def predecir(datos: dict) -> dict:
    """Devuelve {"probabilidad_cancelacion": float, "riesgo": str}."""
    fila = preparar_fila(datos)
    modelo = cargar_modelo()
    probabilidad = float(modelo.predict_proba(fila)[0][1])
    return {
        "probabilidad_cancelacion": round(probabilidad, 4),
        "riesgo": clasificar_riesgo(probabilidad),
    }
