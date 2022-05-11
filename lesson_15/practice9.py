from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import uic
import sys

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap
import sqlite3


class LoginWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.connect = sqlite3.connect('db.db')

        self.auth.clicked.connect(self.nextWindows)

    def checkPassword(self):
        password = self.password_input.toPlainText()
        login = self.login_input.toPlainText()

        request = self.connect.cursor()
        cmd = f"SELECT login, password FROM users WHERE login='{login}' AND password='{password}';"
        request.execute(cmd)
        checkCurrent = request.fetchall()

        checkEmpty = not login == "" and not password == ''
        return checkEmpty and checkCurrent

    def nextWindows(self):
        if self.checkPassword():
            self.next = ImageWindows()
            self.next.show()
            self.close()
        else:
            message('Ошибка', 'Проверьте правильность введенных данных')


class ImageWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('image.ui', self)

        self.btn_save.clicked.connect(self.imageFile)
        self.btn_r.clicked.connect(lambda: self.setColor('r'))
        self.btn_g.clicked.connect(lambda: self.setColor('g'))
        self.btn_b.clicked.connect(lambda: self.setColor('b'))
        self.btn_rgb.clicked.connect(lambda: self.setColor('all'))

    def setImage(self):
        self.gtImage = ImageQt(self.img)
        self.pixmap = QPixmap.fromImage(self.gtImage)
        self.image_text.setPixmap(self.pixmap)

    def imageFile(self):
        try:
            self.fileName = QFileDialog.getOpenFileName(self, 'Выберите картинку', '', "Картинки (*.jpg)")[0]
        except Exception as e:
            pass
        if self.fileName:
            self.img = Image.open(self.fileName)
            size = (440, 440)
            self.img = self.img.resize(size)
            self.newImg = self.img.copy()
            self.setImage()

    def setColor(self, color):
        if hasattr(self, 'img'):
            self.img = self.newImg.copy()
            pixels = self.img.load()
            x, y = self.img.size
            for i in range(x):
                for j in range(y):
                    r, g, b = pixels[i, j]
                    if color == 'r':
                        pixels[i, j] = r, 0, 0
                    elif color == 'g':
                        pixels[i, j] = 0, g, 0
                    elif color == 'b':
                        pixels[i, j] = 0, 0, b
                    else:
                        pixels[i, j] = r, g, b
            self.setImage()
        else:
            self.imageFile()


def message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Warning)
    msg.exec_()


def application():
    app = QApplication(sys.argv)
    mainWindows = LoginWindows()
    mainWindows.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()