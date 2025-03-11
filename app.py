import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import matplotlib.pyplot as plt
import seaborn as sns
from utils import util

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

