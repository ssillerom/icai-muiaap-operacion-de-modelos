"""Inferencia: de un EnvioEntrada validado a un PrediccionSalida validado (B4)."""
from envios.data.features import preparar_fila
from envios.model.cargador import ModeloCargado, cargar_modelo
from envios.schemas import EnvioEntrada, PrediccionSalida

UMBRAL_RIESGO = 0.35
UMBRAL_RETRASO = 0.65


def clasificar_nivel(probabilidad: float) -> str:
    """Devuelve "a_tiempo" si p < 0.35, "riesgo" si p < 0.65 y "retraso_probable" en el resto."""
    # TODO B4a
    raise NotImplementedError("TODO B4a: clasificar_nivel")


def predecir(entrada: EnvioEntrada, modelo: ModeloCargado | None = None) -> PrediccionSalida:
    """Probabilidad de retraso y nivel. Si no se pasa `modelo`, se carga el de disco."""
    # TODO B4b: usa preparar_fila(...) con los datos de la entrada y la
    #   probabilidad de la clase 1 (retraso). Redondea a 4 decimales.
    raise NotImplementedError("TODO B4b: predecir")
