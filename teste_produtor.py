from fabrica_kafka.kafka_consumidor import KafkaConsumidor
from fabrica_kafka.kafka_produtor import KafkaProdutor
from random import randint
from datetime import datetime


def sensor(nome: str):
    return {
        'nome_sensor': nome,
        'temperatura': randint(0, 100),
        'data_hora_temperatura': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


kp = KafkaProdutor()
