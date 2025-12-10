import os
from PySide6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QDialog,
    QPlainTextEdit,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader


class PopupDelete(QDialog):
    confirmed = Signal()  # sinal da instância

    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.setModal(True)
        self.setWindowModality(Qt.ApplicationModal)

        # Ocupa a janela toda do pai (para escurecimento)
        self.syncSizeWithParent()

        # Carrega UI
        ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "popup_delete.ui")
        loader = QUiLoader()
        self.ui = loader.load(ui_path, self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Centraliza
        self.centerPopup(parent)

        # APLICAR SOMBRA NO POPUP
        self.applyShadow(self.ui)

        # Botões
        self.ui.btnCancel.clicked.connect(self.close)
        self.ui.btnConfirm.clicked.connect(self._confirm)

    def centerPopup(self, parent) -> None:
        if parent:
            self.adjustSize()
            popup_width = self.width()
            popup_height = self.height()

            parent_center = parent.geometry().center()

            self.move(
                parent_center.x() - popup_width // 2,
                parent_center.y() - popup_height // 2,
            )

    def _confirm(self) -> None:
        self.confirmed.emit()  # dispara o sinal para quem chamou
        self.close()

    def syncSizeWithParent(self) -> None:
        if self.parent:
            geo = self.parent.geometry()
            self.setGeometry(0, 0, geo.width(), geo.height())

    def applyShadow(self, widget) -> None:
        shadow = QGraphicsDropShadowEffect(widget)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 50))
        widget.setGraphicsEffect(shadow)
