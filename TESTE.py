# ASCYN - SPLASH SCREEN PROFISSIONAL (UM ARQUIVO SÓ)
# PySide6 + Barra de progresso + Efeito Photoshop/Blender
# Bruno, o rei do ASCII – 2025

import sys
import time
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QPushButton, QSplashScreen, QProgressBar
)
from PySide6.QtGui import QPixmap, QFont, QIcon
from PySide6.QtCore import Qt, QTimer, QThread, Signal

# =============================================
# 1. THREAD DE CARREGAMENTO (pra não travar)
# =============================================
class LoadingThread(QThread):
    progress = Signal(int, str)   # valor, mensagem
    finished_loading = Signal()

    def run(self):
        steps = [
            (10,  "Inicializando núcleo..."),
            (25,  "Carregando engine ASCII..."),
            (40,  "Preparando temas cyberpunk..."),
            (55,  "Construindo interface..."),
            (75,  "Aplicando estilo neon..."),
            (90,  "Sincronizando com a Matrix..."),
            (100, "ASCYN PRONTO. BEM-VINDO, HACKER.")
        ]

        for value, msg in steps:
            time.sleep(0.6)  # simula trabalho pesado
            self.progress.emit(value, msg)

        time.sleep(0.5)
        self.finished_loading.emit()

# =============================================
# 2. TELA DE SPLASH FODA (igual Photoshop)
# =============================================
class SplashScreen(QSplashScreen):
    def __init__(self):
        # Cria um pixmap preto com texto neon (sem imagem externa!)
        pixmap = QPixmap(800, 500)
        pixmap.fill(Qt.black)

        from PySide6.QtGui import QPainter, QColor
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Logo ASCYN gigante
        font = QFont("Consolas", 80, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#00ff41"))
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "ASCYN")

        # Slogan
        font.setPointSize(20)
        painter.setFont(font)
        painter.setPen(QColor("#00ffff"))
        painter.drawText(0, 360, 800, 100, Qt.AlignCenter, "ASCII Art Never Dies")

        painter.end()
        super().__init__(pixmap, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # Estilo cyberpunk
        self.setStyleSheet("""
            QSplashScreen {
                color: #00ff41;
                font-family: "Consolas", monospace;
                font-weight: bold;
            }
        """)

        # Barra de progresso neon
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(100, 430, 600, 12)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: #111;
                border: 2px solid #00ff41;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00ff41, stop:1 #00ffff);
                border-radius: 4px;
            }
        """)

        # Mensagem
        self.label = QLabel(self)
        self.label.setGeometry(0, 380, 800, 50)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #00ff41; font-size: 14px;")
        self.label.setText("Iniciando sistema...")

    def update_progress(self, value: int, message: str):
        self.progress_bar.setValue(value)
        self.label.setText(message)
        QApplication.processEvents()

# =============================================
# 3. Janela principal (só pra mostrar que carregou)
# =============================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ASCYN - ASCII Art Never Dies")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background: black; color: #00ff41; font-family: Consolas;")

        central = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("ASCYN CARREGADO COM SUCESSO!")
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #00ff41;")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("O melhor editor de ASCII Art do universo.")
        subtitle.setStyleSheet("font-size: 20px; color: #00ffff;")
        subtitle.setAlignment(Qt.AlignCenter)

        btn = QPushButton("FECHAR E SER LENDÁRIO")
        btn.setStyleSheet("""
            QPushButton {
                background: #00ff41; color: black; font-weight: bold;
                padding: 15px; border-radius: 10px; font-size: 18px;
            }
            QPushButton:hover { background: #00ffff; }
        """)
        btn.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(btn)
        central.setLayout(layout)
        self.setCentralWidget(central)

# =============================================
# 4. MAIN – TUDO ACONTECE AQUI
# =============================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Splash screen
    splash = SplashScreen()
    splash.show()
    app.processEvents()

    # Thread de carregamento
    thread = LoadingThread()
    
    def update_splash(value, msg):
        splash.update_progress(value, msg)
    
    def show_main_window():
        global window
        window = MainWindow()
        window.show()
        splash.finish(window)

    thread.progress.connect(update_splash)
    thread.finished_loading.connect(show_main_window)
    thread.start()

    sys.exit(app.exec())