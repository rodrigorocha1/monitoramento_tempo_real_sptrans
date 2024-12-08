from src.service.sptrans_api import SptransAPI
from src.fabrica_kafka.kafka_produtor import KafkaProdutor
from time import sleep
import os


class Produtor:

    def __init__(self):
        self.__kp = KafkaProdutor(
            bootstrap_servers=os.environ['URL_KAFKA']
        )
        self.__api_sptrans = SptransAPI()

    def enviar_linhas_kafka(self, codigo_linha: str, indice: int, topico: str):
        linhas = self.__api_sptrans.buscar_dados_linha(
            codigo_linha=codigo_linha)
        posicoes = self.__api_sptrans.buscar_posicao_linha(linhas[indice])

        for indice_particao, posicao in enumerate(posicoes):
            self.__kp.enviar_dados(
                topico=topico,
                particao=indice_particao,
                chave=posicao['p'],
                dados=posicao
            )

    def rodar_produtor(self, codigo_linha='2678-10'):
        linhas = self.__api_sptrans.buscar_dados_linha(codigo_linha='2678-10')

        posicoes = self.__api_sptrans.buscar_posicao_linha(
            codigos_interno_linha=linhas)

        topico = f'linha_{codigo_linha}'
        self.__kp.criar_topico(topico=topico, numero_particoes=len(posicoes))

        while True:

            linhas = self.__api_sptrans.buscar_dados_linha(
                codigo_linha=codigo_linha)
            posicoes = self.__api_sptrans.buscar_posicao_linha(
                codigos_interno_linha=linhas)

            for indice_particao, posicao in enumerate(posicoes):
                self.__kp.enviar_dados(
                    topico=topico,
                    particao=indice_particao,
                    chave=posicao['p'],
                    dados=posicao
                )
            sleep(3)


if __name__ == '__main__':
    p = Produtor()
    p.rodar_produtor()
