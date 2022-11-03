import pygame
import random

pygame.init()
game_speed = pygame.time.Clock()

FPS = 60
W, H = 1500, 600

game_display = pygame.display.set_mode((W, H), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
bg = pygame.image.load("../images/Space_background.png")
bg1_x = 0
bg2_x = bg.get_width()
asteroid_images = ["../images/Asteroid_1.png", "../images/Asteroid_2.png", "../images/Asteroid_3.png"]
asteroids = []
player_x = 70
player_y = 300
alien_x = 1500
alien_y = random.randint(0, (H - 64))
enemies = []
MAX_VELOCITY = 4


def draw_window():
    game_display.blit(bg, (bg1_x, 0))
    game_display.blit(bg, (bg2_x, 0))


class Rock:
    def __init__(self):
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1500, random.randint(50, 550))
        self.velocity = 2

    def move(self):
        self.rect.x -= self.velocity
        if self.rect.x < 0:
            del asteroids[0]

    def draw(self):
        game_display.blit(self.image, self.rect)


class Human:
    def __init__(self):
        self.image = pygame.image.load("../images/battleship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)
        self.velocity = MAX_VELOCITY

    def draw(self):
        game_display.blit(self.image, self.rect)


class Alien:
    pass


start_ticks_asteroid = pygame.time.get_ticks()
run = True
while run:
    game_speed.tick(FPS)
    bg1_x -= 2
    bg2_x -= 2

    if bg1_x < bg.get_width() * -1:
        bg1_x = bg.get_width()

    if bg2_x < bg.get_width() * -1:
        bg2_x = bg.get_width()

    draw_window()

    asteroid = Rock()
    asteroid_timer = pygame.time.get_ticks()

    if asteroid_timer - start_ticks_asteroid > random.randint(3000, 6000):
        start_ticks_asteroid = asteroid_timer
        asteroids.append(asteroid)

    if asteroid.rect.x == 0:
        for asteroid in asteroids:
            del asteroids[0]

    for asteroid in asteroids:
        asteroid.move()

    for asteroid in asteroids:
        asteroid.draw()

    player = Human()
    player.draw()
    key_press = pygame.key.get_pressed()

    if key_press[pygame.K_UP] and player.rect.y > 0:
        player_y -= MAX_VELOCITY

    if key_press[pygame.K_DOWN] and player.rect.y < (H - 64):
        player_y += MAX_VELOCITY

    if key_press[pygame.K_LEFT] and player.rect.x > 0:
        player_x -= MAX_VELOCITY

    if key_press[pygame.K_RIGHT] and player.rect.x < (W - 64):
        player_x += MAX_VELOCITY

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
