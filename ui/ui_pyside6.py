# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerzcgVrL.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Signal, QThread)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                               QPushButton, QSizePolicy, QStatusBar, QTextEdit,
                               QVBoxLayout, QWidget, QFileDialog)
from future.moves import sys
import os
from main import run_pro


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(671, 603)
        icon = QIcon(QIcon.fromTheme(u"applications-development"))
        MainWindow.setWindowIcon(icon)
        self.file_path_word = ""
        self.file_path_ppt = ""
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.textEdit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        icon1 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.pushButton_2.setIcon(icon1)

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        icon3 = QIcon(QIcon.fromTheme(u"folder-open"))
        self.pushButton_3.setIcon(icon3)

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")


        self.pushButton_4 = CustomStyledButton2(self)
        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton = CustomStyledButton(self)
        self.verticalLayout.addWidget(self.pushButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi
        self.output_handler = OutputHandler(self.statusbar)
        self.output_handler_edit = OutputHandlerEdit(self.textEdit)
        # Подключаем кнопку к методу запуска программы
        self.pushButton.clicked.connect(self.start_program)
        self.pushButton_2.clicked.connect(self.open_file_dialog)
        self.pushButton_3.clicked.connect(self.open_file_dialog2)
        self.pushButton_4.clicked.connect(self.open_folder)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"VoicedSlides", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c \u043a \u0444\u0430\u0439\u043b\u0443 Word", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0443\u0442\u044c \u043a \u0444\u0430\u0439\u043b\u0443 c \u0440\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u0435\u043c .docx", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0443\u0442\u044c \u043a \u0444\u0430\u0439\u043b\u0443 PowerPoint", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043f\u0443\u0442\u044c \u043a \u0444\u0430\u0439\u043b\u0443 c \u0440\u0430\u0441\u0448\u0438\u0440\u0435\u043d\u0438\u0435\u043c .pptx", None))
#if QT_CONFIG(tooltip)
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0441 \u0432\u0438\u0434\u0435\u043e\u0444\u0430\u0439\u043b\u043e\u043c", None))
        self.pushButton.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>\u041d\u0430\u0447\u0430\u0442\u044c \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0443 \u0444\u0430\u0439\u043b\u043e\u0432</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0430\u0440\u0442", None))

    # retranslateUi
    def start_program(self):
        self.textEdit.clear()
        self.pushButton.setEnabled(False)  # Отключаем кнопку
        self.worker = Worker(run_pro, self.file_path_word, self.file_path_ppt)
        self.worker.progress_signal.connect(self.output_handler.write)
        self.worker.progress_signal_edit.connect(self.output_handler_edit.write)
        self.worker.finished.connect(lambda: self.pushButton.setEnabled(True))  # Включаем кнопку после завершения
        self.worker.start()

    def open_file_dialog(self):
        # Открываем диалоговое окно для выбора файла с расширением .docx
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Документы Word (*.docx)")

        # Если файл был выбран, обновляем метку
        if file_path:
            self.label.setText(file_path)
            self.file_path_word = file_path
        else:
            self.label.setText("Файл не выбран")

    def open_file_dialog2(self):
        # Открываем диалоговое окно для выбора файла с расширением .docx
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Документы PowerPoint (*.pptx)")

        # Если файл был выбран, обновляем метку
        if file_path:
            self.label_2.setText(file_path)
            self.file_path_ppt = file_path
        else:
            self.label_2.setText("Файл не выбран")

    def open_folder(self):
        folder_path = os.path.dirname(os.path.abspath(__file__)) +  '\\output'  # Замените на путь к нужной папке
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            print(f"Папка {folder_path} не существует")

class OutputHandlerEdit(QObject):
    message_signal = Signal(str)

    def __init__(self, text_edit: QTextEdit):
        super().__init__()
        self.text_edit = text_edit
        self.message_signal.connect(self.update_text_edit)

    def update_text_edit(self, message: str):
        # Добавляем сообщение в QTextEdit
        self.text_edit.append(message)

    def write(self, message: str):
        # Эта функция заменяет print, передавая сообщение в сигнал
        self.message_signal.emit(message)

class OutputHandler(QObject):
    message_signal = Signal(str)

    def __init__(self, status_bar: QStatusBar):
        super().__init__()
        self.status_bar = status_bar
        self.message_signal.connect(self.update_status_bar)

    def update_status_bar(self, message: str):
        # Обновляем текст в QStatusBar
        self.status_bar.showMessage(message)

    def write(self, message: str):
        # Эта функция заменяет print, передавая сообщение в сигнал
        self.message_signal.emit(message)

class Worker(QThread):
    progress_signal = Signal(str)  # Signal for progress messages
    progress_signal_edit = Signal(str)

    def __init__(self, main_program_function, file_path_word, file_path_ppt):
        super().__init__()
        self.main_program_function = main_program_function
        self.file_path_word = file_path_word
        self.file_path_ppt = file_path_ppt

    def run(self):
        # Run the main program function with the file paths
        try:
            self.main_program_function(
                self.progress_signal.emit,
                self.progress_signal_edit.emit,
                self.file_path_word,
                self.file_path_ppt
            )
        except Exception as e:
            self.progress_signal.emit(f"Error: {str(e)}")


class CustomStyledButton(QPushButton):
    def __init__(self, parent=None, icon_theme_name="applications-multimedia"):
        super().__init__(parent)
        self.setObjectName(u"pushButton")

        # Установка иконки
        icon = QIcon()
        if QIcon.hasThemeIcon(icon_theme_name):
            icon = QIcon.fromTheme(icon_theme_name)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)

        # Установка стилей
        self.setStyleSheet("""
            QPushButton {
                background-color: green;
                color: white;
                padding: 5px;
                border: 1px solid #4CAF50;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: gray;
                color: black;
                border: 1px solid #cccccc;
            }
        """)

class CustomStyledButton2(QPushButton):
    def __init__(self, parent=None, icon_theme_name="folder-open"):
        super().__init__(parent)
        self.setObjectName(u"pushButton")

        # Установка иконки
        icon = QIcon()
        if QIcon.hasThemeIcon(icon_theme_name):
            icon = QIcon.fromTheme(icon_theme_name)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)
        self.setIcon(icon)

        # # Установка стилей
        # self.setStyleSheet("""
        #     QPushButton {
        #         background-color: green;
        #         color: white;
        #         padding: 5px;
        #         border: 1px solid #4CAF50;
        #         border-radius: 3px;
        #     }
        #     QPushButton:hover {
        #         background-color: #45a049;
        #     }
        #     QPushButton:disabled {
        #         background-color: gray;
        #         color: black;
        #         border: 1px solid #cccccc;
        #     }
        # """)


# class MainWindow(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setupUi(self)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())