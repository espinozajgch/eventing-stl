import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import seaborn as sns
from utils import util
import numpy as np

st.set_page_config(
    page_title="Dashboard Cargas Fisicas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

util.generateMenu()

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
#########################################################

df_unido = util.getJoinedDataFrame(conn)
#########################################################

st.header("Bienvenido")

ultima_fecha = df_unido['FECHA REGISTRO'].iloc[0]

col1, col2, col3, col4 = st.columns(4)

with col1:
    act = 1
    ant = 0
    variacion = 1;
    st.metric(f"Total Asistencia (Mes)",f'{act}', f'{variacion}')

with col2:
    act = 1
    ant = 0
    variacion = 1;
    st.metric(f"% Asistencia (Mes)",f'{act}', f'{variacion}')

with col3:
    act = 1
    ant = 0
    variacion = 1;
    st.metric(f"% Asistencia (Sesion)",f'{act}', f'{variacion}')

with col4:
    # Mostrar la fecha si es válida
    if ultima_fecha is not None and pd.notna(ultima_fecha):
        st.metric("Última Sesión", ultima_fecha)
    else:
        st.metric("Última Sesión", "Fecha no disponible")

#st.dataframe(df_unido)
#st.bar_chart(np.random.randn(50,3))

########################################

