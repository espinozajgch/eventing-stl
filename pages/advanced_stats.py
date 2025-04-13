import streamlit as st
import pandas as pd
from utils import util
from utils import graphics
from utils import connection
from utils import stats

st.set_page_config(
    page_title="StatsLab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header(":material/monitoring: :blue[StatsLab]", divider=True)

util.generarMenu()

df_sb, df_op, df_ws = connection.get_df()
df_all = pd.concat([df_sb, df_ws, df_op], ignore_index=True)

st.markdown("**Distribución de Acciones por proveedor**")

col1, col2, col3 = st.columns(3)

with col1:
  graphics.plot_action_distribution_per_provider(df_op, "Opta")
with col2:
  graphics.plot_action_distribution_per_provider(df_sb, "StatsBomb")
with col3:
  graphics.plot_action_distribution_per_provider(df_ws, "Wyscout")

st.divider()

col_stats, col_graph = st.columns(2)

resumen = stats.resumen_acciones_por_minuto(df_sb, df_op, df_ws)

with col_stats:
  st.markdown("**Resumen estadístico de acciones por minuto**")
  st.dataframe(resumen)
with col_graph:
  with st.container(height=250, border=False):
      graphics.plot_mean_actions(resumen)

graphics.plot_actions_per_minute(df_sb, df_op, df_ws)



