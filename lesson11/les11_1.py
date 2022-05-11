import pygame


class Map:
    def __init__(self, w, h):
        self.weight = w
        self.height = h

        self.left = 0
        self.top = 0
        self.CellSize = 90

    def editSetting(self, left, top, cell_size):
        """Изменение настроек"""
        self.left = left
        self.top = top
        self.CellSize = cell_size

    def RenderModel(self, screen):
        """Отрисовка объекта"""
        for y in range(self.height):
            for x in range(self.weight):
                pygame.draw.rect(screen,
                                 pygame.Color('white'),
                                 (
                                  x * self.CellSize + self.left,
                                  y * self.CellSize + self.top,
                                  self.CellSize,
                                  self.CellSize
                                  ), 1)

def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True

    map = Map(7, 8)
    map.editSetting(10, 50, 40)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0, 0, 0))
        map.RenderModel(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    application()
