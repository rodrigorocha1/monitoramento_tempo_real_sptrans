from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.model.config_base import Base
from sqlalchemy.orm.session import Session
import os


class ConexaoBancoDuckDb:
    def __init__(self):

        self.__CAMINHO_RAIZ = os.getcwd()
        self.__CAMINHO_BANCO = os.path.join(
            self.__CAMINHO_RAIZ,
            'dados',
            'rrrochaa_gtfs'
        )
        self.__DATABASE_URL = 'duckdb:////' + self.__CAMINHO_BANCO
        self.__conexao = create_engine(
            self.__DATABASE_URL,
            echo=False
        )
        self.__Sessao = sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self.__conexao
        )

    def obter_conexao(self):
        return self.__conexao

    def obter_sessao(self):
        return self.__Sessao()
