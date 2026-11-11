"""Inferencia: de una ReservaEntrada validada a una PrediccionSalida validada (HECHO)."""
from reservas.data.features import preparar_fila
from reservas.model.artefacto import Artefacto
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


def predecir(entrada: ReservaEntrada, artefacto: Artefacto | None = None) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el riesgo de una reserva.

    Si no se pasa `artefacto`, se usa el cargado desde disco. Pasarlo
    explicitamente permite probar la inferencia con un modelo falso (y, en la
    API, inyectarlo con Depends).
    """
    if artefacto is None:
        artefacto = cargar_modelo()
    fila = preparar_fila(entrada)
    probabilidad = float(artefacto.modelo.predict_proba(fila)[0][1])
    return PrediccionSalida(
        probabilidad_cancelacion=round(probabilidad, 4),
        riesgo=clasificar_riesgo(probabilidad),
        version_modelo=artefacto.manifiesto.version_modelo,
    )
