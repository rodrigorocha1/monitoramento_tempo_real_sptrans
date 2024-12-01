from fabrica_kafka.kafka_consumidor import KafkaConsumidor

kc = KafkaConsumidor(
    group_id='topico_teste_g',
    topico='temperatura_sensor_um'
)

for dados in kc.consumir_mensagens():
    print(dados)
    print()
    print()
