# =============================================================
# GRAFICOS (pandas + matplotlib)
# Cada funcao recebe:
#   dados -> a lista de clientes da consulta atual (a mesma das estatisticas)
#   eixo  -> o "quadro" do matplotlib onde o grafico vai ser desenhado
# O pandas transforma a lista em uma tabela (DataFrame) e desenha o grafico.
# =============================================================
import pandas as pd

from services.estatisticas import classificar_score

AZUL = "#0B2F8A"
CORES_FAIXAS = ["#1E8E3E", "#0B2F8A", "#E8A317", "#C5221F"]   # Excelente, Bom, Regular, Ruim
ORDEM_FAIXAS = ["Excelente", "Bom", "Regular", "Ruim"]


def deixar_bonito(eixo, titulo):
    # Titulo, letras menores e sem as bordas de cima e da direita.
    eixo.set_title(titulo, fontsize=11, color=AZUL)
    eixo.tick_params(labelsize=8)
    eixo.spines["top"].set_visible(False)
    eixo.spines["right"].set_visible(False)


def grafico_por_pais(dados, eixo):
    # Barras: quantos clientes tem em cada pais.
    tabela = pd.DataFrame(dados, columns=["Geography"])
    contagem = tabela["Geography"].value_counts().sort_index()
    contagem.plot.bar(ax=eixo, color=AZUL, rot=0)
    deixar_bonito(eixo, "Clientes por país")
    eixo.set_xlabel("")


def grafico_por_faixa_score(dados, eixo):
    # Barras: quantos clientes tem em cada faixa de score de credito.
    tabela = pd.DataFrame(dados, columns=["CreditScore"])
    tabela["Faixa"] = tabela["CreditScore"].apply(classificar_score)
    contagem = tabela["Faixa"].value_counts().reindex(ORDEM_FAIXAS, fill_value=0)
    contagem.plot.bar(ax=eixo, color=CORES_FAIXAS, rot=0)
    deixar_bonito(eixo, "Clientes por faixa de score")
    eixo.set_xlabel("")


def grafico_idades(dados, eixo):
    # Histograma: como as idades dos clientes estao distribuidas.
    tabela = pd.DataFrame(dados, columns=["Age"])
    tabela["Age"].plot.hist(ax=eixo, bins=range(18, 96, 3), color=AZUL)
    deixar_bonito(eixo, "Distribuição de idades")
    eixo.set_xlabel("Idade", fontsize=9)
    eixo.set_ylabel("Clientes", fontsize=9)
