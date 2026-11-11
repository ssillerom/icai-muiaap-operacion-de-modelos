"""Punto de entrada de la API (TU).

Arranque, desde la raiz del proyecto:  uv run uvicorn app.main:app --reload
Documentacion interactiva:            http://localhost:8000/docs
"""
from fastapi import FastAPI

from app.routers import health, predict

app = FastAPI(
    title="API de riesgo de cancelacion",
    description="Predice el riesgo de que se cancele una reserva de hotel (datos sinteticos).",
    version="0.6.0",
)

# TODO 1: registra en `app` los routers de health y predict (investiga
#   app.include_router). Sin esto las rutas existen en su fichero pero la API
#   no las expone: responderian 404.
#   Comprobacion: tests/test_api.py::test_health (junto con el TODO 2)
