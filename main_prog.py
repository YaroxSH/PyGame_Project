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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, door = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                door = Door(x, y)
    return new_player, x, y, door


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('clever.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(door_group, all_sprites)


 # Место под классы


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    tile_images = {
        'wall': load_image('floor.png'),
        'empty': load_image('wall.png')
    }
    player_image = load_image('main_h(for time).png')
    tile_width = tile_height = 50
    player, level_x, level_y, door = generate_level(load_level('data/levels_variations/level_1.txt'))
    level_map = load_level('data/levels_variations/level_1.txt')
    # Место под программу
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                x, y = player.rect.x // tile_width, player.rect.y // tile_width
                if event.key == pygame.K_w and (level_map[y - 1][x] == '.' or level_map[y - 1][x] == '@'):
                    player.rect.y -= tile_width
                if event.key == pygame.K_s and (level_map[y + 1][x] == '.' or level_map[y + 1][x] == '@'):
                    player.rect.y += tile_width
                if event.key == pygame.K_a and (level_map[y][x - 1] == '.' or level_map[y][x - 1] == '@'):
                    player.rect.x -= tile_width
                if event.key == pygame.K_d and (level_map[y][x + 1] == '.' or level_map[y][x + 1] == '@'):
                    player.rect.x += tile_width
        if not pygame.sprite.collide_rect(player, door):
            screen.fill('black')
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
            door_group.draw(screen)
        else:
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            door_group.empty()
            player, level_x, level_y, door = generate_level(load_level('data/levels_variations/level_2.txt'))
            level_map = load_level('data/levels_variations/level_2.txt')
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()