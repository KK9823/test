import pygame
from sys import exit
from random import randint, choice, uniform
import math


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.og_img = pygame.image.load('spaceship.png')
        self.image = self.og_img
        self.rect = self.image.get_rect(center=(400, 500))
        self.degree = 0

        self.vector = pygame.math.Vector2()
        self.speed = 5

        self.types = ['normal', 'shotgun', 'machinegun','sniper']

        self.normal_cooldown = 0
        self.normal_maxcooldown = 5
        self.sniper_cooldown = 0
        self.sniper_maxcooldown = 30
        self.shotgun_cooldown = 0
        self.shotgun_maxcooldown = 30
        self.n_bullets = 30
        self.type = 0

        self.f_pressed = False

    def rotate(self):
        self.degree = get_degree(self.rect.centerx, self.rect.centery, mouse_pos[0], mouse_pos[1])
        self.image = pygame.transform.rotate(self.og_img, self.degree)
        self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_w] or k[pygame.K_UP]:
            self.vector.y = -1
        elif k[pygame.K_s] or k[pygame.K_DOWN]:
            self.vector.y = 1
        else:
            self.vector.y = 0

        if k[pygame.K_a] or k[pygame.K_LEFT]:
            self.vector.x = -1
        elif k[pygame.K_d] or k[pygame.K_RIGHT]:
            self.vector.x = 1
        else:
            self.vector.x = 0

        if self.types[self.type] == 'normal':
            if k[pygame.K_SPACE]:
                if self.normal_cooldown <= 0:
                    bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.degree, 5))
                    self.normal_cooldown = self.normal_maxcooldown
            self.normal_cooldown -= 1

        elif self.types[self.type] == 'shotgun':
            if k[pygame.K_SPACE]:
                if self.shotgun_cooldown <= 0:
                    for i in range(self.n_bullets):
                        bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.degree, 20))
                    self.shotgun_cooldown = self.shotgun_maxcooldown
            self.shotgun_cooldown -= 1

        elif self.types[self.type] == 'machinegun':
            if k[pygame.K_SPACE]:
                bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.degree, 5))

        elif self.types[self.type] == 'sniper':
            if k[pygame.K_SPACE]:
                if self.sniper_cooldown <= 0:
                    bullets.add(Bullet(self.rect.centerx, self.rect.centery, self.degree, 0, speed = 20))
                    self.sniper_cooldown = self.sniper_maxcooldown
            self.sniper_cooldown -= 1

        if k[pygame.K_f]:
            if not self.f_pressed:
                self.type += 1
                if self.type > len(self.types) - 1:
                    self.type = 0
                self.f_pressed = True
        else:
            self.f_pressed = False

    def move(self):
        self.rect.x += self.vector.x * self.speed
        self.rect.y += self.vector.y * self.speed

    def display_type(self):
        display_text(type=self.types[self.type])

    def update(self):
        self.rotate()
        self.get_input()
        self.move()
        self.display_type()



class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, degree, spread, speed = 8):
        super().__init__()
        self.image = pygame.image.load('bullet.png')
        self.image = pygame.transform.rotate(self.image, degree)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = speed
        degree = (degree + 90 + uniform(-spread, spread)) * math.pi / 180
        self.vx = self.speed * math.cos(-degree)
        self.vy = self.speed * math.sin(-degree)

        self.rect.x += self.vx * 5
        self.rect.y += self.vy * 5

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top >= 600 or self.rect.bottom <= 0:
            self.kill()
        if self.rect.left >= 800 or self.rect.right <= 0:
            self.kill()

    def update(self):
        self.move()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('icon.png')
        x = randint(0, 800)
        y = randint(50, 200)
        self.rect = self.image.get_rect(center=(x, y))
        self.vector = pygame.math.Vector2()
        self.vector.x = choice([-1, 1])
        self.speed = 3
        self.movedown = 30

    def move(self):
        self.rect.x += self.vector.x * self.speed
        if self.rect.left <= 0:
            self.rect.y += self.movedown
            self.vector.x = 1
        elif self.rect.right >= 800:
            self.rect.y += self.movedown
            self.vector.x = -1

    def collision(self):
        for sprite in bullets.sprites():
            if sprite.rect.colliderect(self.rect):
                self.kill()
                sprite.kill()
                deathsound.play()

    def update(self):
        self.move()
        self.collision()


def get_degree(x1, y1, x2, y2):
    xdiff = abs(x1 - x2)
    ydiff = abs(y1 - y2)

    if xdiff == 0:
        if y2 < y1:
            return 0
        else:
            return 180
    if ydiff == 0:
        if x2 < x1:
            return 90
        else:
            return 270

    degree = math.atan(ydiff / xdiff)
    degree = degree * 180 / math.pi

    if x2 > x1 and y2 < y1:
        return degree + 270
    elif x2 < x1 and y2 < y1:
        return -degree + 90
    elif x2 < x1 and y2 > y1:
        return degree + 90
    else:
        return -degree + 270

def display_text(**kwargs):
    x = 10
    y = 10
    for i in kwargs:
        text = font.render(f"{i} : {kwargs[i]}", True, 'white')
        rect = text.get_rect(topleft=(x, y))
        screen.blit(text, rect)
        y += 42

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
bg = pygame.image.load('background.png')
font = pygame.font.Font('freesansbold.ttf',32)

bgmusic = pygame.mixer.Sound('background.wav')
bgmusic.play(-1)

deathsound = pygame.mixer.Sound('explosion.wav')

player = pygame.sprite.GroupSingle()
player.add(Player())

bullets = pygame.sprite.Group()

enemies = pygame.sprite.Group()
enemy_number = 100
for _ in range(enemy_number):
    enemies.add(Enemy())

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg, (0, 0))

    mouse_pos = pygame.mouse.get_pos()

    player.draw(screen)
    player.update()

    bullets.draw(screen)
    bullets.update()

    enemies.draw(screen)
    enemies.update()

    #enemy limit
    while len(enemies) < enemy_number:
        enemies.add(Enemy())

    pygame.display.update()
    clock.tick(60)
