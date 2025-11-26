from PySide6.QtWidgets import QApplication
from screens.main_window import MainWindow
import sys

if __name__ == "__main__":

    app = QApplication(sys.argv)
    screen = MainWindow()
    screen.ui.show()
    sys.exit(app.exec())