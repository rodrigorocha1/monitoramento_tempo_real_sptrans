import streamlit as st
from src.fabrica_kafka.kafka_produtor import KafkaProdutor
from src.controller.controller import Controller
import folium
from streamlit_folium import st_folium


class DashboardMapa:

    def __init__(self):
        st.set_page_config(
            layout='wide'
        )
        self.__controller = Controller()

        if "mapa_dados" not in st.session_state:
            st.session_state["mapa_dados"] = None
        if "topicos_processados" not in st.session_state:
            st.session_state["topicos_processados"] = []

    def listar_inputs(self):
        topico = st.text_input(
            'Digite o nome do tópico',
            placeholder='Ex: 1012-10'
        )

        botao = st.button(
            'Cadastrar tópico - Linha'
        )
        if botao:

            # if topico in st.session_state["topicos_processados"]:
            #     st.warning("Este tópico já foi processado!")
            #     return

            nome_completo_linha, cor_trajeto, cor_nome_linha, dataframe = self.__controller.gerar_dados_mapa(
                linha=topico)
            coordenadas = dataframe[['lat', 'lon']].values.tolist()

            if st.session_state["mapa_dados"] is None:
                st.session_state["mapa_dados"] = folium.Map(
                    location=[-23.5703934, -46.665128],
                    zoom_start=13
                )
            folium.PolyLine(
                coordenadas,
                color='blue'
            ).add_to(st.session_state["mapa_dados"])
            st.session_state["topicos_processados"].append(topico)

        col_um, col_dois = st.columns([0.70, 0.30])
        with col_um:
            if st.session_state["mapa_dados"]:
                st_folium(
                    st.session_state["mapa_dados"],
                    width=1900,
                    height=1500
                )
        with col_dois:
            pass

    def rodar_dashboard(self):
        self.listar_inputs()
