import sys

from PyQt6.QtWidgets import QApplication

from painter import PainterWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PainterWindow()
    window.show()
    sys.exit(app.exec())
