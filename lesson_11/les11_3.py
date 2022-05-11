import random

import pygame


class Map:
    def __init__(self, w, h):
        self.weight = w
        self.height = h
        self.cells = [[0] * w for _ in range(h)]

        self.start_left = 0
        self.start_top = 0
        self.CellSize = 90

    def editSetting(self, left, top, cell_size):
        """Интерфейс настроек"""
        self.start_left = left
        self.start_top = top
        self.CellSize = cell_size

    def renderCell(self, screen):
        """Отрисовка объекта"""
        colors_list = [
                        pygame.Color('red'),
                        pygame.Color('green'),
                        pygame.Color('blue'),
                        pygame.Color('black'),
                        pygame.Color('pink')
                        ]

        for y in range(self.height):
            for x in range(self.weight):
                pygame.draw.rect(screen,
                                 colors_list[self.cells[y][x]],
                                 (
                                  self.start_left + self.CellSize * x,
                                  self.start_top + self.CellSize * y,
                                  self.CellSize,
                                  self.CellSize
                                  ))
                pygame.draw.rect(screen,
                                 pygame.Color('White'),
                                 (
                                     self.start_left + self.CellSize * x,
                                     self.start_top + self.CellSize * y,
                                     self.CellSize,
                                     self.CellSize
                                 ), 1)

    def paintCell(self, cell):
        # покрас строки
        # for x in range(self.weight):
        #     self.cells[cell[1]][x] = (self.cells[cell[1]][x] + 1) % 2
        # # покрас столбца
        # for y in range(self.height):
        #     if y == cell[1]:
        #         continue
        #     self.cells[y][cell[0]] = (self.cells[y][cell[0]] + 1) % 2

        # одна точка
        for y in range(self.height):
            for x in range(self.weight):
                if x == cell[0] and y == cell[1]:
                    self.cells[cell[1]][cell[0]] = random.randint(1, 4)

    def getCell(self, mousePos):
        """Получение данных о клетке"""
        cell_x = (mousePos[0] - self.start_left) // self.CellSize
        cell_y = (mousePos[1] - self.start_top) // self.CellSize
        if cell_x < 0 or cell_x >= self.weight or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def getClick(self, mousePos):
        """Интерфейс нажатия"""
        cell = self.getCell(mousePos)
        if cell:
            self.paintCell(cell)





def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True

    map = Map(20, 15)
    map.editSetting(0, 0, 40)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                map.getClick(event.pos)
        screen.fill((0, 0, 0))
        map.renderCell(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    application()
