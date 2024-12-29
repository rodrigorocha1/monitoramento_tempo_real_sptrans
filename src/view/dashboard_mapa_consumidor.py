import streamlit as st
from src.fabrica_kafka.kafka_produtor import KafkaProdutor
from src.fabrica_kafka.kafka_consumidor import KafkaConsumidor
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
        self._produtor = KafkaProdutor()
        self.__consumidor = KafkaConsumidor()

    #     if "mapas" not in st.session_state:
    #         st.session_state["mapas"] = {}
    #     if "topicos_processados" not in st.session_state:
    #         st.session_state["topicos_processados"] = []

    # def gerar_input(self):
    #     topico = st.text_input(
    #         'Digite o nome do tópico - Linha',
    #         placeholder='Ex: 1012-10'
    #     )

    #     botao = st.button(
    #         'Cadastrar tópico - Linha'
    #     )
    #     if botao:
    #         if topico in st.session_state["topicos_processados"]:
    #             st.warning("Este tópico já foi processado!")
    #             return

    #         nome_completo_linha, cor_trajeto, cor_nome_linha, dataframe = self.__controller.gerar_dados_mapa(
    #             linha=topico)
    #         coordenadas = dataframe[['lat', 'lon']].values.tolist()
    #         print(cor_trajeto, cor_nome_linha)

    #         novo_mapa = folium.Map(
    #             location=[-23.5703934, -46.665128],
    #             zoom_start=10
    #         )
    #         folium.PolyLine(
    #             coordenadas,
    #             color=f'#{cor_trajeto}'
    #         ).add_to(novo_mapa)

    #         st.session_state["mapas"][topico] = novo_mapa

    #         st.session_state["topicos_processados"].append(topico)
    #         return topico

    # def gerar_produtor(self, codigo_linha: str):
    #     linhas = self.__service_api.buscar_dados_linha(
    #         codigo_linha=codigo_linha)

    #     posicoes = self.__service_api.buscar_posicao_linha(
    #         codigos_interno_linha=linhas)

    #     topico = f'linha_{codigo_linha}'
    #     self._produtor.criar_topico(
    #         topico=topico, numero_particoes=len(posicoes))

    #     while True:

    #         linhas = self.__service_api.buscar_dados_linha(
    #             codigo_linha=codigo_linha)
    #         posicoes = self.__service_api.buscar_posicao_linha(
    #             codigos_interno_linha=linhas)

    #         for indice_particao, posicao in enumerate(posicoes):
    #             self._produtor.enviar_dados(
    #                 topico=topico,
    #                 particao=indice_particao,
    #                 chave=posicao['p'],
    #                 dados=posicao
    #             )
    #         sleep(3)

    def gerar_mapa_consumidor(self):
        mapa_sp = folium.Map(
                location=[-23.5703934, -46.665128],
                zoom_start=10
            )

        for mensagem in self.__consumidor.consumir_mensagens():

            posicoes = mensagem.value
        
            print(posicoes)
        
            folium.Marker(
                    location=[posicoes['py'], posicoes['px']],
                    popup=f'Ônibus: {posicoes["p"]}',
                    icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(mapa_sp)
            st_folium(mapa_sp)


    def rodar_dashboard(self):
        self.gerar_mapa_consumidor()
        
