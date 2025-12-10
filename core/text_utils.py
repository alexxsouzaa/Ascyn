from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit, QPushButton


# ===================================================================
# COPIA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
# ===================================================================
def copyToClipboard(text: str, button: QPushButton) -> bool:
    """
    Copia o texto fornecido para a área de transferência.
    Se houver um botão, altera temporariamente seu texto para indicar sucesso.

    Retorna:
        True se o texto foi copiado.
        False se o texto estiver vazio.
    """

    if not text.strip():
        # QMessageBox.information(None, "Ascyn", "Nada para copiar!")
        return False

    # Copia para o clipboard
    QApplication.clipboard().setText(text)

    """
    ASCII (American Standard Code for Information Interchange) é um padrão de codificação criado na década de 1960 para representar caracteres em computadores e dispositivos eletrônicos.
    Ele associa números inteiros a letras, números, sinais de pontuação e comandos de controle. Por exemplo:
    A = 65
    a = 97
    1 = 49
    O conjunto original do ASCII possui 128 caracteres, incluindo letras do alfabeto inglês, números de 0 a 9, símbolos básicos e caracteres de controle (como Enter e Tab). Mais tarde surgiu o Extended ASCII, com até 256 caracteres.
    O ASCII foi essencial para a comunicação entre sistemas, armazenamento de texto e programação. Embora atualmente o Unicode seja o padrão dominante por suportar milhares de caracteres de diversos idiomas, o ASCII continua sendo a base do Unicode e ainda é amplamente utilizado em sistemas simples e na programação.
    Além disso, o ASCII também inspirou a criação da ASCII Art, desenhos e textos estilizados feitos apenas com caracteres.
    """

    return True


# ===================================================================
# RECORTA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
# ===================================================================
def cutTextToClipboard(widget, button=None) -> bool:
    """Corta o texto do widget e envia para o clipboard."""

    text = widget.toPlainText()
    if not text.strip():
        # QMessageBox.information(None, "Ascyn", "Nada para recortar!")
        return False

    # Copia o texto para o clipboard.
    copyToClipboard(text, button)
    # Limpa o texto do widget.
    widget.clear()

    return True


# ===================================================================
# ATUALIZA A FONTE+TAMANHO DA ASCII ART
# ===================================================================
def updateWidgetFont(widget: QPlainTextEdit, font: QFont, size: int = 10) -> bool:
    """Aplica uma fonte monoespaçada ao widget de texto."""

    if widget is None:
        print("Widget inválido.")
        return False

    # Copia a fonte
    newFont = QFont(font)
    # Define o tamanho da fonte
    newFont.setPointSize(size)
    newFont.setFixedPitch(True)
    # Força espaçamento fixo
    newFont.setStyleHint(QFont.Monospace)
    newFont.setHintingPreference(QFont.PreferFullHinting)

    # Define a fonte
    widget.setFont(newFont)
    # Atualiza o widget
    widget.update()
    # Força a atualização do widget
    widget.viewport().update()

    return True


# ===================================================================
# ATUALIZA A COR DA FONTE DA ASCII ART
# ===================================================================
def setTextColor(text: QPlainTextEdit, hex_color: str = "#ffffff") -> None:
    """Altera a cor do texto da Ascii Art."""

    if not text:
        return

    # Muda a cor do texto
    text.setStyleSheet(f"QPlainTextEdit {{ color: {hex_color}; }}")
    # Atualiza a vizualição
    text.update()


# ===================================================================
# Muda o peso da fonte para bold ou/e italic
# ===================================================================
def applyTextStyle(
    text: QPlainTextEdit, bold: QPushButton, italic: QPushButton
) -> None:
    """Altera o peso da fonte em bold e italic."""

    # Copia a fonte
    font = text.font()
    # Aplica o bold no texto
    if bold is not None:
        font.setBold(bold.isChecked())
    # Aplica o italic no texto
    if italic is not None:
        font.setItalic(italic.isChecked())
    # Aplica as auterações na fonte
    text.setFont(font)
    # Atualiza a vizualição
    text.viewport().update()


# ===================================================================
# ALINHA O TEXTO DO QPlainTextEdit
# ===================================================================
def setAlignmentAscii(text: QPlainTextEdit, button: QPushButton) -> None:
    """Altera o alinhamento do texto no QPlainTextEdit."""

    # Mapeia o nome dos botões para o tipo de alinhamento
    alignment_map = {
        "btnAlignLeft": Qt.AlignLeft,
        "btnAlignCenter": Qt.AlignCenter,
        "btnAlignRight": Qt.AlignRight,
    }

    # Identifica qual alinhamento usar com base no botão clicado
    alignment = alignment_map.get(button.objectName(), Qt.AlignLeft)

    # Obtém as configurações atuais do documento
    opt = text.document().defaultTextOption()

    # Define o novo alinhamento
    opt.setAlignment(alignment)

    # Aplica as configurações de volta ao documento
    text.document().setDefaultTextOption(opt)

    # Redesenha o conteúdo para aplicar visualmente o novo alinhamento
    text.viewport().update()

