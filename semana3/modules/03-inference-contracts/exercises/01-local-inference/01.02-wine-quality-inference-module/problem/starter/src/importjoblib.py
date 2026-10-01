from pathlib import Path
import joblib

# Relativa a la raíz del repositorio
ruta_modelo = Path() / "semana3/models/wine_quality_classifier.joblib"

modelo = joblib.load(ruta_modelo).get("estimator")

print("=== Estructura del modelo ===")
print(modelo)