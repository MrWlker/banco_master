# PONTO DE PARTIDA DO PROGRAMA
# Para rodar:  python src/app.py
import os

from services import filtros
from styles.windows import abrir_janela

# Garante que o programa procura o test.csv a partir da pasta do projeto.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Le o test.csv (funcao do grupo)
filtros.leitura()

# 2. Abre a interface, entregando os dados lidos
abrir_janela(filtros.dados_gerais)
