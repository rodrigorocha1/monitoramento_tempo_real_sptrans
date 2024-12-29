from kafka import KafkaConsumer
import json
import os
from dotenv import load_dotenv

load_dotenv()


class KafkaConsumidor:
    def __init__(self, group_id: str):
        self.__topico = None
        self.__consumer = None

    @property
    def topico(self):
        return self.__topico

    @topico.setter
    def topico(self, novo_topico: str):
        if novo_topico:
            self.__topico = novo_topico
            self.__consumer = KafkaConsumer(
                self.__topico,
                bootstrap_servers=os.environ['URL_KAFKA'],
                group_id='linhas',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                auto_offset_reset='latest',
                enable_auto_commit=True
            )

        else:
            pass

    def consumir_mensagens(self):
        for mensagem in self.__consumer:
            yield mensagem
