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
asteroid_images = ["../images/Asteroid_1.png", "../images/Asteroid_2.png",
                   "../images/Asteroid_3.png"]
asteroids = []
MAX_VELOCITY = 4


def draw_window():
    game_display.blit(bg, (bg1_x, 0))
    game_display.blit(bg, (bg2_x, 0))


class Rock:
    def __init__(self):
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1500, random.randint(100, 500))
        self.velocity = 2

    def move(self):
        self.rect.x -= self.velocity
        if self.rect.x < 0:
            del asteroids[0]

    def draw(self):
        game_display.blit(self.image, self.rect)


class Ship:
    pass


start_ticks = pygame.time.get_ticks()
run = True
while run:
    game_speed.tick(FPS)
    bg1_x -= 2
    bg2_x -= 2
    new_asteroid = Rock()
    asteroid_timer = pygame.time.get_ticks()

    if bg1_x < bg.get_width() * -1:
        bg1_x = bg.get_width()

    if bg2_x < bg.get_width() * -1:
        bg2_x = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_window()

    if asteroid_timer - start_ticks > random.randint(3000, 6000):
        start_ticks = asteroid_timer
        asteroids.append(new_asteroid)

    if new_asteroid.rect.x == 0:
        for asteroid in asteroids:
            del asteroids[0]

    for new_asteroid in asteroids:
        new_asteroid.move()

    for new_asteroid in asteroids:
        new_asteroid.draw()

    pygame.display.update()
