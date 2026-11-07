import streamlit as st
from model import predict
import pandas as pd

st.set_page_config(page_title="S5 · Churn sintético")
st.title("¿Qué cliente podría darse de baja?")
st.caption("Regla docente sintética; no es una probabilidad calibrada.")
simulate_error = st.checkbox("Demo docente: provocar un error de contrato", value=False)
with st.form("churn_form"):
    tenure = st.number_input("Antigüedad (meses)", min_value=0, max_value=120, value=2, step=1)
    spend = st.number_input("Gasto mensual (EUR)", min_value=0.0, max_value=300.0, value=95.0, step=1.0)
    calls = st.number_input("Llamadas a soporte", min_value=0, max_value=20, value=4, step=1)
    annual = st.checkbox("Contrato anual", value=False)
    submitted = st.form_submit_button("Calcular riesgo")

if submitted:
    st.balloons()
    values = {"tenure_months": tenure, "monthly_spend_eur": spend,
              "support_calls": calls, "has_annual_contract": annual}
    if simulate_error:
        values["tenure_months"] = -1
    try:
        result = predict(**values)
    except ValueError:
        st.error("No se pudo calcular el riesgo. Revisa los datos e inténtalo de nuevo.")
    else:
        st.subheader(result["label"])
        st.metric("Score orientativo (0 a 1)", f"{result['risk_score']:.2f}")
        
        score = result["risk_score"]

        if score < 0.35:
            st.success("🟢 Riesgo bajo")
        elif score < 0.70:
            st.warning("🟠 Riesgo medio")
        else:
            st.error("🔴 Riesgo alto")

        st.progress(score)
        st.write(result["explanation"])


        st.divider()
        st.subheader("👤 Perfil del cliente")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Antigüedad:** {tenure} meses")
            st.write(f"**Gasto mensual:** {spend:.2f} €")

        with col2:
            st.write(f"**Llamadas a soporte:** {calls}")
            st.write(f"**Contrato anual:** {'Sí' if annual else 'No'}")
            st.divider()
            st.subheader("📊 Comparación de riesgo")

        chart_data = pd.DataFrame({
            "Escenario": ["Actual", "Con contrato anual"],
            "Riesgo": [
                score,
                alternative["risk_score"]
            ]
        })

        st.bar_chart(
            chart_data,
            x="Escenario",
            y="Riesgo"
        )        

    # Escenario alternativo
    if not annual:
        alternative = predict(
            tenure_months=tenure,
            monthly_spend_eur=spend,
            support_calls=calls,
            has_annual_contract=True
        )

        delta = alternative["risk_score"] - score

        st.divider()
        st.subheader("🧪 ¿Qué pasaría si tuviera contrato anual?")
        st.metric(
            "Nuevo score",
            f"{alternative['risk_score']:.2f}",
            delta=f"{delta:+.2f}"
        )
        
else:
    st.info("Completa el formulario y pulsa Calcular riesgo.")
