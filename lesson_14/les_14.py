from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

import sqlite3

import os
import sys

from configIMG import Ui_Dialog


class Note(QMainWindow):

    # НАСТРОЙКИ

    def __init__(self):
        # загрузка ресурсов
        super().__init__()
        uic.loadUi('notes_2.ui', self)
        self.connect = sqlite3.connect('bdslite.db')
        self.image = None
        self.ID = self.getLastId()

        # контроллеры управления
        self.btn()

        # обновление БД
        self.updateBD()

    # ИНТЕРФЕЙСЫ

    def btn(self):
        """Кнопки управления"""
        self.btn_save.clicked.connect(self.save)
        self.btn_load.clicked.connect(self.load)
        self.btn_change.clicked.connect(self.change)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_img.triggered.connect(self.openOtherWindows)

    # КОНТРОЛЛЕРЫ

    def save(self):
        """Сохранение данных"""
        name = self.name_student.text()
        about = self.note.toPlainText()
        self.ID += 1
        self.askAddItem()
        if self.image:
            data = (self.ID, name, about, self.image)
            cmd = "INSERT INTO user(id, names, about, image) VALUES (?, ?, ?, ?);"
        else:
            data = (self.ID, name, about)
            cmd = "INSERT INTO user(id, names, about) VALUES (?, ?, ?);"

        try:
            request = self.getBDTable()[1]
            request.execute(cmd, data)
            self.connect.commit()
        except Exception as e:
            self.messages(f'{e}')
        else:
            self.messages('Успешно сохранено')
            self.updateBD()

    def load(self):
        """Выгрузка данных"""

        try:
            result = self.getBDTable()[0]
        except Exception as e:
            self.messages(f'{e}')
        else:
            self.ID = result[self.getStudentIdList()][0]
            self.name_student.setText(result[self.getStudentIdList()][1])
            self.note.setText(result[self.getStudentIdList()][3])
            if self.image:
                self.readBlogData(self.getStudentIdList())

    def change(self):
        """Изменение данных"""

        name = self.name_student.text()
        about = self.note.toPlainText()
        try:
            result = self.getBDTable()[0]
            request = self.getBDTable()[1]
            id = result[self.getStudentIdList()][0]
            cmd = """UPDATE user SET names=?, about=? WHERE id=?"""
            data = (name, about, id)
            request.execute(cmd, data)
            self.connect.commit()
        except Exception as e:
            self.messages(f'{e}')
        else:
            self.messages('Изменено')
            self.updateBD()

    def delete(self):
        """Удаление данных"""

        try:
            result = self.getBDTable()[0]
            request = self.getBDTable()[1]
            id = result[self.getStudentIdList()][0]
            name = result[self.getStudentIdList()][1]
            cmd = """DELETE FROM user WHERE id=?"""
            request.execute(cmd, (id,))
            self.connect.commit()
        except Exception as e:
            self.messages(f'{e}')
        else:
            self.messages('Удалено')
            self.updateBD()
            self.ID = self.lastID
        try:
            os.remove(self.setPathImg(name))
        except Exception as e:
            print(f'файла нет: {e}')

    # СИСТЕМА УПРАВЛЕНИЯ

    def getBDTable(self):
        request = self.connect.cursor()
        request.execute("SELECT * FROM user;")
        print("все ок")
        return (request.fetchall(), request)

    def convertToBinaryData(self, filename):
        """Конвертация изображения в набор символов"""
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data

    def writeToFile(self, data, filename):
        """Запись в файл"""
        path_img = self.setPathImg(filename)
        with open(path_img, 'wb+') as file:
            file.write(data)
        print("Данный из blob сохранены в: ", path_img, "\n")

    def setPathImg(self, filename):
        """Путь к файлу"""
        return os.path.abspath(f'{filename}.png')

    def readBlogData(self, id):
        """Скачивание файлов"""
        try:
            result = self.getBDTable()[0]
            request = self.getBDTable()[1]
            name = result[id][1]
            photo = result[id][2]
            print("Id = ", result[id][0], "Name = ", name)
            print("Сохранение изображения сотрудника и резюме на диске \n")
            self.writeToFile(photo, name)
            request.close()
        except Exception as error:
            self.messages(f'{error}')

    def getLastId(self):
        """Получение последнего ID"""

        result = self.getBDTable()[0]
        id = 0
        for student in result:
            id = student[0]
            print(id)
        return id


    def updateBD(self):
        """Обновление данных"""
        try:
            result = self.getBDTable()[0]
        except Exception as e:
            self.messages(f'{e}')
        else:
            self.list_student.clear()
            for student in result:
                self.list_student.addItem(f'{student[0]}. {student[1]}')
            self.lastID = self.getLastId()
            self.connect.commit()

    # ПРОЧИЕ МЕХАНИЗМЫ

    def getStudentIdList(self):
        """Получаем текущий ID"""
        return int(self.list_student.currentRow())

    def getImage(self):
        """Получаем путь к текущему изображению"""
        try:
            result = self.getBDTable()[0]
            student_id = self.getStudentIdList()
            name = result[student_id][1]
        except Exception as e:
            self.messages(f'{e}')
        else:
            path = self.setPathImg(name)
            print(path)
            return path

    def openOtherWindows(self):
        """Запуск нового окна"""
        global Dialog
        Dialog = QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        path = self.getImage()
        ui.img_student.setPixmap(QPixmap(path))
        Dialog.show()

    def askAddItem(self):
        """Вопрос о добавлении картинки"""
        message = QMessageBox()
        message.setWindowTitle('Результат')
        message.setText('Хотите ли вы загрузить картинку?')
        message.setIcon(QMessageBox.Information)
        message.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        message.buttonClicked.connect(self.askInput)
        message.exec_()

    def askInput(self, btn):
        """Вытаскиваем файл из """
        print(btn.text())
        if btn.text() == "&Yes":
            try:
                img_path = str(QFileDialog.getOpenFileName(self)[0])
                self.image = self.convertToBinaryData(img_path)
            except Exception as e:
                self.messages(f'{e}')

    def messages(self, text):
        """Всплывающее окно"""
        message = QMessageBox()
        message.setWindowTitle('Результат')
        message.setText(text)
        message.setIcon(QMessageBox.Information)
        message.setDefaultButton(QMessageBox.Ok)
        message.buttonClicked.connect(self.clearInputs)
        message.exec_()

    def clearInputs(self):
        """Очитка экрана"""
        self.name_student.clear()
        self.note.clear()


# ПРИЛОЖЕНИЕ

def application():
    """Приложение"""
    app = QApplication(sys.argv)
    window = Note()
    window.setFixedSize(341, 804)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
