from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QFontDatabase, QFont
from PySide6.QtWidgets import QFontComboBox, QPlainTextEdit

def copiar_para_clipboard(texto: str, botao=None):
    if not texto.strip():
        QMessageBox.information(None, "Ascyn", "Nada para copiar!")
        return False
    
    clipboard = QApplication.clipboard()
    clipboard.setText(texto)
    
    if botao:
        texto_original = botao.text()
        botao.setText("Copiado!")
        QTimer.singleShot(1500, lambda: botao.setText(texto_original))
        
def recortar_texto(widget, botao=None):
    texto = widget.toPlainText()
    if not texto.strip():
        QMessageBox.information(None, "Ascyn", "Nada para recortar!")
        return
    
    copiar_para_clipboard(texto, botao)
    widget.clear()
    
    
def atualiza_font(widget: QPlainTextEdit, fonte: QFont):
    if not widget:
        return print('Widget invalido')
    
    new_font = QFont(fonte)
    new_font.setFixedPitch(True)
    new_font.setStyleHint(QFont.Monospace)
    new_font.setHintingPreference(QFont.PreferFullHinting)
    
    widget.setFont(new_font)
    widget.update()
    widget.viewport().update()