from time import sleep
import streamlit as st
from src.fabrica_kafka.kafka_produtor import KafkaProdutor
from src.fabrica_kafka.kafka_consumidor import KafkaConsumidor
from src.controller.controller import Controller
from src.service.sptrans_api import SptransAPI
import folium
from streamlit_folium import st_folium


class DashboardMapa:

    def __init__(self):
        st.set_page_config(
            layout='wide'
        )
        self.__controller = Controller()
        self.__kafka_produtor = KafkaProdutor()
        self.__kafka_consumidor = KafkaConsumidor()
        self.__service_sptrans = SptransAPI()

        if "mapas" not in st.session_state:
            st.session_state["mapas"] = {}
        if "topicos_processados" not in st.session_state:
            st.session_state["topicos_processados"] = []

    def gerar_produtor(self):
        codigo_linha = st.text_input(
            'Digite o nome do tópico - Linha',
            placeholder='Ex: 1012-10'
        )
        botao = st.button(
            'Cadastrar tópico - Linha'
        )
        topico = f'linha_{codigo_linha}'
        if botao:
            if topico in st.session_state["topicos_processados"]:
                st.warning("Este tópico já foi processado!")
                return
            linhas = self.__service_sptrans.buscar_dados_linha(
                codigo_linha=codigo_linha)
            posicoes = self.__service_sptrans.buscar_posicao_linha(
                codigos_interno_linha=linhas)

            self.__kafka_produtor.criar_topico(
                topico=topico, numero_particoes=len(posicoes))
            while True:

                linhas = self.__service_sptrans.buscar_dados_linha(
                    codigo_linha=codigo_linha)
                posicoes = self.__service_sptrans.buscar_posicao_linha(
                    codigos_interno_linha=linhas)

                for indice_particao, posicao in enumerate(posicoes):
                    self.__kafka_produtor.enviar_dados(
                        topico=topico,
                        particao=indice_particao,
                        chave=posicao['p'],
                        dados=posicao
                    )
                sleep(3)

    def rodar_dashboard(self):
        self.gerar_produtor()
