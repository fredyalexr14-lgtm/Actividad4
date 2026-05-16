import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Ejemplo mínimo con Streamlit y Plotly")

# Datos de ejemplo
df = pd.DataFrame({
    "Ciudad": ["Bogotá", "Medellín", "Cali", "Barranquilla"],
    "Población": [8000000, 2500000, 2200000, 1200000]
})

# Crear gráfico con Plotly Express
fig = px.bar(df, x="Ciudad", y="Población", title="Población por ciudad")

# Mostrar gráfico en Streamlit
st.plotly_chart(fig)
