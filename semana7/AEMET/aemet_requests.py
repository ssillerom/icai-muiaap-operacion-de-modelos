"""Práctica #2 - Requests + AEMET (semana 7).

Pasos del enunciado:
  1. Inventario de estaciones -> buscar "MADRID, CIUDAD UNIVERSITARIA" -> indicativo (idema).
  2. Climatología diaria de esa estación, octubre de 2019.

La API key se lee de la variable de entorno AEMET_API_KEY (nunca va en el código)
y se envía como query string `api_key`, como pide el enunciado.

Uso:
    export AEMET_API_KEY="..."        # Git Bash
    python aemet_requests.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests

# Endpoints de la documentación de la AEMET (https://opendata.aemet.es/dist/index.html).
BASE_URL = "https://opendata.aemet.es/opendata/api"
INVENTARIO_PATH = "/valores/climatologicos/inventarioestaciones/todasestaciones"
DIARIAS_PATH = (
    "/valores/climatologicos/diarios/datos"
    "/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{idema}"
)

# Valores del enunciado (octubre de 2019).
FECHA_INI = "2019-10-01T00:00:00UTC"
FECHA_FIN = "2019-10-30T23:59:59UTC"
NOMBRE_ESTACION = "MADRID, CIUDAD UNIVERSITARIA"
TIMEOUT = 30
SALIDA = Path(__file__).parent / "salidas"


class AemetError(Exception):
    """Error al hablar con la API (sin incluir nunca la API key en el mensaje)."""


def get_api_key() -> str:
    key = os.environ.get("AEMET_API_KEY", "").strip()
    if not key:
        raise AemetError("Falta la variable de entorno AEMET_API_KEY.")
    return key


def _get_json(url: str, api_key: str | None, session=None):
    """GET y devuelve JSON. La key va por query string (params), no en la URL."""
    params = {"api_key": api_key} if api_key else None
    try:
        response = (session or requests).get(
            url, params=params, headers={"Accept": "application/json"}, timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json()
    except requests.Timeout as error:
        raise AemetError("La API de la AEMET tardó demasiado.") from error
    except requests.HTTPError as error:
        status = error.response.status_code if error.response is not None else "?"
        raise AemetError(f"La AEMET respondió con HTTP {status}.") from error
    except (requests.RequestException, ValueError) as error:
        # Ojo: no usamos str(error): una excepción de requests puede contener la URL con la key.
        raise AemetError(f"Fallo en la petición ({type(error).__name__}).") from error


def pedir_datos(url: str, api_key: str, session=None):
    """La AEMET responde en dos pasos: 1) JSON con 'datos' (un link); 2) GET a ese link."""
    primera = _get_json(url, api_key, session)
    if not isinstance(primera, dict) or primera.get("estado") not in (200, None):
        estado = primera.get("estado") if isinstance(primera, dict) else None
        raise AemetError(f"La AEMET devolvió estado {estado} (ver descripción en la respuesta).")
    enlace = primera.get("datos") if isinstance(primera, dict) else None
    if not enlace:
        raise AemetError("La respuesta no incluye el enlace 'datos'.")
    return _get_json(enlace, None, session)  # el enlace de datos no necesita la key


def buscar_indicativo(estaciones: list[dict], nombre: str = NOMBRE_ESTACION) -> str:
    for estacion in estaciones:
        if str(estacion.get("nombre", "")).strip().upper() == nombre.upper():
            return estacion["indicativo"]
    raise AemetError(f"No se encontró la estación {nombre!r} en el inventario.")


def url_diarias(idema: str, fecha_ini: str = FECHA_INI, fecha_fin: str = FECHA_FIN) -> str:
    return BASE_URL + DIARIAS_PATH.format(fecha_ini=fecha_ini, fecha_fin=fecha_fin, idema=idema)


def main() -> int:
    try:
        api_key = get_api_key()
        estaciones = pedir_datos(BASE_URL + INVENTARIO_PATH, api_key)
        idema = buscar_indicativo(estaciones)
        print(f"Estación {NOMBRE_ESTACION}: indicativo (idema) = {idema}")
        datos = pedir_datos(url_diarias(idema), api_key)
    except AemetError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    SALIDA.mkdir(exist_ok=True)
    destino = SALIDA / "climatologia_madrid_ciudad_universitaria_2019-10.json"
    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{len(datos)} registros diarios guardados en {destino}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
