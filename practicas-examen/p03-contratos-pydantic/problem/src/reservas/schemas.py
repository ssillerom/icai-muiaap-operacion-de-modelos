"""Contratos de entrada y salida del modelo (TU).

Las reglas de cada campo estan en la tabla del enunciado.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

MAX_HUESPEDES = 6


class ReservaEntrada(BaseModel):
    """Datos de una reserva que recibe el modelo."""

    # TODO 1: rechazar campos que no existan en el contrato. Investiga
    #   model_config = ConfigDict(...) y la opcion `extra`.
    #   Comprobacion: test_schemas.py::test_campo_inventado_se_rechaza

    # TODO 2: los 8 campos con su tipo y sus rangos usando Field(ge=, gt=, le=).
    #   `canal` solo admite "web", "agencia" o "telefono": usa Literal.
    #   Los nombres deben coincidir con VARIABLES (data/features.py).
    #   Comprobacion: test_schemas.py::test_valores_fuera_de_rango y test_los_limites_son_validos

    # TODO 3: field_validator sobre `canal` en modo "before" (junto con
    #   @classmethod) que quite espacios y pase a minusculas si el valor es un
    #   str. Tiene que ejecutarse ANTES de comprobar el Literal: por eso "before".
    #   Comprobacion: test_schemas.py::test_canal_se_normaliza

    # TODO 4: model_validator en modo "after" que lance ValueError si
    #   adultos + ninos > MAX_HUESPEDES. El mensaje debe incluir
    #   "6 huespedes" (usa la constante). Devuelve self si todo va bien.
    #   Es una regla ENTRE campos: un field_validator no ve los demas campos.
    #   Comprobacion: test_schemas.py::test_capacidad_*
    pass


class PrediccionSalida(BaseModel):
    """Respuesta del modelo."""

    # TODO 5: probabilidad_cancelacion (float entre 0 y 1) y riesgo
    #   ("bajo", "medio" o "alto"). Validar la salida protege a quien consume
    #   el modelo de un bug nuestro (por ejemplo, devolver 1.3 o "regular").
    #   Comprobacion: test_schemas.py::test_salida_*
    pass
