import pygame
import random

pygame.init()
game_speed = pygame.time.Clock()

W, H = 1500, 600
game_display = pygame.display.set_mode((W, H), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
bg = pygame.image.load("../images/Space_background.png")
bg1_x = 0
bg2_x = bg.get_width()
asteroid_images = ["../images/Asteroid_1.png", "../images/Asteroid_2.png",
                   "../images/Asteroid_3.png"]
asteroids = []
asteroid_group = pygame.sprite.Group()
start_ticks_asteroid = pygame.time.get_ticks()
player_image = ""
player_x = 70
player_y = 300
player_group = pygame.sprite.Group()
enemies = []
enemy_group = pygame.sprite.Group()
start_ticks_enemy = pygame.time.get_ticks()
up_down = (4, -4)


def draw_window():
    game_display.blit(bg, (bg1_x, 0))
    game_display.blit(bg, (bg2_x, 0))


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 2

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x < -64:
            asteroids.remove(asteroid)

    def draw(self):
        game_display.blit(self.image, self.rect)


class Human(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/battleship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)
        self.velocity = 4

    def draw(self):
        game_display.blit(self.image, self.rect)


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/space-ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 4
        self.spawn_start = pygame.time.get_ticks()
        self.spawn_timer = pygame.time.get_ticks()

    def add(self):
        if self.spawn_timer - self.spawn_start > random.randint(1000, 3000):
            enemy_group.add(enemy)
            self.spawn_start = self.spawn_timer

    def update(self):
        self.rect.x -= self.velocity

        if self.rect.x < -64:
            enemies.remove(enemy)

    def draw(self):
        game_display.blit(self.image, self.rect)


run = True
while run:
    bg1_x -= 2
    bg2_x -= 2

    if bg1_x < bg.get_width() * -1:
        bg1_x = bg.get_width()

    if bg2_x < bg.get_width() * -1:
        bg2_x = bg.get_width()

    draw_window()

    player = Human()
    player.draw()
    key_press = pygame.key.get_pressed()

    if key_press[pygame.K_UP] and player.rect.y > 0:
        player_y -= player.velocity

    if key_press[pygame.K_DOWN] and player.rect.y < (H - 64):
        player_y += player.velocity

    if key_press[pygame.K_LEFT] and player.rect.x > 0:
        player_x -= player.velocity

    if key_press[pygame.K_RIGHT] and player.rect.x < (W - 64):
        player_x += player.velocity

    enemy = Alien()
    enemy_timer = pygame.time.get_ticks()

    if enemy_timer - start_ticks_enemy > random.randint(1000, 3000):
        enemies.append(enemy)
        start_ticks_enemy = enemy_timer

    for enemy in enemies:
        enemy_group.add(enemy)
        enemy.draw()
        enemy.update()

    asteroid = Rock()
    asteroid_timer = pygame.time.get_ticks()

    if asteroid_timer - start_ticks_asteroid > random.randint(4000, 8000):
        asteroids.append(asteroid)
        start_ticks_asteroid = asteroid_timer

    for asteroid in asteroids:
        asteroid_group.add(asteroid)
        asteroid.draw()
        asteroid.update()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
