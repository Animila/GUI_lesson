import random
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication


class Windows_layer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('role.ui', self)

        self.list_action = [
            self.enemy_attack,
            self.enemy_magic,
        ]

        # характеристики героя
        self.heroHP = 100
        self.heroMP = 100
        # характеристики врага
        self.titleEnemy = 'Враг'
        self.enemyHP = 100
        self.enemyMP = 100
        # обновление статистики
        self.update_state()

        # кнопки действий
        self.btn_attack.clicked.connect(self.attach)
        self.btn_guard.clicked.connect(self.guard)
        self.btn_magic.clicked.connect(self.magic)

    def update_state(self):
        if self.enemyHP <= 0:
            self.enemyHP = 0
            self.log_game.addItem('Враг уничтожен')
        if self.heroMP <= 0:
            self.heroMP = 0
            self.log_game.addItem('Магия иссякла')
        if self.heroHP <= 0:
            self.heroHP = 0
            self.log_game.addItem('Персонаж уничтожен')
        # герой
        self.HP.setText(f'HP: {self.heroHP}')
        self.MP.setText(f'MP: {self.heroMP}')
        # враг
        self.Enemy.setText(f'Enemy: {self.titleEnemy}')
        self.Enemy_HP.setText(f'HP: {self.enemyHP}')
        self.Enemy_MP.setText(f'MP: {self.enemyMP}')

    def attach(self):
        damage = random.randint(0, 20)
        self.enemyHP -= damage
        self.update_state()
        if not self.enemyHP <= 0:
            self.log_game.addItem(f'Атакован враг. Урон: {damage}')
            random.choice(self.list_action)()

    def guard(self):
        self.log_game.addItem('Защита')

    def magic(self):
        damage = random.randint(0, 20)
        self.heroMP -= damage
        self.enemyHP -= damage
        self.update_state()
        if not self.heroMP <= 0:
            self.log_game.addItem(f'Использована магия. Урон: {damage}')

    def enemy_attack(self):
        damage = random.randint(0, 20)
        self.heroHP -= damage

        if damage == 0:
            self.log_game.addItem('Враг промахнулся')
        else:
            self.log_game.addItem(f'Враг нанес {damage}')

        self.update_state()

    def enemy_magic(self):
        damage = random.randint(0, 30)
        self.heroHP -= damage
        self.enemyMP -= damage

        if damage == 0:
            self.log_game.addItem('Враг промахнулся')
        else:
            self.log_game.addItem(f'Враг использовал магию и нанес {damage}')

        self.update_state()

def application():
    app = QApplication(sys.argv)
    windows_list = Windows_layer()
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
