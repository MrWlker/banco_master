# Aparencia da interface (cores, bordas, fontes).
# Fica separado para a janela.py cuidar so do funcionamento.

ESTILO = """
QMainWindow, #fundo { background: #F4F6FB; }
QLabel { color: #1B2440; font-size: 13px; }

#cabecalho { background: #0B2F8A; }
#titulo { color: white; font-size: 20px; font-weight: bold; }
#subtitulo { color: #C9D4F5; font-size: 12px; }

#busca {
    background: white; color: #1B2440; border: none; border-radius: 18px;
    padding: 9px 16px; font-size: 14px;
}

QPushButton {
    background: #0B2F8A; color: white; border: none; border-radius: 8px;
    padding: 8px 18px; font-size: 13px; font-weight: bold;
}
QPushButton:hover { background: #1541B5; }
#botao_buscar { background: white; color: #0B2F8A; border-radius: 18px; }
#botao_buscar:hover { background: #E3E9FB; }
#botao_limpar { background: #E3E9FB; color: #0B2F8A; }
#botao_limpar:hover { background: #D2DCF8; }

#cartao { background: white; border: 1px solid #E1E6F2; border-radius: 14px; }
#cartao QLabel { border: none; }
#total { font-size: 14px; font-weight: bold; color: #0B2F8A; }

QComboBox, QSpinBox, QDoubleSpinBox {
    background: white; color: #1B2440; border: 1px solid #C9D1E6;
    border-radius: 6px; padding: 5px 8px; font-size: 13px; min-width: 90px;
}
QComboBox QAbstractItemView {
    background: white; color: #1B2440;
    selection-background-color: #E3E9FB; selection-color: #0B2F8A;
}

QTableView {
    background: white; alternate-background-color: #F6F8FD; color: #1B2440;
    border: none; gridline-color: #E9EDF6; font-size: 13px;
    selection-background-color: #DCE5FC; selection-color: #0B2F8A;
}
QTableView::item { padding: 0 10px; }
QHeaderView::section {
    background: #EEF2FB; color: #0B2F8A; font-weight: bold; font-size: 12px;
    border: none; border-bottom: 2px solid #0B2F8A; padding: 7px 14px;
}
QTableCornerButton::section { background: #EEF2FB; border: none; }

#numero { font-size: 19px; font-weight: bold; color: #0B2F8A; }
#legenda { font-size: 12px; color: #6B7590; }
#titulo_cartao { font-size: 14px; font-weight: bold; color: #0B2F8A; }
#pendente { font-size: 12px; color: #B26A00; }

#rodape { background: white; border-top: 1px solid #E1E6F2; }
#rodape QPushButton {
    background: transparent; color: #8A93AD; border-radius: 0;
    padding: 12px; font-size: 13px;
}
#rodape QPushButton:hover { color: #0B2F8A; }
#rodape QPushButton:checked { color: #0B2F8A; border-top: 3px solid #0B2F8A; }
"""
