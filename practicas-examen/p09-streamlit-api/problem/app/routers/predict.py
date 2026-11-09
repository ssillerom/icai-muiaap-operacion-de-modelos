"""POST /predict: riesgo de cancelacion de una reserva (requiere API key)."""
from fastapi import APIRouter, Depends

from app.dependencies import ArtefactoDep
from app.security import verificar_api_key
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

# Todas las rutas de este router exigen la API key. /health esta en otro router
# y sigue siendo publico.
router = APIRouter(tags=["prediccion"], dependencies=[Depends(verificar_api_key)])


@router.post(
    "/predict",
    summary="Predecir riesgo de cancelacion",
    responses={
        401: {"description": "API key incorrecta o ausente"},
        503: {"description": "Modelo no disponible"},
    },
)
def predict(entrada: ReservaEntrada, artefacto: ArtefactoDep) -> PrediccionSalida:
    """Calcula la probabilidad de cancelacion y el nivel de riesgo de una reserva.

    Requiere la cabecera `X-API-Key`.

    - **200**: prediccion con probabilidad, riesgo (bajo, medio o alto) y version del modelo.
    - **401**: falta la cabecera X-API-Key o no es correcta.
    - **422**: la reserva no cumple el contrato (rangos, canal, campos o capacidad).
    - **503**: el modelo no esta disponible; la peticion puede repetirse mas tarde.
    """
    return predecir(entrada, artefacto)
