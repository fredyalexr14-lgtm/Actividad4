---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Actividad 4: Aplicación web interactiva para el análisis de mortalidad en Colombia
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Fredy Alexander Rojas Bautista.
Aplicaciones 1
Direccion URL de la aplicación web:
Direccioón URL al repositorio del proyecto en GitHub:
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Introducción del proyecto:
En la siguiente actividad se va a analisis de datos en python, apoyados en herramientas qye oermiten ver
graficamente los datos con herramientas como DASH  que permite realizar ejecuciones locales y  tabmien se
utilizara herramientas como streamlit  que permite realizar despliegue de aplicaciones y dejarlas publicas,
aprovechando reporitorios como Git-Hub. 

---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
	Objetivo: 
Crear un DashBoard que permita visualizar los datos clave de mortalidad en Colombia, apoyado de las herraminetas
de analisis de datos trabajadas durante el curso.
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Estructura del proyecto: Descripción de las principales carpetas y archivos.

--DASH visualización local
proyecto-aplicacion/
│── app_dash.py                # Contiene todo el codigo el cual grafica y permite las visualizaciones
│── requirements.txt      # Dependencias del proyecto, aquellas librerrias que se requieren
│── data/                 # Carpeta donde se guardan los archivos CSV/XLSX
│    ├── mortalidad.csv
│    ├── Divipola_CE_.csv
│    └── CodigosDeMuerte.csv
││── README.md             # Se documenta todo los requerimientos.


--streamlit para desplegar web
Actividad4/
│── appweb_streamlit.py               # Contiene todo el codigo el cual grafica y permite las visualizaciones
│── requirements.txt      # Dependencias del proyecto, aquellas librerrias que se requieren
│── mortalidad.csv # Carpeta con tus archivos CSV/XLSX
│  ││── README.md             # Se documenta todo los requerimientos.

---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
requirements: Librerías y versiones necesarias para ejecutar la aplicación.

streamlit 
plotly
pandas
dash
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
La aplicación incluye los siguientes elementos visuales:

Mapa: Distribución total de muertes por departamento en Colombia (2019).

Gráfico de líneas: Total de muertes por mes en Colombia.

Gráfico de barras: 5 ciudades más violentas (homicidios, código X95).

Gráfico circular: 10 ciudades con menor índice de mortalidad.

Tabla: 10 principales causas de muerte (código, nombre, total).

Gráfico de barras apiladas: Muertes por sexo en cada departamento.

Histograma: Distribución de muertes según GRUPO_EDAD1


** código (app_dash.py)
#Se importa las librerias a usar
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Cargar datos
df = pd.read_csv("data/mortalidad.csv")

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

---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
***Codigo en streamlit

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


---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Despliegue en streamlit

Crear cuenta en Streamlit y como recomendación se asocia a GIT para qye sea mas facil traer los archivos

Seleccionar New App.

Conectar tu repositorio de GitHub.

Configurar:

Main file path: app_streamlit.py

Python version: 3.11 (o la que uses).

se instalan desde requirements.txt.

Streamlit desplegará y genera la URL
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Software: Herramientas utilizadas:
Python
Dash
streamlit 
plotly
pandas
GitHub
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Instalación: Instrucciones para clonar el repositorio y ejecutar la aplicación localmente.


*Abre el repositorio en GitHub: https://github.com/fredyalexr14-lgtm/Actividad4
*Hacer clic en el botón verde Code (arriba a la derecha).
*Se da en DOnwlosad zip(descarga un archivo descompirmido)
*Se descomprime en la maaquina local  el .zip
*Se ingresa a la carpeta  y se ubica el archivo app_dash.py
*Con bisual estudio code se abre el archivo y se ejecuta.

---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------
Visualizaciones con explicaciones de los resultados: En el documento adjunto.
 Capturas de pantalla acompañadas de una descripción clara de los gráficos interactivos y los hallazgos más relevantes.
---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------

URL GIT: https://github.com/fredyalexr14-lgtm/Actividad4/tree/main
URL Steamlit: https://actividad4-ajxrl3yyygvzs2yltp7jwa.streamlit.app/
https://share.streamlit.io/?utm_source=streamlit&utm_medium=referral&utm_campaign=main&utm_content=-ss-streamlit-io-topright



---------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------






