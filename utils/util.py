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
        provider_options = df['Provider'].dropna().astype(str).str.strip().sort_values().unique().tolist()
        provider = st.selectbox(
            "PROVEEDOR",
            options=[default_option] + provider_options,
            key="selected_provider"
        )
        if provider != default_option:
            df_filtered = df_filtered[df_filtered['Provider'].astype(str).str.strip() == provider]

    # --- FILTRO POR EQUIPO ---
    with team_col:
        team_options = df_filtered['Team'].dropna().astype(str).str.strip().sort_values().unique().tolist()
        team = st.selectbox(
            "EQUIPO",
            options=[default_option] + team_options,
            key="selected_team"
        )
        if team != default_option:
            df_filtered = df_filtered[df_filtered['Team'].astype(str).str.strip() == team]

    # --- FILTRO POR JUGADOR ---
    with player_col:
        player_options = df_filtered['Player'].dropna().astype(str).str.strip().sort_values().unique().tolist()
        player = st.selectbox(
            "JUGADOR",
            options=[default_option] + player_options,
            key="selected_player"
        )
        if player != default_option:
            df_filtered = df_filtered[df_filtered['Player'].astype(str).str.strip() == player]

    # --- FILTRO POR ACCIÓN ---
    with action_col:
        action_options = df_filtered['ActionType'].dropna().astype(str).str.strip().sort_values().unique().tolist()
        action_options = [default_option] + action_options

        # Verifica si la acción seleccionada aún existe, si no, resetear a "Todos"
        current_action = st.session_state.get("selected_action", default_option)
        print(current_action)
        
        if current_action not in action_options:
            st.session_state["selected_action"] = default_option
            current_action = default_option

        # Ahora renderiza el selectbox usando el valor actual válido
        action = st.selectbox(
            "ACCIÓN SPADL",
            options=action_options,
            index=action_options.index(current_action),
            key="selected_action"
        )

        if action != default_option:
            df_filtered = df_filtered[df_filtered['ActionType'].astype(str).str.strip() == action]

    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered

def get_player_map():
    PLAYER_NAME_MAP_TO_OPTA = {
        # StatsBomb / Wyscout → Opta
        "Karim Benzema": "Karim Benzema",
        "K. Benzema": "Karim Benzema",

        "Toni Kroos": "Toni Kroos",
        "T. Kroos": "Toni Kroos",

        "Sergio Ramos García": "Sergio Ramos",
        "Sergio Ramos": "Sergio Ramos",

        "Raphaël Varane": "Raphael Varane",
        "R. Varane": "Raphael Varane",

        "Keylor Navas Gamboa": "Keylor Navas",
        "K. Navas": "Keylor Navas",

        "Carlos Henrique Casimiro": "Casemiro",
        "Casemiro": "Casemiro",

        "Ivan Rakitić": "Ivan Rakitic",
        "I. Rakitić": "Ivan Rakitic",

        "Luka Modrić": "Luka Modric",
        "L. Modrić": "Luka Modric",

        "José Ignacio Fernández Iglesias": "Nacho",
        "Nacho": "Nacho",

        "Marcelo Vieira da Silva Júnior": "Marcelo",
        "Marcelo": "Marcelo",

        "Gerard Piqué Bernabéu": "Gerard Piqué",
        "Piqué": "Gerard Piqué",

        "Sergio Busquets i Burgos": "Sergio Busquets",
        "Sergio Busquets": "Sergio Busquets",

        "Andrés Iniesta Luján": "Andrés Iniesta",
        "Iniesta": "Andrés Iniesta",

        "Philippe Coutinho Correia": "Coutinho",
        "Philippe Coutinho": "Coutinho",

        "Lionel Andrés Messi Cuccittini": "Lionel Messi",
        "L. Messi": "Lionel Messi",
        "Lionel Messi": "Lionel Messi",

        "Sergi Roberto Carnicer": "Sergi Roberto",
        "Sergi Roberto": "Sergi Roberto",

        "Samuel Yves Umtiti": "Samuel Umtiti",
        "S. Umtiti": "Samuel Umtiti",

        "Jordi Alba Ramos": "Jordi Alba",
        "Jordi Alba": "Jordi Alba",

        "Marc-André ter Stegen": "Marc-André ter Stegen",
        "M. ter Stegen": "Marc-André ter Stegen",

        "Gareth Frank Bale": "Gareth Bale",
        "G. Bale": "Gareth Bale",
        "Gareth Bale": "Gareth Bale",

        "Luis Alberto Suárez Díaz": "Luis Suárez",
        "L. Suárez": "Luis Suárez",
        "Luis Suárez": "Luis Suárez",

        "Cristiano Ronaldo dos Santos Aveiro": "Cristiano Ronaldo",
        "Cristiano Ronaldo": "Cristiano Ronaldo",

        "Nélson Cabral Semedo": "Nélson Semedo",
        "Nélson Semedo": "Nélson Semedo",

        "Marco Asensio Willemsen": "Marco Asensio",
        "Marco Asensio": "Marco Asensio",

        "José Paulo Bezzera Maciel Júnior": "Paulinho",
        "Paulinho": "Paulinho",

        "Lucas Vázquez Iglesias": "Lucas Vázquez",
        "Lucas Vázquez": "Lucas Vázquez",

        "Mateo Kovačić": "Mateo Kovačić",
        "Mateo Kovacic": "Mateo Kovačić",
        "M. Kovačić": "Mateo Kovačić",

        "Francisco Alcácer García": "Paco Alcácer",
        "Paco Alcácer": "Paco Alcácer",

        "Ivan Rakitic": "Ivan Rakitic",
        "Luka Modric": "Luka Modric",
        
        "Samuel Umtiti": "Samuel Umtiti",
    }

    return PLAYER_NAME_MAP_TO_OPTA

