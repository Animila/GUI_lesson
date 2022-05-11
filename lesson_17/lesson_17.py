import os
import sys
import pygame
from tkinter import messagebox
from random import randint


def loadImage(name, colorKey=None):
    """Загружаем спрайты (имя файла)"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        messagebox.showinfo(f'Ошибка: {message}.\n Не найден {name}', 'OK')
        raise SystemExit(message)

    if colorKey is not None:
        if colorKey == -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey)
    else:
        image = image.convert_alpha()

    return image


# НАСТРОЙКИ ИГРЫ
pygame.init()
size = w, h = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Игра 1")
allSprites = pygame.sprite.Group()
clock = pygame.time.Clock()


class Bomb(pygame.sprite.Sprite):
    """Шаблон объекта"""
    image = loadImage('bomb2.png', -1)
    imageFitil = loadImage('bomb.png', -1)
    imageBoom = loadImage('boom.png', -1)
    listsBomb = []
    tx, ty = image.get_width(), image.get_height()
    for i in range(10):
        listsBomb.append(pygame.transform.scale(imageFitil, (tx - i * 3, ty - i * 3)))
    listsBomb.append(image)
    listsBomb.append(imageBoom)

    def __init__(self, group):
        # Связывается с группой объектов
        # и указывает, что у всех одна картинка
        # достаем из изображения коллайдер
        super().__init__(group)
        self.actionBomb = Bomb.listsBomb
        self.index = 0
        self.image = self.actionBomb[0]
        self.rect = self.image.get_rect()
        self.boom = False

        # генерация
        while True:
            self.rect.topleft = (
                (randint(0, w - self.rect.width), randint(0, h - self.rect.height))
            )
            if len(pygame.sprite.spritecollide(self, allSprites, False)) == 1:
                break

    def update(self):
        """Анимация"""
        if self.boom and self.index + 1 < len(self.actionBomb):
            self.index += 1
            self.image = self.actionBomb[self.index]

    def getEvent(self, event):
        """Изменение состояния бомбы"""
        # если нажали на коллайдер
        if self.rect.collidepoint(event.pos):
            self.boom = True


def setImage(title, allSprites, alpha=None):
    """Установка курсора"""
    image = loadImage(title, alpha)
    all_image = pygame.sprite.Sprite(allSprites)
    all_image.image = image
    all_image.rect = image.get_rect()
    return all_image


def application():
    """Запуск приложения"""
    for i in range(10):
        Bomb(allSprites)

    while True:
        allSprites.draw(screen)
        allSprites.update( )
        pygame.display.flip()
        screen.fill((0, 0, 0))
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in allSprites:
                    i.getEvent(event)
            if event.type == pygame.QUIT:
                sys.exit()


if __name__ == "__main__":
    application()

