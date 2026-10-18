"""Interfaz Streamlit "Registro fósil": el riesgo de baja como riesgo de extinción.

Estética de museo de historia natural. La lógica de inferencia vive en
`model.py`; este archivo solo presenta datos, llama al contrato y traduce
errores a mensajes comprensibles.
"""

from html import escape
from math import cos, exp, log, pi, sin

import streamlit as st

from model import predict

st.set_page_config(page_title="Registro fósil · Churn S5", page_icon="🦴", layout="wide")

def render_html(markup: str) -> None:
    """Inyecta HTML/CSS propio con `st.markdown`.

    `st.html` sanitiza con DOMPurify y descarta `<style>` y `<svg>`. Se compacta
    en una línea para que Markdown no interprete la sangría como bloque de código.
    """

    st.markdown(" ".join(line.strip() for line in markup.splitlines()), unsafe_allow_html=True)


# --------------------------------------------------------------------------- #
# Estilo: sala de museo en penumbra, tipografía serif y acentos de latón.
# --------------------------------------------------------------------------- #
render_html(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&family=Manrope:wght@400;500;600&display=swap');

:root {
  --night: #11100e;
  --panel: #191714;
  --bone: #ece4d3;
  --muted: #968e7f;
  --brass: #c8a96a;
  --rust: #c2603f;
  --sage: #8fa77a;
  --line: rgba(236, 228, 211, 0.12);
}

.stApp {
  background:
    radial-gradient(1000px 520px at 50% -12%, rgba(200, 169, 106, 0.13), transparent 65%),
    radial-gradient(700px 500px at 100% 100%, rgba(194, 96, 63, 0.08), transparent 60%),
    var(--night);
  color: var(--bone);
}
.stApp::before {   /* grano de papel */
  content: ""; position: fixed; inset: 0; pointer-events: none; opacity: .05;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence baseFrequency='.85' numOctaves='3'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
}
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2.4rem; max-width: 1160px; }
p, label, span, div, li { font-family: 'Manrope', sans-serif; }

.mono { font-family: 'IBM Plex Mono', monospace !important; text-transform: uppercase; letter-spacing: .18em; font-size: .68rem; color: var(--muted); }
.serif { font-family: 'Cormorant Garamond', serif !important; }

/* --- Cabecera --- */
.hero { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 2rem;
  padding-bottom: 1.6rem; margin-bottom: 2rem; border-bottom: 1px solid var(--line); animation: rise .9s ease-out both; }
.hero h1 { font-family: 'Cormorant Garamond', serif !important; font-weight: 400; color: var(--bone);
  font-size: clamp(2.8rem, 6.5vw, 5.4rem); line-height: .95; margin: .7rem 0 1rem; letter-spacing: -.01em; }
.hero h1 em { color: var(--brass); }
.hero p { color: var(--muted); max-width: 50ch; margin: 0; line-height: 1.6; }
.hero .ammonite { width: 150px; opacity: .9; animation: turn 60s linear infinite; }
@media (max-width: 700px) { .hero { grid-template-columns: 1fr; } .hero .ammonite { display: none; } }

/* --- Paneles --- */
[data-testid="stForm"], .card {
  background: linear-gradient(180deg, rgba(255,255,255,.025), rgba(255,255,255,0)), var(--panel);
  border: 1px solid var(--line); border-radius: 4px; padding: 1.7rem 1.7rem 1.3rem;
  box-shadow: 0 40px 80px -50px rgba(0,0,0,.9);
}
.card-head { display: flex; justify-content: space-between; align-items: baseline;
  border-bottom: 1px solid var(--line); padding-bottom: .7rem; margin-bottom: 1.2rem; }
.card-head .t { font-family: 'Cormorant Garamond', serif; font-size: 1.45rem; color: var(--bone); }

[data-testid="stForm"] label p { color: var(--bone) !important; font-weight: 500; font-size: .92rem; }
/* Llevar el color primario de Streamlit (rojo) hacia el latón sin tocar el tema global. */
[data-testid="stSlider"] [role="group"],
[data-testid="stCheckbox"] label > div:first-of-type { filter: hue-rotate(38deg) saturate(.55) brightness(1.05); }

[data-testid="stFormSubmitButton"], [data-testid="stFormSubmitButton"] > * { width: 100%; }
[data-testid="stFormSubmitButton"] button {
  width: 100%; margin-top: .8rem; padding: .8rem 1rem; border-radius: 2px;
  background: transparent; border: 1px solid var(--brass); transition: all .25s ease;
}
[data-testid="stFormSubmitButton"] button p { font-family: 'IBM Plex Mono', monospace !important;
  text-transform: uppercase; letter-spacing: .22em; font-size: .78rem; color: var(--brass) !important; }
[data-testid="stFormSubmitButton"] button:hover { background: var(--brass); }
[data-testid="stFormSubmitButton"] button:hover p { color: var(--night) !important; }

[data-testid="stExpander"] details { border: 1px solid var(--line); border-radius: 2px; background: transparent; }
[data-testid="stExpander"] summary p { font-size: .85rem; color: var(--muted); }

/* --- Ficha de resultado --- */
.verdict { animation: rise .7s ease-out both; }
.headline { display: flex; justify-content: space-between; align-items: flex-end; gap: 1rem; flex-wrap: wrap; }
.headline .label { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; line-height: 1; }
.headline .label i { display: block; font-size: 1rem; color: var(--muted); margin-top: .5rem; font-style: italic; }
.headline .score { font-family: 'Cormorant Garamond', serif; font-size: 4.2rem; line-height: .85; color: var(--bone); text-align: right; }
.strata { margin: 1.6rem 0 .4rem; }
.strata .marker { animation: slide 1.3s cubic-bezier(.2,.8,.2,1) both; }

.factors { margin-top: 1.4rem; border-top: 1px solid var(--line); }
.factor { display: grid; grid-template-columns: 1fr 64px 90px; gap: 1rem; align-items: center;
  padding: .6rem 0; border-bottom: 1px solid var(--line); font-size: .88rem; animation: rise .5s ease-out both; }
.factor .d { font-family: 'IBM Plex Mono', monospace; text-align: right; font-size: .82rem; }
.factor .bar { height: 3px; background: rgba(236,228,211,.08); }
.factor .bar div { height: 100%; animation: grow 1s ease-out both; }
.factor.up .d { color: var(--rust); }   .factor.up .bar div { background: var(--rust); }
.factor.down .d { color: var(--sage); } .factor.down .bar div { background: var(--sage); }
.factor.zero .d { color: var(--muted); }

/* --- Estados vacío y error --- */
.placeholder { text-align: center; padding: 3rem 1.5rem; }
.placeholder svg { width: 120px; opacity: .55; animation: turn 40s linear infinite; }
.placeholder .t { font-family: 'Cormorant Garamond', serif; font-size: 1.7rem; color: var(--bone); margin: 1.2rem 0 .4rem; font-style: italic; }
.placeholder p { color: var(--muted); margin: 0 auto; max-width: 36ch; }

.foot { margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--line); text-align: center; }

@keyframes rise  { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@keyframes turn  { to { transform: rotate(360deg); } }
@keyframes grow  { from { width: 0; } }
@keyframes slide { from { transform: translateX(0); } }
</style>
"""
)


# --------------------------------------------------------------------------- #
# Piezas de presentación (no contienen lógica de negocio).
# --------------------------------------------------------------------------- #
def ammonite_svg(size: int = 200) -> str:
    """Amonite a línea: espiral logarítmica con costillas entre vueltas."""

    c, turns, growth = size / 2, 3.2, 2.15
    b = log(growth) / (2 * pi)
    a = (size * 0.46) / exp(b * turns * 2 * pi)

    def point(theta: float) -> tuple[float, float]:
        r = a * exp(b * theta)
        return c + r * cos(theta), c + r * sin(theta)

    steps = 260
    spiral = " ".join(
        f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}"
        for i, (x, y) in enumerate(point(turns * 2 * pi * i / steps) for i in range(steps + 1))
    )
    ribs = ""
    for k in range(int((turns - 1) * 30)):
        theta = 2 * pi + k * (2 * pi / 30)
        (x1, y1), (x2, y2) = point(theta), point(theta - 2 * pi)
        ribs += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>'
    return (
        f'<svg viewBox="0 0 {size} {size}" fill="none" stroke="#c8a96a" stroke-width="1">'
        f'<path d="{spiral}" stroke-width="1.4"/><g opacity=".55">{ribs}</g></svg>'
    )


def strata_svg(score: float, color: str) -> str:
    """Franja estratigráfica: el umbral 0,50 es el límite K–Pg (la extinción)."""

    width, x = 600, 600 * score
    bands = ["#2b2620", "#342d24", "#2a241d", "#3a3127", "#2e2821", "#3d3329"]
    layers = "".join(
        f'<rect x="0" y="{34 + i * 11}" width="{width}" height="11" fill="{fill}"/>'
        for i, fill in enumerate(bands)
    )
    return f"""
<svg class="strata" viewBox="0 -8 {width} 144" width="100%">
  <defs>
    <linearGradient id="ash" x1="0" x2="1">
      <stop offset=".5" stop-color="#c2603f" stop-opacity="0"/>
      <stop offset="1" stop-color="#c2603f" stop-opacity=".45"/>
    </linearGradient>
  </defs>
  {layers}
  <rect x="0" y="34" width="{width}" height="66" fill="url(#ash)"/>
  <line x1="300" y1="22" x2="300" y2="108" stroke="#c8a96a" stroke-dasharray="3 3"/>
  <text x="300" y="14" text-anchor="middle" fill="#c8a96a" font-family="IBM Plex Mono" font-size="11" letter-spacing="2">LÍMITE K–Pg · 0,50</text>
  <text x="0" y="124" fill="#968e7f" font-family="IBM Plex Mono" font-size="11" letter-spacing="2">MESOZOICO · PERMANENCIA</text>
  <text x="{width}" y="124" text-anchor="end" fill="#968e7f" font-family="IBM Plex Mono" font-size="11" letter-spacing="2">EXTINCIÓN · BAJA</text>
  <g class="marker" style="transform: translateX({x:.1f}px)">
    <line x1="0" y1="26" x2="0" y2="108" stroke="{color}" stroke-width="2"/>
    <path d="M -6 20 L 0 28 L 6 20 Z" fill="{color}"/>
  </g>
</svg>"""


def factor_rows(explanation: str) -> str:
    """Trocea la explicación del contrato en filas; si cambia el formato, la muestra tal cual."""

    body = explanation.removeprefix("Regla docente: ").split(". Score", 1)[0]
    factors = [f.strip() for f in body.split(";") if ":" in f]
    if not factors:
        return f'<p style="color:var(--muted)">{escape(explanation)}</p>'
    rows = []
    for i, factor in enumerate(factors):
        text, _, delta = factor.rpartition(":")
        delta = delta.strip()
        try:
            magnitude = abs(float(delta.replace(",", ".")))
        except ValueError:
            magnitude = 0.0
        kind = "zero" if magnitude == 0 else "down" if delta.startswith("-") else "up"
        rows.append(
            f'<div class="factor {kind}" style="animation-delay:{0.07 * i:.2f}s">'
            f"<span>{escape(text[:1].upper() + text[1:])}</span>"
            f'<span class="d">{escape(delta)}</span>'
            f'<div class="bar"><div style="width:{min(magnitude / 0.30, 1) * 100:.0f}%"></div></div></div>'
        )
    return f'<div class="factors">{"".join(rows)}</div>'


# --------------------------------------------------------------------------- #
# Página
# --------------------------------------------------------------------------- #
render_html(
    f"""
<div class="hero">
  <div>
    <div class="mono">Operación de Modelos · Sala S5 · Colección de clientes</div>
    <h1>¿Sobrevivirá<br>al <em>impacto</em>?</h1>
    <p>Cataloga un ejemplar y sitúalo en el registro fósil: a un lado, la permanencia;
       al otro, la extinción. Regla docente sintética: el score es orientativo,
       no una probabilidad calibrada.</p>
  </div>
  <div class="ammonite">{ammonite_svg()}</div>
</div>
"""
)

left, right = st.columns([5, 7], gap="large")

with left:
    with st.form("churn_form", border=False):
        render_html(
            '<div class="card-head"><span class="t">Ficha del ejemplar</span>'
            '<span class="mono">Nº CH-0004</span></div>'
        )
        tenure = st.slider("Antigüedad (meses)", min_value=0, max_value=120, value=2, step=1)
        spend = st.slider("Gasto mensual (EUR)", min_value=0.0, max_value=300.0, value=95.0, step=1.0)
        calls = st.slider("Llamadas a soporte", min_value=0, max_value=20, value=4, step=1)
        annual = st.toggle("Contrato anual", value=False)
        submitted = st.form_submit_button("Datar ejemplar")

    with st.expander("Laboratorio docente"):
        simulate_error = st.checkbox("Provocar un error de contrato (tenure = -1)", value=False)

with right:
    if submitted:
        values = {"tenure_months": tenure, "monthly_spend_eur": spend,
                  "support_calls": calls, "has_annual_contract": annual}
        if simulate_error:
            values["tenure_months"] = -1
        try:
            with st.spinner("Datando el ejemplar…"):
                result = predict(**values)
        except ValueError:
            render_html(
                f'<div class="card placeholder">{ammonite_svg(120)}'
                '<div class="t">Ejemplar no catalogable</div>'
                "<p>No se pudo calcular el riesgo. Revisa los datos e inténtalo de nuevo.</p></div>"
            )
            st.error("Error de contrato: los datos enviados no cumplen las reglas de entrada.")
        else:
            churn = result["will_churn"]
            color = "#c2603f" if churn else "#8fa77a"
            reading = (
                "Por encima del límite: conviene actuar."
                if churn
                else "Por debajo del límite: el ejemplar persiste."
            )
            render_html(
                f"""
<div class="card verdict">
  <div class="card-head"><span class="t">Datación</span><span class="mono">Score orientativo · 0 a 1</span></div>
  <div class="headline">
    <div class="label" style="color:{color}">{escape(result["label"])}<i>{reading}</i></div>
    <div class="score">{f"{result['risk_score']:.2f}".replace(".", ",")}</div>
  </div>
  {strata_svg(result["risk_score"], color)}
  <div class="mono" style="margin-top:1.4rem">Estratigrafía de factores</div>
  {factor_rows(result["explanation"])}
</div>
"""
            )
            with st.expander("Registro completo del contrato"):
                st.write(result["explanation"])
    else:
        render_html(
            f"""
<div class="card placeholder">
  {ammonite_svg(120)}
  <div class="t">Vitrina vacía</div>
  <p>Completa la ficha del ejemplar y pulsa <b>Datar ejemplar</b> para situarlo en el registro.</p>
</div>
"""
        )

render_html(
    '<div class="foot mono">Regla sintética con fines docentes · '
    "no es un modelo entrenado ni una probabilidad calibrada</div>"
)
