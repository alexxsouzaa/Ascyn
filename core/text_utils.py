from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QPlainTextEdit

# ===================================================================
# COPIA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
# ===================================================================
def copyToClipboard(texto: str, button=None) -> bool:
    """
    Copia o texto fornecido para a área de transferência.
    Se houver um botão, altera temporariamente seu texto para indicar sucesso.

    Retorna:
        True se o texto foi copiado.
        False se o texto estiver vazio.
    """
    
    if not texto.strip():
        QMessageBox.information(None, "Ascyn", "Nada para copiar!")
        return False
    
    # Copia para o clipboard
    QApplication.clipboard().setText(texto)
    
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
def updateWidgetFont(widget: QPlainTextEdit, font: QFont, size: int=10) -> bool:
    """Aplica uma fonte monoespaçada ao widget de texto."""
    
    if widget is None:
        print("Widget inválido.")
        return False
    
    newFont = QFont(font)
    newFont.setPointSize(size)      # Define o tamanho da fonte
    newFont.setFixedPitch(True)
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
def setTextColor(widget: QPlainTextEdit, hex_color: str = "#ffffff") -> None:
    """Altera a cor do texto da Ascii Art."""
    
    if not widget:
        return
    
    # Muda a cor do texto
    widget.setStyleSheet(
        f"QPlainTextEdit {{ color: {hex_color}; }}"
    ) 
    # Atualiza a vizualição
    widget.update()