"""Práctica AEMET: climatología diaria de Madrid, Ciudad Universitaria (oct 2019)."""

import os

import requests

API_KEY = os.environ["AEMET_API_KEY"]  # la clave sale del entorno, nunca del código
BASE_URL = "https://opendata.aemet.es/opendata/api"
TIMEOUT = 30

INVENTARIO = "/valores/climatologicos/inventarioestaciones/todasestaciones"
DIARIOS = (
    "/valores/climatologicos/diarios/datos"
    "/fechaini/{inicio}/fechafin/{fin}/estacion/{idema}"
)


def pedir_aemet(ruta: str):

    respuesta = requests.get(BASE_URL+ruta, params={"api_key":API_KEY}, timeout=TIMEOUT) #primera peticion para sacar url datos
    respuesta.raise_for_status()

    url_datos = respuesta.json()["datos"]

    datos = requests.get(url_datos, timeout=TIMEOUT)
    datos.raise_for_status()  
    datos.encoding = "latin-1"  # AEMET responde en latin-1: sin esto, las tildes salen rotas
    return datos.json()


def buscar_idema(estaciones: list[dict], nombre: str) -> str:
    for estacion in estaciones:
        if estacion["nombre"] == nombre:
            return estacion["indicativo"]
    raise ValueError(f"No existe ninguna estación llamada {nombre!r}")


def main() -> None:
    estaciones = pedir_aemet(INVENTARIO)
    print(f"Estaciones recibidas: {len(estaciones)}")

    idema = buscar_idema(estaciones, "MADRID, CIUDAD UNIVERSITARIA")
    print(f"Indicativo: {idema}")

    ruta = DIARIOS.format(
        inicio="2019-10-01T00:00:00UTC",
        fin="2019-10-30T23:59:59UTC",
        idema=idema,
    )
    dias = pedir_aemet(ruta)
    print(f"Días recibidos: {len(dias)}")
    print(dias[0]) #un dia de ejemplo 


if __name__ == "__main__":
    main()

    """Estaciones recibidas: 926
Indicativo: 3194U
Días recibidos: 30
{'fecha': '2019-10-01', 'indicativo': '3194U', 'nombre': 'MADRID, CIUDAD UNIVERSITARIA', 'provincia': 'MADRID', 'altitud': '664', 'tmed': '19,0', 'prec': '0,0', 'tmin': '10,0', 'horatmin':'06:00', 'tmax': '28,1', 'horatmax': '14:20', 'hrMedia': '41', 'hrMax': '62', 'horaHrMax': 'Varias', 'hrMin': '27', 'horaHrMin': '14:00', 'pintMax': '0,0'}"""