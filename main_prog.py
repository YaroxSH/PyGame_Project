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


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def load_level(filename):
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))
    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            # elif level[y][x] == '@':
                # Tile('empty', x, y)
                # new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


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
        'wall': load_image('floor.png'),
        'empty': load_image('wall.png')
    }
    # player_image = load_image('')
    tile_width = tile_height = 50
    player, level_x, level_y = generate_level(load_level('data/levels.txt'))
    level_map = load_level('data/levels.txt')
    # Место под программу
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill('white')
        all_sprites.draw(screen)
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()