import streamlit as st
import pandas as pd
from utils import util
from utils import connection
from utils import graphics

st.set_page_config(
    page_title="Comparación de Proveedores",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

util.generarMenu()

st.header('Comparación de Eventing :orange[Opta - Statsbomb - Wyscout]', divider=True)
st.subheader(':orange[Temporadas] :material/event_available:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(f":orange[Opta]","2017/18", border=True)
with col2:
    st.metric(f":blue[Statsbomb]","2017/18", border=True)
with col3:
    st.metric(f":green[Wyscout]","2017/18", border=True)

#st.divider()

df_sb, df_op, df_ws, df_all = connection.get_df()

col1, col2 = st.columns([1.2,2])
with col1:
    with st.container(height=450, border=False):
        graphics.plot_spadl_action_heatmap(df_all)
with col2:
    st.markdown("**Resumen de Acciones SPADL**")
    st.dataframe(df_all.sample(n=20, random_state=42))
