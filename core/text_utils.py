from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit, QPushButton


# ===================================================================
# COPIA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
# ===================================================================
def copyToClipboard(text: str, button=None) -> bool:
    """
    Copia o texto fornecido para a área de transferência.
    Se houver um botão, altera temporariamente seu texto para indicar sucesso.

    Retorna:
        True se o texto foi copiado.
        False se o texto estiver vazio.
    """

    if not text.strip():
        QMessageBox.information(None, "Ascyn", "Nada para copiar!")
        return False

    # Copia para o clipboard
    QApplication.clipboard().setText(text)

    # Feedback visual no botão
    if button:
        texto_original = button.text()
        button.setText("Copiado!")
        QTimer.singleShot(1500, lambda: button.setText(texto_original))

    return True


# ===================================================================
# RECORTA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
# ===================================================================
def cutTextToClipboard(widget, button=None) -> bool:
    """Corta o texto do widget e envia para o clipboard."""

    text = widget.toPlainText()
    if not text.strip():
        QMessageBox.information(None, "Ascyn", "Nada para recortar!")
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
