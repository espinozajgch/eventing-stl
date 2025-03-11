import streamlit as st
from utils import util
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="PlayerHub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.header("PlayerHub")
st.subheader("Datos individuales, comparaciones y seguimiento")

util.generateMenu()

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = util.getJoinedDataFrame(conn)
df = util.generateFilters(df)

st.text("# Tablero de datos")
st.dataframe(df)