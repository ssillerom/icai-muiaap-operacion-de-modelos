"""Puente entre el frontend y el backend local.

`app.py` solo conoce `consultar_modelo()` y `Respuesta`. Todo lo que tiene que
ver con Pydantic, el modelo y sus errores se queda aqui, de modo que en la
practica 9 bastara con cambiar este fichero para llamar a la API por HTTP.
"""
from dataclasses import dataclass, field

from pydantic import ValidationError

from reservas.inference import predecir
from reservas.model.artefacto import ArtefactoIncompatible
from reservas.schemas import PrediccionSalida, ReservaEntrada

# Nombres que ve el usuario en el formulario
ETIQUETAS = {
    "antelacion_dias": "Antelación (días)",
    "noches": "Noches",
    "adultos": "Adultos",
    "ninos": "Niños",
    "precio_noche": "Precio por noche (€)",
    "canal": "Canal de reserva",
    "cancelaciones_previas": "Cancelaciones previas",
    "peticiones_especiales": "Peticiones especiales",
}
MENSAJE_MODELO_NO_DISPONIBLE = (
    "El modelo no está disponible en este momento. Inténtalo más tarde o avisa al equipo técnico."
)


@dataclass
class Respuesta:
    """Lo que recibe app.py: o una prediccion, o una lista de mensajes para el usuario."""

    ok: bool
    prediccion: PrediccionSalida | None = None
    errores: list[str] = field(default_factory=list)


def traducir_errores(error: ValidationError) -> list[str]:
    """Convierte los errores de Pydantic en frases con la etiqueta del formulario."""
    mensajes = []
    for detalle in error.errors():
        campo = detalle["loc"][0] if detalle["loc"] else None
        etiqueta = ETIQUETAS.get(campo, "Reserva")
        texto = detalle["msg"].removeprefix("Value error, ")
        mensajes.append(f"{etiqueta}: {texto}")
    return mensajes


def consultar_modelo(valores: dict) -> Respuesta:
    """Valida los valores del formulario, llama al modelo y devuelve una Respuesta."""
    try:
        entrada = ReservaEntrada(**valores)
    except ValidationError as error:
        return Respuesta(ok=False, errores=traducir_errores(error))

    try:
        prediccion = predecir(entrada)
    except (FileNotFoundError, ArtefactoIncompatible, ValidationError):
        return Respuesta(ok=False, errores=[MENSAJE_MODELO_NO_DISPONIBLE])

    return Respuesta(ok=True, prediccion=prediccion)
