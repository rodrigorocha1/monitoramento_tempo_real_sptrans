from src.controller.controller import Controller

c = Controller()
dados = c.gerar_dados_mapa(linha='1012-10')
print(dados)
