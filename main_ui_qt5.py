import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont
from ui.ui_qt5 import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont()
    font.setPointSize(10)  # Установите желаемый размер шрифта
    app.setFont(font)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())