"""Inferencia: de un diccionario de datos a una prediccion (TU)."""
from reservas.data.features import preparar_fila
from reservas.model.cargador import cargar_modelo

UMBRAL_MEDIO = 0.3
UMBRAL_ALTO = 0.6


def clasificar_riesgo(probabilidad: float) -> str:
    """Devuelve "bajo" si p < 0.3, "medio" si p < 0.6 y "alto" en el resto."""
    # TODO: usa las constantes UMBRAL_MEDIO y UMBRAL_ALTO (no escribas los
    #   numeros a mano). Fijate en los limites: 0.3 ya es "medio".
    #   Comprobacion: tests/test_inference.py::test_clasificar_riesgo
    raise NotImplementedError("TODO: clasificar_riesgo")


def predecir(datos: dict) -> dict:
    """Devuelve {"probabilidad_cancelacion": float, "riesgo": str}."""
    # TODO: prepara la fila, carga el modelo y calcula la probabilidad de la
    #   clase 1 (cancelada) con predict_proba(fila)[0][1]. Conviertela a float
    #   de Python, redondea a 4 decimales y anade el riesgo.
    #   Comprobacion: tests/test_inference.py::test_predecir_*
    raise NotImplementedError("TODO: predecir")
