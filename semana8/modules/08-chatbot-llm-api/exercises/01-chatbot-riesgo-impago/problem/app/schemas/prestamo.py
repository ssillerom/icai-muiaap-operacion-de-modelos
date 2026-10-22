from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.
# TODO: field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.
# TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).
