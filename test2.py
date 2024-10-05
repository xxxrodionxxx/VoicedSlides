from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import QThread, Signal
import time


class Worker(QThread):
    progress = Signal(int)

    def run(self):
        for i in range(101):
            time.sleep(0.1)  # Имитация длительной операции
            self.progress.emit(i)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QThread Example")

        layout = QVBoxLayout()

        self.button = QPushButton("Start Long Process")
        self.button.clicked.connect(self.start_long_process)
        layout.addWidget(self.button)

        self.label = QLabel("Progress: 0%")
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.thread = Worker()
        self.thread.progress.connect(self.update_progress)

    def start_long_process(self):
        self.button.setEnabled(False)
        self.thread.start()

    def update_progress(self, value):
        self.label.setText(f"Progress: {value}%")
        if value == 100:
            self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()