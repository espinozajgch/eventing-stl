import streamlit as st

def clean_unicode(text):
    if not isinstance(text, str):
        return text
    try:
        # Decodificar unicode doblemente escapado
        return text.encode('utf-8').decode('unicode_escape').strip()
    except UnicodeDecodeError:
        return text.strip()

def generarMenu():     
    with st.sidebar:
        st.logo("assets/images/sdc.png", size="large")
        st.page_link("app.py", label="Inicio", icon=":material/home:")
        st.subheader("Tableros")
        st.page_link("pages/scout.py", label="ScoutingHub", icon=":material/contacts:")
        st.page_link("pages/advanced_stats.py", label="Advanced Stats", icon=":material/monitoring:")

def generate_spadl_filters(df):
    default_option = "Todos"
    df_filtered = df.copy()

    # Columnas Streamlit: proveedor, equipo, jugador, acción
    provider_col, team_col, player_col, action_col = st.columns(4)

# --- FILTRO POR PROVEEDOR ---
    with provider_col:
        provider_options = df[['Provider']].drop_duplicates().dropna()['Provider'].astype(str).str.strip().sort_values().tolist()
        provider = st.selectbox("PROVEEDOR", options=[default_option] + provider_options, index=0)
        if provider != default_option:
            df_filtered = df_filtered[df_filtered['Provider'] == provider]

    # --- FILTRO POR EQUIPO ---
    with team_col:
        team_options = df_filtered[['Team']].drop_duplicates().dropna()['Team'].astype(str).str.strip().sort_values().tolist()
        team = st.selectbox("EQUIPO", options=[default_option] + team_options, index=0)
        if team != default_option:
            df_filtered = df_filtered[df_filtered['Team'] == team]

    # --- FILTRO POR JUGADOR ---
    with player_col:
        player_options = df_filtered[['Player']].drop_duplicates().dropna()['Player'].astype(str).str.strip().sort_values().tolist()
        player = st.selectbox("JUGADOR", options=[default_option] + player_options, index=0)
        if player != default_option:
            df_filtered = df_filtered[df_filtered['Player'] == player]

    # --- FILTRO POR ACCIÓN ---
    with action_col:
        action_options = df_filtered[['ActionType']].drop_duplicates().dropna()['ActionType'].astype(str).str.strip().sort_values().tolist()
        action = st.selectbox("ACCIÓN SPADL", options=[default_option] + action_options, index=0)
        if action != default_option:
            df_filtered = df_filtered[df_filtered['ActionType'] == action]

    return df_filtered

