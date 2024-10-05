import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog

# Импортируем сгенерированный класс (замените на правильное имя класса)
from ui import Ui_Dialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())