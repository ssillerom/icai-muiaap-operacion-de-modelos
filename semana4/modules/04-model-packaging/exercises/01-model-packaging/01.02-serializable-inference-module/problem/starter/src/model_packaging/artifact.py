"""Puntos de extensión del taller de serialización."""

from __future__ import annotations

import json
import math
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import joblib
from pydantic import BaseModel, ConfigDict, Field, model_validator

from model_packaging.contracts import (
    QualityBand,
    WineQualityPrediction,
    WineQualityRequest,
)

from model_packaging.preprocess import(
    FEATURE_NAMES,
    PREPROCESSING_VERSION,
    preprocess_wine_request
)

ARTIFACT_SCHEMA_VERSION = "wine-quality-bundle-v1"
DEFAULT_BUNDLE_PATH = Path("models/wine_quality_bundle")
MANIFEST_FILENAME = "manifest.json"
MODEL_FILENAME = "model.joblib"
OUTPUT_LABELS: tuple[QualityBand, ...] = (
    "needs_review",
    "acceptable",
    "excellent",
)


class WineQualityEstimator(Protocol):
    """Interfaz mínima que debe cumplir el estimador cargado."""

    def predict(self, features: list[list[float]]) -> Sequence[str]:
        """Devuelve una etiqueta por fila."""

    def predict_proba(self, features: list[list[float]]) -> Sequence[Sequence[float]]:
        """Devuelve probabilidades por fila."""

#
# # # 1
# Clase que hereda BaseModel de Pydantic
class ArtifactManifest(BaseModel):
    """TODO: declara y valida los metadatos del bundle."""

    # no se permiten campos adicionales
    model_config = ConfigDict(extra="forbid")

    # campos obligatorios del manifiesto
    schema_version: str
    model_version: str = Field(min_length=1)
    preprocessing_version: str
    feature_names: tuple[str, ...] # los ... significa que la tupla puede contener un número variable de elementos. Todavía no establece que deban ser exacatemente 11 elementos. Eso lo comprobaremos nosotros
    output_labels: tuple[QualityBand, ...]
    estimator_type: str = Field(min_length=1)

    # @model_validator(mode="after") es un decorador Pydantic que indica: Después de validar los campos individuales y crear el objeto, ejecuta también esta función para comprobar otras condiciones.
    # self representa el propio objeto de la clase ArtifactManifest sobre el que estamos ejecutando el método
    @model_validator(mode="after")
    def validate_contract(self) -> ArtifactManifest:

        if self.schema_version != ARTIFACT_SCHEMA_VERSION:
            raise ValueError("Versión de esquema incompatible")

        if self.preprocessing_version != PREPROCESSING_VERSION:
            raise ValueError("Versión del preprocesado incompatible")

        if self.feature_names != FEATURE_NAMES:
            raise ValueError("Las características o su orden son incompatibles")

        if self.output_labels != OUTPUT_LABELS:
            raise ValueError("Las etiquetas de salida son incompatibles")

        return self

# Esta clase sirve para guardar dos objetos: 
# - el estimador recuperado de model.joblib
# - el manifiesto recuperado de manifest.json
# @dataclass es una herramienta de Python para crear clases que almacenan datos sin tener que escribir 
# manualmente todo su constructor
# Por ejemplo: bundle = LoadedModelBundle(estimator = estimator, manifest = manifest)
# Luego podemos acceder a ellos: bundle.estimator
@dataclass(frozen=True)
class LoadedModelBundle:
    """Bundle cargado; no modificar esta interfaz pública."""

    estimator: WineQualityEstimator
    manifest: ArtifactManifest

# Lo de poner _ es para indicar que es una función auxiliar (es una convención, no es obligatorio)
# Comprobar que el estimador contiene los métodos necesarios para hacer predicciones
def _validate_estimator(estimator: WineQualityEstimator) -> None:
    # callable comprueba si lo que hemos encontrado puede llamarse como una función. Es decir, si predict y predict_proba pueden llamarse como una función
    # getattr(estimator, "predict", None) -> Busca el atributo predict dentro del estimador. Si no existe, devuelve None
    if not callable(getattr(estimator, "predict", None)):
        raise ValueError("El estimador no tiene un método predict()")

    if not callable(getattr(estimator, "predict_proba", None)):
        raise ValueError("El estimador no tiene un método predict_proba()")


#
#### 2
# 
def create_manifest(
    estimator: WineQualityEstimator, model_version: str
) -> ArtifactManifest:
    """TODO: devuelve un manifiesto compatible con el contrato."""
   
    _validate_estimator(estimator)

    return ArtifactManifest(
        schema_version = ARTIFACT_SCHEMA_VERSION,
        model_version = model_version,
        preprocessing_version = PREPROCESSING_VERSION,
        feature_names = FEATURE_NAMES,
        output_labels=OUTPUT_LABELS,
        estimator_type= type(estimator).__name__,
    )   

#
#### 3
# Guardar el modelo y el manifesto (manifest.json). Pero no devuelve el manifiesto como json
def save_model_bundle(
    bundle_path: Path,
    estimator: WineQualityEstimator,           # Si no recibimos un manifiesto, podemos crearlo usando la función create_manifest
    manifest: ArtifactManifest | None = None, # significa que manifest es opcional. Puede ser un objeto ArtifactManifest o None
) -> ArtifactManifest:
    """TODO: escribe manifest.json y model.joblib de forma segura."""

    _validate_estimator(estimator)

    if manifest is None:
        manifest = create_manifest(estimator, "wine-quality-rf-v1")
    else:
        manifest = ArtifactManifest.model_validate(
            manifest.model_dump()
        )

    if manifest.estimator_type != type(estimator).__name__:
        raise ValueError("El tipo de estimador no coincide con el manifiesto")

    # Crear la carpeta donde guardaremos los arhcivos
    bundle_path.mkdir(parents=True, exist_ok=True)

    # Guardar el modelo entrenado
    joblib.dump(estimator, bundle_path / MODEL_FILENAME)

    # Guardar el manifiesto como JSON
    (bundle_path / MANIFEST_FILENAME).write_text(
        json.dumps(
            manifest.model_dump(mode="json"),
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # devuelve el manifiesto (no es json)
    return manifest

    
#
### 4
# El enunciado pide validar el manifiesto y después cargar el modelo serializado
def load_model_bundle(bundle_path: Path) -> LoadedModelBundle:
    """TODO: valida el manifiesto antes de cargar el estimador."""
    # Definir las rutas de los dos archivos
    manifest_path = bundle_path / MANIFEST_FILENAME
    model_path = bundle_path / MODEL_FILENAME

    # Comprobar que existe el manifiesto
    if not manifest_path.is_file():
        raise FileNotFoundError("No se ha encontrado el manifiesto")

    # Leer y validar el manifiesto
    # La función model_validate_json() viene de Pydanticm concretamente de la clase
    # BaseModel, de la que hereda ArtifactManifest
    # El método model_validate_json de Pydantic hace 3 cosas:
    #   1. Convierte el texto JSON en datos que Pydantic pueda interpretar
    #   2. Comprueba que cumplen los tipos y requisitos definidos en ArtifactManifest
    #   3. Ejecuta la función validate_contract() gracias a @model_validator(mode="after")
    manifest = ArtifactManifest.model_validate_json(
        manifest_path.read_text(encoding="UTF-8")
    )

    # Comprobar que existe el archivo del modelo
    if not model_path.is_file():
        raise FileNotFoundError("No existe el modelo")

    # Cargar el modelo entrenado
    estimator = joblib.load(model_path)

    # Comprobar que el estimador tiene los métodos necesarios
    _validate_estimator(estimator)

    # Comprobar que su tipo coincide con el manifiesto
    if type(estimator).__name__ != manifest.estimator_type:
        raise ValueError("El tipo del estimador no coincide con el indicado en el manifiesto")

    # Devolver el bundle cargado
    return LoadedModelBundle(
        estimator = estimator,
        manifest = manifest
    )



   

# Esta función tiene que recibir los datos de un vino y devolver su calidad

def infer_wine_quality(
    bundle: LoadedModelBundle,
    request: WineQualityRequest,
) -> WineQualityPrediction:
    """TODO: preprocesa, invoca el estimador y valida la respuesta."""

    # Preparar las características del vino
    vector = preprocess_wine_request(request).as_vector()

    # Realizar la predicción
    labels = bundle.estimator.predict([vector])

    # Comprobar que hemos recibido una predicción
    if len(labels) != 1:
        raise ValueError(
            "El modelo debe devolver una sola predicción por muestra"
        )

    # Obtener y validar la etiqueta
    label = str(labels[0])

    if label not in bundle.manifest.output_labels:
        raise ValueError(f"Etiqueta de salida no permitida: {label}")

    # Obtener las probabilidades
    probabilities = bundle.estimator.predict_proba([vector])

    if len(probabilities) != 1:
        raise ValueError("El modelo debe devolver probabilidades para una muestra")

    # Obtener las probabilidades y comprobar que son numéricas
    try:
        row_probs = [float(prob) for prob in probabilities[0]]
    except (TypeError, ValueError) as error:
        raise ValueError("Las probabilidades deben ser numéricas") from error

    # Comprobar que están entre 0 y 1 y son finitas
    if not row_probs or any(
        not math.isfinite(prob) or not 0 <= prob <= 1
        for prob in row_probs
    ):
        raise ValueError("Las probabilidades deben estar entre 0 y 1 y ser finitas")

    # Comprobar que suman aproximadamente 1
    if not math.isclose(sum(row_probs), 1.0, abs_tol=1e-6):
        raise ValueError("Las probabilidades deben sumar 1")

    # Obtener las clases conocidas del estimador
    classes = getattr(bundle.estimator, "classes_", None)

    if classes is not None:
        known_classes = [str(item) for item in classes]

        if label not in known_classes or len(row_probs) != len(known_classes):
            raise ValueError(
                "Las probabilidades no coinciden con las etiquetas del modelo"
            )

        # Probabilidad correspondiente a la etiqueta predicha
        confidence = row_probs[known_classes.index(label)]

    elif len(row_probs) == 1:
        confidence = row_probs[0]

    else:
        raise ValueError(
            "No se puede asociar la confianza sin classes_ del modelo"
        )

    return WineQualityPrediction(
        quality_band=label,
        confidence=float(confidence),
        model_version=bundle.manifest.model_version,
        preprocessing_version=bundle.manifest.preprocessing_version,
    )