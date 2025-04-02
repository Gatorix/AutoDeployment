import sys

from PyQt6.QtWidgets import QApplication
from biz.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec())
