import streamlit as st
import pandas as pd

def generateMenu():
    with st.sidebar:
        st.page_link('app.py', label="Inicio", icon="🏠")
        st.page_link('pages/player.py', label="PlayerHub", icon="⚽")
        st.page_link('pages/team.py', label="StatsLab", icon="📊")

def generateFilters(df):

    categorias_unicas = df["CATEGORIA"].unique().tolist()
    equipos_unicos = df["EQUIPO"].dropna().astype(str).str.strip().unique().tolist()
    anios = df["anio"].dropna().astype(str).str.strip().unique().tolist()

    col1, col2, col3 = st.columns(3)

    with col1:
        categoria = st.selectbox("CATEGORIAS:", options=["Mostrar todos"]+categorias_unicas)

    with col2:
        equipo = st.multiselect("EQUIPOS:", options=equipos_unicos)

    with col3:
        anio = st.selectbox("Año", options=anios, index=0)

    if categoria == "Mostrar todos":
        df_filtrado = df  
    else:
        df_filtrado=df[df["CATEGORIA"]==categoria]
        df_filtrado = df_filtrado.reset_index(drop=True)  # Reinicia los índices

    if anio:
        df_filtrado=df_filtrado[df_filtrado["anio"]==anio]
        df_filtrado = df_filtrado.reset_index(drop=True)  # Reinicia los índices

    return df_filtrado


def getJoinedDataFrame(conn):
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

    df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True)
    df_unido["anio"] = df_unido["FECHA REGISTRO"].dt.year.astype(str)
    df_unido["mes"] = df_unido["FECHA REGISTRO"].dt.month.astype(str)
    df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True).dt.date
    df_unido = df_unido.fillna(0).replace("None", 0)
    df_unido = df_unido[(df_unido != 0).any(axis=1)]  # Elimina filas donde todos los valores son 0

    return df_unido