from datetime import datetime
import streamlit as st

st.title("Entradas y rerun")
st.caption("Última ejecución: " + datetime.now().isoformat(timespec="microseconds"))
tenure = st.number_input("Antigüedad (meses)", min_value=0, max_value=120, value=2, step=1)
spend = st.number_input("Gasto mensual (EUR)", min_value=0.0, max_value=300.0, value=95.0, step=1.0)
calls = st.number_input("Llamadas a soporte", min_value=0, max_value=20, value=4, step=1)
annual = st.checkbox("Contrato anual", value=False)
st.write({"tenure_months": tenure, "monthly_spend_eur": spend,
          "support_calls": calls, "has_annual_contract": annual})
st.info("Aquí solo recogemos valores. No ejecutamos inferencia.")
