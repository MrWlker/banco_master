# Interface grafica (PyQt5).
# A janela so CHAMA as funcoes de src/services e mostra a resposta.
# Nenhuma busca, filtro ou conta e feita aqui.
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QButtonGroup, QComboBox, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton, QSpinBox, QStackedWidget,
    QTableView, QVBoxLayout, QWidget,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from services import estatisticas, filtros, graficos
from styles.style import ESTILO
from styles.tables import TabelaClientes, formatar_dinheiro


def com_pontos(numero):
    # 110023 -> 110.023
    return f"{numero:,}".replace(",", ".")


def com_virgula(numero):
    # 38.1234 -> 38,12
    return f"{numero:.2f}".replace(".", ",")


class Janela(QMainWindow):
    def __init__(self, dados_gerais):
        super().__init__()
        self.dados_gerais = dados_gerais
        self.clientes_atuais = dados_gerais   # resultado da consulta atual

        self.setWindowTitle("Sistema de Análise de Clientes")
        self.resize(1200, 760)
        self.setStyleSheet(ESTILO)

        # A janela e uma pilha: cabecalho em cima, paginas no meio, abas embaixo.
        fundo = QWidget()
        fundo.setObjectName("fundo")
        pilha = QVBoxLayout(fundo)
        pilha.setContentsMargins(0, 0, 0, 0)
        pilha.setSpacing(0)
        self.setCentralWidget(fundo)

        self.paginas = QStackedWidget()
        self.paginas.addWidget(self.montar_corpo())
        self.paginas.addWidget(self.montar_pagina_estatisticas())

        pilha.addWidget(self.montar_cabecalho())
        pilha.addWidget(self.paginas, 1)
        pilha.addWidget(self.montar_rodape())

        self.consultar()

    # ------------------------------------------------------------
    # MONTAGEM DA TELA
    # ------------------------------------------------------------
    def montar_cabecalho(self):
        cabecalho = QFrame()
        cabecalho.setObjectName("cabecalho")
        linha = QHBoxLayout(cabecalho)
        linha.setContentsMargins(24, 18, 24, 18)
        linha.setSpacing(12)

        titulo = QLabel("Análise de Clientes")
        titulo.setObjectName("titulo")
        subtitulo = QLabel(f"{com_pontos(len(self.dados_gerais))} clientes carregados")
        subtitulo.setObjectName("subtitulo")
        textos = QVBoxLayout()
        textos.setSpacing(2)
        textos.addWidget(titulo)
        textos.addWidget(subtitulo)

        self.campo_busca = QLineEdit()
        self.campo_busca.setObjectName("busca")
        self.campo_busca.setPlaceholderText("Buscar por sobrenome ou código do cliente")
        self.campo_busca.setClearButtonEnabled(True)
        self.campo_busca.returnPressed.connect(self.consultar)

        botao_buscar = QPushButton("Buscar")
        botao_buscar.setObjectName("botao_buscar")
        botao_buscar.clicked.connect(self.consultar)

        linha.addLayout(textos)
        linha.addSpacing(24)
        linha.addWidget(self.campo_busca, 1)
        linha.addWidget(botao_buscar)
        return cabecalho

    def montar_corpo(self):
        # Aba "Inicio": filtros, tabela e total.
        corpo = QWidget()
        coluna = QVBoxLayout(corpo)
        coluna.setContentsMargins(24, 18, 24, 18)
        coluna.setSpacing(14)

        # --- quadro grande: filtros + tabela ---
        cartao = QFrame()
        cartao.setObjectName("cartao")
        dentro = QVBoxLayout(cartao)
        dentro.setContentsMargins(16, 14, 16, 14)
        dentro.setSpacing(12)

        self.campo_idade = QSpinBox()
        self.campo_idade.setRange(0, 120)
        self.campo_idade.setSpecialValueText("Todas")   # 0 = sem filtro de idade
        self.campo_idade.editingFinished.connect(self.consultar)

        self.campo_genero = QComboBox()
        self.campo_genero.addItem("Todos", None)
        self.campo_genero.addItem("Feminino", "Female")
        self.campo_genero.addItem("Masculino", "Male")
        self.campo_genero.currentIndexChanged.connect(self.consultar)

        self.campo_ativo = QComboBox()
        self.campo_ativo.addItem("Todos", None)
        self.campo_ativo.addItem("Ativos", "1")
        self.campo_ativo.addItem("Inativos", "0")
        self.campo_ativo.currentIndexChanged.connect(self.consultar)

        botao_limpar = QPushButton("Limpar filtros")
        botao_limpar.setObjectName("botao_limpar")
        botao_limpar.clicked.connect(self.limpar)

        linha_filtros = QHBoxLayout()
        linha_filtros.setSpacing(10)
        linha_filtros.addWidget(QLabel("Idade:"))
        linha_filtros.addWidget(self.campo_idade)
        linha_filtros.addSpacing(10)
        linha_filtros.addWidget(QLabel("Gênero:"))
        linha_filtros.addWidget(self.campo_genero)
        linha_filtros.addSpacing(10)
        linha_filtros.addWidget(QLabel("Situação:"))
        linha_filtros.addWidget(self.campo_ativo)
        linha_filtros.addStretch(1)
        linha_filtros.addWidget(botao_limpar)

        self.tabela = TabelaClientes()
        visao = QTableView()
        visao.setModel(self.tabela)
        visao.setAlternatingRowColors(True)
        visao.setSelectionBehavior(QTableView.SelectRows)
        visao.setEditTriggers(QTableView.NoEditTriggers)
        visao.setShowGrid(False)
        visao.verticalHeader().setVisible(False)
        visao.verticalHeader().setDefaultSectionSize(30)
        # Cada coluna fica da largura do seu conteudo (olhando so 50 linhas,
        # para nao ficar lento) e a ultima ocupa o espaco que sobrar.
        visao.horizontalHeader().setResizeContentsPrecision(50)
        visao.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        visao.horizontalHeader().setStretchLastSection(True)

        dentro.addLayout(linha_filtros)
        dentro.addWidget(visao, 1)

        # --- caixa de baixo: total encontrado ---
        resumo = QFrame()
        resumo.setObjectName("cartao")
        linha = QHBoxLayout(resumo)
        linha.setContentsMargins(16, 12, 16, 12)
        self.texto_total = QLabel()
        self.texto_total.setObjectName("total")
        linha.addWidget(self.texto_total)

        coluna.addWidget(cartao, 1)
        coluna.addWidget(resumo)
        return corpo

    def montar_cartao_numero(self, legenda):
        # Cartao pequeno: numero grande em cima, legenda embaixo.
        cartao = QFrame()
        cartao.setObjectName("cartao")
        dentro = QVBoxLayout(cartao)
        dentro.setContentsMargins(16, 14, 16, 14)
        numero = QLabel("-")
        numero.setObjectName("numero")
        texto = QLabel(legenda)
        texto.setObjectName("legenda")
        dentro.addWidget(numero)
        dentro.addWidget(texto)
        return cartao, numero

    def montar_cartao_lista(self, titulo):
        # Cartao com titulo e uma listinha de "nome  quantidade".
        cartao = QFrame()
        cartao.setObjectName("cartao")
        dentro = QVBoxLayout(cartao)
        dentro.setContentsMargins(16, 14, 16, 14)
        dentro.setSpacing(10)
        rotulo = QLabel(titulo)
        rotulo.setObjectName("titulo_cartao")
        lista = QLabel()
        lista.setTextFormat(Qt.RichText)
        lista.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        dentro.addWidget(rotulo)
        dentro.addWidget(lista, 1)
        return cartao, lista

    def montar_pagina_estatisticas(self):
        # Aba "Estatisticas": 4 medias em cima, 2 contagens embaixo.
        pagina = QWidget()
        coluna = QVBoxLayout(pagina)
        coluna.setContentsMargins(24, 18, 24, 18)
        coluna.setSpacing(14)

        self.texto_base = QLabel()
        self.texto_base.setObjectName("legenda")
        coluna.addWidget(self.texto_base)

        numeros = QHBoxLayout()
        numeros.setSpacing(14)
        cartao, self.numero_saldo = self.montar_cartao_numero("Saldo médio")
        numeros.addWidget(cartao)
        cartao, self.numero_salario = self.montar_cartao_numero("Salário estimado médio")
        numeros.addWidget(cartao)
        cartao, self.numero_score = self.montar_cartao_numero("Score médio")
        numeros.addWidget(cartao)
        cartao, self.numero_idade = self.montar_cartao_numero("Idade média")
        numeros.addWidget(cartao)
        coluna.addLayout(numeros)

        # Embaixo: as duas listas na esquerda e os graficos na direita.
        baixo = QHBoxLayout()
        baixo.setSpacing(14)

        listas = QVBoxLayout()
        listas.setSpacing(14)
        cartao, self.lista_paises = self.montar_cartao_lista("Clientes por país")
        listas.addWidget(cartao, 1)
        cartao, self.lista_score = self.montar_cartao_lista("Classificação por score de crédito")
        listas.addWidget(cartao, 1)
        baixo.addLayout(listas)

        baixo.addWidget(self.montar_cartao_graficos(), 1)
        coluna.addLayout(baixo, 1)
        return pagina

    def montar_cartao_graficos(self):
        # Cartao com uma "folha" do matplotlib dividida em 3 graficos lado a lado.
        cartao = QFrame()
        cartao.setObjectName("cartao")
        dentro = QVBoxLayout(cartao)
        dentro.setContentsMargins(10, 10, 10, 10)

        self.figura = Figure(figsize=(9, 3.4), tight_layout=True)
        self.eixo_pais = self.figura.add_subplot(1, 3, 1)
        self.eixo_score = self.figura.add_subplot(1, 3, 2)
        self.eixo_idade = self.figura.add_subplot(1, 3, 3)
        self.quadro_graficos = FigureCanvasQTAgg(self.figura)

        dentro.addWidget(self.quadro_graficos)
        return cartao

    def atualizar_graficos(self, clientes):
        # Apaga os graficos antigos e pede para graficos.py desenhar de novo.
        for eixo in (self.eixo_pais, self.eixo_score, self.eixo_idade):
            eixo.clear()
        if clientes:
            graficos.grafico_por_pais(clientes, self.eixo_pais)
            graficos.grafico_por_faixa_score(clientes, self.eixo_score)
            graficos.grafico_idades(clientes, self.eixo_idade)
        else:
            self.eixo_pais.set_title("Nenhum cliente na consulta atual")
        self.quadro_graficos.draw()

    def montar_rodape(self):
        rodape = QFrame()
        rodape.setObjectName("rodape")
        linha = QHBoxLayout(rodape)
        linha.setContentsMargins(0, 0, 0, 0)
        linha.setSpacing(0)

        self.abas = QButtonGroup(self)
        for numero, nome in enumerate(["Início", "Estatísticas"]):
            botao = QPushButton(nome)
            botao.setCheckable(True)
            self.abas.addButton(botao, numero)
            linha.addWidget(botao)
        self.abas.button(0).setChecked(True)
        self.abas.idClicked.connect(self.trocar_pagina)
        return rodape

    # ------------------------------------------------------------
    # FUNCIONAMENTO
    # ------------------------------------------------------------
    def consultar(self, *ignorado):
        # 1. Le o que o usuario escolheu na tela.
        termo = self.campo_busca.text().strip()
        idade = self.campo_idade.value() or None      # 0 vira None (sem filtro)
        genero = self.campo_genero.currentData()
        ativo = self.campo_ativo.currentData()

        # 2. Busca por sobrenome/codigo. Sem texto, comeca com todos os clientes.
        if termo:
            clientes = filtros.pesquisar_nome_id(self.dados_gerais, termo)
        else:
            clientes = self.dados_gerais

        # 3. Aplica os filtros em cima do resultado da busca.
        if idade or genero or ativo:
            clientes = filtros.pesquisar_idade_genero_atividade(
                clientes, idade=idade, genero=genero, membro_ativo=ativo
            )

        # 4. Mostra a resposta.
        self.clientes_atuais = clientes
        self.tabela.trocar_clientes(clientes)
        self.texto_total.setText(f"Total encontrado: {com_pontos(len(clientes))} cliente(s)")

    def limpar(self):
        # Volta tudo para o inicio sem disparar uma consulta por campo.
        for campo in (self.campo_genero, self.campo_ativo):
            campo.blockSignals(True)
            campo.setCurrentIndex(0)
            campo.blockSignals(False)
        self.campo_idade.setValue(0)
        self.campo_busca.clear()
        self.consultar()

    def atualizar_estatisticas(self):
        # Chama as funcoes de estatisticas.py com a consulta atual e mostra o resultado.
        clientes = self.clientes_atuais
        self.texto_base.setText(
            "Estatísticas da consulta atual "
            f"({com_pontos(len(clientes))} de {com_pontos(len(self.dados_gerais))} clientes)"
        )

        self.numero_saldo.setText(formatar_dinheiro(estatisticas.media_saldo(clientes)))
        self.numero_salario.setText(formatar_dinheiro(estatisticas.media_salario(clientes)))
        self.numero_score.setText(com_virgula(estatisticas.media_score(clientes)))
        self.numero_idade.setText(com_virgula(estatisticas.media_idade(clientes)))

        paises = estatisticas.contar_por_pais(clientes)
        self.lista_paises.setText(self.montar_lista(paises, sorted(paises)))

        faixas = estatisticas.contar_por_faixa_score(clientes)
        regras = {"Excelente": "750 ou mais", "Bom": "650 a 749",
                  "Regular": "500 a 649", "Ruim": "abaixo de 500"}
        nomes = [f"{faixa} ({regras[faixa]})" for faixa in faixas]
        self.lista_score.setText(self.montar_lista(dict(zip(nomes, faixas.values())), nomes))

        self.atualizar_graficos(clientes)

    def montar_lista(self, contagem, ordem):
        # Transforma {nome: quantidade} em uma tabelinha para o QLabel.
        if not contagem:
            return "Nenhum cliente na consulta atual."
        texto = "<table cellspacing=0 cellpadding=6>"
        for nome in ordem:
            texto += (f"<tr><td>{nome}</td>"
                      f"<td align=right><b>&nbsp;&nbsp;{com_pontos(contagem[nome])}</b></td></tr>")
        return texto + "</table>"

    def trocar_pagina(self, numero):
        if numero == 1:
            self.atualizar_estatisticas()
        self.paginas.setCurrentIndex(numero)


def abrir_janela(dados_gerais):
    aplicativo = QApplication(sys.argv)
    janela = Janela(dados_gerais)
    janela.show()
    sys.exit(aplicativo.exec_())
