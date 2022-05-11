import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class Windows_layer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('window.ui', self)
        self.btn_1.clicked.connect(lambda: self.cmd("1"))
        self.btn_2.clicked.connect(lambda: self.cmd("2"))
        self.btn_3.clicked.connect(lambda: self.cmd("3"))
        self.btn_4.clicked.connect(lambda: self.cmd("+"))
        self.btn_5.clicked.connect(lambda: self.result())
        self.btn_6.clicked.connect(lambda: self.delete())

        self.errors = [
            'ERROR: VALUE',
            'ERROR: SYNTAX',
            'ERROR: NO NUMBER',
            'ERROR: ZERO'
        ]

    def cmd(self, number):
        text = self.label.text()
        if len(text) == 0 or text == '0' or (text in self.errors):
            text = number
        else:
            text += number
        self.label.setText(text)

    def result(self):
        text = self.label.text()
        try:
            text = eval(text)
            text = str(text)
            self.label.setText(text)
        except ValueError:
            self.label.setText(self.errors[0])
        except SyntaxError:
            self.label.setText(self.errors[1])
        except NameError:
            self.label.setText(self.errors[2])
        except ZeroDivisionError:
            self.label.setText(self.errors[3])

    def delete(self):
        text = self.label.text()
        text = text[:len(text)-1]
        self.label.setText(text)



def application():
    app = QApplication(sys.argv)
    windows_list = Windows_layer()
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
