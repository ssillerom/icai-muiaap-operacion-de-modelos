# UBICACION FINAL (ejercicio 1): src/claims_triage/inference.py
"""EJERCICIO 4: cargar el modelo, ejecutarlo y validar la salida."""

import joblib  # noqa: F401  (lo necesitareis en load_model)

from claims_triage.contracts import ClaimPrediction  # noqa: F401
from claims_triage.preprocess import FEATURE_NAMES, preprocess  # noqa: F401

# Con una probabilidad de riesgo igual o superior a este valor, el siniestro
# se envia a revision manual.
THRESHOLD = 0.5


def load_model(path):
    """Carga el fichero .joblib y devuelve el diccionario que contiene.

    El diccionario tiene 3 claves:
      "estimator"     -> el modelo (ofrece el metodo predict_proba)
      "feature_names" -> las columnas, en orden, con las que se entreno
      "model_version" -> un texto con la version del modelo
    """
    # TODO 4.5: cargar el modelo desde el fichero indicado.

    # TODO 4.6: asegurarse de que el modelo cargado espera exactamente las
    #   mismas columnas y en el mismo orden que usa este codigo (FEATURE_NAMES).
    #   Si no es asi, no debe usarse: avisar con un ValueError y un mensaje claro.

    # TODO 4.7: devolver el diccionario del modelo.
    raise NotImplementedError("TODO: ejercicio 4 (load_model)")


def predict(model, request):
    """Predice un siniestro (un ClaimRequest) y devuelve un ClaimPrediction."""
    # TODO 4.8: preparar los datos del siniestro para el modelo (ejercicio 3).

    # TODO 4.9: obtener del modelo la probabilidad de que el siniestro sea de
    #   riesgo. predict_proba devuelve, para cada fila, una probabilidad por
    #   clase en el orden [no riesgo, riesgo].

    # TODO 4.10: decidir: "revision_manual" si la probabilidad alcanza el
    #   umbral THRESHOLD, y "tramitacion_normal" si no.

    # TODO 4.11: devolver el resultado como ClaimPrediction (ejercicio 4),
    #   con la probabilidad redondeada a 3 decimales. Asi la salida tambien
    #   queda validada.
    raise NotImplementedError("TODO: ejercicio 4 (predict)")
