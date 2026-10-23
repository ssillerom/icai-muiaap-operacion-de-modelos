Como configurar y ejecutar:

Asegurar que estamos en semana2/stater/wine_quality_project
Si no es así, hacer: cd semana2/starter/wine_quality_project

Una vez en la carpeta adecuada, hacer: uv sync --locked. Las dependencias se instalaran junto al entorno virtual

Para ejecutar main: python (o uv run) .\src\wine_quality\train.py 
Para ejecutar test: python (o uv run) pytest .\tests\test_train.py
Para ruff: uv run ruff check    o    uv run ruff format --check