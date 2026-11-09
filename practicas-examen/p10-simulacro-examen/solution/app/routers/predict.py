"""POST /predict: riesgo de retraso de un envio (requiere API key)."""
from fastapi import APIRouter, Depends

from app.dependencies import ModeloDep
from app.security import verificar_api_key
from envios.inference import predecir
from envios.schemas import EnvioEntrada, PrediccionSalida

router = APIRouter(tags=["prediccion"], dependencies=[Depends(verificar_api_key)])


@router.post(
    "/predict",
    summary="Predecir riesgo de retraso",
    responses={
        401: {"description": "API key incorrecta o ausente"},
        503: {"description": "Modelo no disponible"},
    },
)
def predict(entrada: EnvioEntrada, modelo: ModeloDep) -> PrediccionSalida:
    """Probabilidad de que el envio llegue tarde y nivel de riesgo. Requiere X-API-Key."""
    return predecir(entrada, modelo)
