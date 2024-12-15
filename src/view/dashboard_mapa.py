import streamlit as st
from src.fabrica_kafka.kafka_produtor import KafkaProdutor


class DashboardMapa:
    st.set_page_config(
        layout='wide'
    )

    # def __init__(self):
    #     self.__kafka_produtor = KafkaProdutor()

    def listar_inputs(self):
        topico = st.text_input('Digite o nome do tótpico')

    def rodar_dashboard(self):
        self.listar_inputs()
