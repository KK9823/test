import pygame
import sys
import random


class Player(pygame.sprite.Sprite):
    def __init__(self, colliderects):
        super().__init__()
        self.surf = pygame.Surface((40, 40))
        self.surf.fill('green')
        self.image = self.surf
        self.rect = self.surf.get_rect(center=(lane_size * 5, lane_size * 8.5))
        self.vector = pygame.Vector2()
        self.speed = 3
        self.colliderects = colliderects

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.vector.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.vector.y = 1
        else:
            self.vector.y = 0

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vector.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vector.x = 1
        else:
            self.vector.x = 0

    def apply_boundaries(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
        elif self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0

    def horizontal_collision(self):
        self.rect.x += self.vector.x * self.speed
        for rect in self.colliderects:
            if self.rect.colliderect(rect):
                if self.vector.x == 1:
                    self.rect.right = rect.left
                if self.vector.x == -1:
                    self.rect.left = rect.right

    def vertical_collision(self):
        self.rect.y += self.vector.y * self.speed
        for rect in self.colliderects:
            if self.rect.colliderect(rect):
                if self.vector.y == 1:
                    self.rect.bottom = rect.top
                if self.vector.y == -1:
                    self.rect.top = rect.bottom

    def update(self):
        self.get_input()
        self.horizontal_collision()
        self.vertical_collision()
        self.apply_boundaries()


class car(pygame.sprite.Sprite):
    def __init__(self, y, direction, type='notinit'):
        super().__init__()
        self.surf = pygame.Surface((150, 50))
        self.surf.fill('red')
        self.image = self.surf
        self.direction = direction
        self.speed = random.randint(4, 7)
        if type == 'notinit':
            if direction == 'left':
                self.rect = self.surf.get_rect(center=(random.randint(768, 1200), y))
            else:
                self.rect = self.surf.get_rect(center=(random.randint(-496, -64), y))
        else:
            self.rect = self.surf.get_rect(center=(random.randint(0,screen_width),y))

    def move(self):
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.x < -200 and self.direction == 'left':
            self.kill()
        elif self.rect.x > screen_width+200 and self.direction == 'right':
            self.kill()

    def update(self):
        self.move()


class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill('green')
        self.image = self.surf
        self.rect = self.surf.get_rect(center=(lane_size * 5, 0))


def collision():
    return not pygame.sprite.spritecollide(player.sprite, cars, False)


def checkwin():
    return pygame.sprite.spritecollide(player.sprite, goal, False)


def draw_multiple_rects(surf, rect_list):
    for rect in rect_list:
        screen.blit(surf, rect)


def gettextsurfaces(*strngs):
    return [font1.render(strng, True, 'white') for strng in strngs]


def initialize_game():
    cars.empty()
    cars.add(car(lane_size * 1.5, 'right', 'init'))
    cars.add(car(lane_size * 2.5, 'left', 'init'))
    cars.add(car(lane_size * 3.5, 'right', 'init'))

    cars.add(car(lane_size * 5.5, 'left', 'init'))
    cars.add(car(lane_size * 6.5, 'right', 'init'))
    cars.add(car(lane_size * 7.5, 'left', 'init'))

    cars.add(car(lane_size * 1.5, 'right'))
    cars.add(car(lane_size * 2.5, 'left'))
    cars.add(car(lane_size * 3.5, 'right'))

    cars.add(car(lane_size * 5.5, 'left'))
    cars.add(car(lane_size * 6.5, 'right'))
    cars.add(car(lane_size * 7.5, 'left'))
    player.sprite.rect.center = (lane_size * 5, lane_size * 8.5)


pygame.init()

lane_size = 64
screen_width = lane_size * 10
screen_height = lane_size * 9
screen = pygame.display.set_mode((screen_width, screen_height))
font1 = pygame.font.Font('freesansbold.ttf', 50)

surf = pygame.Surface((lane_size * 4, lane_size))
surf.fill('gray')

base_rects = [
    surf.get_rect(bottomleft=(0, screen_height)),
    surf.get_rect(bottomright=(screen_width, screen_height)),
    surf.get_rect(bottomleft=(0, lane_size * 5)),
    surf.get_rect(bottomright=(screen_width, lane_size * 5)),
    surf.get_rect(topleft=(0, 0)),
    surf.get_rect(topright=(screen_width, 0))
]

player = pygame.sprite.GroupSingle()
player.add(Player(base_rects))

cars = pygame.sprite.Group()

goal = pygame.sprite.GroupSingle()
goal.add(Goal())

obstacletimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacletimer, 2000)

gamestate = 'menu'

while True:
    screen.fill('black')

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gamestate == 'playing' and event.type == obstacletimer:
            cars.add(car(lane_size * 1.5, 'right'))
            cars.add(car(lane_size * 2.5, 'left'))
            cars.add(car(lane_size * 3.5, 'right'))

            cars.add(car(lane_size * 5.5, 'left'))
            cars.add(car(lane_size * 6.5, 'right'))
            cars.add(car(lane_size * 7.5, 'left'))

    if gamestate == 'playing':
        draw_multiple_rects(surf, base_rects)

        player.draw(screen)
        player.update()

        cars.draw(screen)
        cars.update()

        goal.draw(screen)

        if not collision(): gamestate = 'lose'
        if checkwin(): gamestate = 'win'

    elif gamestate == 'lose':
        text = font1.render('You got hit by a car', True, 'white')
        textrect = text.get_rect(center=(screen_width / 2, lane_size * 4))
        screen.blit(text, textrect)

        text = font1.render('Press Space To Start', True, 'white')
        textrect = text.get_rect(center=(screen_width / 2, lane_size * 5))
        screen.blit(text, textrect)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            gamestate = 'playing'
            initialize_game()

    elif gamestate == 'win':
        texts = gettextsurfaces('You win!', 'Press space to play again')
        screen.blit(texts[0], texts[0].get_rect(center=(screen_width / 2, lane_size * 4)))
        screen.blit(texts[1], texts[1].get_rect(center=(screen_width / 2, lane_size * 5)))
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            gamestate = 'playing'
            initialize_game()

    elif gamestate == 'menu':
        text = font1.render('Press Space To Start', True, 'white')
        textrect = text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(text, textrect)

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            gamestate = 'playing'
            initialize_game()

    pygame.display.update()
    pygame.time.Clock().tick(60)
