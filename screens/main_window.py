from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QLabel,
    QPlainTextEdit,
    QSlider,
    QFontComboBox,
    QSpinBox,
    QComboBox,
    QCheckBox,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent, QFileInfo
from core.ascii_engine import AsciiEngine
from core.text_utils import (
    copyToClipboard,
    cutTextToClipboard,
    updateWidgetFont,
    setTextColor,
    applyTextStyle,
)
from PySide6.QtGui import QFont, QShortcut, QKeySequence
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
        ui_file = QFile("ui/MainWindow.ui")
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
        self.wdgFileSelector = self.ui.findChild(QWidget, "wdgFileSelector")
        self.lbl_file_path = self.ui.findChild(QLabel, "lblFilePath")
        self.lbl_file_name = self.ui.findChild(QLabel, "lblFileName")
        self.lbl_file_size = self.ui.findChild(QLabel, "lblFileSize")
        self.btn_converter = self.ui.findChild(QPushButton, "btnConverter")
        self.pteAsciiArt = self.ui.findChild(QPlainTextEdit, "pteAsciiArt")
        self.sldBrightness = self.ui.findChild(QSlider, "sldBrightness")
        self.sldContrast = self.ui.findChild(QSlider, "sldContrast")
        self.sldSaturation = self.ui.findChild(QSlider, "sldSaturation")
        self.btnResetAdjustments = self.ui.findChild(QPushButton, "btnResetAdjustments")
        self.btnCopy = self.ui.findChild(QPushButton, "btnCopy")
        self.btnCut = self.ui.findChild(QPushButton, "btnCut")
        self.cmbFonte = self.ui.findChild(QFontComboBox, "cmbFonte")
        self.cmbChars = self.ui.findChild(QComboBox, "cmbChars")
        self.spnFontSize = self.ui.findChild(QSpinBox, "spnFontSize")
        self.chkInverteCores = self.ui.findChild(QCheckBox, "chkInverteCores")
        self.cmbTextColor = self.ui.findChild(QComboBox, "cmbTextColor")
        self.sldWidth = self.ui.findChild(QSlider, "sldWidth")
        self.lblWidthValue = self.ui.findChild(QLabel, "lblWidthValue")
        self.lblSaturation = self.ui.findChild(QLabel, "lblSaturation")
        self.lblContrast = self.ui.findChild(QLabel, "lblContrast")
        self.lblBrightness = self.ui.findChild(QLabel, "lblBrightness")
        self.btnBoldText = self.ui.findChild(QPushButton, "btnBoldText")
        self.btnItalicText = self.ui.findChild(QPushButton, "btnItalicText")

        # ===============================================================
        # 4. Configuração dos valores padrões dos widgts
        # ===============================================================
        # Define os valores iniciais do sliders
        sliders_config = {
            self.sldBrightness: (0, 300, 120),
            self.sldContrast: (0, 400, 120),
            self.sldSaturation: (0, 300, 120),
            self.sldWidth: (40, 300, 120),
        }
        # Define os valores do range minimo, maximo e padrão dos sliders
        for slider, (min_val, max_val, default) in sliders_config.items():
            if slider:
                slider.setRange(min_val, max_val)
                slider.setValue(default)
                slider.setSingleStep(5)
                slider.setPageStep(20)
                slider.valueChanged.connect(self.updateAsciiArt)

        # ===============================================================
        # 5. Atualiza os valores das labels dos sliders
        # ===============================================================
        self.lblBrightness.setText(f"{str(self.sldBrightness.value())}%")
        self.lblContrast.setText(f"{str(self.sldContrast.value())}%")
        self.lblSaturation.setText(f"{str(self.sldSaturation.value())}%")
        self.lblWidthValue.setText(f"{str(self.sldWidth.value())} cols")

        # Dicionario de cores do texto da Ascii Art
        self.text_colors = {
            "White Classic": "#ffffff",
            "Matrix Green": "#00ff41",
            "Cyberpunk Pink": "#ff00ff",
            "Blood Red": "#ff0033",
            "Electric Blue": "#00ffff",
            "Neon Yellow": "#ffff00",
            "Toxic Purple": "#cc00ff",
            "Orange Fire": "#ff6600",
            "Acid Lime": "#aaff00",
            "Ice Blue": "#00aaff",
        }

        # ===============================================================
        # 6. CONFIGURAÇÕES DOS WIDGETS
        # ===============================================================
        if self.wdgFileSelector:
            self.wdgFileSelector.setCursor(Qt.PointingHandCursor)
            self.wdgFileSelector.installEventFilter(self)

        # ===============================================================
        # 7. CONFIGURAÇÕES DOS BOTÕES
        # ===============================================================
        # Botão de resetar os ajustes de imagem
        if self.btnResetAdjustments:
            self.btnResetAdjustments.clicked.connect(self.resetAdjustments)
        # Botão de copiar a Ascii Art
        if self.btnCopy:
            self.btnCopy.clicked.connect(
                lambda: copyToClipboard(self.pteAsciiArt.toPlainText(), self.btnCopy)
            )
        # Botão de cortar a Ascii Art
        if self.btnCut:
            self.btnCut.clicked.connect(
                lambda: cutTextToClipboard(self.pteAsciiArt, self.btnCut)
            )
        # Botão de peso Bold da fonte
        if self.btnBoldText:
            self.btnBoldText.toggled.connect(
                lambda: applyTextStyle(
                    self.pteAsciiArt, self.btnBoldText, self.btnItalicText
                )
            )
        # Botão de peso Italic da fonte
        if self.btnItalicText:
            self.btnItalicText.toggled.connect(
                lambda: applyTextStyle(
                    self.pteAsciiArt, self.btnBoldText, self.btnItalicText
                )
            )

        # Radio Buttum → inverter as cores
        self.chkInverteCores.clicked.connect(self.updateAsciiArt)

        # ===============================================================
        # 8. CONFIGURAÇÕES DO PLAIN TEXT
        # ===============================================================
        font = QFont("Courier", 10)  # Melhor fonte
        font.setStyleHint(QFont.Monospace)  # Força espaçamento fixo
        font.setFixedPitch(True)  # Garante alinhamento perfeito
        self.pteAsciiArt.setFont(font)

        # ===============================================================
        # 9. CONFIGURAÇÕES DOS COMBOXS E SPINBOXS
        # ===============================================================
        # Combox → muda os caracteres da Ascii Art
        self.cmbChars.currentTextChanged.connect(self.updateAsciiArt)
        # ComboBox → muda a família da fonte
        self.cmbFonte.currentFontChanged.connect(
            lambda font: font
            and updateWidgetFont(
                widget=self.pteAsciiArt,
                font=font,
                size=self.spnFontSize.value() if self.spnFontSize else 10,
            )
        )
        # Combox → Adiciona as cores do dicionario de cores no combox de cores
        self.cmbTextColor.clear()
        for name in self.text_colors:
            self.cmbTextColor.addItem(name)
        # Define cor padrão
        self.cmbTextColor.setCurrentText("White Classic")

        # ComboBox → muda a cor da fonte
        self.cmbTextColor.currentTextChanged.connect(
            lambda name: name
            and setTextColor(self.pteAsciiArt, self.text_colors.get(name, "#ffffff"))
        )
        # SpinBox → muda o tamanho da fonte
        self.spnFontSize.valueChanged.connect(
            lambda size: updateWidgetFont(
                widget=self.pteAsciiArt, font=self.pteAsciiArt.font(), size=size
            )
        )

        # ===============================================================
        # 10. CONFIGURAÇÕES DOS SLIDERS
        # ===============================================================
        # Slider → Atualiza o texto do label do slider de escala
        self.sldWidth.valueChanged.connect(
            lambda value: (
                self.updateAsciiArt,
                self.updateLabelFromSlider(self.sldWidth, self.lblWidthValue, " cols"),
            )
        )
        # Slider → Atualiza o texto do label do slider de Brilho
        self.sldBrightness.valueChanged.connect(
            lambda value: (
                self.updateLabelFromSlider(self.sldBrightness, self.lblBrightness, "%")
            )
        )
        # Slider → Atualiza o texto do label do slider de Contraste
        self.sldContrast.valueChanged.connect(
            lambda value: (
                self.updateLabelFromSlider(self.sldContrast, self.lblContrast, "%")
            )
        )
        # Slider → Atualiza o texto do label do slider de Saturação
        self.sldSaturation.valueChanged.connect(
            lambda value: {
                self.updateLabelFromSlider(self.sldSaturation, self.lblSaturation, "%")
            }
        )
        
        # ===============================================================
        # 11. ATALHOS GLOBAL
        # ===============================================================
        # Atalho para abrir a seleção de imagem
        QShortcut(QKeySequence("Ctrl+O"), self.wdgFileSelector).activated.connect(self.selectImageFile)

    # ===================================================================
    # EVENT FILTER – Abrir arquivo
    # ===================================================================
    def eventFilter(self, obj, event):
        # --- CLIQUE NO BOTÃO DE ABRIR ARQUIVO ---
        if obj == self.wdgFileSelector:
            if (
                event.type() == QEvent.MouseButtonPress
                and event.button() == Qt.LeftButton
            ):
                self.selectImageFile()
                return True

        return super().eventFilter(obj, event)

    # ===================================================================
    # ABRIR ARQUIVO E ATUALIZAR INFORMAÇÕES
    # ===================================================================
    def selectImageFile(self) -> str | None:
        self.file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione uma imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.webp);;Todos os arquivos (*.*)",
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
        self.engine.set_adjustment("brightness", self.sldBrightness.value() / 100.0)
        self.engine.set_adjustment("contrast", self.sldContrast.value() / 100.0)
        self.engine.set_adjustment("saturation", self.sldSaturation.value() / 100.0)
        self.engine.set_adjustment("invert", self.chkInverteCores.isChecked())

        # Converte imagem em ASCII
        asciiText = self.engine.to_ascii(
            self.cmbChars.currentText(), width=self.sldWidth.value()
        )

        # Atualiza exibição
        self.pteAsciiArt.setPlainText(asciiText)

    # ===================================================================
    # REVERTE OS AJUSTES FEITOS NA IMAGEM
    # ===================================================================
    def resetAdjustments(self):
        # Define o valor inicial dos sliders para o padrão que é 100
        for slider in [self.sldBrightness, self.sldContrast, self.sldSaturation]:
            if slider:
                slider.setValue(120)
        # Restaura os ajustes feitos na imagem
        self.engine.reset()
        # Atualiza exibição
        self.updateAsciiArt()

    # ===================================================================
    # ATUALIZA O TEXTO DOS QLABELS
    # ===================================================================
    def updateLabelFromSlider(
        self, slider: QSlider, label: QLabel, suffix: str = ""
    ) -> None:
        """Atualiza o texto de uma QLabel com o valor atual de um QSlider."""

        if not slider or not label:
            return

        # Pega o valor do slider
        value = slider.value()
        # Adiciona o novo texto na label
        label.setText(f"{value}{suffix}")
