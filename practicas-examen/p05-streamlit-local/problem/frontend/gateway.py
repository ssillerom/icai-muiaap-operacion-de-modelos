"""Puente entre el frontend y el backend local (TU).

`app.py` solo conoce `consultar_modelo()` y `Respuesta`. Todo lo que tiene que
ver con Pydantic, el modelo y sus errores se queda aqui, de modo que en la
practica 9 bastara con cambiar este fichero para llamar a la API por HTTP.
"""
from dataclasses import dataclass, field

from pydantic import ValidationError

from reservas.inference import predecir
from reservas.model.artefacto import ArtefactoIncompatible
from reservas.schemas import PrediccionSalida, ReservaEntrada

# Nombres que ve el usuario en el formulario (HECHO)
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
    """Lo que recibe app.py: o una prediccion, o una lista de mensajes para el usuario (HECHO)."""

    ok: bool
    prediccion: PrediccionSalida | None = None
    errores: list[str] = field(default_factory=list)


def traducir_errores(error: ValidationError) -> list[str]:
    """Convierte los errores de Pydantic en frases con la etiqueta del formulario."""
    # TODO 1: recorre error.errors() y devuelve una frase por error con el
    #   formato "<etiqueta>: <mensaje>".
    #   - La etiqueta sale de ETIQUETAS usando el primer elemento de
    #     detalle["loc"]. Los errores del model_validator tienen loc == ():
    #     para ellos usa "Reserva".
    #   - Pydantic antepone "Value error, " a los ValueError de tus
    #     validadores: quitalo (investiga str.removeprefix).
    #   Comprobacion: tests/test_gateway.py::test_traducir_*
    raise NotImplementedError("TODO 1: traducir_errores")


def consultar_modelo(valores: dict) -> Respuesta:
    """Valida los valores del formulario, llama al modelo y devuelve una Respuesta."""
    # TODO 2:
    #   1) construye ReservaEntrada con los valores; si no son validos, devuelve
    #      Respuesta(ok=False, errores=traducir_errores(...)) SIN llamar al modelo;
    #   2) llama a predecir(); si el modelo no esta disponible
    #      (FileNotFoundError, ArtefactoIncompatible o ValidationError del
    #      manifiesto) devuelve MENSAJE_MODELO_NO_DISPONIBLE. Nunca muestres al
    #      usuario el texto de la excepcion: puede contener rutas internas;
    #   3) si todo va bien, Respuesta(ok=True, prediccion=...).
    #   Comprobacion: tests/test_gateway.py::test_consulta_* y test_modelo_no_disponible_*
    raise NotImplementedError("TODO 2: consultar_modelo")
