"""Ajustes del proyecto (YA HECHO)."""
import os
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODEL_PATH = os.environ.get("MODEL_PATH", str(RAIZ / "models" / "modelo_impago.joblib"))
