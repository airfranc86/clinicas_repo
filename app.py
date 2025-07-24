import streamlit as st

st.set_page_config(page_title="Clínica OralTeams - Dashboard", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#2E86C1; font-size:3em;'>🦷 Clínica OralTeams</h1>
<h2 style='text-align:center; color:#1B2631; font-size:1.5em;'>Bienvenido al sistema de métricas y reportes</h2>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; margin-top: 2em;'>
    <p style='font-size:1.2em;'>
        Accede a los dashboards de <b>rentabilidad</b>, <b>pacientes</b> y <b>análisis interactivo</b> usando las pestañas de la barra lateral.<br>
        ¡Visualiza, explora y toma mejores decisiones para tu clínica!
    </p>
</div>
""", unsafe_allow_html=True)

# Si tienes un logo, puedes agregarlo así:
# st.image('ruta/a/logo.png', width=200)