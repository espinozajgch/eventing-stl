import streamlit as st
from utils import util
from streamlit_gsheets import GSheetsConnection

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
df = util.getJoinedDataFrame(conn)
df = util.generateFilters(df)

st.text("# Tablero de datos")
st.dataframe(df)

