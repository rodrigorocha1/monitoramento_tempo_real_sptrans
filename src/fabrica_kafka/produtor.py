from src.service.sptrans_api import SptransAPI
from fabrica_kafka.kafka_produtor import KafkaProdutor
from random import randint
from datetime import datetime
from time import sleep
import os


class Produtor:

    def __init__(self):
        self.__kp = KafkaProdutor(
            bootstrap_servers=os.environ['URL_KAFKA']
        )
        self.__api_sptrans = SptransAPI()

    def rodar_produtor(self, codigo_linha='2678-10'):
        while True:
            linhas = self.__api_sptrans.buscar_dados_linha(
                codigo_linha=codigo_linha)
            for linha in linhas:
                topico = f'linha_{linha}'
                posicoes = self.__api_sptrans.buscar_posicao_linha(
                    codigo_interno_linha=linha)
                total_particoes = len(posicoes)

                self.__kp.criar_topico(
                    topico=topico, numero_particoes=total_particoes)
                for posicao in posicoes:
                    self.__kp.enviar_dados(
                        topico=topico,
                        particao=total_particoes,
                        chave=posicao['p'],
                        dados=posicao
                    )
