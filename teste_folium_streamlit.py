import folium
import streamlit as st
from streamlit_folium import st_folium

# Criando o mapa
m = folium.Map(location=[-21.1791039, -47.8850273], zoom_start=16)

# Adicionando um marcador com ícone de ônibus
folium.Marker(
    location=[-21.1791039, -47.8850273],
    popup='Ribeirão Preto',
    icon=folium.Icon(icon="bus", prefix="fa", color="red")
).add_to(m)

# Exibindo o mapa no Streamlit
st_data = st_folium(m, width=1000)
