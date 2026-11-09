"""POST /predict: riesgo de cancelacion de una reserva."""
from fastapi import APIRouter

from app.dependencies import ArtefactoDep
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

router = APIRouter(tags=["prediccion"])


@router.post(
    "/predict",
    summary="Predecir riesgo de cancelacion",
    responses={503: {"description": "Modelo no disponible"}},
)
def predict(entrada: ReservaEntrada, artefacto: ArtefactoDep) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el nivel de riesgo de una reserva.

    - **200**: prediccion con probabilidad, riesgo (bajo, medio o alto) y version del modelo.
    - **422**: la reserva no cumple el contrato (rangos, canal, campos o capacidad).
    - **503**: el modelo no esta disponible; la peticion puede repetirse mas tarde.
    """
    return predecir(entrada, artefacto)
