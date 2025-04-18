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

df_sb, df_op, df_ws = connection.get_df()
df_all = pd.concat([df_sb, df_ws, df_op], ignore_index=True)

st.header(":material/contacts: :blue[ScoutingHub]", divider=True)

df_datos_filtrado = util.generate_spadl_filters(df_all)

tab1, tab2= st.tabs(["GRAFICO", "TABLA"])
with tab1:
    st.markdown("**Distribución Espacial de Acciones**")
    graphics.plot_all_action_symbols(df_datos_filtrado)
with tab2:
    st.markdown("**Tabla de Acciones SPADL**")
    st.dataframe(df_datos_filtrado)