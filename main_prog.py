import os
import sys
import pygame
import random


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


class Laser_horz_tel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('laser_tel_horz.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(lasers_group, all_sprites)


class Laser_vert_tel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('laser_tel_vert.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(lasers_group, all_sprites)


class Laser_horz_act(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('laser_act_horz.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(lasers_group, all_sprites)


class Laser_vert_act(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('laser_act_vert.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(lasers_group, all_sprites)



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


def regenerate_level(level):
    x, y, door, laser_horz_act, laser_vert_act = None, None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '&':
                Tile('empty', x, y)
                door = Door(x, y)
            elif level[y][x] == '1':
                Tile('empty', x, y)
                laser_horz_tel = Laser_horz_tel(x, y)
            elif level[y][x] == '2':
                Tile('empty', x, y)
                laser_vert_tel = Laser_vert_tel(x, y)
            elif level[y][x] == '3':
                Tile('empty', x, y)
                laser_horz_act = Laser_horz_act(x, y)
            elif level[y][x] == '4':
                Tile('empty', x, y)
                laser_vert_act = Laser_vert_act(x, y)
    return x, y, door, laser_horz_act, laser_vert_act


def terminate():
    pygame.quit()
    sys.exit()


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = load_image('door.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(50 * pos_x, 50 * pos_y)
        self.add(door_group, all_sprites)


def scoring(n):
    fil = open('data/score.txt', 'w')
    fil.write(str(n))
    fil.close()


def open_score():
    fil = open('data/score.txt')
    scr = fil.read()
    fil.close()
    return int(scr)


def laser_tlg():
    level_map[horz_coord] = '1' * w
    for i in range(h):
        st = level_map[i]
        jst = ''
        for j in range(w):
            if j != vert_coord:
                jst += st[j]
            else:
                jst += '2'
        level_map[i] = jst


def laser_act():
    for i in range(h):
        st = level_map[i]
        jst = ''
        for j in st:
            if j == '1':
                jst += '3'
            elif j == '2':
                jst += '4'
            else:
                jst += j
        level_map[i] = jst


def start_screen():
    scr = open_score()
    intro_text = ['ЛАБИРИНТ', '',
                  'Добро пожаловать в "Лабиринт",',
                  'игру в которой вы продвигаетесьпо подземелью.',
                  'Чем ниже вы спускаетесь, тем больше опасностей вас ждёт.',
                  'Лабиринт бесконечный, поэтому вы спускаетесь пока не умрёте.', '',
                  f'Ваш рекорд: {scr}', '',
                  'Нажмите на любую кнопку чтобы начать игру.']
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 150
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1350, 1000
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 30
    start_screen()
    running = True
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    door_group = pygame.sprite.Group()
    lasers_group = pygame.sprite.Group()
    score = 0
    tile_images = {
        'wall': load_image('floor.png'),
        'empty': load_image('wall.png')
    }
    levels = os.listdir('data/levels_variations')
    usd_levels = []
    player_image = load_image('main_h(for time).png')
    tile_width = tile_height = 50
    strt_lvl = 'level_1.txt'
    player, level_x, level_y, door = generate_level(load_level(f'data/levels_variations/{strt_lvl}'))
    level_map = load_level(f'data/levels_variations/{strt_lvl}')
    cur_l = strt_lvl
    time_s = -5
    time_c = -5
    time_a = -5
    total_t = 30
    field = level_map[:-1]
    h = len(field)
    w = len(field[0])
    laser_horz_act, laser_vert_act = None, None
    act_lasers = False
    while running:
        x, y = player.rect.x // tile_width, player.rect.y // tile_width
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and level_map[y - 1][x] != '#':
                    player.rect.y -= tile_width
                if event.key == pygame.K_s and level_map[y + 1][x] != '#':
                    player.rect.y += tile_width
                if event.key == pygame.K_a and level_map[y][x - 1] != '#':
                    player.rect.x -= tile_width
                if event.key == pygame.K_d and level_map[y][x + 1] != '#':
                    player.rect.x += tile_width
        if not pygame.sprite.collide_rect(player, door):
            screen.fill('black')
            all_sprites.draw(screen)
            tiles_group.draw(screen)
            player_group.draw(screen)
            door_group.draw(screen)
            lasers_group.draw(screen)
            fnt = pygame.font.Font(None, 50)
            score_rendered = fnt.render(f'Счет: {score}', 1, pygame.Color('white'))
            score_rect = score_rendered.get_rect()
            score_rect.top = 1
            score_rect.x = 1
            screen.blit(score_rendered, score_rect)
        else:
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            door_group.empty()
            lasers_group.empty()
            levels.remove(cur_l)
            next_l = random.choice(levels)
            player, level_x, level_y, door = generate_level(load_level(f'data/levels_variations/{next_l}'))
            level_map = load_level(f'data/levels_variations/{next_l}')
            usd_levels.append([cur_l, 4])
            cur_l = next_l
            for i in range(len(usd_levels)):
                usd_levels[i][1] = usd_levels[i][1] - 1
                if usd_levels[i][1] <= 0:
                    ret = usd_levels[i][0]
                    levels.append(ret)
            for i in usd_levels:
                if i[1] <= 0:
                    usd_levels.remove(i)
            time_s = total_t
            total_t = time_s * 0.75
            score += 100
            time_a = -5
            time_c = -5
        if level_map[y][x] == '3' or level_map[y][x] == '4':
            all_sprites.empty()
            tiles_group.empty()
            player_group.empty()
            door_group.empty()
            lasers_group.empty()
            levels.remove(cur_l)
            time_s = -5
            time_c = -5
            time_a = -5
            total_t = 30
            rs = open_score()
            if score > rs:
                scoring(score)
            score = 0
            start_screen()
            levels = os.listdir('data/levels_variations')
            usd_levels = []
            player, level_x, level_y, door = generate_level(load_level(f'data/levels_variations/{strt_lvl}'))
            level_map = load_level(f'data/levels_variations/{strt_lvl}')
            cur_l = strt_lvl
        clock.tick(fps)
        pygame.display.flip()
        if time_s != -5:
            time_s -= 1
            if time_s <= 0:
                time_s = -5
                time_c = 10
                vert_coord = random.randint(0, w - 1)
                horz_coord = random.randint(0, h - 1)
                if vert_coord == 13 or horz_coord == 13:
                    vert_coord = random.randint(0, w - 1)
                    horz_coord = random.randint(0, h - 1)
                laser_tlg()
                level_x, level_y, door, laser_horz_act, laser_vert_act = regenerate_level(level_map)
        if time_c != -5:
            time_c -= 1
            if time_c <= 0:
                time_c = -5
                time_a = 7
                laser_act()
                level_x, level_y, door, laser_horz_act, laser_vert_act = regenerate_level(level_map)
                act_lasers = True
        if time_a != -5:
            time_a -= 1
            if time_a <= 0:
                time_a = -5
                time_s = 35
                tiles_group.empty()
                door_group.empty()
                level_x, level_y, door, laser_horz_act, laser_vert_act = regenerate_level(
                    load_level(f'data/levels_variations/{cur_l}'))
                level_map = load_level(f'data/levels_variations/{cur_l}')
                lasers_group.empty()
                act_lasers = False
    pygame.quit()