import pygame


def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True
    x = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # на любое действие
            x += 1

        # смена цвета
        screen.fill((255, 255, 255))
        # рисуем круг (на экране, черного цвета, на (0, 300) пикелях, диаметром 10)
        pygame.draw.circle(screen, (0, 255, 0), (x, 300), 10)
        pygame.draw.rect(screen, pygame.Color('red'), (0, x, 50, 50))
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    application()
