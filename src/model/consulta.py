from typing import Tuple
from src.model.conexao_banco import ConexaoBancoDuckDb
from src.model.config_base import Base
from sqlalchemy import text
import pandas as pd


class Consulta:

    def __init__(self):
        self.__db = ConexaoBancoDuckDb()
        Base.metadata.create_all(self.__db.obter_conexao())

    def consultar_rotas(self, linha: str = '1012-10'):
        sql = """
        SELECT 
            r.route_id route_id,
            r.route_long_name  route_long_name,
            r.route_color as route_color,
            r.route_text_color as route_text_color
        from rotas r
        where r.route_id = ?

        """

        parametros = (linha, )
        tipos = {
            'route_id': 'string',
            'route_long_name': 'string',
            'route_color': 'string',
            'route_text_color': 'string'
        }
        try:
            dataframe = pd.read_sql_query(
                sql=sql,
                con=self.__db.obter_conexao(),
                params=parametros,
                dtype=tipos

            )
        finally:
            self.__db.obter_sessao().close()

        return dataframe

    def consultar_viagens(self, linha: str = '1012-10'):
        sql = """
            SELECT shape_id
            FROM viagens
            WHERE  route_id = ?

        """

        parametros = (linha, )
        tipos = {
            'shape_id': 'int64',
        }
        try:
            dataframe = pd.read_sql_query(
                sql=sql,
                con=self.__db.obter_conexao(),
                params=parametros,
                dtype=tipos

            )
        finally:
            self.__db.obter_sessao().close()

        return dataframe['shape_id'].to_list()

    def consultar_trajeto(self, shape_id):
        sql = """
            SELECT shape_pt_lat lat,
                shape_pt_lon lon
            FROM trajetos
            WHERE shape_id IN ({})
        """.format(','.join(['?'] * len(shape_id)))
        parametros = tuple(shape_id)

        tipos = {
            'lat': 'float64',
            'lon': 'float64'
        }
        try:
            dataframe = dataframe = pd.read_sql_query(
                sql=sql,
                con=self.__db.obter_conexao(),
                params=parametros,
                dtype=tipos

            )
        finally:
            self.__db.obter_sessao().close()

        return dataframe
