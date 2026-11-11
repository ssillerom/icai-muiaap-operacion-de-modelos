"""Bloque A - Proyecto y entorno (NO MODIFICAR)."""
import tomllib

from conftest import CLAVE_TEST
from envios.config import RAIZ


def pyproject():
    with open(RAIZ / "pyproject.toml", "rb") as fichero:
        return tomllib.load(fichero)


def nombres(lista):
    return " ".join(lista)


# --- A1: pyproject.toml ---------------------------------------------------------------


def test_a1_dependencias_para_servir_la_api():
    dependencias = nombres(pyproject()["project"]["dependencies"])
    assert "fastapi" in dependencias
    assert "uvicorn" in dependencias


def test_a1_pytest_es_de_desarrollo():
    datos = pyproject()
    assert "pytest" not in nombres(datos["project"]["dependencies"])
    assert "pytest" in nombres(datos["dependency-groups"]["dev"])


def test_a1_comando_entrenar():
    assert pyproject()["project"]["scripts"].get("entrenar") == "envios.train:main"


# --- A2: que se versiona y que no ------------------------------------------------------


def test_a2_gitignore():
    lineas = [linea.strip() for linea in (RAIZ / ".gitignore").read_text(encoding="utf-8").splitlines()]
    for patron in [".venv", "models/", ".env"]:
        assert patron in lineas, f"Falta {patron} en .gitignore"


def test_a2_env_example():
    contenido = (RAIZ / ".env.example").read_text(encoding="utf-8")
    assert "API_KEY=" in contenido
    assert "API_URL=" in contenido
    assert CLAVE_TEST not in contenido
