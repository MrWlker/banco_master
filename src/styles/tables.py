# Tabela que mostra os clientes na tela.
# Ela so desenha as linhas que estao aparecendo, por isso aguenta
# os 110 mil clientes sem travar.
from PyQt5.QtCore import QAbstractTableModel, Qt

# (nome da coluna no CSV, titulo que aparece na tela, tipo do valor)
COLUNAS = [
    ("id", "ID", "inteiro"),
    ("CustomerId", "Cód. cliente", "inteiro"),
    ("Surname", "Sobrenome", "texto"),
    ("CreditScore", "Score", "inteiro"),
    ("Geography", "País", "texto"),
    ("Gender", "Gênero", "genero"),
    ("Age", "Idade", "inteiro"),
    ("Tenure", "Anos no banco", "inteiro"),
    ("Balance", "Saldo", "dinheiro"),
    ("NumOfProducts", "Produtos", "inteiro"),
    ("HasCrCard", "Tem cartão", "sim_nao"),
    ("IsActiveMember", "Ativo", "sim_nao"),
    ("EstimatedSalary", "Salário", "dinheiro"),
]


def formatar_dinheiro(valor):
    # 1234.5 -> R$ 1.234,50
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_valor(valor, tipo):
    # Transforma o valor guardado em um texto bonito para a tela.
    try:
        if tipo == "inteiro":
            return str(int(valor))
        if tipo == "dinheiro":
            return formatar_dinheiro(valor)
        if tipo == "sim_nao":
            return "Sim" if valor == 1 else "Não"
        if tipo == "genero":
            return "Feminino" if valor == "Female" else "Masculino"
    except (ValueError, TypeError):
        pass
    return str(valor)


class TabelaClientes(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self.clientes = []

    def trocar_clientes(self, clientes):
        # Chamado toda vez que uma nova consulta e feita.
        self.beginResetModel()
        self.clientes = clientes
        self.endResetModel()

    def rowCount(self, pai=None):
        return len(self.clientes)

    def columnCount(self, pai=None):
        return len(COLUNAS)

    def data(self, posicao, papel=Qt.DisplayRole):
        chave, titulo, tipo = COLUNAS[posicao.column()]
        if papel == Qt.DisplayRole:
            cliente = self.clientes[posicao.row()]
            return formatar_valor(cliente.get(chave), tipo)
        if papel == Qt.TextAlignmentRole and tipo in ("inteiro", "dinheiro"):
            return int(Qt.AlignRight | Qt.AlignVCenter)
        return None

    def headerData(self, numero, orientacao, papel=Qt.DisplayRole):
        if papel == Qt.DisplayRole and orientacao == Qt.Horizontal:
            return COLUNAS[numero][1]
        return None
