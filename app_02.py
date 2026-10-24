"""Atajo para lanzar semana5/app_02.py desde la raíz del repo:

    uv run streamlit run app_02.py
"""

import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parent / "semana5" / "app_02.py"))
