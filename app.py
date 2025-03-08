import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Dashboard Cargas Fisicas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

#[connections.gsheets]
url = "https://docs.google.com/spreadsheets/d/1ppYrz95Jrf8Fq91rhQzzh0bR2WE0IaDQafjJv7xTVLg/edit?usp=sharing"

df2 = conn.read(worksheet="DATOS", ttl="15m")
df2 = df2.iloc[:, 2:] ##Elimina las primeras 2 columnas del DataFrame df2, manteniendo el resto.

df = conn.read(worksheet="DATATEST", ttl="15m")
df = df.reset_index(drop=True)  # Reinicia los índices
df.columns = df.iloc[0]  # Usa la primera fila como nombres de columna
df = df[1:]  # Elimina la fila de encabezado original
df = df.reset_index(drop=True)  # Reinicia los índices

##print(df.columns)   # Ver columnas de df
##print(df2.columns)  # Ver columnas de df2

df_unido = pd.merge(df2, df, on=['ID','JUGADOR','CATEGORIA','EQUIPO'], how="inner")

############################################################################################################

#categorias_unicas = df["CATEGORIA"].unique().tolist()  # Obtener elementos únicos
categorias_unicas = df.iloc[:, 2].dropna().astype(str).str.strip().unique().tolist()
equipos_unicos = df["EQUIPO"].dropna().astype(str).str.strip().unique().tolist()

# Reemplazar cualquier valor no válido por NaT (Not a Time) o por un valor por defecto
#df_unido['FECHA REGISTRO'] = pd.to_datetime(df_unido['FECHA REGISTRO'], errors='coerce', format='%d/%m/%Y')
df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True)
#.dt.date
#df_unido["FECHA REGISTRO"] = df_unido["FECHA REGISTRO"].dt.strftime("%d/%m/%Y")

#df["FECHA REGISTRO"] = pd.to_datetime(df["FECHA REGISTRO"], dayfirst=True)  # Asegurar que es tipo datetime
df_unido["anio"] = df_unido["FECHA REGISTRO"].dt.year.astype(str)
df_unido["mes"] = df_unido["FECHA REGISTRO"].dt.month.astype(str)
#df["dia"] = df["FECHA REGISTRO"].dt.day

anios = df_unido["FECHA REGISTRO"].dt.year.dropna().astype(int).sort_values(ascending=False).astype(str).unique().tolist()

df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True).dt.date

df_unido = df_unido.fillna(0).replace("None", 0)
df_unido = df_unido[(df_unido != 0).any(axis=1)]  # Elimina filas donde todos los valores son 0

with st.sidebar:
    st.header("Menú")
    pagina = st.multiselect("SELECCIONE UN DASHBOARD:", options=["Principal", "Perfil Individual", "Comparación",])
    #categoria = st.radio("CATEGORIAS:", options=["Mostrar todos"]+categorias_unicas,index=0)
    #equipo = st.multiselect("EQUIPOS:", options=equipos_unicos)
    #anio = st.selectbox("Año", options=anios, index=0)


# Mostrar las métricas en columnas usando st.columns
col1, col2, col3 = st.columns(3)

with col1:
    categoria = st.selectbox("CATEGORIAS:", options=["Mostrar todos"]+categorias_unicas)

with col2:
    equipo = st.multiselect("EQUIPOS:", options=equipos_unicos)

with col3:
    anio = st.selectbox("Año", options=anios, index=0)


############################################################################################################

if categoria == "Mostrar todos":
    df_filtrado = df_unido  
else:
    df_filtrado=df_unido[df_unido["CATEGORIA"]==categoria]
    df_filtrado = df_filtrado.reset_index(drop=True)  # Reinicia los índices

if anio:
    df_filtrado=df_filtrado[df_filtrado["anio"]==anio]
    df_filtrado = df_filtrado.reset_index(drop=True)  # Reinicia los índices


st.write("""
   # Tablero de datos     
         """)

# Ver columnas duplicadas
##duplicated_columns = df.columns[df.columns.duplicated()]
##print("Columnas duplicadas:", duplicated_columns)
#df_filtrado['FECHA'] = pd.to_datetime(df_filtrado['FECHA'], format='%d/%m/%Y')
st.dataframe(df_unido)


