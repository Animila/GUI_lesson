from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import uic
import sys


class Note(QMainWindow):
    def __init__(self):
        # загрузка ресурсов
        super().__init__()
        uic.loadUi('notes.ui', self)

        # "база данных"
        self.ID = 1
        self.BD = {
            'id': [],
            'name': [],
            'image': [],
            'about': [],

        }

        # кнопки управления
        self.btn_save.clicked.connect(self.save)
        self.btn_load.clicked.connect(self.load)
        self.btn_change.clicked.connect(self.change)
        self.btn_delete.clicked.connect(self.delete)

    def save(self):
        """Сохранение данных"""

        name = self.name_student.text()
        about = self.note.toPlainText()

        self.BD['id'].append(self.ID)
        self.BD['name'].append(name)
        self.BD['about'].append(about)
        self.ID += 1
        self.messages('Успешно')
        self.updateList()

    def load(self):
        """Выгрузка данных"""

        id_student = self.list_student.currentRow()

        self.name_student.setText(self.BD['name'][id_student])
        self.note.setText(self.BD['about'][id_student])

    def change(self):
        """Изменение данных"""

        id_student = self.list_student.currentRow()
        name = self.name_student.text()
        about = self.note.toPlainText()

        self.BD['name'][id_student] = name
        self.BD['about'][id_student] = about
        self.messages('Изменено')
        self.updateList()

    def delete(self):
        """Удаление данных"""

        id_student = self.list_student.currentRow()

        self.BD['id'].pop(id_student)
        self.BD['name'].pop(id_student)
        self.BD['about'].pop(id_student)
        self.messages('Удалено')
        self.updateList()

    def updateList(self):
        """Обновление списка студентов"""

        self.list_student.clear()

        for student in self.BD['name']:
            self.list_student.addItem(student)

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


def application():
    """Приложение"""
    app = QApplication(sys.argv)
    window = Note()
    window.setFixedSize(341, 804)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
