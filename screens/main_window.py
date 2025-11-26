from PySide6.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout,
    QFileDialog, QLabel, QPlainTextEdit,
    QSlider, QFontComboBox, QSpinBox, QComboBox, QRadioButton
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent, QFileInfo
from core.ascii_engine import AsciiEngine
from core.text_utils import copyToClipboard, cutTextToClipboard, updateWidgetFont
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
        # 2. ENGINE ASCII
        # ===============================================================
        self.engine = AsciiEngine()
        self.file_path = None  # Guarda o caminho da imagem
        
        # ===============================================================
        # 3. CACHE DOS WIDGETS CARREGADOS DO ARQUIVO UI
        # ===============================================================
        self.wdgFileSelector = self.ui.findChild(QWidget,        "wdgFileSelector")
        self.lbl_file_path = self.ui.findChild(QLabel,         "lblFilePath")
        self.lbl_file_name = self.ui.findChild(QLabel,         "lblFileName")
        self.lbl_file_size = self.ui.findChild(QLabel,         "lblFileSize")
        self.btn_converter = self.ui.findChild(QPushButton,    "btnConverter")
        self.pteAsciiArt   = self.ui.findChild(QPlainTextEdit, "pteAsciiArt")
        self.sldBrilho     = self.ui.findChild(QSlider,        "sldBrilho")
        self.sldContraste  = self.ui.findChild(QSlider,        "sldContraste")
        self.sldSaturacao  = self.ui.findChild(QSlider,        "sldSaturacao")
        self.btnReset      = self.ui.findChild(QPushButton,       "btnResetAjustes")
        self.btnCopiar     = self.ui.findChild(QPushButton,    "btnCopiar")
        self.btnRecortar   = self.ui.findChild(QPushButton,    "btnRecortar")
        self.cmbFonte      = self.ui.findChild(QFontComboBox,  "cmbFonte")
        self.cmbChars      = self.ui.findChild(QComboBox,      "cmbChars")
        self.spnFontSize    = self.ui.findChild(QSpinBox,       "spnFontSize")
        self.radioInverteCores = self.ui.findChild(QRadioButton, "radioInverteCores")
        
        # ===============================================================
        # 4. Configuração os valores padrões é range dos sliders
        # ===============================================================
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
                slider.valueChanged.connect(self.updateAsciiArt)

        # ===============================================================
        # 5. CONFIGURAÇÕES DOS WIDGETS
        # ===============================================================
        if self.wdgFileSelector:
            self.wdgFileSelector.setCursor(Qt.PointingHandCursor)
            self.wdgFileSelector.installEventFilter(self)

        # Botões
        if self.btn_converter:
            self.btn_converter.clicked.connect(self.updateAsciiArt)
        if self.btnReset:
            self.btnReset.clicked.connect(self.resetAdjustments)
        if self.btnCopiar:
            self.btnCopiar.clicked.connect(self.copyAsciiToClipboard)
        if self.btnRecortar:
            self.btnRecortar.clicked.connect(self.cutAsciiToClipboard)
        
        # Plain Text
        if self.pteAsciiArt:
            font = QFont("Courier", 10)          # Melhor fonte
            font.setStyleHint(QFont.Monospace)    # Força espaçamento fixo
            font.setFixedPitch(True)              # Garante alinhamento perfeito
            self.pteAsciiArt.setFont(font)
        
        # Combox
        self.cmbFonte.currentFontChanged.connect(lambda font: updateWidgetFont(self.pteAsciiArt, font))
        self.cmbChars.currentTextChanged.connect(self.updateAsciiArt)
        
        # Radio Buttum
        self.radioInverteCores.clicked.connect(self.updateAsciiArt)

        # ComboBox → muda a família da fonte
        self.cmbFonte.currentFontChanged.connect(
            lambda font: font and updateWidgetFont(
                widget=self.pteAsciiArt,
                font=font,
                size=self.spnFontSize.value() if self.spnFontSize else 10
            )
        )
        
        # SpinBox → muda só o tamanho
        self.spnFontSize.valueChanged.connect(
            lambda size: updateWidgetFont(
                widget=self.pteAsciiArt,
                font=self.pteAsciiArt.font(),
                size=size
            )
        )
                    
    # ===================================================================
    # EVENT FILTER – Abrir arquivo
    # ===================================================================
    def eventFilter(self, obj, event):
        # --- CLIQUE NO BOTÃO DE ABRIR ARQUIVO ---
        if obj == self.wdgFileSelector:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.selectImageFile()
                return True

        return super().eventFilter(obj, event)

    # ===================================================================
    # ABRIR ARQUIVO E ATUALIZAR INFORMAÇÕES
    # ===================================================================
    def selectImageFile(self) -> str | None:
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
            
        # Carrega a imagem no engine
        self.engine.load_image(self.file_path)
        # Gera o primeiro ASCII
        self.updateAsciiArt()
        # Reseta as ajuste da imagem
        self.resetAdjustments()
    
    # ===================================================================
    # CONVERTE A IMAGEM E ATUALIZA A PRÉVIA DA ASCII ART
    # ===================================================================
    def updateAsciiArt(self):
        """Atualiza ASCII art com ajustes atuais – CHAMADA PELOS SLIDERS!"""
        
        if not self.file_path or not self.engine.original_image:
            return

        # Pega os valores dos sliders
        self.engine.set_adjustment("brightness",     self.sldBrilho.value()     / 100.0)
        self.engine.set_adjustment("contrast",       self.sldContraste.value()  / 100.0)
        self.engine.set_adjustment("saturation",     self.sldSaturacao.value()  / 100.0)
        self.engine.set_adjustment("invert",         self.radioInverteCores.isChecked())
        
        # Converte imagem em ASCII    
        asciiText  = self.engine.to_ascii(self.cmbChars.currentText())
        
        # Atualiza exibição
        self.pteAsciiArt.setPlainText(asciiText)
            
    # ===================================================================
    # REVERTE OS AJUSTES FEITOS NA IMAGEM
    # ===================================================================
    def resetAdjustments(self):
        # Define o valor inicial dos sliders para o padrão que é 100
        for slider in [self.sldBrilho, self.sldContraste, self.sldSaturacao]:
            if slider:
                slider.setValue(100)
        # Restaura os ajustes feitos na imagem
        self.engine.reset()
        # Atualiza exibição
        self.updateAsciiArt()
        
    # ===================================================================
    # COPIA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
    # ===================================================================
    def copyAsciiToClipboard(self):
        asciiText = self.pteAsciiArt.toPlainText()
        # Nada para copiar
        if not asciiText.strip():
            return
        
        copyToClipboard(asciiText, self.btnCopiar)
        
    # ===================================================================
    # RECORTA O CONTEÚDO ASCII PARA A ÁREA DE TRANSFERÊNCIA
    # ===================================================================
    def cutAsciiToClipboard(self):
        cutTextToClipboard(self.pteAsciiArt, self.btnRecortar)