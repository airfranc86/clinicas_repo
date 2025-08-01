import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv('backend/datos.csv')

# Pacientes por doctor
df_pacientes = df['Doctor/a'].value_counts().reset_index()
df_pacientes.columns = ['Doctor', 'Pacientes']

# Ingreso total por doctor
df_ingreso = df[df['Asistió'].str.lower() == 'sí'].copy()
df_ingreso['Ingreso'] = df_ingreso['Costo Aproximado'].replace({'[$,]': ''}, regex=True).astype(float)
df_ingreso = df_ingreso.groupby('Doctor/a')['Ingreso'].sum().reset_index()
df_ingreso.columns = ['Doctor', 'Ingreso']

# Unir los datos
df_interactivo = pd.merge(df_pacientes, df_ingreso, on='Doctor')

st.title('Ingreso vs Pacientes por Doctor')
st.write('Datos para el gráfico interactivo:')
st.dataframe(df_interactivo)

# Selección múltiple de doctor desde la leyenda
doctor_selection = alt.selection_multi(fields=['Doctor'], bind='legend')

# Gráfico Altair: línea y puntos por doctor con selección
line = alt.Chart(df_interactivo).mark_line(point=alt.OverlayMarkDef(filled=True, size=100)).encode(
    x=alt.X('Pacientes:Q', title='Pacientes'),
    y=alt.Y('Ingreso:Q', title='Ingreso (U$)'),
    color=alt.Color('Doctor:N', legend=alt.Legend(orient='bottom', title='Doctor')),
    opacity=alt.condition(doctor_selection, alt.value(1), alt.value(0.15)),
    tooltip=['Doctor', 'Pacientes', 'Ingreso']
).add_selection(
    doctor_selection
).properties(
    width=800,
    height=500,
    background='#0e1117',
    title='Ingreso vs Pacientes por Doctor'
)

st.altair_chart(line, use_container_width=True) 