import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.lines import Line2D
from mplsoccer import Pitch

def plot_actions_per_minute(df_sb, df_op, df_ws):
    # Añadir columna Minute y Provider
    df_sb['Minute'] = df_sb['StartTime'] // 60
    df_sb['Provider'] = 'StatsBomb'

    df_op['Minute'] = df_op['StartTime'] // 60
    df_op['Provider'] = 'Opta'

    df_ws['Minute'] = df_ws['StartTime'] // 60
    df_ws['Provider'] = 'Wyscout'

    # Unir todos los DataFrames
    df_all = pd.concat([df_sb, df_op, df_ws])

    # Agrupar por minuto y proveedor
    grouped = df_all.groupby(['Provider', 'Minute']).size().reset_index(name='Acciones')

    # Crear gráfico interactivo con plotly
    fig = px.line(
        grouped,
        x='Minute',
        y='Acciones',
        color='Provider',
        markers=True,
        title='Número de acciones SPADL por minuto',
        labels={
            'Minute': 'Minuto del partido',
            'Acciones': 'Número de acciones',
            'Provider': 'Proveedor'
        }
    )

    fig.update_layout(
        height=500,
        template='simple_white',
        title_font=dict(size=15, color='black'),
        font=dict(color='black'),
        legend=dict(title='Proveedor')
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)


def plot_mean_actions(summary):
    colors = {
        'StatsBomb': '#1f77b4',
        'Opta': '#ff7f0e',
        'Wyscout': '#2ca02c'
    }

    providers = summary.index.tolist()
    means = summary['Media'].values
    color_list = [colors[p] for p in providers]

    # Crear gráfico de barras con etiquetas encima
    fig = go.Figure()

    for provider, media, color in zip(providers, means, color_list):
        fig.add_trace(go.Bar(
            x=[provider],
            y=[media],
            name=provider,
            marker_color=color,
            text=[f"{media:.2f}"],
            textposition='inside',
            textfont=dict(size=10, color='black')
        ))

    # Layout limpio
    fig.update_layout(
        height=250,  # equivalente a figsize=(8, 2.5)
        title='Promedio de acciones por minuto',
        title_font=dict(size=14, color='black'),
        yaxis_title='Media de acciones',
        yaxis=dict(color='black', tickfont=dict(size=10)),
        xaxis=dict(color='black', tickfont=dict(size=10)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        margin=dict(l=30, r=30, t=40, b=30)
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def plot_spadl_action_heatmap(df_all):
    # Validar que la columna Provider existe
    if 'Provider' not in df_all.columns:
        st.error("El DataFrame no contiene la columna 'Provider'")
        return

    # Calcular frecuencia por proveedor
    freq = df_all.groupby('Provider')['ActionType'].value_counts().unstack(fill_value=0).T

    # Reordenar columnas si están presentes
    expected_order = ["opta", "wyscout", "statsbomb"]
    freq = freq[[col for col in expected_order if col in freq.columns]]

    # Ordenar por suma total para visualización más clara
    freq = freq.loc[freq.sum(axis=1).sort_values(ascending=False).index]

    # Mostrar tabla con estilo
    st.markdown("**Acciones SPADL por proveedor**")
    st.dataframe(freq.style.background_gradient(cmap="RdYlGn", axis=1))

def plot_action_distribution_per_provider(df, provider_name):
    
    # Colores por proveedor
    colors = {
        'StatsBomb': '#1f77b4',  # azul
        'Opta': '#ff7f0e',       # naranja
        'Wyscout': '#2ca02c'     # verde
    }

    color = colors[provider_name]
    
    sns.set_theme(style="whitegrid")

    # Calcular acciones y ordenar
    action_counts = df["ActionType"].value_counts(normalize=True).sort_values(ascending=False)
    plot_df = action_counts.reset_index()
    plot_df.columns = ['ActionType', 'Frequency']
    plot_df["Label"] = plot_df.apply(lambda x: f"{x['ActionType']} ({x['Frequency']:.2%})", axis=1)

    # Calcular altura del gráfico según cantidad de acciones
    #height = max(4, 0.3 * len(plot_df))
    fig, ax = plt.subplots(figsize=(5, 4))

    # Gráfico horizontal    
    sns.barplot(
        data=plot_df,
        x="Frequency",
        y="ActionType",
        hue="ActionType",
        palette={k: color for k in plot_df["ActionType"]},
        ax=ax,
        width=0.8,
        legend=False
    )

    # Estilo y etiquetas
    ax.set_yticks(range(len(plot_df)))
    ax.set_yticklabels(plot_df["Label"], fontsize=8, color='black')
    ax.set_title(f"Distribución de acciones - {provider_name}", fontsize=8, color='black')
    ax.set_xlabel("Frecuencia relativa", fontsize=8, color='black')
    ax.set_ylabel("")
    ax.tick_params(axis='x', colors='black', labelsize=6)
    ax.tick_params(axis='y', colors='black', labelsize=6)

    # Limpiar bordes y fondo
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.spines['bottom'].set_linewidth(1)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")
    ax.xaxis.set_ticks_position('bottom')
    ax.tick_params(axis='x', direction='out', length=3, width=1)
    ax.grid(False)

    # Mostrar en Streamlit
    st.pyplot(fig)

def plot_pass_map_raw(df_all):
    pitch_type_map = {
        'statsbomb': 'statsbomb',
        'wyscout': 'wyscout',
        'opta': 'opta'
    }

    # Detectar proveedores presentes en los datos
    proveedores_presentes = df_all['Provider'].dropna().unique()
    #st.dataframe(proveedores_presentes)
    proveedores_presentes = [p for p in pitch_type_map if p in proveedores_presentes]
    #st.dataframe(proveedores_presentes)
    num_proveedores = len(proveedores_presentes)

    if num_proveedores == 0:
        st.warning("No hay datos de proveedores disponibles para graficar.")
        return

    fig, axs = plt.subplots(1, num_proveedores, figsize=(6 * num_proveedores, 6))

    if num_proveedores == 1:
        axs = [axs]  # convertir a lista si hay solo un subplot

    for i, proveedor in enumerate(proveedores_presentes):
        df = df_all[df_all['Provider'] == proveedor]
        pitch_type = pitch_type_map[proveedor]
        pitch = Pitch(pitch_type=pitch_type, line_zorder=2, pitch_color='grass', line_color='white')
        pitch.draw(ax=axs[i])

        passes = df[df["ActionType"] == "pass"]

        x_start = passes["StartLoc"].apply(lambda x: x[0])
        y_start = passes["StartLoc"].apply(lambda x: x[1])
        x_end = passes["EndLoc"].apply(lambda x: x[0])
        y_end = passes["EndLoc"].apply(lambda x: x[1])

        for x0, y0, x1, y1 in zip(x_start, y_start, x_end, y_end):
            dx, dy = x1 - x0, y1 - y0
            axs[i].arrow(x0, y0, dx, dy, width=0.2, head_width=1.2,
                         length_includes_head=True, color='blue', alpha=0.4, zorder=1)

        axs[i].set_title(proveedor.capitalize(), fontsize=14)

    plt.tight_layout()
    st.pyplot(fig)

def plot_all_action_symbols(df_all):
    pitch_type_map = {
        'statsbomb': 'statsbomb',
        'wyscout': 'wyscout',
        'opta': 'opta'
    }

    action_groups = {
        'Ofensivas': [
            'pass', 'cross', 'throw_in', 'freekick_crossed',
            'freekick_short', 'corner_crossed', 'corner_short',
            'take_on', 'shot', 'freekick_shot', 'penalty_shot', 'dribble'
        ],
        'Defensivas': [
            'foul', 'tackle', 'interception', 'clearance', 'bad_touch'
        ],
        'Portero': [
            'keeper_save', 'keeper_claim', 'keeper_punch', 'keeper_pick_up'
        ]
    }

    all_actions = sum(action_groups.values(), [])
    cmap = plt.get_cmap('tab20')
    markers = ['o', '^', 's', 'P', 'D', 'X', '*', 'h', 'v', '<', '>', '8', 'p']
    action_color_map = {a: cmap(i % 20) for i, a in enumerate(all_actions)}
    action_marker_map = {a: markers[i % len(markers)] for i, a in enumerate(all_actions)}

    proveedores = list(df_all['Provider'].dropna().unique())
    if not proveedores:
        st.warning("No hay proveedores presentes en los datos.")
        return

    ncols = len(proveedores)
    nrows = len(action_groups)
    group_names = list(action_groups.keys())

    fig, axs = plt.subplots(
        nrows, ncols,
        figsize=(5 * ncols, 5 * nrows),
        gridspec_kw={'wspace': 0.1, 'hspace': -0.50}
    )

    if nrows == 1:
        axs = [axs]
    if ncols == 1:
        axs = [[ax] for ax in axs]

    for row_idx, group_name in enumerate(group_names):
        actions = action_groups[group_name]
        for col_idx, proveedor in enumerate(proveedores):
            df = df_all[df_all['Provider'] == proveedor]
            ax = axs[row_idx][col_idx]
            pitch = Pitch(pitch_type=pitch_type_map[proveedor], line_color='black')
            pitch.draw(ax=ax)

            for action in actions:
                subset = df[df['ActionType'] == action]
                if subset.empty:
                    continue
                x = subset["StartLoc"].apply(lambda loc: loc[0])
                y = subset["StartLoc"].apply(lambda loc: loc[1])
                color = action_color_map[action]
                marker = action_marker_map[action]
                ax.scatter(x, y, marker=marker, c=color, s=70, alpha=0.7)

            ax.set_title(f"{proveedor.capitalize()} - {group_name}", fontsize=11)

    # ➕ UNA ÚNICA LEYENDA, AGRUPADA POR TIPO DE ACCIÓN
    legend_elements = []
    for group, actions in action_groups.items():
        legend_elements.append(Line2D([0], [0], linestyle='none', label=f"— {group} —", color='black'))
        for action in actions:
            legend_elements.append(Line2D(
                [0], [0], marker=action_marker_map[action], color='w',
                label=action, markerfacecolor=action_color_map[action],
                markersize=8, markeredgecolor='black'
            ))

    fig.legend(
        handles=legend_elements,
        loc='upper center',
        bbox_to_anchor=(0.5, 0.08),
        ncol=4,
        frameon=True,
        fontsize=8,
        title="Acciones SPADL",
        title_fontsize=9
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom=-0.01, top=0.75)
    st.pyplot(fig)
