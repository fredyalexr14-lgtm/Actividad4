import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Mortalidad en Colombia - Actividad número 4")


# Configuración de la página
st.set_page_config(
    page_title="Mortalidad en Colombia",
    page_icon="📊",
    layout="wide",   # opciones: "centered" o "wide"
    initial_sidebar_state="expanded"  # opciones: "auto", "expanded", "collapsed"
)

# Cargar datos
df = pd.read_csv(
    'https://raw.githubusercontent.com/fredyalexr14-lgtm/Actividad4/refs/heads/main/mortalidad.csv'
)

# Mapa: muertes por departamento
mapa = px.choropleth(
    df.groupby("DEPARTAMENTO")["MUERTES"].sum().reset_index(),
    locations="DEPARTAMENTO",
    locationmode="geojson-id",
    color="MUERTES",
    color_continuous_scale=["#f7fbff", "#6baed6", "#08306b"],
    title="Distribución total de muertes por departamento en Colombia (2019)"
)
st.plotly_chart(mapa)

# Gráfico de líneas: muertes por mes
lineas = px.line(
    df.groupby("MES")["MUERTES"].sum().reset_index(),
    x="MES", y="MUERTES",
    title="Total de muertes por mes en Colombia (2019)"
)
st.plotly_chart(lineas)

# Barras: 5 ciudades más violentas
violentas = df[df["CODIGO"].isin(["X95"])].groupby("CIUDAD")["MUERTES"].sum().nlargest(5).reset_index()
barras = px.bar(violentas, x="CIUDAD", y="MUERTES", title="5 ciudades más violentas (homicidios)")
st.plotly_chart(barras)

# Circular: 10 ciudades con menor mortalidad
menores = df.groupby("CIUDAD")["MUERTES"].sum().nsmallest(10).reset_index()
pie = px.pie(menores, names="CIUDAD", values="MUERTES", title="10 ciudades con menor mortalidad")
st.plotly_chart(pie)

# Tabla: 10 principales causas de muerte
causas = df.groupby(["CODIGO", "CAUSA"])["MUERTES"].sum().nlargest(10).reset_index()
st.subheader("10 principales causas de muerte")
st.dataframe(causas)

# Barras apiladas: muertes por sexo y departamento
sexo_dep = df.groupby(["DEPARTAMENTO","SEXO"])["Total"].sum().reset_index()
sexo_dep = sexo_dep.rename(columns={"DEPARTAMENTO": "Departamento", "SEXO": "Sexo", "Total": "Muertes"})
barras_apiladas = px.bar(
    sexo_dep,
    x="Departamento",
    y="Muertes",
    color="Sexo",
    title="Muertes por sexo en cada departamento"
)
st.plotly_chart(barras_apiladas)

# Histograma: muertes por grupo de edad
histograma = px.histogram(df, x="GRUPO_EDAD1", title="Distribución de muertes por grupo de edad")
st.plotly_chart(histograma)
