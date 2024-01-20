import pygame
import sys
import random

pygame.init()


def copy(lst):
    return [[i for i in j] for j in lst]


def print2dArr(lst):
    for i in lst: print(i)


def check_out_of_bounds(newRowI, newColI):
    return newRowI < 0 or newRowI > 24 or newColI < 0 or newColI > 24


def get_snake_length(lst):
    max = 0
    for row in lst:
        for value in row:
            if value.isdigit() and int(value) > max:
                max = int(value)
    return max


def produce_fruit(lst):
    while True:
        row_index = random.randint(0, 24)
        col_index = random.randint(0, 24)
        if not lst[row_index][col_index].isdigit(): break
    lst[row_index][col_index] = 'F'
    return lst



def update_game(lst, input, gamestate):
    rowI, colI = get_pos(lst, '1')
    length = get_snake_length(lst)

    if input == 'up':
        newRowI, newColI = rowI - 1, colI
        if lst[newRowI][newColI] == 'F':
            length += 1
            lst = produce_fruit(lst)
        elif lst[newRowI][newColI].isdigit() or check_out_of_bounds(newRowI, newColI):
            gamestate = 'lose'
        lst[newRowI][newColI] = '1'

    elif input == 'left':
        newRowI, newColI = rowI, colI - 1
        if lst[newRowI][newColI] == 'F':
            length += 1
            lst = produce_fruit(lst)
        elif lst[newRowI][newColI].isdigit() or check_out_of_bounds(newRowI, newColI):
            gamestate = 'lose'
        lst[newRowI][newColI] = '1'

    elif input == 'down':
        newRowI, newColI = rowI + 1, colI
        if lst[newRowI][newColI] == 'F':
            length += 1
            lst = produce_fruit(lst)
        elif lst[newRowI][newColI].isdigit() or check_out_of_bounds(newRowI, newColI):
            gamestate = 'lose'
        lst[newRowI][newColI] = '1'

    else:
        newRowI, newColI = rowI, colI + 1
        if lst[newRowI][newColI] == 'F':
            length += 1
            lst = produce_fruit(lst)
        elif lst[newRowI][newColI].isdigit() or check_out_of_bounds(newRowI, newColI):
            gamestate = 'lose'
        lst[newRowI][newColI] = '1'

    for row_index, row in enumerate(lst):
        for col_index, value in enumerate(row):
            if row_index == newRowI and col_index == newColI:
                continue
            elif value.isdigit() and int(value) < length:
                lst[row_index][col_index] = str(int(value) + 1)
            elif value != 'F':
                lst[row_index][col_index] = ' '

    return lst, gamestate, length


def draw_tiles(lst):
    for row_index, row in enumerate(lst):
        for col_index, val in enumerate(row):
            if val != ' ':
                x = col_index * tile_size + 25
                y = row_index * tile_size + 25
                surf = pygame.Surface((tile_size, tile_size))

                if val == 'F':
                    surf.fill('red')

                elif val.isdigit():
                    surf.fill('grey')

                rect = surf.get_rect(center=(x, y))
                screen.blit(surf, rect)


def get_pos(lst, cell):
    for row_index, row in enumerate(lst):
        for col_index, val in enumerate(row):
            if val == cell:
                return row_index, col_index


tile_size = 32
screen_height = tile_size * 25
screen_width = tile_size * 25
screen = pygame.display.set_mode((screen_width, screen_height))
gamestate = 'Lose'
font1 = pygame.font.Font('freesansbold.ttf', 32)
length = 4
framerate = 8

direction, prev = 'right', 'right'

initial_game = [
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', '4', '3', '2', '1', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
     ' ', ' ']]

game = copy(initial_game)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_UP]:
                direction = 'up'
            elif event.key in [pygame.K_a, pygame.K_LEFT]:
                direction = 'left'
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                direction = 'down'
            elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                direction = 'right'

    screen.fill('black')

    if gamestate == 'playing':
        draw_tiles(game)

        if prev == 'left' and direction == 'right':
            direction = 'left'
        elif prev == 'right' and direction == 'left':
            direction = 'right'
        elif prev == 'up' and direction == 'down':
            direction = 'up'
        elif prev == 'down' and direction == 'up':
            direction = 'down'

        try:
            game, gamestate, length = update_game(game, direction, gamestate)
        except IndexError: gamestate = 'lose'

        prev = direction

    else:
        instructiontext = font1.render('Enter space to start playing', True, 'white')
        instructionrect = instructiontext.get_rect(center=(400, 350))
        screen.blit(instructiontext, instructionrect)

        lengthtext = font1.render('length:' + str(length), True, 'white')
        lengthrect = lengthtext.get_rect(center=(400, 450))
        screen.blit(lengthtext,lengthrect)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            gamestate = 'playing'
            direction, prev = 'right', 'right'
            game = copy(initial_game)
            game = produce_fruit(game)



    pygame.display.update()
    clock.tick(framerate)
