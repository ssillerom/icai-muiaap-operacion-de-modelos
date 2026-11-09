"""Tests de la practica 1 (NO MODIFICAR). Van en tests/test_train.py del proyecto."""
import tomllib
from pathlib import Path

import joblib

from reservas import train

RAIZ_PROYECTO = Path(__file__).resolve().parents[1]


def leer_pyproject():
    with open(RAIZ_PROYECTO / "pyproject.toml", "rb") as fichero:
        return tomllib.load(fichero)


def test_estructura_del_proyecto():
    for ruta in [
        "pyproject.toml",
        "uv.lock",
        ".python-version",
        ".gitignore",
        "src/reservas/__init__.py",
        "src/reservas/train.py",
        "data/raw/reservas_hotel.csv",
    ]:
        assert (RAIZ_PROYECTO / ruta).exists(), f"Falta {ruta}"


def test_gitignore_excluye_entorno_y_modelos():
    contenido = (RAIZ_PROYECTO / ".gitignore").read_text(encoding="utf-8")
    assert ".venv" in contenido
    assert "models/" in contenido


def test_dependencias_en_pyproject():
    pyproject = leer_pyproject()
    dependencias = " ".join(pyproject["project"]["dependencies"])
    for paquete in ["pandas", "scikit-learn", "joblib"]:
        assert paquete in dependencias, f"Falta la dependencia {paquete}"
    assert "pytest" not in dependencias, "pytest es una dependencia de desarrollo"
    desarrollo = " ".join(pyproject["dependency-groups"]["dev"])
    assert "pytest" in desarrollo


def test_comando_entrenar():
    scripts = leer_pyproject()["project"]["scripts"]
    assert scripts.get("entrenar") == "reservas.train:main"


def test_rutas_relativas_a_la_raiz():
    assert Path(train.RAIZ) == RAIZ_PROYECTO
    assert Path(train.RUTA_DATOS) == RAIZ_PROYECTO / "data" / "raw" / "reservas_hotel.csv"
    assert Path(train.RUTA_MODELO) == RAIZ_PROYECTO / "models" / "modelo.joblib"


def test_cargar_datos():
    datos = train.cargar_datos()
    assert datos.shape == (2000, 9)
    assert set(datos.columns) == set(train.VARIABLES + [train.OBJETIVO])


def test_entrenamiento_reproducible():
    _, metricas_1 = train.entrenar()
    _, metricas_2 = train.entrenar()
    assert train.SEMILLA is not None
    assert metricas_1 == metricas_2
    assert metricas_1["filas"] == 2000
    assert 0.0 <= metricas_1["f1"] <= 1.0


def test_guardar_modelo(tmp_path):
    modelo, _ = train.entrenar()
    destino = tmp_path / "carpeta_nueva" / "modelo.joblib"
    train.guardar_modelo(modelo, destino)
    assert destino.exists()
    recargado = joblib.load(destino)
    datos = train.cargar_datos().head(3)
    assert recargado.predict_proba(datos[train.VARIABLES]).shape == (3, 2)
