"""Estado de sesión de Streamlit aislado para poder probarlo sin Streamlit."""

from __future__ import annotations

from collections.abc import MutableMapping

from model_ui.telemetry import Telemetry

from model_ui.contracts import UiState

LAST_STATE_KEY = "last_state"
TELEMETRY_KEY = "telemetry"
LAST_VALUES_KEY = "last_values"


def initialize_session_state(session_state: MutableMapping[str, object],) -> None:
    
    session_state.setdefault(TELEMETRY_KEY, Telemetry())
    session_state.setdefault(LAST_STATE_KEY, UiState(phase="idle"))
    session_state.setdefault(LAST_VALUES_KEY, {})
    
    """TODO: crea solo las entradas de sesión que todavía no existan."""

   

def clear_last_state(session_state: MutableMapping[str, object]) -> None:
    """TODO: vuelve a idle sin perder la telemetría acumulada."""
    session_state[LAST_STATE_KEY]=UiState(phase="idle")
    session_state[LAST_VALUES_KEY]={}

