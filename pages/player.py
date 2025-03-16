import streamlit as st
from utils import util
from utils import graphics

from streamlit_gsheets import GSheetsConnection

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns

st.set_page_config(
    page_title="PlayerHub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

util.generateMenu()

st.header(" :blue[Player Hub]")
st.subheader("Datos individuales, historicos y alertas")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df_joined = util.getJoinedDataFrame(conn)
datos = util.getDatos(conn)

df_datos = datos.drop_duplicates(subset=["ID"], keep="first")
df_datos_filtrado = util.generateFilters(df_datos)

#st.dataframe(df_datos)

#st.button("📄 Generar PDF")
    #pdf = util.generar_pdf()
    #pdf.output("reporte.pdf")  # Guardar el archivo
    #with open("reporte.pdf", "rb") as file:
    #    st.download_button("📥 Descargar PDF", file, file_name="reporte.pdf", mime="application/pdf")

st.divider()
###################################################

if df_datos_filtrado.empty:
    st.text("Debe seleccionar un jugador")
else:
    jugador_id = df_datos_filtrado["ID"].dropna().astype(str).str.strip().unique().tolist()        
    df_jugador = df_datos[df_datos["ID"]==jugador_id[0]]
    df_joined_filtrado=df_joined[df_joined["ID"]==jugador_id[0]]

    response = util.get_photo(df_jugador['URL'].iloc[0])

    nombre = df_jugador['JUGADOR'].iloc[0]
    nacionalidad = df_jugador['NACIONALIDAD'].iloc[0]
    bandera = util.obtener_bandera(nacionalidad.replace(",", "."))

    st.markdown(f"## {nombre}")
    st.markdown(f"##### **_:blue[NACIONALIDAD:]_** _{nacionalidad}_ {bandera}")

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        if response:
            st.image(response.content, width=150)

    with col2:
        categoria = df_jugador['CATEGORIA'].iloc[0]
        equipo = df_jugador['EQUIPO'].iloc[0]
        fnacimiento = df_jugador['FECHA DE NACIMIENTO'].iloc[0]

        st.metric(label="Equipo - Categoria", value=f" {categoria} {equipo}", border=True)
        st.metric(label="F. Nacimiento", value=f"{fnacimiento}", border=True)

    with col3:
        edad = df_jugador['EDAD'].iloc[0]
        demarcacion = df_jugador['DEMARCACIÓN'].iloc[0]
        st.metric(label="Posición", value=f"{demarcacion.capitalize()}", border=True)
        st.metric(label="Edad", value=f"{edad} años", border=True)

###################################################

if not df_datos_filtrado.empty:
    ##tab1,tab2,tab3 = st.tabs(["👤 Perfil", "📆 Historicos" ,"📉 Comparaciones"])
    tab1,tab2,tab3 = st.tabs(["📈 Rendimiento", "📆 Historicos" ,"🏥 Alertas"])
    with tab1:
        if len(df_joined_filtrado) > 0:

            ###################################################
            ###################################################
            ## ANTROPOMETRIA - AGILIDAD

            c1, c2 = st.columns(2)

            with c1:
                #with st.container(border=True):
                df_anthropometrics = df_joined_filtrado[["FECHA REGISTRO", "ALTURA", "PESO", "MG [KG]", "GRASA (%)"]]
                df_anthropometrics = df_anthropometrics.reset_index(drop=True)
                
                st.markdown("### :blue[ANTROPOMETRÍA]")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    act = df_anthropometrics['ALTURA'].iloc[0]
                    ant = df_anthropometrics['ALTURA'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"Altura (cm)",f'{act:,.2f}', f'{variacion:,.2f}')
    
                with col2:
                    act = df_anthropometrics['PESO'].iloc[0]
                    ant = df_anthropometrics['PESO'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"Peso (Kg)",f'{act:,.2f}', f'{variacion:,.2f}')

                with col3:
                    act = df_anthropometrics['MG [KG]'].iloc[0]
                    ant = df_anthropometrics['MG [KG]'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"MG (Kg)",f'{act:,.2f}', f'{variacion:,.2f}')

                with col4:
                    act = df_anthropometrics['GRASA (%)'].iloc[0]
                    ant = df_anthropometrics['GRASA (%)'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"Grasa (%)",f'{act:,.2f}', f'{variacion:,.2f}')

                #st.markdown("#### Ultimos 5")
                #st.dataframe(df_anthropometrics)
                graphics.get_anthropometrics_graph(df_anthropometrics)

            with c2:
                df_agilty = df_joined_filtrado[["FECHA REGISTRO", "505-DOM [SEG]", "505-ND [SEG]"]]
                df_agilty = df_agilty.reset_index(drop=True)
                
                st.markdown("### :blue[AGILIDAD 505]")
                
                col1, col2 = st.columns(2)

                with col1:
                    act = df_agilty['505-DOM [SEG]'].iloc[0]
                    ant = df_agilty['505-DOM [SEG]'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"505-DOM [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')
                    
                with col2:
                    act = df_agilty['505-ND [SEG]'].iloc[0]
                    ant = df_agilty['505-ND [SEG]'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"505-ND [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')

                #st.markdown("#### Ultimos 5")
                #st.dataframe(df_agilty)
                graphics.get_agilty_graph(df_agilty)

            st.divider()
######################################################################################################

            ## SPRINT LINEAL

            df_sprint = df_joined_filtrado[["FECHA REGISTRO", "TOTAL 40M [SEG]", "TIEMPO 0-5M [SEG]", "VEL 0-5M [M/S]", 
                                            "TIEMPO 5-20M [SEG]", "VEL 5-20M [M/S]", "TIEMPO 20-40M [SEG]",
                                            "VEL 20-40M [M/S]"]]
            
            df_sprint = df_sprint.reset_index(drop=True)
            #df_sprint = df_sprint.round(2)
            #pd.options.display.float_format = '{:,.2f}'.format

            st.markdown("### :blue[SPRINT LINEAL]")

            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

            with col1:
                act = df_sprint['TOTAL 40M [SEG]'].iloc[0]
                ant = df_sprint['TOTAL 40M [SEG]'].iloc[1]
                variacion = act - ant;
                st.metric(f"TOTAL 40M [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col2:
                act = df_sprint['TIEMPO 0-5M [SEG]'].iloc[0]
                ant = df_sprint['TIEMPO 0-5M [SEG]'].iloc[1]
                variacion = act - ant;
                st.metric(f"TIEMPO 0-5M [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col3:
                act = df_sprint['VEL 0-5M [M/S]'].iloc[0]
                ant = df_sprint['VEL 0-5M [M/S]'].iloc[1]
                variacion = act - ant;
                st.metric(f"VEL 0-5M [M/S]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col4:
                act = df_sprint['TIEMPO 5-20M [SEG]'].iloc[0]
                ant = df_sprint['TIEMPO 5-20M [SEG]'].iloc[1]
                variacion = act - ant;
                st.metric(f"TIEMPO 5-20M [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col5:
                act = df_sprint['VEL 5-20M [M/S]'].iloc[0]
                ant = df_sprint['VEL 5-20M [M/S]'].iloc[1]
                variacion = act - ant;
                st.metric(f"VEL 5-20M [M/S]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col6:
                act = df_sprint['TIEMPO 20-40M [SEG]'].iloc[0]
                ant = df_sprint['TIEMPO 20-40M [SEG]'].iloc[1]
                variacion = act - ant;
                st.metric(f"TIEMPO 20-40M [SEG]",f'{act:,.2f}', f'{variacion:,.2f}')

            with col7:
                act = df_sprint['VEL 20-40M [M/S]'].iloc[0]
                ant = df_sprint['VEL 20-40M [M/S]'].iloc[1]
                variacion = act - ant;
                st.metric(f"VEL 20-40M [M/S]",f'{act:,.2f}', f'{variacion:,.2f}')

            styled_df = util.aplicar_semaforo(df_sprint)

            # Mostrar el DataFrame estilizado en Streamlit
            #st.markdown("#### Ultimos 5")
            st.dataframe(styled_df)
            #st.dataframe(df_sprint)

            st.divider()
######################################################################################################

            ## CMJ - YOYO

            c1, c2 = st.columns(2)

            with c1:
                df_cmj = df_joined_filtrado[["FECHA REGISTRO", "CMJ [cm]", "CMJ [W]"]]
                df_cmj = df_cmj.reset_index(drop=True)
                
                st.markdown("### :blue[CMJ]")

                col1, col2 = st.columns(2)

                with col1:
                    act = df_cmj['CMJ [cm]'].iloc[0]
                    ant = df_cmj['CMJ [cm]'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"CMJ [cm]",f'{act:,.1f}', f'{variacion:,.1f}')

                with col2:
                    act = df_cmj['CMJ [W]'].iloc[0]
                    ant = df_cmj['CMJ [W]'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"CMJ [W]",f'{act:,.1f}', f'{variacion:,.1f}')

                #st.markdown("#### Ultimos 5")
                #st.dataframe(df_cmj)
                graphics.get_cmj_graph(df_cmj)

            with c2:
                df_rsa = df_joined_filtrado[["FECHA REGISTRO", "MEDIDA EN TIEMPO (SEG)","VELOCIDAD (M*SEG)" ]]

                df_rsa = df_rsa.reset_index(drop=True)
                
                st.markdown("### :blue[RSA]")

                col1, col2 = st.columns(2)

                with col1:
                    act = df_rsa['MEDIDA EN TIEMPO (SEG)'].iloc[0]
                    ant = df_rsa['MEDIDA EN TIEMPO (SEG)'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"MEDIDA EN TIEMPO (SEG)",f'{act:,.1f}', f'{variacion:,.1f}')

                with col2:
                    act = df_rsa['VELOCIDAD (M*SEG)'].iloc[0]
                    ant = df_rsa['VELOCIDAD (M*SEG)'].iloc[1]
                    variacion = act - ant;
                    st.metric(f"VELOCIDAD (M*SEG)",f'{act:,.1f}', f'{variacion:,.1f}')

                #st.markdown("#### Ultimos 5")
                #st.dataframe(df_rsa)
                graphics.get_rsa_graph(df_rsa)

            st.divider()
######################################################################################################

            df_yoyo = df_joined_filtrado[["FECHA REGISTRO", "TEST", "SPEED [km/h]", "ACCUMULATED SHUTTLE DISTANCE [m]"]]
            df_yoyo = df_yoyo.reset_index(drop=True)
        
            st.markdown("### :blue[YO-YO]")
            col1, col2, col3 = st.columns(3)

            with col1:
                act = df_yoyo['SPEED [km/h]'].iloc[0]
                ant = df_yoyo['SPEED [km/h]'].iloc[1]
                variacion = 1;
                st.metric(f"505-ND [SEG]",f'{act:,.1f}', f'{variacion:,.1f}')

            with col2:
                act = df_yoyo['ACCUMULATED SHUTTLE DISTANCE [m]'].iloc[0]
                ant = df_yoyo['ACCUMULATED SHUTTLE DISTANCE [m]'].iloc[1]
                variacion = 1;
                st.metric(f"505-ND [SEG]",f'{act:,.1f}', f'{variacion:,.1f}')
            
            with col3:
                act = df_yoyo['TEST'].iloc[0]
                st.metric(f"TEST",act)

            #st.markdown("#### Ultimos 5")
            #st.dataframe(df_yoyo)           
            graphics.get_yoyo_graph(df_yoyo)

######################################################################################################
        else:
            st.text("El Jugador seleccionado no cuenta con datos suficientes")
    with tab2:
        
        if len(df_joined_filtrado) > 0:
            ###################################################
            ###################################################
            ## ANTROPOMETRIA - AGILIDAD

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.markdown("### :blue[ANTROPOMETRÍA]")
                st.dataframe(df_anthropometrics)
            with c2:
                st.markdown("### :blue[AGILIDAD 505]")
                st.dataframe(df_agilty)
            with c3:
                st.markdown("### :blue[CMJ]")
                st.dataframe(df_cmj)
            with c4:
                st.markdown("### :blue[RSA]")
                st.dataframe(df_rsa)

            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("### :blue[SPRINT LINEAL]")
                st.dataframe(df_sprint)
            with c2:
                st.markdown("### :blue[YO-YO]")
                st.dataframe(df_yoyo) 

        else:
            st.text("El Jugador seleccionado no cuenta con datos suficientes")
            
    with tab3:

        if len(df_joined_filtrado) > 0:
            
            df = pd.DataFrame(df_anthropometrics)

            df["FECHA REGISTRO"] = pd.to_datetime(df["FECHA REGISTRO"], format="%d/%m/%Y")

            # Cálculo de estadísticas
            stats = {
                "ALTURA": [df["ALTURA"].mean(), df["ALTURA"].max(), df["ALTURA"].min()],
                "PESO": [df["PESO"].mean(), df["PESO"].max(), df["PESO"].min()],
                "MG [KG]": [df["MG [KG]"].mean(), df["MG [KG]"].max(), df["MG [KG]"].min()],
                "GRASA (%)": [df["GRASA (%)"].mean(), df["GRASA (%)"].max(), df["GRASA (%)"].min()],
            }

            stats_df = pd.DataFrame(stats, index=["Promedio", "Máximo", "Mínimo"])

            c1, c2 = st.columns(2)     
            with c1:
                st.subheader(":blue[Valores promedio, máximos y mínimos]")
                with st.container(border=True):
                    st.markdown(":blue[ALTURA]")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        act = stats_df['ALTURA'].iloc[0]
                        #ant = df_anthropometrics['ALTURA'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Promedio",f'{act:,.2f}')

                    with col2:
                        act = stats_df['ALTURA'].iloc[1]
                        #act = df_anthropometrics['PESO'].iloc[0]
                        #ant = df_anthropometrics['PESO'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Max",f'{act:,.2f}')

                    with col3:
                        act = stats_df['ALTURA'].iloc[2]
                        #act = df_anthropometrics['MG [KG]'].iloc[0]
                        #ant = df_anthropometrics['MG [KG]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Min",f'{act:,.2f}')

                with st.container(border=True):
                    st.markdown(":blue[PESO]")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        act = stats_df['PESO'].iloc[0]
                        #ant = df_anthropometrics['PESO'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Promedio",f'{act:,.2f}')

                    with col2:
                        act = stats_df['PESO'].iloc[1]
                        #act = df_anthropometrics['PESO'].iloc[0]
                        #ant = df_anthropometrics['PESO'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Max",f'{act:,.2f}')

                    with col3:
                        act = stats_df['PESO'].iloc[2]
                        #act = df_anthropometrics['MG [KG]'].iloc[0]
                        #ant = df_anthropometrics['MG [KG]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Min",f'{act:,.2f}')

                with st.container(border=True):
                    st.markdown(":blue[MG [KG]]")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        act = stats_df['MG [KG]'].iloc[0]
                        #ant = df_anthropometrics['MG [KG]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Promedio",f'{act:,.2f}')

                    with col2:
                        act = stats_df['MG [KG]'].iloc[1]
                        #act = df_anthropometrics['MG [KG]'].iloc[0]
                        #ant = df_anthropometrics['MG [KG]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Max",f'{act:,.2f}')

                    with col3:
                        act = stats_df['MG [KG]'].iloc[2]
                        #act = df_anthropometrics['MG [KG]'].iloc[0]
                        #ant = df_anthropometrics['MG [KG]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Min",f'{act:,.2f}')

                with st.container(border=True):
                    st.markdown(":blue[GRASA (%)]")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        act = stats_df['GRASA (%)'].iloc[0]
                        #ant = df_anthropometrics['GRASA (%)]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Promedio",f'{act:,.2f}')

                    with col2:
                        act = stats_df['GRASA (%)'].iloc[1]
                        #act = df_anthropometrics['GRASA (%)]'].iloc[0]
                        #ant = df_anthropometrics['GRASA (%)]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Max",f'{act:,.2f}')

                    with col3:
                        act = stats_df['GRASA (%)'].iloc[2]
                        #act = df_anthropometrics['GRASA (%)]'].iloc[0]
                        #ant = df_anthropometrics['GRASA (%)]'].iloc[1]
                        #variacion = act - ant;
                        st.metric(f"Min",f'{act:,.2f}')

            with c2:
                # Cálculo del IMC
                df["IMC"] = df["PESO"] / ((df["ALTURA"] / 100) ** 2)
            
                df["Categoría IMC"] = df["IMC"].apply(util.categorizar_imc)
                
                # Índice de grasa corporal
                df["Índice de grasa"] = (df["GRASA (%)"] * df["PESO"]) / 100

                df["Categoría Grasa"] = df["GRASA (%)"].apply(util.categorizar_grasa)

                # Streamlit UI
                #st.dataframe(stats_df)

                st.subheader(":blue[Análisis de IMC y Porcentaje de Grasa Corporal]")
                #st.dataframe(df[["FECHA REGISTRO", "ALTURA", "PESO", "IMC", "Categoría IMC", "Índice de grasa", "Categoría Grasa"]]
                #             .style.applymap(util.color_categorias, subset=["Categoría IMC", "Categoría Grasa"]))
                st.markdown(df[["FECHA REGISTRO", "ALTURA", "PESO", "IMC", "Categoría IMC", "Índice de grasa", "Categoría Grasa"]].to_html(escape=False, index=False), unsafe_allow_html=True)

        ############################

        else:
            st.text("El Jugador seleccionado no cuenta con datos suficientes")   