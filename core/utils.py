from PySide6.QtWidgets import QMessageBox, QApplication
from PySide6.QtCore import QTimer

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