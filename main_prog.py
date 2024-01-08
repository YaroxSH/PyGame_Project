import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


 # Место под классы


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    tile_images = {
        #
    }
    player_image = load_image('')
    tile_width = tile_height = 50
    # Место под программу
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')
        # Место под прорисовку
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()