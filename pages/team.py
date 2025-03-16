import streamlit as st
from utils import util
from streamlit_gsheets import GSheetsConnection
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="StatsLab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("StatsLab")
st.subheader("Métricas Grupales y alertas")

util.generateMenu()

conn = st.connection("gsheets", type=GSheetsConnection)
df1 = util.getJoinedDataFrame(conn)
df = util.generateFilters(df1)

st.text("# Tablero de datos")
datos = util.getDatos(conn)
st.dataframe(df1)

#st.bar_chart(np.random.randn(50,3))

# Datos de ejemplo con solo promedios
data = {
    "METRICA": ["ALTURA", "PESO", "MG [KG]", "GRASA (%)"],
    "PROMEDIO": [173.5, 60.6, 9.0, 5.4]  # Valores de ejemplo
}

# Convertir en DataFrame
df_stats = pd.DataFrame(data)

# Crear gráfico polar con los promedios
fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=df_stats["PROMEDIO"],   # Valores de las métricas
      theta=df_stats["METRICA"], # Nombres de las métricas
      fill='toself',
      name='Promedio',
      line=dict(color='blue') # Personalización del color
))

# Configuración del gráfico
fig.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, max(df_stats["PROMEDIO"]) + 5]  # Ajusta el rango según el máximo valor de las métricas
    )),
  showlegend=True
)

# Mostrar en Streamlit
st.subheader("Comparación de Promedios de Métricas")
st.plotly_chart(fig)

#############################################

