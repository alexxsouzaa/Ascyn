from typing import Self
from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QLabel, QPlainTextEdit, QSlider
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent, QFileInfo
from core.ascii_engine import AsciiEngine
from PySide6.QtGui import QFont
import sys
import os

# ===================================================================
# IMPORTA RECURSOS ESTÁTICOS (ícones, estilos, etc.) compilados do .qrc
# ===================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import core.resources  # noqa: F401


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        # ===============================================================
        # 1. CARREGA A INTERFACE DO ARQUIVO .UI
        # ===============================================================
        loader = QUiLoader()
        ui_file = QFile("ui/MainWindow3.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)

        # ===============================================================
        # 2. INSTANCIA O ENGINE
        # ===============================================================
        self.engine = AsciiEngine()
        self.file_path = None  # Guarda o caminho da imagem
        
        # ===============================================================
        # 3. CACHE DOS WIDGETS PRINCIPAIS
        # ===============================================================
        self.wdg_open_file = self.ui.findChild(QWidget,   "wdgOpenFile")
        self.lbl_file_path = self.ui.findChild(QLabel,    "lblFilePath")
        self.lbl_file_name = self.ui.findChild(QLabel,    "lblFileName")
        self.lbl_file_size = self.ui.findChild(QLabel,    "lblFileSize")
        self.btn_converter = self.ui.findChild(QPushButton, "btnConverter")
        self.pteAsciiArt = self.ui.findChild(QPlainTextEdit, "pteAsciiArt")
        self.sldBrilho = self.ui.findChild(QSlider, "sldBrilho")
        self.sldContraste = self.ui.findChild(QSlider, "sldContraste")
        self.sldSaturacao = self.ui.findChild(QSlider, "sldSaturacao")
        self.btnReset = self.findChild(QPushButton, "btnResetAjustes")
        
        # Configuração perfeita dos sliders
        sliders_config = {
            self.sldBrilho:     (0, 300, 100),
            self.sldContraste:  (0, 400, 100),
            self.sldSaturacao:  (0, 300, 100),
        }

        for slider, (min_val, max_val, default) in sliders_config.items():
            if slider:
                slider.setRange(min_val, max_val)
                slider.setValue(default)
                slider.setSingleStep(5)
                slider.setPageStep(20)
                slider.valueChanged.connect(self.atualizar_ascii)

        # ===============================================================
        # 4. CONFIGURAÇÕES INICIAIS
        # ===============================================================
        if self.wdg_open_file:
            self.wdg_open_file.setCursor(Qt.PointingHandCursor)
            self.wdg_open_file.installEventFilter(self)

        if self.btn_converter:
            self.btn_converter.clicked.connect(self.atualizar_ascii)
        
        if self.pteAsciiArt:
            font = QFont("Consolas", 10)          # Melhor fonte
            font.setStyleHint(QFont.Monospace)    # Força espaçamento fixo
            font.setFixedPitch(True)              # Garante alinhamento perfeito
            self.pteAsciiArt.setFont(font)
                
        if self.btnReset:
            self.btnReset.clicked.connect(self.resetar_ajustes)
                
    # ===================================================================
    # EVENT FILTER – Arrastar + Clique duplo + Abrir arquivo
    # ===================================================================
    def eventFilter(self, obj, event):
        # --- CLIQUE NO BOTÃO DE ABRIR ARQUIVO ---
        if obj == self.wdg_open_file:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.open_file()
                return True

        return super().eventFilter(obj, event)

    # ===================================================================
    # ABRIR ARQUIVO E ATUALIZAR INFORMAÇÕES
    # ===================================================================
    def open_file(self) -> str | None:
        self.file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecione uma imagem", "",
            "Imagens (*.png *.jpg *.jpeg *.webp);;Todos os arquivos (*.*)"
        )

        if not self.file_path:
            return None

        # Nome do arquivo
        if self.lbl_file_name:
            self.lbl_file_name.setText(os.path.basename(self.file_path))
        # Caminho completo
        if self.lbl_file_path:
            self.lbl_file_path.setText(self.file_path)
        # Tamanho em MB
        size_mb = QFileInfo(self.file_path).size() / (1024 * 1024)
        if self.lbl_file_size:
            self.lbl_file_size.setText(f"{size_mb:.2f} MB")
            
        # Carrega a imagem no engine e já gera o primeiro ASCII
        self.engine.carregar_imagem(self.file_path)
        self.atualizar_ascii()
    
    # ===================================================================
    # CONVERSÃO
    # ===================================================================
    def atualizar_ascii(self):
        """Atualiza ASCII art com ajustes atuais – CHAMADA PELOS SLIDERS!"""
        if not self.file_path or not self.engine.imagem_original:
            return

        # PEGA OS VALORES DOS SLIDERS
        self.engine.set_ajuste("brilho",     self.sldBrilho.value()     / 100.0)
        self.engine.set_ajuste("contraste",  self.sldContraste.value()  / 100.0)
        self.engine.set_ajuste("saturacao",  self.sldSaturacao.value()  / 100.0)
            
        ascii_art = self.engine.converter_imagem()
        if self.pteAsciiArt:
            self.pteAsciiArt.setPlainText(ascii_art)
            
    def resetar_ajustes(self):
        """Botão Reset"""
        for slider in [self.sldBrilho, self.sldContraste, self.sldSaturacao]:
            if slider:
                slider.setValue(100)
        self.engine.reset()
        self.atualizar_ascii()
