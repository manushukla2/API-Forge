import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui.theme import STYLESHEET
from ui.app import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("APIForge")
    app.setApplicationVersion("0.1.0")
    app.setStyleSheet(STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
