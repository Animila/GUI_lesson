import random
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap


# ГЛАВНОЕ ОКНО

class Windows_Game(QMainWindow):
    def __init__(self):
        # загрузка ресурсов
        super().__init__()
        uic.loadUi('role.ui', self)
        self.index_img = 0
        self.list_img_enemy = [
            'img/enemy/p1.png',
            'img/enemy/p2.png',
            'img/enemy/p3.png',
            'img/enemy/p4.png',
        ]
        self.list_img_hero = [
            'img/hero/walk0.png',
            'img/hero/walk1.png',
            'img/hero/walk2.png',
            'img/hero/walk3.png',
            'img/hero/walk4.png',
            'img/hero/walk5.png',
            'img/hero/walk6.png',
            'img/hero/walk7.png',

        ]
        self.view_image(self.img_enemy, self.list_img_enemy)
        self.view_image(self.img_hero, self.list_img_hero)

        # характеристики героя
        self.heroHP = 100
        self.heroMP = 100

        # характеристики врага
        self.titleEnemy = 'Враг'
        self.enemyHP = 1
        self.enemyMP = 1
        self.countEnemy = 5
        self.enemes = []

        self.countBoter = 3
        self.boters = []

        # список действий врага
        self.list_action = [
            self.enemy_attack,
            self.enemy_magic,
            # self.enemy_guard,
        ]

        # первоначальная генерация карты
        self.ui_map()

        # обновление статистики
        self.update_state()

        # кнопки действий
        # self.btn_action()

        # кнопки передвижения
        self.btn_moving()

    # КОНТРОЛЛЕРЫ ИГРЫ

    def ui_map(self):
        """Настройки и параметры """
        self.stopForward = False
        self.stopBack = False
        self.stopLeft = False
        self.stopRight = False

        self.stopEnemyForward = False
        self.stopEnemyBack = False
        self.stopEnemyLeft = False
        self.stopEnemyRight = False

        self.x_map = 20
        self.y_map = 10

        self.unit = 'H'
        self.enemy = 'E'
        self.magic_boter = 'W'
        self.map_page = '-'


        self.generate_map()

        self.x, self.y = 1, 1

        for _ in range(1, self.countEnemy):
            self.x_enemy, self.y_enemy = random.randint(0, len(self.levels)-1), random.randint(0, len(self.levels)-1)
            self.levels[self.y_enemy][self.x_enemy] = self.enemy
            self.enemes.append([self.y_enemy, self.x_enemy])

        for _ in range(1, self.countBoter):
            self.x_magic_boter, self.y_magic_boter = random.randint(0, len(self.levels)-1), random.randint(0, len(self.levels)-1)
            self.levels[self.y_magic_boter][self.x_magic_boter] = self.magic_boter
            self.boters.append([self.y_magic_boter, self.x_magic_boter])

        self.levels[self.y][self.x] = self.unit

        self.update_map()

    def btn_action(self):
        """Контроллеры кнопок действий"""
        self.btn_attack.clicked.connect(self.attach)
        self.btn_guard.clicked.connect(self.guard)
        self.btn_magic.clicked.connect(self.magic)

    def btn_moving(self):
        """Контроллеры кнопок передвижения"""
        self.btn_forward.clicked.connect(self.forward)
        self.btn_back.clicked.connect(self.back)
        self.btn_left.clicked.connect(self.left)
        self.btn_right.clicked.connect(self.right)

    def update_state(self):
        """Обновления и проверка статистики"""
        self.max_min_state()

        # герой
        self.HP.setText(f'HP: {self.heroHP}')
        self.MP.setText(f'MP: {self.heroMP}')
        # враг
        self.Enemy.setText(f'Enemy: {self.titleEnemy}')
        self.Enemy_HP.setText(f'HP: {self.enemyHP}')
        self.Enemy_MP.setText(f'MP: {self.enemyMP}')

    def max_min_state(self):
        """Проверка статистики на предмет некорректных данных"""

        # здоровье персонажа
        if self.heroHP <= 0:
            self.heroHP = 0
            self.log_game.addItem('Персонаж уничтожен')
        if self.heroHP >= 100:
            self.heroHP = 100

        # здоровье врага
        if self.enemyHP <= 0:
            self.enemyHP = 0
            self.stopEnemyRight = False
            self.log_game.addItem('Враг уничтожен')
        if self.enemyHP >= 100:
            self.enemyHP = 100

        # мана персонажа
        if self.heroMP <= 0 and self.enemyHP > 0:
            self.heroMP = 0
            self.log_game.addItem('Магия иссякла')
        if self.heroMP >= 100:
            self.heroMP = 100

        # мана врага
        if self.enemyMP >= 100:
            self.enemyMP = 100
        if self.enemyMP <= 0:
            self.enemyMP = 0

    def generate_map(self):
        """Генерация карты"""
        self.levels = [[self.map_page for x in range(self.x_map)] for y in range(self.y_map)]
        self.update_map()

    def update_map(self):
        """Обновление карты"""

        self.map.setText('')

        # столбцы
        # поля
        for y in range(len(self.levels)):
            for x in range(len(self.levels[y])):
                text = self.map.text()
                self.map.setText(text + str(self.levels[y][x]))
            text = self.map.text()
            self.map.setText(text + '\n')

    def search_hero(self):
        """Поиск позиции героя"""
        for y in range(len(self.levels)):
            for x in range(len(self.levels[y])):
                if self.levels[y][x] == self.unit:

                    self.y, self.x = y, x
                    print(f'герой x: {self.x} y:{self.y}')
        self.distance_wall()

    def distance_wall(self):
        """Проверка на наличие стенок"""
        # Если текущий шаг будет равен длине массива,
        # то движение вперед будет запрещено.
        # И наоборот
        if len(self.levels) == self.y + 1:
            self.stopBack = True
            self.stopForward = False
        if self.y - 1 < 0:
            self.stopBack = False
            self.stopForward = True

        if len(self.levels[self.y]) == self.x + 1:
            self.stopLeft = False
            self.stopRight = True
        if self.x - 1 < 0:
            self.stopLeft = True
            self.stopRight = False

    def distance_enemy(self):
        """Проверка дистанции до врага"""
        hero = [self.y, self.x]
        if hero in self.enemes:
            self.index_img = 2
            self.view_image(self.img_enemy, self.list_img_enemy)
            random.choice(self.list_action)()
            self.update_state()
            print('враг атакует')
        self.update_map()


    def distance_boter(self):
        """Проверка дистанции до врага"""
        hero = [self.y, self.x]
        if hero in self.boters:
            self.guard()
            self.update_state()
            print('отдых')
        self.update_map()

    def view_image(self, state, var):
        """Вывод изображения персонажа"""
        list_img = var
        if self.index_img > len(list_img) - 1:
            self.index_img = 0

        self.img = QPixmap(list_img[self.index_img])
        state.setPixmap(self.img)

    # КОНТРОЛЛЕР ПЕРЕДВИЖЕНИЯ

    def forward(self):

        self.index_img += 1
        self.view_image(self.img_hero, self.list_img_hero)

        self.search_hero()
        self.distance_enemy()
        self.distance_boter()

        if not self.stopForward:
            self.levels[self.y - 1][self.x] = self.unit
            self.levels[self.y][self.x] = self.map_page
            self.log_game.addItem('Идет вперед')
        else:
            self.log_game.addItem('Стена')

        self.update_map()

    def back(self):
        self.index_img += 1
        self.view_image(self.img_hero, self.list_img_hero)

        self.search_hero()
        self.distance_enemy()
        self.distance_boter()

        if not self.stopBack:
            self.levels[self.y + 1][self.x] = self.unit
            self.levels[self.y][self.x] = self.map_page
            self.log_game.addItem('Идет назад')
        else:
            self.log_game.addItem('Стена')

        self.update_map()

    def left(self):
        self.index_img += 1
        self.view_image(self.img_hero, self.list_img_hero)

        self.search_hero()
        self.distance_enemy()
        self.distance_boter()

        if not self.stopLeft:
            self.levels[self.y][self.x - 1] = self.unit
            self.levels[self.y][self.x] = self.map_page
            self.log_game.addItem('Идет влево')
        else:
            self.log_game.addItem('Стена')

        self.update_map()

    def right(self):
        self.index_img += 1
        self.view_image(self.img_hero, self.list_img_hero)

        self.search_hero()
        self.distance_enemy()
        self.distance_boter()

        if not self.stopRight and not self.stopEnemyRight:
            self.levels[self.y][self.x + 1] = self.unit
            self.levels[self.y][self.x] = self.map_page
            self.log_game.addItem('Идет вправо')
        else:
            self.log_game.addItem('Стена')

        self.update_map()

    # КОНТРОЛЛЕР КНОПОК ДЕЙСТВИЯ

    def attach(self):
        """Атака персонажа"""

        self.search_hero()
        self.search_enemy()

        if self.stopEnemyRight :
            from time import sleep
            sleep(1)
            if not self.enemyHP <= 0 and self.heroHP > 0:
                damage = random.randint(0, 20)

                self.enemyHP -= damage
                self.log_game.addItem(f'Атакован враг. Урон: {damage}')

                random.choice(self.list_action)()

            self.update_state()

    def magic(self):
        """Использование магии"""

        if not self.heroMP <= 0 and self.enemyHP > 0 and self.heroHP > 0:
            damage = random.randint(0, 30)

            self.heroMP -= damage
            self.enemyHP -= damage
            self.log_game.addItem(f'Использована магия. Урон: {damage}')

            random.choice(self.list_action)()

        self.update_state()

    def guard(self):
        """Защита от атаки"""
        if not self.heroHP <= 0:
            random.seed(4324)
            health = random.randint(10, 30)
            magic = random.randint(5, 10)
            self.heroHP += health
            self.heroMP += magic
            self.log_game.addItem('Персонаж отдыхает')

        self.update_state()

    # КОНТРОЛЛЕР ДЕЙСТВИЙ ВРАГА

    def enemy_attack(self):
        """ответная атака врага"""

        if not self.enemyHP <= 0:

            random.seed(328731)
            damage_enemy = random.randint(10, 30)

            self.heroHP -= damage_enemy
            if damage_enemy == 0:
                self.log_game.addItem('Враг промахнулся')
            else:
                self.log_game.addItem(f'Враг нанес {damage_enemy}')

        self.update_state()

    def enemy_magic(self):
        """ответная магическая атака врага"""

        if not self.enemyMP <= 0:
            random.seed(294898)
            damage = random.randint(10, 40)

            self.heroHP -= damage
            self.enemyMP -= damage
            if damage == 0:
                self.log_game.addItem('Враг промахнулся')
            else:
                self.log_game.addItem(f'Враг использовал магию и нанес {damage}')

        self.update_state()

    def enemy_guard(self):
        """Восстановление врага"""
        if not self.enemyHP >= 100 and self.enemyHP > 0:
            health = random.random()
            magic = random.randint(5, 10)
            self.enemyHP += round(health * 100 - 50)
            self.enemyMP += magic
            self.log_game.addItem('Враг отдыхает')

        self.update_state()


# СОЗДАНИЕ ПРИЛОЖЕНИЯ

def application():
    app = QApplication(sys.argv)
    windows_list = Windows_Game()
    windows_list.setFixedSize(1058, 510)
    windows_list.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
