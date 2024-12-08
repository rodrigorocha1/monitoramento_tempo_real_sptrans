from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
import json
from typing import Dict


class KafkaProdutor:
    def __init__(self, bootstrap_servers: str):
        self.__produtor = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8')
        )

        self.__admin_cliente = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers
        )

    def criar_topico(self, topico: str, numero_particoes: int):
        try:
            novo_topico = NewTopic(
                name=topico,
                num_partitions=numero_particoes,
                replication_factor=1
            )
            self.__admin_cliente.create_topics([novo_topico])

        except:
            pass

    def verificar_particoes(self, topico: str) -> int:
        particoes = self.__admin_cliente.describe_topics([topico])
        return len(particoes[0]['partitions'])

    def enviar_dados(self, topico: str, dados: Dict, chave: str, particao: int):

        self.__produtor.send(
            topic=topico,
            value=dados,
            key=chave,
            partition=particao
        )
        self.__produtor.flush()
