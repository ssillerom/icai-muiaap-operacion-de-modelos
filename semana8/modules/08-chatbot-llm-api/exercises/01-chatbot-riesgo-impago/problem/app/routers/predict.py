from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()


# TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)
