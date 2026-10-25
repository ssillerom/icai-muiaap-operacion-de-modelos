# UBICACION FINAL (ejercicio 1): src/claims_triage/contracts.py
"""Contratos de datos: describen que datos son validos.

Aqui hay DOS modelos de Pydantic:
  - ClaimRequest    -> una fila del CSV de entrada (EJERCICIO 2)
  - ClaimPrediction -> el resultado que devuelve el programa (EJERCICIO 4)

Un modelo de Pydantic es una clase con campos y tipos. Al crear un objeto,
Pydantic comprueba los datos y lanza ValidationError si algo no cuadra.
"""

from typing import Literal  # noqa: F401  (lo usareis en los TODO)

from pydantic import BaseModel, ConfigDict, Field, field_validator  # noqa: F401


# ---------------------------------------------------------------------------
# EJERCICIO 2: modelo de ENTRADA (una fila de data/claims.csv)
# ---------------------------------------------------------------------------
class ClaimRequest(BaseModel):
    """Una fila del CSV de siniestros.

    El lector de CSV entrega TODOS los valores como texto ("29", "3.5"...).
    Pydantic debe convertirlos al tipo correcto y rechazar los que no cuadren.
    """

    # Ya hecho: no se admiten columnas que no esten declaradas en este modelo.
    model_config = ConfigDict(extra="forbid")

    # Ejemplo ya hecho: un texto que no puede estar vacio.
    claim_id: str = Field(min_length=1)

    # TODO 2.1: policy_type. Solo se admiten los valores "basico",
    #           "terceros_ampliado" y "todo_riesgo".

    # TODO 2.2: driver_age. Numero entero; el conductor debe ser mayor de edad
    #           y no pasar de 90 anos.

    # TODO 2.3: vehicle_age_years. Numero decimal entre 0 y 30 anos.
    #           Es OPCIONAL: puede no venir informado.

    # TODO 2.4: claim_amount_eur. Numero decimal; el importe debe ser mayor
    #           que 0 y como maximo 100000.

    # TODO 2.5: injuries. Entero que solo puede valer 0 o 1.

    # TODO 2.6: police_report. Entero que solo puede valer 0 o 1.

    # TODO 2.7: en el CSV, un dato que falta llega como "" (texto vacio), y ""
    #           no es un numero. Haced que, para vehicle_age_years, el valor ""
    #           se interprete como "no informado" (None) y cualquier otro valor
    #           pase sin cambios. Plantilla de un validador de Pydantic:
    #
    #   @field_validator("vehicle_age_years", mode="before")
    #   @classmethod
    #   def empty_is_none(cls, value):
    #       # mode="before": recibe el valor ANTES de que Pydantic lo convierta
    #       if value == "":
    #           return ...        # que devolver cuando esta vacio
    #       return value          # en cualquier otro caso, el valor tal cual


# ---------------------------------------------------------------------------
# EJERCICIO 4: modelo de SALIDA (lo que devuelve el programa)
# ---------------------------------------------------------------------------
class ClaimPrediction(BaseModel):
    """Resultado del triaje de un siniestro. Validar la salida evita que
    un error del modelo o del codigo produzca un resultado absurdo."""

    model_config = ConfigDict(extra="forbid")

    # TODO 4.1: claim_id: el identificador del siniestro (texto).
    # TODO 4.2: decision: solo puede ser "revision_manual" o "tramitacion_normal".
    # TODO 4.3: risk_probability: una probabilidad, es decir, un decimal entre 0 y 1.
    # TODO 4.4: model_version: la version del modelo que ha hecho la prediccion (texto).
