from src.model.conexao_banco import ConexaoBancoDuckDb
from src.model.config_base import Base


class Consulta:

    def __init__(self):
        self.__db = ConexaoBancoDuckDb()
        Base.metadata.create_all(self.__db.obter_conexao())

    def consultar_rotas(self):
