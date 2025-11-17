from PySide6.QtWidgets import QApplication
from screens.main_window_screen import MainWindow
import sys


app = QApplication(sys.argv)
screen = MainWindow()
screen.ui.show()
sys.exit(app.exec())