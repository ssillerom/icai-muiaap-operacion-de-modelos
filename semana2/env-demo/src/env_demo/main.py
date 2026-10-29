import os
from rich import print
VALID_ENVIRONMENTS = {"dev", "pre", "pro"}
def environment_message(environment: str) -> str:
    normalized = environment.strip().lower()
    if normalized not in VALID_ENVIRONMENTS:
        raise ValueError("APP_ENV debe ser dev, pre o pro")
    return f"Entorno activo: {normalized.upper()}"
def main() -> None:
    print(environment_message(os.getenv("APP_ENV", "dev")))
if __name__ == "__main__":
    main()