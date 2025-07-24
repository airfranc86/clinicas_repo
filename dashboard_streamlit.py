import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el CSV
csv_path = 'backend/datos.csv'
df = pd.read_csv(csv_path)

st.set_page_config(page_title="Reporte de Rentabilidad y Pacientes", layout="wide")
st.markdown('<h1 style="text-align:center; color:#2E86C1; font-size:2.5em;">🦷 CLÍNICA ORALTEAMS 📊</h1>', unsafe_allow_html=True)

# KPIs
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

# Pacientes por especialidad (%)
pacientes_especialidad = df['Especialidad'].value_counts().reset_index()
pacientes_especialidad.columns = ['Especialidad', 'Cantidad']
pacientes_especialidad['Porcentaje'] = pacientes_especialidad['Cantidad'] / total_pacientes * 100
fig1 = px.bar(pacientes_especialidad, y='Especialidad', x='Porcentaje', orientation='h', title='Pacientes por Especialidad (%)', text='Porcentaje', color='Especialidad')
fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig1, use_container_width=True)

# Tasa de asistencia por especialidad
asistencia_especialidad = df.groupby('Especialidad')['Asistió'].apply(lambda x: (x.str.lower() == 'sí').mean() * 100).reset_index(name='Tasa de Asistencia (%)')
fig2 = px.bar(asistencia_especialidad, y='Especialidad', x='Tasa de Asistencia (%)', orientation='h', title='Tasa de Asistencia por Especialidad (%)', text='Tasa de Asistencia (%)', color='Especialidad')
fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig2, use_container_width=True)

# Ingreso total por especialidad
ingreso_especialidad = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_especialidad['Ingreso'] = ingreso_especialidad['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_especialidad = ingreso_especialidad.groupby('Especialidad')['Ingreso'].sum().reset_index()
fig3 = px.bar(ingreso_especialidad, y='Especialidad', x='Ingreso', orientation='h', title='Ingreso Total por Especialidad', text='Ingreso', color='Especialidad')
fig3.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
st.plotly_chart(fig3, use_container_width=True)

# Top 3 motivos de inasistencia (%)
motivos = df[df['Asistió'].str.lower() == 'no']['Motivo de Inasistencia'].value_counts().head(3).reset_index()
motivos.columns = ['Motivo', 'Cantidad']
total_inasistencias = motivos['Cantidad'].sum()
motivos['Porcentaje'] = motivos['Cantidad'] / total_inasistencias * 100 if total_inasistencias else 0
fig4 = px.scatter(motivos, y='Motivo', x='Porcentaje', title='Top 3 Motivos de Inasistencia (%)', text='Porcentaje', color='Motivo', size='Porcentaje', size_max=40)
fig4.update_traces(texttemplate='%{text:.1f}%', textposition='middle right', marker=dict(line=dict(width=2, color='DarkSlateGrey')))
st.plotly_chart(fig4, use_container_width=True)

# Pacientes por doctor (%)
pacientes_doctor = df['Doctor/a'].value_counts().reset_index()
pacientes_doctor.columns = ['Doctor', 'Cantidad']
pacientes_doctor['Porcentaje'] = pacientes_doctor['Cantidad'] / total_pacientes * 100
# Definir colores consistentes para los doctores
unique_doctors = pacientes_doctor['Doctor'].unique()
color_palette = px.colors.qualitative.Plotly
color_map = {doctor: color_palette[i % len(color_palette)] for i, doctor in enumerate(unique_doctors)}
fig5 = px.bar(pacientes_doctor, y='Doctor', x='Porcentaje', orientation='h', title='Pacientes por Doctor (%)', text='Porcentaje', color='Doctor', color_discrete_map=color_map)
fig5.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig5, use_container_width=True)

# Ingreso total por doctor (sin decimales)
ingreso_doctor = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_doctor['Ingreso'] = ingreso_doctor['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_doctor = ingreso_doctor.groupby('Doctor/a')['Ingreso'].sum().reset_index()
ingreso_doctor.columns = ['Doctor', 'Ingreso']
fig6 = px.scatter(ingreso_doctor, y='Doctor', x='Ingreso', title='Ingreso Total por Doctor (USD)', text='Ingreso', color='Doctor', size='Ingreso', size_max=20, color_discrete_map=color_map)
fig6.update_traces(texttemplate='$%{text:,.0f}', textposition='middle right', marker=dict(line=dict(width=2, color='DarkSlateGrey')))
st.plotly_chart(fig6, use_container_width=True) 
