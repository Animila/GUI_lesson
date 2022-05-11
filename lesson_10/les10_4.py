import pygame
import random


def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill((0,0,0))
        for i in range(10000):
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                        (random.random() * w,
                         random.random() * h, 5, 5))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    application()
