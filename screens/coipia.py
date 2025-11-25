from PySide6.QtWidgets import (
    QWidget, QPushButton, QApplication, QVBoxLayout,
    QFileDialog, QLabel
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QEvent, QFileInfo
import sys
import os

# ===================================================================
# IMPORTA RECURSOS ESTÁTICOS (ícones, estilos, etc.) compilados do .qrc
# ===================================================================
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import core.resources  # noqa: F401


class MainWindow(QWidget):
    """Janela principal do aplicativo Ascyn – Frameless com barra personalizada"""

    def __init__(self):
        super().__init__()

        # ===============================================================
        # 1. CARREGA A INTERFACE DO ARQUIVO .UI
        # ===============================================================
        loader = QUiLoader()
        ui_file = QFile("ui/MainWindow.ui")
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)   # Carrega o conteúdo dentro da janela
        ui_file.close()

        # ===============================================================
        # 2. AJUSTA O LAYOUT PRINCIPAL (necessário para o widget carregado ocupar 100%)
        # ===============================================================
        layout = QVBoxLayout(self)
        layout.addWidget(self.ui)
        layout.setContentsMargins(0, 0, 0, 0)

        # ===============================================================
        # 3. REMOVE BORDA E FUNDO PADRÃO DO WINDOWS (Frameless + fundo transparente)
        # ===============================================================
        self.ui.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.ui.setAttribute(Qt.WA_TranslucentBackground)

        # ===============================================================
        # 4. ESTADO DA JANELA
        # ===============================================================
        self.is_maximized = False          # Controla se está maximizada
        self.drag_pos = None               # Armazena posição do mouse ao arrastar

        # ===============================================================
        # 5. CACHE DOS WIDGETS PRINCIPAIS (evita buscas repetidas)
        # ===============================================================
        self.title_bar        = self.ui.findChild(QWidget,   "wdgTitleBar")
        self.btn_close        = self.ui.findChild(QPushButton, "btnClose")
        self.btn_minimize     = self.ui.findChild(QPushButton, "btnMinimize")
        self.btn_maximize     = self.ui.findChild(QPushButton, "btnMaximize")
        self.wdg_open_file    = self.ui.findChild(QWidget,   "wdgOpenFile")
        self.lbl_file_path    = self.ui.findChild(QLabel,    "lblFilePath")
        self.lbl_file_name    = self.ui.findChild(QLabel,    "lblFileName")
        self.lbl_file_size    = self.ui.findChild(QLabel,    "lblFileSize")

        # ===============================================================
        # 6. CONEXÃO DOS BOTÕES DA BARRA DE TÍTULO
        # ===============================================================
        if self.btn_close:
            self.btn_close.clicked.connect(QApplication.quit)                 # Fecha o app

        if self.btn_minimize:
            self.btn_minimize.clicked.connect(self.ui.showMinimized)             # Minimiza a janela

        if self.btn_maximize:
            self.btn_maximize.clicked.connect(self.toggle_maximize)           # Alterna maximizar/restaurar

        # ===============================================================
        # 7. TORNA ÁREAS CLICÁVEIS/ARRASTÁVEIS
        # ===============================================================
        if self.wdg_open_file:
            self.wdg_open_file.setCursor(Qt.PointingHandCursor)                # Cursor de "clicável"
            self.wdg_open_file.installEventFilter(self)                        # Captura cliques

        if self.title_bar:
            self.title_bar.setMouseTracking(True)        # ← IMPORTANTE!
            self.title_bar.installEventFilter(self)                            # Permite arrastar a janela
            

             
    # ===================================================================
    # EVENT FILTER – Gerencia cliques e arraste em widgets personalizados
    # ===================================================================
    def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
        # ---------- CLIQUE NO WIDGET DE ABERTURA DE ARQUIVO ----------
        if obj == self.wdg_open_file:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.open_file()                     # Abre o explorador de arquivos
                return True                          # Consome o evento

        # ---------- ARRASTAR A JANELA PELA BARRA DE TÍTULO ----------
        if obj == self.title_bar:
            if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
                self.drag_pos = event.globalPosition().toPoint()
                return True

            elif event.type() == QEvent.MouseMove and event.buttons() & Qt.LeftButton:
                if self.drag_pos:
                    delta = event.globalPosition().toPoint() - self.drag_pos
                    self.ui.showNormal()
                    self.ui.move(self.ui.pos() + delta)    # Move a janela inteira
                    self.drag_pos = event.globalPosition().toPoint()
                return True

            elif event.type() == QEvent.MouseButtonRelease:
                self.drag_pos = None
                return True
            
            
        # === CLIQUE DUPLO NA BARRA (NÃO CONSUMIR O EVENTO!) ===
        if obj == self.title_bar and event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.LeftButton:
                self.toggle_maximize()
                return True  # ou False – tanto faz, o importante é tratar aqui
        

        # Evento não tratado por nós → deixa o Qt processar normalmente
        return super().eventFilter(obj, event)

    # ===================================================================
    # MAXIMIZAR / RESTAURAR JANELA (sem bordas do Windows ao restaurar)
    # ===================================================================
    def toggle_maximize(self):
        if self.is_maximized:
            # Restaura tamanho/posição anterior sem bordas
            self.ui.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
            self.ui.showNormal()
            self.is_maximized = False
        else:
            # Maximiza ocupando toda a tela
            self.ui.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
            self.ui.showMaximized()
            self.is_maximized = True
    
    # ===================================================================
    # ABRE EXPLORADOR DE ARQUIVOS E ATUALIZA INFORMAÇÕES DO ARQUIVO
    # ===================================================================
    def open_file(self) -> str | None:
        """
        Abre o diálogo nativo de seleção de arquivo.
        Atualiza labels com caminho completo, nome e tamanho do arquivo.
        Retorna o caminho completo ou None se cancelado.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Selecione uma imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg *.webp);;Todos os arquivos (*.*)"
        )
        
        if file_path:
            # --- Nome do arquivo (sem caminho) ---
            file_name = os.path.basename(file_path)
            if self.lbl_file_name:
                self.lbl_file_name.setText(file_name)

            # --- Caminho completo ---
            if self.lbl_file_path:
                self.lbl_file_path.setText(file_path)

            # --- Tamanho do arquivo em MB ---
            file_info = QFileInfo(file_path)
            size_mb = file_info.size() / (1024 * 1024)  # bytes → MB
            if self.lbl_file_size:
                self.lbl_file_size.setText(f"{size_mb:.2f} MB")

            return file_path
        else:
            return None
        
    def mouseDoubleClickEvent(self, event):
        if (event.button() == Qt.LeftButton and 
            self.title_bar and 
            self.title_bar.geometry().contains(event.position().toPoint())):
            
            self.toggle_maximize()
        
        super().mouseDoubleClickEvent(event)