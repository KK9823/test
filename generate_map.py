import pygame
import sys
import random


def iterate(main_map, include_edges=False):
    if include_edges:
        for ri, row in enumerate(main_map):
            for ci, val in enumerate(row):
                yield ri, ci, val
    else:
        for ri, row in enumerate(main_map[1:-1], 1):
            for ci, val in enumerate(row[1:-1], 1):
                yield ri, ci, val


def generate_land(main_map):
    for ri, ci, _ in iterate(main_map):
        if random.uniform(0, 1) < land_chance:
            main_map[ri][ci] = 1

    return main_map


def generate_highland(main_map):
    for ri, ci, val in iterate(main_map):
        if val == 1 and random.uniform(0, 1) < highland_chance:
            main_map[ri][ci] = 2

    return main_map


def generate_mountain(main_map):
    for ri, ci, val in iterate(main_map):
        if val == 2 and random.uniform(0, 1) < mountain_chance:
            main_map[ri][ci] = 3

    return main_map


def neighbours(ri, ci):
    return [
        (ri - 1, ci - 1), (ri - 1, ci), (ri - 1, ci + 1),
        (ri, ci - 1), (ri, ci + 1),
        (ri + 1, ci - 1), (ri + 1, ci), (ri + 1, ci + 1)
    ]


def color_sea():
    return 0, 95, random.randint(118, 128)


def color_land():
    return random.randint(87, 97), random.randint(108, 118), random.randint(44, 54)


def color_highlands():
    return random.randint(131, 151), random.randint(114, 124), random.randint(63, 83)


def color_mountain():
    return random.randint(128, 148), random.randint(142, 152), random.randint(135, 155)

def color(n):
    if n == 0:
        return color_sea()
    if n == 1:
        return color_land()
    if n == 2:
        return color_highlands()
    if n == 3:
        return color_mountain()


def color_map(main_map):
    res = [[(0,0,0) for _ in range(len(main_map[0]))] for __ in range(len(main_map))]

    for ri, ci, val in iterate(main_map, include_edges=True):
        res[ri][ci] = color(val)

    return res


def draw(color_map):
    tile_size = screen_length // len(color_map)

    for ri, ci, rgb in iterate(color_map, include_edges=True):
        surf = pygame.Surface((tile_size,tile_size))
        surf.fill(rgb)
        rect = surf.get_rect(topleft=(ri * tile_size, ci * tile_size))
        screen.blit(surf, rect)


def clean(main_map):
    for ri, ci, val in iterate(main_map):
        lands = 0
        for r, c in neighbours(ri, ci):
            lands += main_map[r][c]

        if lands > 4:
            main_map[ri][ci] = 1
        elif lands < 4:
            main_map[ri][ci] = 0

    return main_map


def clean_highland(main_map):
    for ri, ci, val in iterate(main_map):
        if val not in [1, 2]:
            continue

        highlands = lands = 0
        for r, c in neighbours(ri, ci):
            if main_map[r][c] == 2:
                highlands += 1
            elif main_map[r][c] == 1:
                lands += 1

        if highlands > lands:
            main_map[ri][ci] = 2
        elif highlands < lands:
            main_map[ri][ci] = 1

    return main_map


def clean_mountain(main_map):
    for ri, ci, val in iterate(main_map):
        if val not in [2, 3]:
            continue

        highlands = mountains = 0
        for r, c in neighbours(ri, ci):
            if main_map[r][c] == 2:
                highlands += 1
            elif main_map[r][c] == 3:
                mountains += 1

        if highlands > mountains:
            main_map[ri][ci] = 2
        elif highlands < mountains:
            main_map[ri][ci] = 3

    return main_map


def expand4x(main_map):
    new_map = [[0 for _ in range(len(main_map[0]) * 2)] for __ in range(len(main_map) * 2)]

    for ri, ci, val in iterate(main_map, include_edges=True):
        choices = [0, 0, 0, 1] if val == 0 else [1, 1, 1, 0]

        for r, c in ((ri * 2, ci * 2), (ri * 2, ci * 2 + 1), (ri * 2 + 1, ci * 2), (ri * 2 + 1, ci * 2 + 1)):
            if r == 0 or r == len(new_map) - 1:
                continue
            if c == 0 or c == len(new_map[0]) - 1:
                continue
            new_map[r][c] = random.choice(choices)

    return new_map


def generate_full_map():
    m = [[0 for _ in range(initial_length)] for __ in range(initial_length)]

    m = generate_land(m)
    m = clean(m)
    m = expand4x(m)
    m = clean(m)
    m = expand4x(m)
    m = clean(m)
    m = clean(m)

    m = generate_highland(m)
    m = clean_highland(m)

    m = generate_mountain(m)
    m = clean_mountain(m)

    color_m = color_map(m)

    return m, color_m


screen_length = 640

pygame.init()
screen = pygame.display.set_mode((screen_length, screen_length))
clock = pygame.time.Clock()

initial_length = 32
land_chance = 0.5
highland_chance = 0.45
mountain_chance = 0.4

main_map, color_m = generate_full_map()
pressed = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pygame.mouse.get_pressed()[0]:
        if not pressed:
            main_map, color_m = generate_full_map()
            pressed = True
    else:
        pressed = False

    draw(color_m)

    pygame.display.update()
    clock.tick(60)
