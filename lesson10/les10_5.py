import pygame
import random


def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True
    click = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # захват движение мышки
            elif event.type == pygame.MOUSEMOTION and click:
                pygame.draw.circle(screen, (0, 200, 200), event.pos, 10)
            # при клике
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click = True
            # при отпускании кнопки
            elif event.type == pygame.MOUSEBUTTONUP:
                click = False


        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    application()
