"""POST /predict: riesgo de retraso de un envio (C3)."""
from fastapi import APIRouter, Depends

from app.dependencies import ModeloDep
from app.security import verificar_api_key
from envios.inference import predecir
from envios.schemas import EnvioEntrada, PrediccionSalida

# TODO C3a: todas las rutas de este router exigen la API key.
router = APIRouter(tags=["prediccion"])


# TODO C3b: POST /predict
#   - cuerpo EnvioEntrada, respuesta PrediccionSalida, modelo con ModeloDep;
#   - documenta en `responses` los codigos 401 y 503.
