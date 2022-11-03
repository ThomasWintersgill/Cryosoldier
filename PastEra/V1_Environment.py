import pygame
from pygame.locals import *
import os
import sys
import random

pygame.init()
game_speed = pygame.time.Clock()

# Games speed
FPS = 30
WIDTH, HEIGHT = 1000, 512

# Game window and caption
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")

# Two of the same images displayed side by
# side for the game surface
surface_1 = pygame.image.load("../images/Grass.png")
surface_2 = pygame.image.load("../images/Grass.png")

# Sprite group trees
trees = pygame.sprite.Group()

# Lists for the tree positions so that the trees will
# never overlap when spawned randomly
x_pos = [50, 100, 150, 200, 250, 300, 350, 400, 450,
         500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
y_pos = [40, 50, 75, 100, 125, 150, 175, 200, 225, 250,
         275, 300, 325, 350, 375, 400, 425, 450]


# Function draws the game window
def draw_window():
    window.blit(surface_1, (0, 0))
    window.blit(surface_1, (500, 0))


# Class for the trees, individual tree is instance of a sprite
# in the sprite group trees
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        # Initialise sprite
        pygame.sprite.Sprite.__init__(self, trees)
        # Randomly chooses an x position from x_pos list
        self.x = random.choice(x_pos)
        # removes the position so it cant be chosen again
        if self.x in x_pos:
            x_pos.remove(self.x)
        # Randomly chooses y position
        self.y = random.choice(y_pos)
        # removes it from the list
        if self.y in y_pos:
            y_pos.remove(self.y)
        # loads the tree image from the directory
        self.image = pygame.image.load("../images/tree.png")
        # creates rect from the image to automatically get the size
        self.rect = self.image.get_rect()
        # places the rect in the x and y positions
        self.rect.center = (self.x, self.y)


# Class for the soldiers, used for the attributes of player and enemies
class Soldier:
    pass


# for loop to add all of the tree sprites to the trees sprite group
for i in range(0, 12):
    tree = Tree()
    trees.add(tree)

# main game loop
run = True
while run:
    # game speed set to the FPS variable
    game_speed.tick(FPS)

    # event handler for quitting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

    # function call to draw the game window
    draw_window()

    # function call to draw the entire tree sprite group at the same time
    trees.draw(window)

    # updates the game display
    pygame.display.flip()
