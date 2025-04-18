import streamlit as st
from utils import util
from utils import graphics
from utils import connection
import pandas as pd

st.set_page_config(
    page_title="ScoutHub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

util.generarMenu()

df_sb, df_op, df_ws, df_all = connection.get_df()

st.header(":material/contacts: :blue[ScoutingHub]", divider=True)

df_datos_filtrado = util.generate_spadl_filters(df_all)

 # --- FILTRO POR MINUTOS ---
if 'StartTime' in df_datos_filtrado.columns:
    min_sec = int(df_datos_filtrado['StartTime'].min())
    max_sec = int(df_datos_filtrado['StartTime'].max())
    min_min = min_sec // 60
    max_min = (max_sec // 60) + 1

    min_selected, max_selected = st.slider(
        "RANGO DE MINUTOS",
        min_value=0,
        max_value=90,
        value=(min_min, max_min),
        step=1
    )

    df_filtered = df_datos_filtrado[
        (df_datos_filtrado['StartTime'] >= min_selected * 60) &
        (df_datos_filtrado['StartTime'] < max_selected * 60)
    ]

tab1, tab2 = st.tabs(["GRÁFICOS", "TABLAS"])
with tab1:
    st.markdown("**Distribución Espacial de Acciones**")
    graphics.plot_all_action_symbols(df_filtered)
with tab2:
    col1, col2 = st.columns([1.1,2])
    with col1:
        #with st.container(height=450, border=False):
        graphics.plot_spadl_action_heatmap(df_filtered)
    with col2:
        st.markdown("**Tabla de Acciones SPADL**")
        st.dataframe(df_filtered)

