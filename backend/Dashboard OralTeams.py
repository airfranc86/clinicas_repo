import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Leer el CSV
csv_path = 'backend/datos.csv'
df = pd.read_csv(csv_path)

st.set_page_config(page_title="Reporte de Rentabilidad y Pacientes", layout="wide")
st.markdown('<h1 style="text-align:center; color:#2E86C1; font-size:2.5em;">🦷 CLÍNICA ORALTEAMS (Métricas) 📊</h1>', unsafe_allow_html=True)

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
specialidades_unicas = pacientes_especialidad['Especialidad'].unique()
color_palette_especialidad = px.colors.qualitative.Plotly
color_map_especialidad = {esp: color_palette_especialidad[i % len(color_palette_especialidad)] for i, esp in enumerate(specialidades_unicas)}

# Tasa de asistencia por especialidad
asistencia_especialidad = df.groupby('Especialidad')['Asistió'].apply(lambda x: (x.str.lower() == 'sí').mean() * 100).reset_index(name='Tasa de Asistencia (%)')

# Ingreso total por especialidad
ingreso_especialidad = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_especialidad['Ingreso'] = ingreso_especialidad['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_especialidad = ingreso_especialidad.groupby('Especialidad')['Ingreso'].sum().reset_index()

# Motivos de inasistencia (%)
motivos = df[df['Asistió'].str.lower() == 'no']['Motivo de Inasistencia'].value_counts().head(3).reset_index()
motivos.columns = ['Motivo', 'Cantidad']
total_inasistencias = motivos['Cantidad'].sum()
motivos['Porcentaje'] = motivos['Cantidad'] / total_inasistencias * 100 if total_inasistencias else 0

# Pacientes por doctor (%)
pacientes_doctor = df['Doctor/a'].value_counts().reset_index()
pacientes_doctor.columns = ['Doctor', 'Cantidad']
pacientes_doctor['Porcentaje'] = pacientes_doctor['Cantidad'] / total_pacientes * 100
# Definir colores consistentes para los doctores
unique_doctors = pacientes_doctor['Doctor'].unique()
color_palette = px.colors.qualitative.Plotly
color_map = {doctor: color_palette[i % len(color_palette)] for i, doctor in enumerate(unique_doctors)}

# Ingreso total por doctor (sin decimales)
ingreso_doctor = df[df['Asistió'].str.lower() == 'sí'].copy()
ingreso_doctor['Ingreso'] = ingreso_doctor['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
ingreso_doctor = ingreso_doctor.groupby('Doctor/a')['Ingreso'].sum().reset_index()
ingreso_doctor.columns = ['Doctor', 'Ingreso']

# Selectores para gráficos
tipo_grafico_especialidad = st.selectbox(
    "Selecciona el tipo de gráfico para Pacientes por Especialidad",
    ("Barras", "Dispersión"),
    key="grafico_especialidad"
)
if tipo_grafico_especialidad == "Barras":
    bar1 = alt.Chart(pacientes_especialidad).mark_bar().encode(
        x=alt.X('Porcentaje:Q', title='Pacientes (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10, values=list(range(0, 101, 10)), gridColor='gray', gridDash=[2,2], labelColor='white', titleColor='white')),
        y=alt.Y('Especialidad:N', sort='-x'),
        color=alt.Color('Especialidad:N', legend=alt.Legend(orient='right', title='Especialidad', symbolType='circle'))
    ).properties(title='Pacientes por Especialidad (%)', height=400)
    text1 = alt.Chart(pacientes_especialidad).mark_text(
        align='left', baseline='middle', dx=3, fontSize=14, color='white'
    ).encode(
        x='Porcentaje:Q',
        y='Especialidad:N',
        color=alt.Color('Especialidad:N', legend=alt.Legend(orient='right', title='Especialidad', symbolType='circle')),
        text=alt.Text('Porcentaje:Q', format='.2f%')
    )
    st.altair_chart(bar1 + text1, use_container_width=True)
elif tipo_grafico_especialidad == "Dispersión":
    scatter1 = alt.Chart(pacientes_especialidad).mark_circle(size=600, opacity=0.85, stroke='white', strokeWidth=4).encode(
        x=alt.X('Porcentaje:Q', title='Pacientes (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10)),
        y=alt.Y('Especialidad:N', sort='-x'),
        color='Especialidad:N'
    ).properties(title='Pacientes por Especialidad (Dispersión)', height=400)
    rule1 = alt.Chart(pacientes_especialidad).mark_rule(color='gray', strokeDash=[4,2], opacity=0.5).encode(
        y='Especialidad:N'
    )
    text_scatter1 = alt.Chart(pacientes_especialidad).mark_text(
        align='center', baseline='middle', fontSize=12, color='black', fontWeight='bold'
    ).encode(
        x='Porcentaje:Q',
        y='Especialidad:N',
        text=alt.Text('Porcentaje:Q', format='.0f')
    )
    st.altair_chart(rule1 + scatter1 + text_scatter1, use_container_width=True)

# Tasa de asistencia por especialidad (%)
tipo_grafico_asistencia = st.selectbox(
    "Selecciona el tipo de gráfico para Tasa de Asistencia por Especialidad",
    ("Barras", "Dispersión"),
    key="grafico_asistencia"
)
if tipo_grafico_asistencia == "Barras":
    bar2 = alt.Chart(asistencia_especialidad).mark_bar().encode(
        x=alt.X('Tasa de Asistencia (%):Q', title='Tasa de Asistencia (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10, values=list(range(0, 101, 10)), gridColor='gray', gridDash=[2,2], labelColor='white', titleColor='white')),
        y=alt.Y('Especialidad:N', sort='-x'),
        color=alt.Color('Especialidad:N', legend=alt.Legend(orient='right', title='Especialidad', symbolType='circle'))
    ).properties(title='Tasa de Asistencia por Especialidad (%)', height=400)
    text2 = alt.Chart(asistencia_especialidad).mark_text(
        align='left', baseline='middle', dx=3, fontSize=14, color='white'
    ).encode(
        x='Tasa de Asistencia (%):Q',
        y='Especialidad:N',
        color=alt.Color('Especialidad:N', legend=alt.Legend(orient='right', title='Especialidad', symbolType='circle')),
        text=alt.Text('Tasa de Asistencia (%):Q', format='.2f%')
    )
    st.altair_chart(bar2 + text2, use_container_width=True)
elif tipo_grafico_asistencia == "Dispersión":
    scatter2 = alt.Chart(asistencia_especialidad).mark_circle(size=600, opacity=0.85, stroke='white', strokeWidth=4).encode(
        x=alt.X('Tasa de Asistencia (%):Q', title='Tasa de Asistencia (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10)),
        y=alt.Y('Especialidad:N', sort='-x'),
        color='Especialidad:N'
    ).properties(title='Tasa de Asistencia por Especialidad (Dispersión)', height=400)
    rule2 = alt.Chart(asistencia_especialidad).mark_rule(color='gray', strokeDash=[4,2], opacity=0.5).encode(
        y='Especialidad:N'
    )
    text_scatter2 = alt.Chart(asistencia_especialidad).mark_text(
        align='center', baseline='middle', fontSize=12, color='black', fontWeight='bold'
    ).encode(
        x='Tasa de Asistencia (%):Q',
        y='Especialidad:N',
        text=alt.Text('Tasa de Asistencia (%):Q', format='.0f')
    )
    st.altair_chart(rule2 + scatter2 + text_scatter2, use_container_width=True)

# Ingreso total por especialidad
tipo_grafico_ingreso_esp = st.selectbox(
    "Selecciona el tipo de gráfico para Ingreso Total por Especialidad",
    ("Barras", "Dispersión"),
    key="grafico_ingreso_esp"
)
if tipo_grafico_ingreso_esp == "Barras":
    bar3 = alt.Chart(ingreso_especialidad).mark_bar().encode(
        x=alt.X('Ingreso:Q', title='Ingreso ($)', axis=alt.Axis(grid=True, tickMinStep=10, gridColor='gray', gridDash=[2,2], labelColor='white', titleColor='white')),
        y=alt.Y('Especialidad:N', sort='-x'),
        color=alt.Color('Especialidad:N', legend=alt.Legend(orient='right'))
    ).properties(title='Ingreso Total por Especialidad', height=400)
    text3 = alt.Chart(ingreso_especialidad).mark_text(
        align='left', baseline='middle', dx=3, fontSize=14, color='white'
    ).encode(
        x='Ingreso:Q',
        y='Especialidad:N',
        text=alt.Text('Ingreso:Q', format='$,.2f')
    )
    st.altair_chart(bar3 + text3, use_container_width=True)
elif tipo_grafico_ingreso_esp == "Dispersión":
    scatter3 = alt.Chart(ingreso_especialidad).mark_circle(size=200).encode(
        x=alt.X('Ingreso:Q', title='Ingreso ($)', axis=alt.Axis(grid=True, tickMinStep=10)),
        y=alt.Y('Especialidad:N', sort='-x'),
        color='Especialidad:N'
    ).properties(title='Ingreso Total por Especialidad (Dispersión)', height=400)
    text_scatter3 = alt.Chart(ingreso_especialidad).mark_text(
        align='center', baseline='middle', fontSize=18, color='black', fontWeight='bold'
    ).encode(
        x='Ingreso:Q',
        y='Especialidad:N',
        text=alt.Text('Ingreso:Q', format='$,.2f')
    )
    st.altair_chart(scatter3 + text_scatter3, use_container_width=True)

# Motivos de inasistencia (solo pastel)
fig4 = px.pie(motivos, values='Porcentaje', names='Motivo', title='Motivos de Inasistencia (%)', color='Motivo', hole=0.4)
fig4.update_traces(textinfo='percent+label')
st.plotly_chart(fig4, use_container_width=True)

# Pacientes por doctor (%)
tipo_grafico_doctor = st.selectbox(
    "Selecciona el tipo de gráfico para Pacientes por Doctor",
    ("Barras", "Dispersión"),
    key="grafico_doctor"
)
if tipo_grafico_doctor == "Barras":
    bar5 = alt.Chart(pacientes_doctor).mark_bar().encode(
        x=alt.X('Porcentaje:Q', title='Pacientes (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10, values=list(range(0, 101, 10)), gridColor='gray', gridDash=[2,2], labelColor='white', titleColor='white')),
        y=alt.Y('Doctor:N', sort='-x'),
        color=alt.Color('Doctor:N', legend=alt.Legend(orient='right', title='Doctor', symbolType='circle'))
    ).properties(title='Pacientes por Doctor (%)', height=400)
    text5 = alt.Chart(pacientes_doctor).mark_text(
        align='left', baseline='middle', dx=3, fontSize=14, color='white'
    ).encode(
        x='Porcentaje:Q',
        y='Doctor:N',
        color=alt.Color('Doctor:N', legend=alt.Legend(orient='right', title='Doctor', symbolType='circle')),
        text=alt.Text('Porcentaje:Q', format='.2f%')
    )
    st.altair_chart(bar5 + text5, use_container_width=True)
elif tipo_grafico_doctor == "Dispersión":
    scatter5 = alt.Chart(pacientes_doctor).mark_circle(size=600, opacity=0.85, stroke='white', strokeWidth=4).encode(
        x=alt.X('Porcentaje:Q', title='Pacientes (%)', scale=alt.Scale(domain=[0, 100]), axis=alt.Axis(grid=True, tickMinStep=10)),
        y=alt.Y('Doctor:N', sort='-x'),
        color='Doctor:N'
    ).properties(title='Pacientes por Doctor (Dispersión)', height=400)
    rule5 = alt.Chart(pacientes_doctor).mark_rule(color='gray', strokeDash=[4,2], opacity=0.5).encode(
        y='Doctor:N'
    )
    text_scatter5 = alt.Chart(pacientes_doctor).mark_text(
        align='center', baseline='middle', fontSize=12, color='black', fontWeight='bold'
    ).encode(
        x='Porcentaje:Q',
        y='Doctor:N',
        text=alt.Text('Porcentaje:Q', format='.0f')
    )
    st.altair_chart(rule5 + scatter5 + text_scatter5, use_container_width=True)

# Ingreso total por doctor
tipo_grafico_ingreso_doc = st.selectbox(
    "Selecciona el tipo de gráfico para Ingreso Total por Doctor",
    ("Barras", "Dispersión"),
    key="grafico_ingreso_doc"
)
if tipo_grafico_ingreso_doc == "Barras":
    bar6 = alt.Chart(ingreso_doctor).mark_bar().encode(
        x=alt.X('Ingreso:Q', title='Ingreso ($)', axis=alt.Axis(grid=True, tickMinStep=10, gridColor='gray', gridDash=[2,2], labelColor='white', titleColor='white')),
        y=alt.Y('Doctor:N', sort='-x'),
        color=alt.Color('Doctor:N', legend=alt.Legend(orient='right'))
    ).properties(title='Ingreso Total por Doctor (USD)', height=400)
    text6 = alt.Chart(ingreso_doctor).mark_text(
        align='left', baseline='middle', dx=3, fontSize=14, color='white'
    ).encode(
        x='Ingreso:Q',
        y='Doctor:N',
        text=alt.Text('Ingreso:Q', format='$,.2f')
    )
    st.altair_chart(bar6 + text6, use_container_width=True)
elif tipo_grafico_ingreso_doc == "Dispersión":
    scatter6 = alt.Chart(ingreso_doctor).mark_circle(size=200).encode(
        x=alt.X('Ingreso:Q', title='Ingreso ($)', axis=alt.Axis(grid=True, tickMinStep=10)),
        y=alt.Y('Doctor:N', sort='-x'),
        color='Doctor:N'
    ).properties(title='Ingreso Total por Doctor (Dispersión)', height=400)
    text_scatter6 = alt.Chart(ingreso_doctor).mark_text(
        align='center', baseline='middle', fontSize=18, color='black', fontWeight='bold'
    ).encode(
        x='Ingreso:Q',
        y='Doctor:N',
        text=alt.Text('Ingreso:Q', format='$,.2f')
    )
    st.altair_chart(scatter6 + text_scatter6, use_container_width=True)