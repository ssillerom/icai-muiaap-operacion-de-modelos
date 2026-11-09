"""Tests de src/reservas/model/artefacto.py (NO MODIFICAR)."""
import json
from datetime import datetime

import pytest
import sklearn
from pydantic import ValidationError

from reservas.config import VERSION_MODELO
from reservas.data.features import VARIABLES
from reservas.model import artefacto as art

MANIFIESTO_OK = {
    "version_modelo": "1.0.0",
    "fecha_entrenamiento": "2026-11-09T10:00:00Z",
    "variables": VARIABLES,
    "metricas": {"f1": 0.75},
    "version_sklearn": "1.7.0",
}


def leer_json(carpeta):
    return json.loads((carpeta / art.NOMBRE_MANIFIESTO).read_text(encoding="utf-8"))


def escribir_json(carpeta, datos):
    (carpeta / art.NOMBRE_MANIFIESTO).write_text(json.dumps(datos), encoding="utf-8")


# --- TODO 1: Manifiesto ---------------------------------------------------------


def test_manifiesto_valido():
    manifiesto = art.Manifiesto(**MANIFIESTO_OK)
    assert isinstance(manifiesto.fecha_entrenamiento, datetime)
    assert manifiesto.variables == VARIABLES


@pytest.mark.parametrize("campo", list(MANIFIESTO_OK))
def test_manifiesto_sin_un_campo_no_es_valido(campo):
    datos = dict(MANIFIESTO_OK)
    del datos[campo]
    with pytest.raises(ValidationError):
        art.Manifiesto(**datos)


def test_manifiesto_con_metrica_no_numerica_no_es_valido():
    datos = dict(MANIFIESTO_OK, metricas={"f1": "alta"})
    with pytest.raises(ValidationError):
        art.Manifiesto(**datos)


# --- TODO 2: guardar_artefacto ----------------------------------------------------


def test_guardar_crea_carpeta_con_los_dos_ficheros(tmp_path, modelo_y_metricas):
    carpeta = tmp_path / "nueva" / "cancelacion"
    devuelta = art.guardar_artefacto(*modelo_y_metricas, carpeta=carpeta)
    assert devuelta == carpeta
    assert (carpeta / art.NOMBRE_MODELO).exists()
    assert (carpeta / art.NOMBRE_MANIFIESTO).exists()


def test_contenido_del_manifiesto(tmp_path, modelo_y_metricas):
    _, metricas = modelo_y_metricas
    art.guardar_artefacto(*modelo_y_metricas, carpeta=tmp_path)
    contenido = leer_json(tmp_path)
    assert contenido["version_modelo"] == VERSION_MODELO
    assert contenido["variables"] == VARIABLES
    assert contenido["metricas"]["f1"] == metricas["f1"]
    assert contenido["version_sklearn"] == sklearn.__version__
    datetime.fromisoformat(contenido["fecha_entrenamiento"])


def test_guardar_con_otra_version(tmp_path, modelo_y_metricas):
    art.guardar_artefacto(*modelo_y_metricas, carpeta=tmp_path, version="2.0.0")
    assert leer_json(tmp_path)["version_modelo"] == "2.0.0"


# --- TODO 3: leer_manifiesto ------------------------------------------------------


def test_leer_manifiesto(tmp_path):
    escribir_json(tmp_path, MANIFIESTO_OK)
    assert art.leer_manifiesto(tmp_path).version_modelo == "1.0.0"


def test_leer_manifiesto_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="entrenar"):
        art.leer_manifiesto(tmp_path)


def test_leer_manifiesto_corrupto(tmp_path):
    escribir_json(tmp_path, {"version_modelo": "1.0.0"})
    with pytest.raises(ValidationError):
        art.leer_manifiesto(tmp_path)


# --- TODO 4: cargar_artefacto -----------------------------------------------------


def test_ida_y_vuelta_da_las_mismas_predicciones(tmp_path, modelo_y_metricas):
    modelo, _ = modelo_y_metricas
    art.guardar_artefacto(*modelo_y_metricas, carpeta=tmp_path)
    cargado = art.cargar_artefacto(tmp_path)
    assert isinstance(cargado, art.Artefacto)
    assert isinstance(cargado.manifiesto, art.Manifiesto)
    from reservas.train import cargar_datos

    muestra = cargar_datos().head(5)[VARIABLES]
    assert (cargado.modelo.predict_proba(muestra) == modelo.predict_proba(muestra)).all()


def test_cargar_sin_modelo(tmp_path, modelo_y_metricas):
    art.guardar_artefacto(*modelo_y_metricas, carpeta=tmp_path)
    (tmp_path / art.NOMBRE_MODELO).unlink()
    with pytest.raises(FileNotFoundError, match="entrenar"):
        art.cargar_artefacto(tmp_path)


def test_cargar_con_variables_distintas(tmp_path, modelo_y_metricas):
    art.guardar_artefacto(*modelo_y_metricas, carpeta=tmp_path)
    contenido = leer_json(tmp_path)
    contenido["variables"] = list(reversed(VARIABLES))
    escribir_json(tmp_path, contenido)
    with pytest.raises(art.ArtefactoIncompatible):
        art.cargar_artefacto(tmp_path)


def test_artefacto_incompatible_es_un_value_error():
    assert issubclass(art.ArtefactoIncompatible, ValueError)
