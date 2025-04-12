import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import seaborn as sns
from utils import util
import numpy as np
import login as login

st.set_page_config(
    page_title="Comparación de Proveedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

util.generarMenu()


#login.generarLogin()

# 🔹 Bloquear contenido si el usuario no está en session_state
#if 'usuario' not in st.session_state:
#    #st.warning("Debes iniciar sesión para acceder a esta página.")
#    st.stop()  # 🔹 Detiene la ejecución del código si no hay sesión activa
#else:
    
st.header('Comparación de Eventing :orange[Opta - Statsbomb - Wyscout]')
#util.generateMenu()

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
#########################################################

df_datos = util.getDatos(conn)
df_joined = util.getJoinedDataFrame(conn)
#datatest= util.getDataTest(conn)
total_jugadores = len(df_datos)
df_sesiones = util.resumen_sesiones(df_joined, total_jugadores)
#########################################################

##st.header("Bienvenido")
#st.dataframe(datatest)
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(f"Total de Jugadores",f'{total_jugadores}')

with col2:
    act = df_sesiones["TSUM"].iloc[0]
    ant = df_sesiones["TSUM"].iloc[1]
    variacion = act - ant
    st.metric(f"Total Asistencia (Mes)",f'{act}', f'{variacion:,.2f}')

with col3:
    act = df_sesiones["APUS"].iloc[0]
    ant = df_sesiones["APUS"].iloc[1]
    variacion = act - ant
    st.metric(f"% Asistencia (Mes)",f'{act:,.3f}', f'{variacion:,.2f}')

with col4:
    act = df_sesiones["JUS"].iloc[0]
    ant = df_sesiones["JUS"].iloc[1]
    variacion = act - ant
    st.metric(f"Asistencia Ultima Sesion",f'{act}', f'{variacion:,.2f}')

with col5:
    # Mostrar la fecha si es válida
    if not df_joined.empty: 
        ultima_fecha = df_joined['FECHA REGISTRO'].iloc[0]
        if isinstance(ultima_fecha, pd.Timestamp):
            ultima_fecha_str = ultima_fecha.strftime('%d/%m/%Y')
        elif isinstance(ultima_fecha, str):
            ultima_fecha_str = ultima_fecha  # Ya es string, no necesita conversión
        else:
            ultima_fecha_str = str(ultima_fecha)  # Convertir otros tipos a string
        st.metric("Última Sesión", ultima_fecha_str)

    else:
        st.metric("Última Sesión", "####")

st.divider()
#st.dataframe(util.contar_jugadores_por_categoria(df_datos))
#st.dataframe(df_sesiones)
if not df_joined.empty: 
    st.markdown("📆 **Cantidad de Sesiones por jugador**")
    st.dataframe(util.sesiones_por_test(df_joined))


#st.bar_chart(np.random.randn(50,3))

########################################

