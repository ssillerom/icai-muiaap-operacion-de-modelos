"""TODO: carga del .joblib e inferencia sobre características preparadas."""

# Declara DEFAULT_MODEL_PATH, load_wine_quality_model() e infer_wine_quality().
# Comprueba las características del artefacto antes de llamar al clasificador.
from pathlib import Path

import joblib

from model_inference.contracts import WineQualityPrediction
from model_inference.preprocess import (
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    WineFeatures,
)

# Ruta del modelo cuando no se indica otra con --model.
DEFAULT_MODEL_PATH = Path("models/wine_quality_classifier.joblib")


def load_wine_quality_model(model_path: Path = DEFAULT_MODEL_PATH) -> dict:
    """Carga el .joblib y comprueba que sirve antes de predecir."""
    contenido = joblib.load(model_path)

    # Recorremos las tres claves que DEBE tener el diccionario
    # Si alguna no esta, paramos con un error que dice cuál falta
    for clave in ["estimator", "feature_names", "model_version"]:
        if clave not in contenido:
            raise ValueError(f"El modelo no sirve,no hay clasificador compatible. Falta {clave}")

    # Sacamos el modelo del diccionario para comprobarlo
    modelo = contenido["estimator"]

    # Un modelo tiene los métodos predict y predict_proba
    # getattr(modelo, "predict", None) pide ese método, si existe lo devuelve,
    # y si no existe devuelve None. Si sale None, falta, y paramos con un error
    for metodo in ["predict", "predict_proba"]:
        if getattr(modelo, metodo, None) is None:
            raise ValueError(f"El modelo no sirve,no hay clasificador compatible. Falta {metodo}")

    # Comparamos las columnas del modelo con las nuestras (FEATURE_NAMES)
    # tuple(...) convierte la lista del archivo en tupla para poder compararla pq FEATURE es una tupla
    # Si no son las mismas, o están en otro orden, paramos con un error
    if tuple(contenido["feature_names"]) != FEATURE_NAMES:  #
        raise ValueError(
            "El modelo no sirve porque sus columnas (feature_names) no son las "
            f"nuestras o están en otro orden: {contenido['feature_names']}"
        )
    # Si ha pasado las tres comprobaciones devolvemos el diccionario para usarlo
    return contenido


def infer_wine_quality(
    sample_id: str,
    features: WineFeatures,
    payload: dict,
) -> WineQualityPrediction:
    """Predice la categoría de un vino y devuelve la salida ya validada."""
    modelo = payload["estimator"]
    # El modelo recibe una lista de filas (una fila por vino).
    # Solo tenemos un vino, así que ponemos su lista de 11 números dentro de otra lista
    matriz = [features.as_vector()]  # el modelo espera una lista de filas

    # predict devuelve una respuesta por fila, por ejemplo ['needs_review']
    # Con [0] nos quedamos con la primera, que es la única.
    categoria = modelo.predict(matriz)[0]

    # predict_proba devuelve las probabilidades de cada categoría, por ejemplo
    # [[0.05, 0.09, 0.86]]. Con [0] nos quedamos con la lista de nuestra fila.
    probabilidades = modelo.predict_proba(matriz)[0]

    # La confianza es la probabilidad más alta.
    confianza = probabilidades[0]
    for probabilidad in probabilidades:
        if probabilidad > confianza:
            confianza = probabilidad

    return WineQualityPrediction(
        sample_id=sample_id,
        quality_band=categoria,
        confidence=confianza,
        model_version=payload["model_version"],
        preprocessing_version=PREPROCESSING_VERSION,
    )
