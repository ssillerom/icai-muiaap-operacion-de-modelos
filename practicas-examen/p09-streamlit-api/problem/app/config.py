"""Configuracion de la API: se lee del entorno y, si existe, de un fichero .env.

Los secretos NUNCA se escriben en el codigo. En local se ponen en .env (que no
se sube al repositorio); en produccion, en variables de entorno del servidor.
"""
import os

from dotenv import load_dotenv

# Busca .env subiendo desde la carpeta de este fichero (llega a la raiz del
# proyecto), arranques desde donde arranques. No pisa las variables
# que ya esten definidas en el entorno (las del servidor tienen prioridad).
load_dotenv()


def obtener_api_key() -> str | None:
    """Clave que deben enviar los clientes, o None si no esta configurada.

    Se lee en cada llamada (no al importar) para que un cambio en el entorno,
    por ejemplo en los tests, se tenga en cuenta.
    """
    return os.getenv("API_KEY") or None
