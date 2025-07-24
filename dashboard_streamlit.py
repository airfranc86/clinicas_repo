import streamlit as st
import pandas as pd
import altair as alt

# Configuración general
st.set_page_config(page_title="Reporte de Rentabilidad y Pacientes", layout="wide")
st.markdown('<h1 style="text-align:center; color:#2E86C1; font-size:2.5em;">🦷 CLÍNICA ORALTEAMS (Métricas) 📊</h1>', unsafe_allow_html=True)

# Leer CSV
csv_path = 'backend/datos.csv'
df = pd.read_csv(csv_path)

# ----------------------- KPIs -----------------------
total_pacientes = len(df)
total_asistencias = df[df['Asistió'].str.lower() == 'sí'].shape[0]
tasa_asistencia = (total_asistencias / total_pacientes * 100) if total_pacientes else 0
ingreso_total = df[df['Asistió'].str.lower() == 'sí']['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float).sum()
pérdida_inasistencia = df[df['Asistió'].str.lower() == 'no']['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float).sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Pacientes", total_pacientes)
col2.metric("Tasa de Asistencia (%)", f"{tasa_asistencia:.1f}%")
col3.metric("Ingreso Total", f"$ {ingreso_total:,.2f}")
col4.metric("Pérdida por Inasistencia", f"$ {pérdida_inasistencia:,.2f}")

st.markdown("---")

# ------------------ Pacientes por especialidad (%) ------------------
pacientes_especialidad = df['Especialidad'].value_counts().reset_index()
pacientes_especialidad.columns = ['Especialidad', 'Cantidad']
pacientes_especialidad['Porcentaje'] = pacientes_especialidad['Cantidad'] / total_pacientes * 100

bar1 = alt.Chart(pacientes_especialidad).mark_bar().encode(
    x=alt.X('Porcentaje:Q', title='Pacientes (%)'),
    y=alt.Y('Especialidad:N', sort='-x'),
    color='Especialidad:N'
).properties(title='Pacientes por Especialidad (%)', height=400)

text1 = alt.Chart(pacientes_especialidad).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Porcentaje:Q',
    y='Especialidad:N',
    text=alt.Text('Porcentaje:Q', format='.1f')
)

st.altair_chart(bar1 + text1, use_container_width=True)

# ------------------ Tasa de asistencia por especialidad (%) ------------------
asistencia_especialidad = df.groupby('Especialidad')['Asistió'].apply(
    lambda x: (x.str.lower() == 'sí').mean() * 100
).reset_index(name='Tasa de Asistencia (%)')

asistencia_especialidad = asistencia_especialidad.sort_values(by='Tasa de Asistencia (%)', ascending=False)

bar2 = alt.Chart(asistencia_especialidad).mark_bar().encode(
    x=alt.X('Tasa de Asistencia (%):Q', title='Tasa de Asistencia (%)'),
    y=alt.Y('Especialidad:N', sort='-x'),
    color='Especialidad:N'
).properties(title='Tasa de Asistencia por Especialidad (%)', height=400)

text2 = alt.Chart(asistencia_especialidad).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Tasa de Asistencia (%):Q',
    y='Especialidad:N',
    text=alt.Text('Tasa de Asistencia (%):Q', format='.1f')
)

st.altair_chart(bar2 + text2, use_container_width=True)

# ------------------ Ingreso total por especialidad ------------------
ingreso_especialidad = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_especialidad['Ingreso'] = ingreso_especialidad['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_especialidad = ingreso_especialidad.groupby('Especialidad')['Ingreso'].sum().reset_index()

bar3 = alt.Chart(ingreso_especialidad).mark_bar().encode(
    x=alt.X('Ingreso:Q', title='Ingreso ($)'),
    y=alt.Y('Especialidad:N', sort='-x'),
    color='Especialidad:N'
).properties(title='Ingreso Total por Especialidad', height=400)

text3 = alt.Chart(ingreso_especialidad).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Ingreso:Q',
    y='Especialidad:N',
    text=alt.Text('Ingreso:Q', format='$,.0f')
)

st.altair_chart(bar3 + text3, use_container_width=True)

# ------------------ Motivos de inasistencia ------------------
motivos = df[df['Asistió'].str.lower() == 'no']['Motivo de Inasistencia'].value_counts().head(3).reset_index()
motivos.columns = ['Motivo', 'Cantidad']
total_inasistencias = motivos['Cantidad'].sum()
motivos['Porcentaje'] = motivos['Cantidad'] / total_inasistencias * 100 if total_inasistencias else 0

bar4 = alt.Chart(motivos).mark_bar().encode(
    x=alt.X('Porcentaje:Q', title='Porcentaje (%)'),
    y=alt.Y('Motivo:N', sort='-x'),
    color='Motivo:N'
).properties(title='Motivos de Inasistencia (%)', height=300)

text4 = alt.Chart(motivos).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Porcentaje:Q',
    y='Motivo:N',
    text=alt.Text('Porcentaje:Q', format='.1f')
)

st.altair_chart(bar4 + text4, use_container_width=True)

# ------------------ Pacientes por doctor (%) ------------------
pacientes_doctor = df['Doctor/a'].value_counts().reset_index()
pacientes_doctor.columns = ['Doctor', 'Cantidad']
pacientes_doctor['Porcentaje'] = pacientes_doctor['Cantidad'] / total_pacientes * 100

bar5 = alt.Chart(pacientes_doctor).mark_bar().encode(
    x=alt.X('Porcentaje:Q', title='Pacientes (%)'),
    y=alt.Y('Doctor:N', sort='-x'),
    color='Doctor:N'
).properties(title='Pacientes por Doctor (%)', height=400)

text5 = alt.Chart(pacientes_doctor).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Porcentaje:Q',
    y='Doctor:N',
    text=alt.Text('Porcentaje:Q', format='.1f')
)

st.altair_chart(bar5 + text5, use_container_width=True)

# ------------------ Ingreso total por doctor ------------------
ingreso_doctor = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_doctor['Ingreso'] = ingreso_doctor['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_doctor = ingreso_doctor.groupby('Doctor/a')['Ingreso'].sum().reset_index()
ingreso_doctor.columns = ['Doctor', 'Ingreso']

bar6 = alt.Chart(ingreso_doctor).mark_bar().encode(
    x=alt.X('Ingreso:Q', title='Ingreso ($)'),
    y=alt.Y('Doctor:N', sort='-x'),
    color='Doctor:N'
).properties(title='Ingreso Total por Doctor (USD)', height=400)

text6 = alt.Chart(ingreso_doctor).mark_text(
    align='left', baseline='middle', dx=3, fontSize=14, color='black'
).encode(
    x='Ingreso:Q',
    y='Doctor:N',
    text=alt.Text('Ingreso:Q', format='$,.0f')
)

st.altair_chart(bar6 + text6, use_container_width=True)

