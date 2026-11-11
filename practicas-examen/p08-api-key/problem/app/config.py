"""Configuracion de la API: se lee del entorno y, si existe, de un fichero .env (TU).

Los secretos NUNCA se escriben en el codigo. En local se ponen en .env (que no
se sube al repositorio); en produccion, en variables de entorno del servidor.
"""
import os

from dotenv import load_dotenv

# TODO 1a: carga el fichero .env (si existe) llamando a load_dotenv(). Por
#   defecto no pisa las variables que ya existen en el entorno.


def obtener_api_key() -> str | None:
    """Clave que deben enviar los clientes, o None si no esta configurada."""
    # TODO 1b: devuelve la variable de entorno API_KEY (os.getenv). Si no
    #   existe o esta vacia, devuelve None. Leela aqui dentro, en cada llamada,
    #   y no en una constante al importar el modulo: asi los tests pueden
    #   cambiarla con monkeypatch.setenv.
    #   Comprobacion: tests/test_seguridad.py::test_la_clave_* y test_sin_clave_* y test_clave_vacia_*
    raise NotImplementedError("TODO 1b: obtener_api_key")
