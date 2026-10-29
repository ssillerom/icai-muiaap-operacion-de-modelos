import requests
from dotenv import load_dotenv
import os


def get_aemet_data(url: str, params: dict = None):
    load_dotenv()
    params = params or {}
    params["api_key"] = os.getenv("AEMET_KEY")
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response


def get_aemet_inventario_estaciones(nombre_estacion: str = None):
    url = (
        "https://opendata.aemet.es/opendata/api/"
        "valores/climatologicos/inventarioestaciones/todasestaciones"
    )
    response = get_aemet_data(url)
    inventario_url = response.json()["datos"]
    estaciones = get_aemet_data(inventario_url).json()
    if not nombre_estacion:
        return estaciones
    for estacion in estaciones:
        if estacion["nombre"] == nombre_estacion:
            return estacion


def get_aemet_climatologia(idema: str, fecha_inicio: str, fecha_fin: str):
    url = (
        "https://opendata.aemet.es/opendata/api/"
        "valores/climatologicos/diarios/datos/"
        f"fechaini/{fecha_inicio}/"
        f"fechafin/{fecha_fin}/"
        f"estacion/{idema}"
    )
    response = get_aemet_data(url)
    climatologia_url = response.json()["datos"]
    return get_aemet_data(climatologia_url).json()


if __name__ == "__main__":
    nombre_estacion = "MADRID, CIUDAD UNIVERSITARIA"
    fecha_inicio = "2019-10-01T00:00:00UTC"
    fecha_fin = "2019-10-30T23:59:59UTC"

    estacion = get_aemet_inventario_estaciones(nombre_estacion)
    climatologia = get_aemet_climatologia(estacion["indicativo"], fecha_inicio, fecha_fin)
    print(climatologia)
