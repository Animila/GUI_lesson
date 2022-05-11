import sys
from PyQt5.QtWidgets import QMainWindow, QApplication

# для импортирования из другого файла с дизайном
from qt_1 import Ui_MainWindow


class Windows_layer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn.clicked.connect(self.cmd1)


    def cmd1(self):
        text = self.input_text.text()
        self.result.setText(text)


def application():
    app = QApplication(sys.argv)
    windows_list = Windows_layer()
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
