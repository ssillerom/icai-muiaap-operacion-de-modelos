"""Inferencia: de un EnvioEntrada validado a un PrediccionSalida validado."""
from envios.data.features import preparar_fila
from envios.model.cargador import ModeloCargado, cargar_modelo
from envios.schemas import EnvioEntrada, PrediccionSalida

UMBRAL_RIESGO = 0.35
UMBRAL_RETRASO = 0.65


def clasificar_nivel(probabilidad: float) -> str:
    """Devuelve "a_tiempo" si p < 0.35, "riesgo" si p < 0.65 y "retraso_probable" en el resto."""
    if probabilidad < UMBRAL_RIESGO:
        return "a_tiempo"
    if probabilidad < UMBRAL_RETRASO:
        return "riesgo"
    return "retraso_probable"


def predecir(entrada: EnvioEntrada, modelo: ModeloCargado | None = None) -> PrediccionSalida:
    """Probabilidad de retraso y nivel. Si no se pasa `modelo`, se carga el de disco."""
    if modelo is None:
        modelo = cargar_modelo()
    fila = preparar_fila(entrada.model_dump())
    probabilidad = float(modelo.modelo.predict_proba(fila)[0][1])
    return PrediccionSalida(
        probabilidad_retraso=round(probabilidad, 4),
        nivel=clasificar_nivel(probabilidad),
        version_modelo=modelo.version,
    )
