from kafka import KafkaConsumer
import json
import os
from dotenv import load_dotenv

load_dotenv()


class KafkaConsumidor:
    def __init__(self, group_id: str, topico: str):
        self.__consumer = KafkaConsumer(
            topico,
            bootstrap_servers=os.environ['URL_KAFKA'],
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )

    def consumir_mensagens(self):
        for mensagem in self.__consumer:
            yield mensagem
