import streamlit as st
from src.fabrica_kafka.kafka_produtor import KafkaProdutor
from src.service.sptrans_api import SptransAPI
from src.controller.controller import Controller
import folium
from streamlit_folium import st_folium
from time import sleep


class DashboardMapa:

    def __init__(self):
        st.set_page_config(
            layout='wide'
        )
        self.__controller = Controller()
        self.__consumidor = KafkaProdutor()
        self.__service_api = SptransAPI()

        if "mapas" not in st.session_state:
            st.session_state["mapas"] = {}
        if "topicos_processados" not in st.session_state:
            st.session_state["topicos_processados"] = []

    def gerar_input(self):
        topico = st.text_input(
            'Digite o nome do tópico - Linha',
            placeholder='Ex: 1012-10'
        )

        botao = st.button(
            'Cadastrar tópico - Linha'
        )
        if botao:
            if topico in st.session_state["topicos_processados"]:
                st.warning("Este tópico já foi processado!")
                return

            nome_completo_linha, cor_trajeto, cor_nome_linha, dataframe = self.__controller.gerar_dados_mapa(
                linha=topico)
            coordenadas = dataframe[['lat', 'lon']].values.tolist()
            print(cor_trajeto, cor_nome_linha)

            novo_mapa = folium.Map(
                location=[-23.5703934, -46.665128],
                zoom_start=10
            )
            folium.PolyLine(
                coordenadas,
                color=f'#{cor_trajeto}'
            ).add_to(novo_mapa)

            st.session_state["mapas"][topico] = novo_mapa

            st.session_state["topicos_processados"].append(topico)
            return topico

    def gerar_produtor(self, codigo_linha: str):
        linhas = self.__service_api.buscar_dados_linha(
            codigo_linha=codigo_linha)

        posicoes = self.__service_api.buscar_posicao_linha(
            codigos_interno_linha=linhas)

        topico = f'linha_{codigo_linha}'
        self.__consumidor.criar_topico(
            topico=topico, numero_particoes=len(posicoes))

        while True:

            linhas = self.__service_api.buscar_dados_linha(
                codigo_linha=codigo_linha)
            posicoes = self.__service_api.buscar_posicao_linha(
                codigos_interno_linha=linhas)

            for indice_particao, posicao in enumerate(posicoes):
                self.__consumidor.enviar_dados(
                    topico=topico,
                    particao=indice_particao,
                    chave=posicao['p'],
                    dados=posicao
                )
            sleep(3)

    def gerar_mapa(self):

        for topico, mapa in st.session_state["mapas"].items():
            with st.container():
                col1, col2 = st.columns([0.75, 0.25])
                with col1:
                    st.markdown(
                        f"## Mapa para o tópico - Linha: {topico}")
                    st_folium(
                        mapa,
                        width=1000,
                        height=800
                    )
                with col2:
                    st.write('Coluna 2')

    def rodar_dashboard(self):
        topico = self.gerar_input()
        self.gerar_mapa()
