import streamlit as st
import pandas as pd
import plotly.express as px


# Cargar datos
#df = pd.read_csv("data/mortalidad.csv")
df = pd.read_csv('https://raw.githubusercontent.com/fredyalexr14-lgtm/Actividad4/refs/heads/main/mortalidad.csv')



app = dash.Dash(__name__)

#Mapa: Visualización de la distribución total de muertes por departamento en Colombia para el año 2019.

mapa = px.choropleth(
    df.groupby("DEPARTAMENTO")["MUERTES"].sum().reset_index(),
    locations="DEPARTAMENTO",
    locationmode="geojson-id",
    color="MUERTES",
    #color_continuous_scale=["#f7fbff","#26086b"],  # azul claro a azul oscuro
    color_continuous_scale=["#f7fbff", "#6baed6", "#08306b"],
    #color_continuous_scale="Reds",
    title="Distribución total de muertes por departamento en Colombia para el año 2019"
)





#Gráfico de líneas: Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año.

lineas = px.line(
    df.groupby("MES")["MUERTES"].sum().reset_index(),
    x="MES", y="MUERTES",
    title="Representación del total de muertes por mes en Colombia, mostrando variaciones a lo largo del año."
)

#Gráfico de barras: Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios (códigos X95, agresión con disparo de armas de fuego y casos no especificados).

violentas = df[df["CODIGO"].isin(["X95"])].groupby("CIUDAD")["MUERTES"].sum().nlargest(5).reset_index()
barras = px.bar(violentas, x="CIUDAD", y="MUERTES", title="Visualización de las 5 ciudades más violentas de Colombia, considerando homicidios")

#Gráfico circular: Muestra las 10 ciudades con menor índice de mortalidad.
menores = df.groupby("CIUDAD")["MUERTES"].sum().nsmallest(10).reset_index()
pie = px.pie(menores, names="CIUDAD", values="MUERTES", title="Muestra las 10 ciudades con menor índice de mortalidad")

# Tabla: Listado de las 10 principales causas de muerte en Colombia, incluyendo su código, nombre y total de casos (ordenadas de mayor a menor).
causas = df.groupby(["CODIGO", "CAUSA"])["MUERTES"].sum().nlargest(10).reset_index()

#Gráfico de barras apiladas: Comparación del total de muertes por sexo en cada departamento, para analizar diferencias significativas entre géneros.
sexo_dep = df.groupby(["DEPARTAMENTO","SEXO"])["Total"].sum().reset_index()
sexo_dep = sexo_dep.rename(columns={"DEPARTAMENTO": "Departamento", "SEXO": "Sexo", "Total": "Muertes"})
barras_apiladas = px.bar(
    sexo_dep,
    x="Departamento",
    y="Muertes",
    color="Sexo",
    title="Comparación del total de muertes por sexo en cada departamento, para analizar diferencias significativas entre géneros"
)



#Histograma: Distribución de muertes, agrupando los valores de la variable GRUPO_EDAD1 según los rangos definidos en la tabla de referencia para identificar patrones de mortalidad a lo largo del ciclo de vida.

histograma = px.histogram(df, x="GRUPO_EDAD1", title="Distribución de muertes por grupo de edad")

app.layout = html.Div([
    html.H1("Mortalidad en Colombia - Actividad número 4 "),
    dcc.Graph(figure=mapa),
    dcc.Graph(figure=lineas),
    dcc.Graph(figure=barras),
    dcc.Graph(figure=pie),
    html.H3("10 principales causas de muerte"),
    html.Table([
        html.Tr([html.Th(col) for col in causas.columns])] +
        [html.Tr([html.Td(causas.iloc[i][col]) for col in causas.columns]) for i in range(len(causas))]
    ),
    dcc.Graph(figure=barras_apiladas),
    dcc.Graph(figure=histograma)
])

if __name__ == "__main__":
    app.run_server(debug=True)
