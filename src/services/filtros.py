# =============================================================
# FUNCOES DO GRUPO (vieram do notebook do Colab)
# O codigo das funcoes e o mesmo do notebook original, que esta
# guardado em docs/codigo_original_colab.ipynb.
# Unica linha trocada: o endereco do test.csv dentro de leitura()
# (o proprio comentario da funcao pede essa troca).
#
# A parte 4 (pais, faixa de idade, faixa de score e saldo) foi
# adicionada depois, seguindo o mesmo jeito da parte 3.
# =============================================================
from services.estatisticas import classificar_score


# ---------- 1. LEITURA DO ARQUIVO ----------
#lembrar de trocar o endereço do arquivo pra testar
def leitura():
    with open('data/test.csv', 'r', encoding = 'utf-8') as f:
        linha = 0
        global nomes_das_variaveis
        nomes_das_variaveis = []
        global dados_gerais
        dados_gerais = []
        dados_especificos = {}
        for i in f:
            linha += 1
            if linha == 1:
                for j in i.strip().split(','):
                    nomes_das_variaveis.append(j)
                    dados_especificos = { j: ('')}
            else:
                for j in range(len(nomes_das_variaveis)):
                    try:
                        dados_especificos[nomes_das_variaveis[j]] = float(i.strip().split(',')[j])
                    except (ValueError, TypeError):
                        dados_especificos[nomes_das_variaveis[j]] = i.strip().split(',')[j]
                dados_gerais.append(dados_especificos.copy())


# ---------- 2. BUSCA ----------
#pesquisar por nome ou id

def pesquisar_nome_id(dados_gerais, nome_id=None):
    resultados = []
    if nome_id:
        for i in dados_gerais:
            try:
                nome_id = float(nome_id)
                if nome_id == i.get('CustomerId'):
                    resultados.append(i)
            except (ValueError, TypeError):
                if nome_id.lower() == i.get('Surname').lower():
                    resultados.append(i)
    return resultados


# ---------- 3. FILTROS ----------
#pesquisa por idade, genero ou atividade
def pesquisar_idade_genero_atividade(dados_gerais, idade=None, genero=None, membro_ativo=None):
    resultados = []
    for i in dados_gerais:
        if genero and (i.get('Gender').lower() != genero.lower()):
            continue
        if membro_ativo:
            try:
                if i.get('IsActiveMember') != float(membro_ativo):
                    continue
            except (ValueError, TypeError):
                continue
        if idade:
            try:
                if i.get('Age') != float(idade):
                    continue
            except (ValueError, TypeError):
                continue
        resultados.append(i)
    return resultados


# ---------- 4. OUTROS FILTROS ----------
#pesquisa por pais, faixa de idade, faixa de score ou saldo minimo
def pesquisar_pais_idade_score_saldo(dados_gerais, pais=None, idade_minima=None, idade_maxima=None, faixa_score=None, saldo_minimo=None):
    resultados = []
    for i in dados_gerais:
        if pais and (i.get('Geography').lower() != pais.lower()):
            continue
        if idade_minima is not None:
            try:
                if i.get('Age') < float(idade_minima):
                    continue
            except (ValueError, TypeError):
                continue
        if idade_maxima is not None:
            try:
                if i.get('Age') > float(idade_maxima):
                    continue
            except (ValueError, TypeError):
                continue
        if faixa_score and (classificar_score(i.get('CreditScore')) != faixa_score):
            continue
        if saldo_minimo is not None:
            try:
                if i.get('Balance') < float(saldo_minimo):
                    continue
            except (ValueError, TypeError):
                continue
        resultados.append(i)
    return resultados
