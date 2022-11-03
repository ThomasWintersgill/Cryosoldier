import pygame
import random
import math

pygame.init()
# Title of the game window.
pygame.display.set_caption("Cryosoldier")

FPS = 60
CLOCK = pygame.time.Clock()

# Create the game window.
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the background image.
background = pygame.image.load('../images/whitehouse.jpg')

# Player image.
player = pygame.image.load('../images/tank.png')

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = +5
        self.rect.x += self.speedx

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game loop

running = True
while running:
    CLOCK.tick(FPS)
    screen.blit(background, (0, 0))

    # Update
    all_sprites.draw(screen)
    all_sprites.update()

    # Draw/Render
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    pygame.display.update()

pygame.quit()
