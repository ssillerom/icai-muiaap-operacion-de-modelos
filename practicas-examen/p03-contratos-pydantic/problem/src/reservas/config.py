"""Configuracion del proyecto (HECHO).

La ruta del modelo se puede cambiar con la variable de entorno MODEL_PATH.
"""
import os
from pathlib import Path

# src/reservas/config.py -> parents[2] es la raiz del proyecto
RAIZ = Path(__file__).resolve().parents[2]
RUTA_DATOS = RAIZ / "data" / "raw" / "reservas_hotel.csv"
RUTA_MODELO = Path(os.environ.get("MODEL_PATH", RAIZ / "models" / "modelo.joblib"))
SEMILLA = 42
