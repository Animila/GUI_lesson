import pygame


def application():
    # инициализация
    pygame.init()
    # размер
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    # для выхода
    run = True

    # если программа не выходит
    while run:
        for event in pygame.event.get():
            # перехват событий
            if event.type == pygame.QUIT:
                run = False


        pygame.display.flip() #обновление экрана
    pygame.quit()


if __name__ == "__main__":
    application()