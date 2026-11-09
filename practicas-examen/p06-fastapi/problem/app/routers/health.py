"""GET /health: comprobar que la API esta viva (TU)."""
from fastapi import APIRouter

router = APIRouter(tags=["salud"])


# TODO 2: ruta GET /health que devuelva {"status": "ok"}. Anota el tipo de
#   retorno (dict[str, str]) y escribe un docstring: FastAPI lo muestra en /docs.
#   Comprobacion: tests/test_api.py::test_health
