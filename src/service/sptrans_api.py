from dotenv import load_dotenv
import requests
import os
load_dotenv()


class SptransAPI:
    def __init__(self):
        self.__chave = os.environ['API_SPTRANS_TOKEN']
        self.__url_api = os.environ['URL_SPTRANS']

    def __gerar_autenticacao(self):
        requisicao = requests.post(
            self.__url_api + 'Login/Autenticar?token=' + self.__chave
        )
        return requisicao.headers['Set-Cookie'].split(';')[0].split('=')[-1]

    def buscar_dados_linha(self, codigo_linha: str):
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

    def buscar_posicao_linha(self, codigo_interno_linha: int):
        cookie = self.__gerar_autenticacao()
        response = requests.get(
            f"{self.__url_api}Posicao/Linha?codigoLinha={codigo_interno_linha}",
            cookies={
                'apiCredentials': cookie
            }
        )
        return response.json()['vs']


if __name__ == "__main__":
    sptransapi = SptransAPI()
    linhas = sptransapi.buscar_dados_linha(codigo_linha='2678-10')
    for linha in linhas:
        print()

        print(linha)
        print(len(sptransapi.buscar_posicao_linha(codigo_interno_linha=linha)))
        for posicao in sptransapi.buscar_posicao_linha(codigo_interno_linha=linha):
            print(posicao)
