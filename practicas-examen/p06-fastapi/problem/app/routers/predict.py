"""POST /predict: riesgo de cancelacion de una reserva (TU)."""
from fastapi import APIRouter

from app.dependencies import ArtefactoDep
from reservas.inference import predecir
from reservas.schemas import PrediccionSalida, ReservaEntrada

router = APIRouter(tags=["prediccion"])


# TODO 4: ruta POST /predict.
#   - Entrada: el cuerpo JSON se valida con ReservaEntrada (basta con declarar
#     un parametro de ese tipo).
#   - El modelo llega como parametro de tipo ArtefactoDep (no lo cargues aqui).
#   - Salida: anota el retorno como PrediccionSalida; FastAPI la valida y la
#     documenta.
#   - Llama a predecir(entrada, artefacto) del backend: la API no repite la
#     logica de inferencia.
#   Comprobacion: tests/test_api.py::test_predict_*
