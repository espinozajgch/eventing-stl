import streamlit as st
import pandas as pd
from fpdf import FPDF
import numpy as np
import requests

def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Este es un informe generado en Streamlit", ln=True, align="C")
    return pdf

def generateMenu():
    with st.sidebar:
        st.page_link('app.py', label="Inicio", icon="🏠")
        st.page_link('pages/player.py', label="PlayerHub", icon="⚽")
        #st.page_link('pages/team.py', label="StatsLab", icon="📊")
        #st.page_link('pages/perfil.py', label="Perfil", icon="📊")

def generateFilters(df):

    ##anios = df["anio"].dropna().astype(str).str.strip().unique().tolist()
    df_filtrado = pd.DataFrame() 
    default_option = "Todos";

    category_col, team_col, position_col, nationality_col, player_col = st.columns(5)

    with category_col:
        category_list = df["CATEGORIA"].dropna().astype(str).str.strip().unique().tolist()
        category_list.sort()
        category = st.selectbox("CATEGORIA:", options=[default_option]+category_list, index=0)

    with team_col:

        if category == default_option:
            team_list = df["EQUIPO"]
        else:
            team_list = df[df['CATEGORIA'] == category]["EQUIPO"]
    
        team_list = team_list.dropna().astype(str).str.strip().unique().tolist()
        team_list.sort()
        team = st.selectbox("EQUIPO:", options=[default_option]+team_list)
    
    with position_col:
        position_list = df

        if category != default_option:
            position_list = position_list[position_list['CATEGORIA'] == category]

        if team != default_option:
            position_list = position_list[position_list['EQUIPO'] == team]

        position_list = position_list["DEMARCACIÓN"].dropna().astype(str).str.strip().unique().tolist()
        position_list.sort()
        position = st.selectbox("DEMARCACIÓN", options=[default_option]+position_list, index=0)

    with nationality_col:
        nationality_list = df

        if category != default_option:
            nationality_list = nationality_list[nationality_list['CATEGORIA'] == category]

        if team != default_option:
            nationality_list = nationality_list[nationality_list['EQUIPO'] == team]

        if position != default_option:
            nationality_list = nationality_list[nationality_list['DEMARCACIÓN'] == position]

        nationality_list = nationality_list["NACIONALIDAD"].dropna().astype(str).str.strip().unique().tolist()
        nationality_list.sort()
        nationality = st.selectbox("NACIONALIDAD:", options=[default_option]+nationality_list, index=0)
        
    with player_col:
        player_list = df
        
        if category != default_option:
            player_list = player_list[player_list['CATEGORIA'] == category]

        if team != default_option:
            player_list = player_list[player_list['EQUIPO'] == team]

        if position != default_option:
            player_list = player_list[player_list['DEMARCACIÓN'] == position]
        
        if nationality != default_option:
            player_list = player_list[player_list['NACIONALIDAD'] == nationality]

        player_list = player_list["JUGADOR"].dropna().astype(str).str.strip().unique().tolist()
        player_list.sort()
        player = st.selectbox("JUGADOR:", options=[default_option]+player_list, index=0)

    if player != default_option:
        df_filtrado=df[df["JUGADOR"]==player]

    #if anio:
    #    df_filtrado=df_filtrado[df_filtrado["anio"]==anio]
    #    df_filtrado = df_filtrado.reset_index(drop=True)  # Reinicia los índices

    return df_filtrado

def getDatos(conn):
    df = conn.read(worksheet="DATOS", ttl="10m")
    df = df.iloc[:, 2:] ##Elimina las primeras 2 columnas del DataFrame df2, manteniendo el resto.
    df.drop(columns=['BANDERA','FOTO PERFIL'],inplace=True)
    df = df.reset_index(drop=True)  # Reinicia los índices
    df['EDAD'] = df['EDAD'].fillna(0).astype(int).astype(str)
    df["NACIONALIDAD"] = df["NACIONALIDAD"].astype(str).str.replace(",", ".", regex=False).str.strip()

    return df

def getDataTest(conn):
    df = conn.read(worksheet="DATATEST", ttl="10m")
    df = df.reset_index(drop=True)  # Reinicia los índices
    df.columns = df.iloc[0]  # Usa la primera fila como nombres de columna
    df = df[1:]  # Elimina la fila de encabezado original
    df = df.reset_index(drop=True)  # Reinicia los índices

    return df

def getJoinedDataFrame(conn):
    df_datos = getDatos(conn)
    df_data_test = getDataTest(conn)

    #st.dataframe(df_data_test)

    #df = conn.read(worksheet="DATATEST", ttl="10m")
    #df = df.reset_index(drop=True)  # Reinicia los índices
    #df.columns = df.iloc[0]  # Usa la primera fila como nombres de columna
    #df = df[1:]  # Elimina la fila de encabezado original
    #df = df.reset_index(drop=True)  # Reinicia los índices

    df_unido = pd.merge(df_datos, df_data_test, on=['ID','JUGADOR','CATEGORIA','EQUIPO'], how="inner")

    df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True)
    df_unido["anio"] = df_unido["FECHA REGISTRO"].dt.year.astype(str)
    df_unido["mes"] = df_unido["FECHA REGISTRO"].dt.month.astype(str)
    
    df_unido["FECHA REGISTRO"] = pd.to_datetime(df_unido["FECHA REGISTRO"], dayfirst=True)

    # Ordenar por fecha de más reciente a más antigua
    df_unido = df_unido.sort_values(by="FECHA REGISTRO", ascending=False)

    # Convertir de nuevo a string si es necesario
    df_unido["FECHA REGISTRO"] = df_unido["FECHA REGISTRO"].dt.strftime("%d/%m/%Y")

    df_unido = df_unido.fillna(0).replace("None", 0)
    df_unido = df_unido[(df_unido != 0).any(axis=1)]  # Elimina filas donde todos los valores son 0
    #df_unido['EDAD'] = df_unido['EDAD'].fillna(0).astype(int).astype(str)

    return df_unido

def get_photo(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si hubo un error (por ejemplo, 404 o 500)
    except requests.exceptions.RequestException:
        response = None  # Si hay un error, no asignamos nada a response

    return response

def categorizar_grasa(porcentaje_grasa):
    if porcentaje_grasa is None:
        return "No disponible"
    elif porcentaje_grasa < 20:
        return "Saludable"
    else:
        return "No saludable"
    
def categorizar_imc(valor):
    if valor < 18.5:
        return "Bajo peso"
    elif 18.5 <= valor < 24.9:
        return "Normal"
    elif 25 <= valor < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"

def color_categorias(val):
    if val == "Bajo peso":
        return "background-color: lightblue"
    elif val == "Normal":
        return "background-color: lightgreen"
    elif val == "Sobrepeso":
        return "background-color: yellow"
    elif val == "Obesidad":
        return "background-color: red"
    elif val == "Saludable":
        return "background-color: lightgreen"
    elif val == "No saludable":
        return "background-color: orange"
    return ""

def categorizar_imc(valor):
    if valor < 18.5:
        return "<span style='color: blue'>Bajo peso</span>"
    elif 18.5 <= valor < 24.9:
        return "<span style='color: green'>Normal</span>"
    elif 25 <= valor < 29.9:
        return "<span style='color: orange'>Sobrepeso</span>"
    else:
        return "<span style='color: red'>Obesidad</span>"

def categorizar_grasa(porcentaje_grasa):
    if porcentaje_grasa is None:
        return "No disponible"
    elif porcentaje_grasa < 20:
        return "<span style='color: green'>Saludable</span>"
    else:
        return "<span style='color: orange'>No saludable</span>"


def aplicar_semaforo(df, exclude_columns=["FECHA REGISTRO"]):
    """
    Aplica un formato de color semáforo con opacidad a un DataFrame.

    - Rojo (peor valor de la columna).
    - Verde (mejor valor de la columna).
    - Amarillo (valores intermedios).
    - Blanco/transparente para NaN o columnas excluidas.

    Parámetros:
    df : pd.DataFrame  ->  DataFrame a estilizar.
    exclude_columns : list  ->  Lista de columnas a excluir de la pintura.

    Retorna:
    df.style -> DataFrame estilizado.
    """

    def semaforo(val, column):
        # Excluir columnas no numéricas o especificadas
        if column in exclude_columns or not np.issubdtype(df[column].dtype, np.number):
            return ''

        # Manejar valores NaN
        if pd.isna(val):  
            return 'background-color: rgba(255, 255, 255, 0)'

        # Obtener mínimo y máximo de la columna
        column_min = df[column].min()
        column_max = df[column].max()

        # Normalizar el valor entre 0 (mínimo) y 1 (máximo)
        if column_max != column_min:  
            normalized = (val - column_min) / (column_max - column_min)
        else:  
            normalized = 0.5  # Si todos los valores son iguales, usar amarillo

        # Interpolar colores (rojo -> amarillo -> verde)
        r = int(255 * (1 - normalized))  # Rojo se reduce cuando el valor sube
        g = int(255 * normalized)  # Verde aumenta cuando el valor sube
        b = 0  # Mantener el azul en 0 para tonos cálidos
        opacity = 0.4  # Opacidad fija

        return f'background-color: rgba({r}, {g}, {b}, {opacity})'

    # Aplicar la función a todas las columnas excepto las excluidas
    return df.style.apply(lambda x: [semaforo(val, x.name) for val in x], axis=0)


def obtener_bandera(pais):
    # Diccionario de códigos de país ISO 3166-1 alfa-2
    paises = {
        "ALBANIA": "🇦🇱", "ALEMANIA": "🇩🇪", "ANDORRA": "🇦🇩", "ARGENTINA": "🇦🇷",
        "ARMENIA": "🇦🇲", "AUSTRALIA": "🇦🇺", "AUSTRIA": "🇦🇹", "AZERBAIJAN": "🇦🇿",
        "BARBADOS": "🇧🇧", "BELGIUM": "🇧🇪", "BENIN": "🇧🇯", "BOLIVIA": "🇧🇴",
        "BOSNIA AND HERZEGOVINA": "🇧🇦", "BRASIL": "🇧🇷", "BULGARIA": "🇧🇬", "CAMEROON": "🇨🇲",
        "CANADA": "🇨🇦", "CHILE": "🇨🇱", "CHINA": "🇨🇳", "COLOMBIA": "🇨🇴",
        "COSTA DE MARFIL": "🇨🇮", "DINAMARCA": "🇩🇰", "DOMINICAN REPUBLIC": "🇩🇴", "ECUADOR": "🇪🇨",
        "EGIPTO": "🇪🇬", "EL SALVADOR": "🇸🇻", "ESPAÑA": "🇪🇸", "ETIOPÍA": "🇪🇹", "FILIPINAS": "🇵🇭",
        "FRANCIA": "🇫🇷", "GABON": "🇬🇦", "GAMBIA": "🇬🇲", "GEORGIA": "🇬🇪", "GERMANY": "🇩🇪",
        "GHANA": "🇬🇭", "GUATEMALA": "🇬🇹", "GUINEA": "🇬🇳", "HOLANDA": "🇳🇱", "HONDURAS": "🇭🇳",
        "HUNGRIA": "🇭🇺", "INDIA": "🇮🇳", "INGLATERRA": "🇬🇧", "IRLANDA": "🇮🇪", "ISRAEL": "🇮🇱",
        "ITALIA": "🇮🇹", "JORDANIA": "🇯🇴", "KAZAKHSTAN": "🇰🇿", "LATVIA": "🇱🇻", "LÍBANO": "🇱🇧",
        "LIBERIA": "🇱🇷", "LITUANIA": "🇱🇹", "MADAGASCAR": "🇲🇬", "MALTA": "🇲🇹", "MARRUECOS": "🇲🇦",
        "MÉXICO": "🇲🇽", "MONGOLIA": "🇲🇳", "MOROCCO": "🇲🇦", "MOZAMBIQUE": "🇲🇿", "NIGERIA": "🇳🇬",
        "PAÍS VASCO": "🇪🇸", "PANAMÁ": "🇵🇦", "PERÚ": "🇵🇪", "POLAND": "🇵🇱", "POLINESIA FRANCESA": "🇵🇫",
        "POLONIA": "🇵🇱", "PORTUGAL": "🇵🇹", "R. DOMINICANA": "🇩🇴", "RUMANIA": "🇷🇴", "RUSIA": "🇷🇺",
        "SIRIA": "🇸🇾", "SUECIA": "🇸🇪", "SUIZA": "🇨🇭", "TANZANIA": "🇹🇿", "TUNEZ": "🇹🇳",
        "TURKMENISTAN": "🇹🇲", "UCRANIA": "🇺🇦", "USA": "🇺🇸", "VENEZUELA": "🇻🇪", "VIRGIN ISLANDS": "🇻🇬"
    }

    
    # Normalizar el nombre del país
    pais = pais.strip().upper()

    if pais in paises:
        codigo = paises[pais]
        # Convertir el código de país a su bandera en Unicode
        #bandera_unicode = ''.join(chr(0x1F1E6 + ord(c)) for c in codigo)
        return codigo
    else:
        return ""
