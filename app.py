import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Clínica OralTeams - Dashboard", layout="wide")

# Si tienes un logo local, descomenta la siguiente línea y pon el nombre correcto del archivo:
# st.image('backend/logo.png', width=180)

st.title("🦷 Clínica OralTeams")
st.subheader("Bienvenido al sistema de métricas y reportes")

st.write("""
Accede a los dashboards de **rentabilidad**, **pacientes** y **análisis interactivo** usando las pestañas de la barra lateral.

¡Visualiza, explora y toma mejores decisiones !
""")

# Pie de página
st.markdown(f"""
---
<div style='text-align:center; font-size:0.95em; color:#888;'>
    {datetime.now().strftime('%d/%m/%Y')}<br>
    Registrado para <b>Clínica OralTeams</b>.<br>
    <b>Prohibida la transferencia de datos o cualquier otro uso fuera de norma por la privacidad de la información.</b>
</div>
""", unsafe_allow_html=True)
