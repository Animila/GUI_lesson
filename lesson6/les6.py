import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Windows_layer(QMainWindow):
    def __init__(self):
        super().__init__()
        # заголовок
        self.setWindowTitle('Мое окно')
        # X, Y с левого верхнего окна, ширина и высота
        self.setGeometry(700, 300, 500, 600)

        # создание объектов

        # поле для ввода
        # настройка расположения
        # размер (ширина и высота)
        self.input_text = QtWidgets.QLineEdit(self)
        self.input_text.move(200, 250)
        self.input_text.resize(150, 50)

        # кнопка
        self.button = QtWidgets.QPushButton('пуск', self)
        self.button.move(200, 300)
        self.button.resize(150, 40)
        # подключение
        self.button.clicked.connect(self.cmd1)

        # заголовок
        self.label = QtWidgets.QLabel(self)
        self.label.move(200, 340)
        self.label.resize(150, 50)

    def cmd1(self):
        text = self.input_text.text()
        self.label.setText(text)


def application():
    app = QApplication(sys.argv)
    windows_list = Windows_layer()
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
