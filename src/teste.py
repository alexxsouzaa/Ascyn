from PySide6.QtWidgets import QApplication, QSlider, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

class ShadowSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cria sombra
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setOffset(0, 0)  # X=0, Y=0
        shadow.setBlurRadius(4) # desfoque
        shadow.setColor(QColor(0, 0, 0, 64))  # preto com 25% opacidade

        # Aplica sombra no slider inteiro (inclusive handle)
        self.setGraphicsEffect(shadow)

if __name__ == "__main__":
    app = QApplication([])
    slider = ShadowSlider(Qt.Horizontal)
    slider.setMinimum(0)
    slider.setMaximum(100)
    slider.setValue(50)
    slider.resize(300, 50)
    slider.show()
    app.exec()
