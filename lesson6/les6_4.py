import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from calc import Ui_MainWindow


class Windows_layer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_result.clicked.connect(self.cmd_result)
        self.btn_one.clicked.connect(lambda: self.cmd('1'))
        self.btn_two.clicked.connect(lambda: self.cmd('2'))
        self.btn_three.clicked.connect(lambda: self.cmd('3'))
        self.btn_four.clicked.connect(lambda: self.cmd('4'))
        self.btn_five.clicked.connect(lambda: self.cmd('5'))
        self.btn_six.clicked.connect(lambda: self.cmd('6'))
        self.btn_seven.clicked.connect(lambda: self.cmd('7'))
        self.btn_eight.clicked.connect(lambda: self.cmd('8'))
        self.btn_nine.clicked.connect(lambda: self.cmd('9'))
        self.btn_zero.clicked.connect(lambda: self.cmd('0'))
        self.btn_div.clicked.connect(lambda: self.cmd('/'))
        self.btn_plus.clicked.connect(lambda: self.cmd('+'))
        self.btn_minus.clicked.connect(lambda: self.cmd('-'))
        self.btn_sub.clicked.connect(lambda: self.cmd('*'))

        self.errors = [
            'ERROR: VALUE',
            'ERROR: SYNTAX',
            'ERROR: NO NUMBER',
            'ERROR: ZERO'
        ]

    def cmd_result(self):
        text = self.result_text.text()
        try:
            result = eval(text)
            result = str(result)
            self.result_text.setText(result)
        except ValueError:
            self.result_text.setText(self.errors[0])
        except SyntaxError:
            self.result_text.setText(self.errors[1])
        except NameError:
            self.result_text.setText(self.errors[2])
        except ZeroDivisionError:
            self.result_text.setText(self.errors[3])

    def cmd(self, number):
        text = self.result_text.text()
        if len(text) == 0 or text == '0' or (text in self.errors):
            self.result_text.setText(number)
        else:
            self.result_text.setText(text + number)

def application():
    app = QApplication(sys.argv)
    windows_list = Windows_layer()
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
