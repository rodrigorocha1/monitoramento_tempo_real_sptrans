from src.model.consulta import Consulta


class Controller:

    def __init__(self):
        self.__consulta = Consulta()

    def gerar_dados_mapa(self, linha: str):
        dataframe = self.__consulta.consultar_rotas(linha=linha)

        nome_completo_linha = dataframe.loc[0, 'route_long_name']
        cor_trajeto = dataframe.loc[0, 'route_color']
        cor_nome_linha = dataframe.loc[0, 'route_text_color']
        print(dataframe)
        print(cor_nome_linha)
        print(cor_trajeto)
        print(nome_completo_linha)
        codigos_linha = self.__consulta.consultar_viagens(linha=linha)
        print(codigos_linha)
        dataframe = self.__consulta.consultar_trajeto(shape_id=codigos_linha)
