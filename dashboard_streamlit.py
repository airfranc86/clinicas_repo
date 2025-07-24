import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el CSV
csv_path = 'datos.csv'
df = pd.read_csv(csv_path)

st.set_page_config(page_title="Reporte de Rentabilidad y Pacientes", layout="wide")
st.title("Reporte de Rentabilidad y Pacientes")

# KPIs
total_pacientes = len(df)
total_asistencias = df[df['Asistió'].str.lower() == 'sí'].shape[0]
tasa_asistencia = (total_asistencias / total_pacientes * 100) if total_pacientes else 0
ingreso_total = df[df['Asistió'].str.lower() == 'sí']['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Pacientes", total_pacientes)
col2.metric("Tasa de Asistencia (%)", f"{tasa_asistencia:.1f}%")
col3.metric("Ingreso Total", f"$ {ingreso_total:,.2f}")

st.markdown("---")

# Tabla de pacientes
st.subheader("Tabla de Pacientes")
st.dataframe(df, use_container_width=True)

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
fig4 = px.pie(motivos, values='Porcentaje', names='Motivo', title='Top 3 Motivos de Inasistencia (%)', hole=0.4)
st.plotly_chart(fig4, use_container_width=True)

# Pacientes por doctor (%)
pacientes_doctor = df['Doctor/a'].value_counts().reset_index()
pacientes_doctor.columns = ['Doctor', 'Cantidad']
pacientes_doctor['Porcentaje'] = pacientes_doctor['Cantidad'] / total_pacientes * 100
fig5 = px.bar(pacientes_doctor, y='Doctor', x='Porcentaje', orientation='h', title='Pacientes por Doctor (%)', text='Porcentaje', color='Doctor')
fig5.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
st.plotly_chart(fig5, use_container_width=True) 


# Presiona enter para cerrar el dashboard
st.write("Presiona enter para cerrar el dashboard")
# Cerrar el dashboard con enter
st.stop()