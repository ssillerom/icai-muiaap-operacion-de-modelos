import pytest
from env_demo.main import environment_message
@pytest.mark.parametrize("environment", ["dev", "pre", "pro"])
def test_known_environment(environment: str) -> None:
    assert environment.upper() in environment_message(environment)
def test_unknown_environment() -> None:
    with pytest.raises(ValueError, match="APP_ENV"):
        environment_message("local")