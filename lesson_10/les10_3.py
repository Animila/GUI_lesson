import pygame


def myText(screen, w, h):
    """Установка текста"""
    screen.fill((255, 255, 255))
    # текст (шрифт, размер)
    font = pygame.font.Font(None, 50)
    # сам текст (текст, гладкость, цвет)
    text = font.render("Привет мир", 1, pygame.Color('black'))
    # для размещения текста посередине
    text_x = w // 2 - text.get_width() // 2
    text_y = h // 2 - text.get_height() // 2
    # размещение
    screen.blit(text, (text_x, text_y))
    # для рамки (углы начала, углы конца, толщина)
    pygame.draw.rect(screen, (0, 0, 255), (text_x, text_y, text.get_width(), text.get_height()), 1)


def application():
    pygame.init()
    size = w, h = 800, 600
    screen = pygame.display.set_mode(size)
    run = True
    x = 0

    # для заливки
    screen.fill((255, 255, 255))
    myText(screen, w, h)
    pygame.display.flip()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    application()
