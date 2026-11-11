"""Configuracion del modelo (HECHO). La ruta se puede cambiar con MODEL_PATH."""
import os
from pathlib import Path

# src/envios/config.py -> parents[2] es la raiz del proyecto
RAIZ = Path(__file__).resolve().parents[2]
RUTA_MODELO = Path(os.environ.get("MODEL_PATH", RAIZ / "models" / "modelo_envios.joblib"))
VERSION_MODELO = "1.0.0"
SEMILLA = 7
