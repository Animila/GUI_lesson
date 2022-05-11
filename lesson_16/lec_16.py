import os
import sys
import pygame
from tkinter import messagebox


class Car(pygame.sprite.Sprite):
    """Машина"""
    image_right = None
    image_left = None

    def __init__(self, group, size):
        super().__init__(group)
        if Car.image_right is None:
            Car.image_right = loadImage("car2.png", -1)
            Car.image_left = pygame.transform.flip(Car.image_right, True, False)

        self.w_image, self.h_image = size
        self.image = Car.image_right
        self.rect = self.image.get_rect()
        self.speedX = 5
        self.speedY = 5
        self.ticks = 0

    def update(self):
        if self.rect.left + self.rect.width > self.w_image or self.rect.left < 0:
            self.speedX = -self.speedX
            if self.speedX > 0:
                self.image = Car.image_right
            else:
                self.image = Car.image_left
        if self.rect.top + self.rect.height > self.h_image or self.rect.top < 0:
            self.speedY = - self.speedY
        self.rect.left = self.rect.left + self.speedX
        self.rect.top = self.rect.top + self.speedY
        self.ticks = 0


def loadImage(name, color_key=None):
    """Загружаем спрайты (имя файла)"""

    # получаем путь к изображениям
    # преобразуем
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        messagebox.showinfo(f'Ошибка: {message}.\n Не найден {name}', 'OK')
        raise SystemExit(message)

    # проверяем условие
    # если -1 - удаляем черный цвет
    # иначе удаляем альфа канал
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


def setting():
    """Различные настройки для игры"""
    # инициализация игры
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Игра 1")

    clock = pygame.time.Clock()

    # загрузка ресурсов
    all_sprites = pygame.sprite.Group()
    Car(all_sprites, size)
    cursor = setImage(title='arrow.png', alpha=-1, all_sprites=all_sprites)
    pygame.mouse.set_visible(False)

    return all_sprites, screen, cursor, clock


def setImage(title, all_sprites, alpha=None):
    """Установка курсора"""
    image = loadImage(title, alpha)
    all_image = pygame.sprite.Sprite(all_sprites)
    all_image.image = image
    all_image.rect = image.get_rect()
    return all_image


def application():
    """Запуск приложения"""
    all_sprites, screen, cursor, clock = setting()


    while True:
        all_sprites.draw(screen)
        pygame.display.flip()
        all_sprites.update()

        screen.fill((255, 255, 255))

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.center = event.pos

if __name__ == "__main__":
    application()

