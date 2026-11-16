# =============================================================
# FUNCOES DE ESTATISTICA
# Todas recebem "dados": a lista de clientes da consulta atual
# (se tiver filtro na tela, so os clientes filtrados).
# Cada cliente e um dicionario, e os numeros ja vem como float.
# =============================================================


# ---------- MEDIAS ----------
def calcular_media(dados, coluna):
    if len(dados) == 0:
        return 0
    soma = 0
    for cliente in dados:
        soma += cliente[coluna]
    return soma / len(dados)


def media_saldo(dados):
    return calcular_media(dados, 'Balance')


def media_salario(dados):
    return calcular_media(dados, 'EstimatedSalary')


def media_score(dados):
    return calcular_media(dados, 'CreditScore')


def media_idade(dados):
    return calcular_media(dados, 'Age')


# ---------- CONTAGEM POR PAIS ----------
def contar_por_pais(dados):
    # Devolve um dicionario: {'France': 63171, 'Germany': 22939, ...}
    contagem = {}
    for cliente in dados:
        pais = cliente['Geography']
        if pais in contagem:
            contagem[pais] += 1
        else:
            contagem[pais] = 1
    return contagem


# ---------- SCORE DE CREDITO ----------
def classificar_score(score):
    # Faixas pedidas no enunciado do trabalho.
    if score >= 750:
        return 'Excelente'
    elif score >= 650:
        return 'Bom'
    elif score >= 500:
        return 'Regular'
    else:
        return 'Ruim'


def contar_por_faixa_score(dados):
    # Devolve um dicionario: {'Excelente': 12525, 'Bom': 47558, ...}
    contagem = {'Excelente': 0, 'Bom': 0, 'Regular': 0, 'Ruim': 0}
    for cliente in dados:
        faixa = classificar_score(cliente['CreditScore'])
        contagem[faixa] += 1
    return contagem
