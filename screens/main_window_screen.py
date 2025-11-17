from PySide6.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout, QFileDialog, QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent, QFileInfo
import sys
import os

# === IMPORTA resources.py da pasta core/ ===
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # Adiciona raiz ao PATH
import core.resources  # noqa: F401

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # === CARREGA O .UI DENTRO DA JANELA ===
        loader = QUiLoader()
        ui_file = QFile("ui/MainWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        
        # === LAYOUT: coloca o .ui dentro da janela ===
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)

        # === JANELA SEM BORDA (NO `self`) ===
        self.ui.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.ui.setAttribute(Qt.WA_TranslucentBackground)
        
        # === ESTADO ===
        self.is_maximized = False  # ← Estado inicial: não maximizado
        
        # === CACHE DOS WIDGETS ===
        self.title_bar = self.ui.findChild(QWidget, "wdgTitleBar")
        self.btn_close = self.ui.findChild(QPushButton, "btnClose")
        self.btn_minimize = self.ui.findChild(QPushButton, "btnMinimize")
        self.btn_maximize = self.ui.findChild(QPushButton, "btnMaximize")
        self.widget_open_file = self.ui.findChild(QWidget, "wdgOpenFile")
        self.lbl_file_path = self.ui.findChild(QLabel, "lblFilePath")
        self.lbl_file_name = self.ui.findChild(QLabel, "lblFileName")
        self.lbl_file_size = self.ui.findChild(QLabel, "lblFileSize")
        
        # === CONECTA O BOTÃÕES DE FECHAR, MINIMIZAR ===
        if self.btn_close:
            self.btn_close.clicked.connect(QApplication.quit)  # ← FECHA A JANELA
        if self.btn_minimize:
            self.btn_minimize.clicked.connect(self.ui.showMinimized)
        if self.btn_maximize:
            self.btn_maximize.clicked.connect(self.toggle_maximize)
        if self.widget_open_file:
            self.widget_open_file.installEventFilter(self)

       # === ARRASTAR NA BARRA  ===
        self.dragPos = None
        if self.title_bar:
            self.title_bar.installEventFilter(self)
            
             
    # EVENT FILTER
    def eventFilter(self, obj, event):
        if obj == self.widget_open_file:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.open_file()
                return True
        
        if obj == self.title_bar:

            # Pressionar botão esquerdo
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.dragPos = event.globalPosition().toPoint()
                return True

            # Mover
            if event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                if self.dragPos:
                    newPos = event.globalPosition().toPoint()
                    diff = newPos - self.dragPos
                    self.ui.move(self.ui.pos() + diff)
                    self.dragPos = newPos
                return True

            # Soltar
            if event.type() == QEvent.MouseButtonRelease:
                self.dragPos = None
                return True

        return super().eventFilter(obj, event)

    # === MAXIMIZAR / RESTAURAR ===
    def toggle_maximize(self):
        if self.is_maximized:
            self.ui.showNormal()
            self.is_maximized = False
        else:
            self.ui.showMaximized()
            self.is_maximized = True
            
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione uma imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            file_name = os.path.basename(file_path)
            if self.lbl_file_name:
                self.lbl_file_name.setText(file_name)
                
            # === MUDA O TEXTO DA LABEL ===
            if self.lbl_file_path:
                self.lbl_file_path.setText(file_path)
                
            info_file = QFileInfo(file_path)
            file_size = info_file.size()
            file_size = file_size / 1024
            if self.lbl_file_size:
                self.lbl_file_size.setText(f"{file_size:.2f} MB")
            
            return file_path