"""Inferencia: de una ReservaEntrada validada a una PrediccionSalida validada (TU)."""
from reservas.data.features import preparar_fila
from reservas.model.cargador import cargar_modelo
from reservas.schemas import PrediccionSalida, ReservaEntrada

UMBRAL_MEDIO = 0.3
UMBRAL_ALTO = 0.6


def clasificar_riesgo(probabilidad: float) -> str:
    """Devuelve "bajo" si p < 0.3, "medio" si p < 0.6 y "alto" en el resto."""
    if probabilidad < UMBRAL_MEDIO:
        return "bajo"
    if probabilidad < UMBRAL_ALTO:
        return "medio"
    return "alto"


def predecir(entrada: ReservaEntrada) -> dict:
    """Calcula la probabilidad de cancelacion y el riesgo de una reserva."""
    # TODO 6: esta version es la de la practica 2 y devuelve un dict.
    #   Cambiala para que devuelva un PrediccionSalida (actualiza tambien la
    #   anotacion de tipo). Asi la salida tambien queda validada.
    #   Comprobacion: test_inference.py::test_predecir_devuelve_una_prediccion_salida
    fila = preparar_fila(entrada)
    modelo = cargar_modelo()
    probabilidad = float(modelo.predict_proba(fila)[0][1])
    return {
        "probabilidad_cancelacion": round(probabilidad, 4),
        "riesgo": clasificar_riesgo(probabilidad),
    }
