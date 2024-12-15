import streamlit as st
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()

KAFKA_BROKER = os.environ['URL_KAFKA']


def criar_topico(admin_client: KafkaAdminClient, nome_topico: str, num_particoes: int, num_replicas: int) -> str:
    try:
        topico = NewTopic(
            name=nome_topico, num_partitions=num_particoes, replication_factor=num_particoes)
        admin_client.create_topics([topico])
        return f'Tópico "{nome_topico}" criado com sucesso!'
    except TopicAlreadyExistsError:
        return f'Tópico {nome_topico} já existe'
    except Exception as e:
        return f'Erro ao criar tópico: {str(e)}'


def listar_topicos(admin_client: KafkaAdminClient) -> List[str]:
    return admin_client.list_topics()


def apagar_topico(admin_cliente: KafkaAdminClient, nome_topico: str) -> str:
    try:
        admin_cliente.delete_topics([nome_topico])
        return f'Tópico {nome_topico} excluído com sucesso'
    except UnknownTopicOrPartitionError:
        return f'Erro: O tópico {nome_topico} não existe'
    except Exception as e:
        return f'Erro ao apagar o tópico : {str(e)}'


st.title('Dashboard de gerenciamento de tópicos do apache kafka')

try:
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_BROKER, client_id='streamlit-dashboard')
    st.success('Conectado ao apache kafka')
except Exception as e:
    st.error(f'Erro ao conectar ao kafka: {str((e))}')
    st.stop()

st.subheader('Criar novo tópico')
nome_topico = st.text_input('Nome do tópico')
num_particoes = st.number_input(
    'Número de partições', min_value=1, value=1, step=1)
num_replicas = st.number_input(
    'Fator de replicação', min_value=1, value=1, step=1)
if st.button('Criar tópico'):
    if nome_topico:
        mensagem = criar_topico(admin_client, nome_topico, int(
            num_particoes), int(num_replicas))
        st.info(mensagem)
    else:
        st.warning('Insira o nome do tópico')

st.subheader("Apagar Tópico")
nome_topico_apagar = st.text_input("Nome do Tópico para Apagar")

if st.button("Apagar Tópico"):
    if nome_topico_apagar:
        mensagem = apagar_topico(admin_client, nome_topico_apagar)
        st.info(mensagem)
    else:
        st.warning("Por favor, insira o nome do tópico para apagar.")

# Interface para listar tópicos existentes
st.subheader("Tópicos Existentes")
if st.button("Atualizar Lista de Tópicos"):
    try:
        topicos = listar_topicos(admin_client)
        st.write(topicos)
    except Exception as e:
        st.error(f"Erro ao listar tópicos: {str(e)}")
