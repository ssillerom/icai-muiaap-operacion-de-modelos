"""Configuracion de la API (HECHO): API_KEY desde el entorno o desde .env."""
import os

from dotenv import load_dotenv

load_dotenv()


def obtener_api_key() -> str | None:
    """Clave que deben enviar los clientes, o None si no esta configurada."""
    return os.getenv("API_KEY") or None
