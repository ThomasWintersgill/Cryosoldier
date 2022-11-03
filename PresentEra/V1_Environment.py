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

running = True
while running:
    CLOCK.tick(FPS)

    # Keep the background appearing on screen.
    screen.blit(background, (0, 0))
    #enemy_group.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


pygame.quit()
