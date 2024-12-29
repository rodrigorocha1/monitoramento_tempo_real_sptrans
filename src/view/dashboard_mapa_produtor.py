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

        self._produtor = KafkaProdutor()
        self.__service_api = SptransAPI()

    def gerar_input(self):
        topico = st.text_input(
            'Digite o nome do tópico - Linha',
            placeholder='Ex: 1012-10'
        )

        botao = st.button(
            'Cadastrar tópico - Linha'
        )
        if botao:

            return topico

    def gerar_produtor(self, codigo_linha: str):
        linhas = self.__service_api.buscar_dados_linha(
            codigo_linha=codigo_linha)
        print(codigo_linha, linhas)

        posicoes = self.__service_api.buscar_posicao_linha(
            codigos_interno_linha=linhas)
        print(codigo_linha, linhas, posicoes)

        topico = f'posicoes_onibus'
        print(codigo_linha, linhas, posicoes, topico)
        self._produtor.criar_topico(
            topico=topico, numero_particoes=len(posicoes))

        while True:

            linhas = self.__service_api.buscar_dados_linha(
                codigo_linha=codigo_linha)
            posicoes = self.__service_api.buscar_posicao_linha(
                codigos_interno_linha=linhas)

            for indice_particao, posicao in enumerate(posicoes):
                self._produtor.enviar_dados(
                    topico=topico,
                    particao=indice_particao,
                    chave=posicao['p'],
                    dados=posicao
                )
            sleep(3)

    def gerar_mapa_consumidor(self, topico: str):
        consumidor = self.__consumidor
        topico = f'linha_{topico}'
        consumidor.topico = topico
        mensagens_container = st.empty()

        for mensagem in consumidor.consumir_mensagens():
            valor = mensagem.value
            st.write(valor)

    def rodar_dashboard(self):
        topico = self.gerar_input()

        if topico is not None:
            self.gerar_produtor(codigo_linha=topico)
            st.success(f'Tópico {topico} cadastrado com sucesso')
