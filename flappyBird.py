import pygame
from sys import exit
from random import randint


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=(200, 300))
        self.gravity = 0
        self.state = 'fall'

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.state == 'fall':
                self.gravity = -10
                self.state = 'jump'
        else:
            self.state = 'fall'

    def apply_gravity(self):
        self.gravity += 0.7
        self.rect.y += self.gravity

    def update(self):
        self.get_input()
        self.apply_gravity()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y):
        super().__init__()
        self.pipe_end = pygame.Surface((100, 50))
        self.pipe_end.fill('green')
        self.pipe_body = pygame.Surface((75, 600))
        self.pipe_body.fill('green ')
        self.pipe_end_rects = [
            self.pipe_end.get_rect(midbottom=(1100, y - 75)),
            self.pipe_end.get_rect(midtop=(1100, y + 75))
        ]
        self.pipe_body_rects = [
            self.pipe_body.get_rect(midbottom=(1100, y - 125)),
            self.pipe_body.get_rect(midtop=(1100, y + 125))
        ]

        self.passed = False

    def draw(self):
        for rect in self.pipe_end_rects:
            screen.blit(self.pipe_end, rect)
        for rect in self.pipe_body_rects:
            screen.blit(self.pipe_body, rect)

    def move(self):
        self.pipe_end_rects[0].x -= 5
        self.pipe_end_rects[1].x -= 5
        self.pipe_body_rects[0].x -= 5
        self.pipe_body_rects[1].x -= 5

        if self.pipe_end_rects[0].x <= -100:
            self.kill()

    def detect(self):
        if self.pipe_body_rects[0].x < 100:
            self.passed = True
            global score
            score += 1

    def update(self):
        self.draw()
        self.move()
        if not self.passed:
            self.detect()


def draw_base():
    for rect in base_rects:
        screen.blit(base_surf, rect)


def collision():
    global gamestate
    for rect in base_rects:
        if rect.colliderect(player.sprite.rect):
            gamestate = 'lose'
    for pipe in obstacle.sprites():
        for rect in pipe.pipe_end_rects:
            if rect.colliderect(player.sprite.rect):
                gamestate = 'lose'
        for rect in pipe.pipe_body_rects:
            if rect.colliderect(player.sprite.rect):
                gamestate = 'lose'


pygame.init()

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
gamestate = 'lose'
font = pygame.font.Font('freesansbold.ttf', 64)
font2 = pygame.font.Font('freesansbold.ttf', 32)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.Group()

base_surf = pygame.Surface((1000, 50))
base_surf.fill('gray')
base_rects = [
    base_surf.get_rect(topleft=(0, 0)),
    base_surf.get_rect(bottomleft=(0, 600))
]

obstacletimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacletimer, 1400)

score = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == obstacletimer and gamestate == 'playing':
            obstacle.add(Obstacle(randint(150, 450)))

    screen.fill('black')
    if gamestate == 'lose':
        text = font.render('Flappy Bird', True, 'white')
        rect = text.get_rect(center=(500, 200))
        screen.blit(text, rect)

        text = font2.render('Press Space To Start Playing', True, 'white')
        rect = text.get_rect(center=(500, 300))
        screen.blit(text, rect)

        text = font2.render(f"Score:{score}", True, 'white')
        rect = text.get_rect(center=(500, 400))
        screen.blit(text, rect)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            gamestate = 'playing'
            player.sprite.rect.center = (300, 300)
            obstacle.empty()
            score = 0

    if gamestate == 'playing':
        player.draw(screen)
        player.update()
        obstacle.update()

        draw_base()

        collision()

        text = font2.render(f"Score:{score}", True, 'white')
        rect = text.get_rect(topleft=(10, 10))
        screen.blit(text, rect)

    pygame.display.update()
    clock.tick(60)
