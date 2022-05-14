import os
from random import randint
import pygame


def loadImage(name, colorKey=None):
    """Загружаем спрайты (имя файла)"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print(f'Ошибка {message}')
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
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("Игра 1")
clock = pygame.time.Clock()
FPS = 60
allSprite = pygame.sprite.Group()
verSprite = pygame.sprite.Group()
horSprite = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, rad, x, y):
        super().__init__(allSprite)
        self.radius = rad
        self.image = pygame.Surface((2 * rad, 2 * rad), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color('green'), (rad, rad), rad)
        self.rect = pygame.Rect(x, y, 2 * rad, 2 * rad)
        self.vectorX = randint(-5, 5)
        self.vectorY = randint(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vectorX, self.vectorY)
        if pygame.sprite.spritecollideany(self, horSprite):
            self.vectorY = - self.vectorY
        if pygame.sprite.spritecollideany(self, verSprite):
            self.vectorX = - self.vectorX


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(allSprite)
        if x1 == x2:
            self.add(verSprite)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horSprite)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


if __name__ == "__main__":
    for i in range(50):
        Ball(20, 100, 100)
    Border(5, 5, w - 5, 5)
    Border(5, h - 5, w - 5, h - 5)
    Border(5, 5, 5, h - 5)
    Border(w - 5, 5, w - 5, h - 5)

    while True:
        
        screen.fill((0, 0, 0))
        allSprite.draw(screen)
        allSprite.update()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()




