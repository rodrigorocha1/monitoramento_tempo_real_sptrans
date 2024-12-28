from typing import List
import requests
import os
from config.config import URL_API_SPTRANS, CHAVE_API_SPTRANS


class SptransAPI:
    def __init__(self):
        self.__chave = URL_API_SPTRANS
        self.__url_api = CHAVE_API_SPTRANS

    def __gerar_autenticacao(self):
        requisicao = requests.post(
            self.__url_api + 'Login/Autenticar?token=' + self.__chave
        )
        return requisicao.headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def buscar_dados_linha(self, codigo_linha: str) -> List[int]:
        cookie = self.__gerar_autenticacao()
        response = requests.get(
            f"{self.__url_api}Linha/Buscar?termosBusca={codigo_linha}",
            cookies={
                'apiCredentials': cookie
            }
        )
        if response.status_code == 200:
            return list(map(lambda x: x['cl'], response.json()))
        else:
            raise Exception("Erro ao obter posições de ônibus.")

    def buscar_posicao_linha(self, codigos_interno_linha: List):
        cookie = self.__gerar_autenticacao()
        response_completo = []
        for codigo_interno_linha in codigos_interno_linha:
            response = requests.get(
                f"{self.__url_api}Posicao/Linha?codigoLinha={codigo_interno_linha}",
                cookies={
                    'apiCredentials': cookie
                }
            )
            response_completo += response.json()['vs']

        return response_completo


if __name__ == "__main__":
    sptransapi = SptransAPI()
    linhas = sptransapi.buscar_dados_linha(codigo_linha='2678-10')

    posicoes = sptransapi.buscar_posicao_linha(
        codigos_interno_linha=linhas)
    print(posicoes)

    # posicao = sptransapi.buscar_posicao_linha(codigo_interno_linha=linha)
