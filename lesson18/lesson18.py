import os
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
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Игра 1")
clock = pygame.time.Clock()
FPS = 60
allSprite = pygame.sprite.Group()


class Mount(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(allSprite)
        self.image = loadImage('mountains.png', -1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = h



class Parachute(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(allSprite)
        self.image = loadImage('pt.png', -1)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = h
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self):
        if not pygame.sprite.collide_mask(self, mount):
            self.rect = self.rect.move(0, 1)


if __name__ == "__main__":
    mount = Mount()

    while True:

        screen.fill((0, 0, 0))
        allSprite.draw(screen)
        allSprite.update()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                Parachute(event.pos)



