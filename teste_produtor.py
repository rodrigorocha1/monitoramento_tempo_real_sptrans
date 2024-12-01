from fabrica_kafka.kafka_consumidor import KafkaConsumidor
from fabrica_kafka.kafka_produtor import KafkaProdutor
from random import randint
from datetime import datetime
from time import sleep
import os


def sensor(nome: str):
    return {
        'nome_sensor': nome,
        'temperatura': randint(0, 100),
        'data_hora_temperatura': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


kp = KafkaProdutor(
    bootstrap_servers=os.environ['URL_KAFKA']
)
while True:
    sensor_um = sensor('sensor_um')
    topico = 'temperatura_sensor_um'
    kp.criar_topico(topico=topico, numero_particoes=1)
    total_particoes = kp.verificar_particoes(topico=topico)
    kp.enviar_dados(
        chave='temperatura_sensor_um_chave',
        particao=0,
        dados=sensor_um,
        topico=topico
    )
    sleep(3)
