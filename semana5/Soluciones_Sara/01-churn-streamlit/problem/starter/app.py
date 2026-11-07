"""Starter: conecta una función de inferencia pura con Streamlit."""

from collections.abc import Callable
from typing import Any

from churn_demo.model import ChurnPrediction, predict

Predictor = Callable[..., ChurnPrediction]


def collect_profile(st: Any) -> tuple[bool, dict[str, object]]:
    """Renderiza cuatro widgets dentro de un único formulario."""
    # TODO 1 (alumno): usa st.form("churn_form"), los cuatro widgets con las
    # claves indicadas en el README y st.form_submit_button. El formulario evita
    # inferencias durante cada edición. Compruébalo con el primer test de app.
    # 1 Debe recoger los cuatro datos del cliente dentro de un único formulario.
    with st.form("churn_form"):
        values = {
            "tenure_months": st.slider(
                "Antiguerdad (meses)",
                min_value=0,
                max_value=120,
                value=12,
                key="tenure_months",
            ),
            "monthly_spend_eur": st.number_input(
                "Gasto mensual (€)",
                min_value=0.0,
                max_value=300.0,
                value=60.0,
                key="monthly_spend_eur",
            ),
            "support_calls": st.slider(
                "Llamadas a soporte",
                min_value=0,
                max_value=20,
                value=1,
                key="support_calls",
            ),
            "has_annual_contract": st.checkbox(
                "Contrato anual",
                value=False,
                key="has_annual_contract",
            ),
        }
        submitted = st.form_submit_button(
            "Calcular riesgo"
        )  # Es un booleano, true cuando se pulsa, false cuando no.

    return submitted, values


def render_prediction(st: Any, result: ChurnPrediction) -> None:
    """Muestra etiqueta, score orientativo y explicación."""
    # TODO 3 (alumno): presenta label, risk_score y explanation con componentes
    # Streamlit. No recalcules el score. Compruébalo con el test de presentación.
    st.write("Resultado de la predicción")

    if result["will_churn"]:
        st.warning(result["label"])
    else:
        st.success(result["label"])
    st.write(f"Score: {result['risk_score']}")
    st.write(f"Explicación: {result['explanation']}")


def run_app(st: Any, predictor: Predictor) -> None:
    """Conecta submit, llamada al predictor y actualización visible."""
    # TODO 2 (alumno): llama a collect_profile, ejecuta predictor(**values) solo
    # tras el submit y una única vez; convierte ValueError en un mensaje seguro.
    # Los tests de 0/1 llamadas y de error verifican este contrato.
    submitted, values = collect_profile(
        st
    )  # Recogemos si se ha pulsado el boton y los cuatro valores del formulario
    if not submitted:  # Si el usuario no ha pulsado el botón, se termina la función
        st.info("Introduce los datos y pulsa Calcular riesgo.")
        return

    try:
        result = predictor(
            **values
        )  # Cuando se pulsa, se envían los 4 valores a la función de predicción
    except (
        ValueError
    ):  # Si el predictor rechaza los datos mostramos mensaje para que se revise.
        st.error("No se pudo calcular")
        return
    render_prediction(
        st, result
    )  # St es la interfaz de streamlit y te devuelve result con la prediccion


def main() -> None:
    """Configura la página real y delega el flujo comprobable en run_app."""
    import streamlit as st

    st.set_page_config(page_title="Churn sintético · S5", page_icon="📉")
    st.title("¿Qué cliente podría darse de baja?")
    st.caption("Caso docente sintético; el score no es una probabilidad calibrada.")
    run_app(st, predict)


if __name__ == "__main__":
    main()
