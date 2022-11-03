
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
trees = pygame.sprite.Group()
# side for the game surface
surface_1 = pygame.image.load("../images/Grass.png")
surface_2 = pygame.image.load("../images/Grass.png")
soldier = pygame.image.load('../images/soldier_right.png')
# All sprites group to allow for easy update on game window


# Lists for the tree positions so that the trees will
# never overlap when spawned randomly
x_pos = [50, 100, 150, 200, 250, 300, 350, 400, 450,
         500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
y_pos = [40, 50, 75, 100, 125, 150, 175, 200, 225, 250,
         275, 300, 325, 350, 375, 400, 425, 450]

MAX_SPEED = 9
# Function draws the game window
def draw_screen():
    window.blit(surface_1, (0, 0))
    window.blit(surface_1, (500, 0))

sprites = pygame.sprite.Group()
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

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, pygame.Color('orange'), (4, 4), 4)
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.pos = pygame.Vector2(self.rect.center)

    def update(self, events, dt):
        self.pos += self.direction * dt
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()

# Class for the Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = soldier
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(200, 200))
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 3

    def update(self, events, dt):

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.angle += 3
        if pressed[pygame.K_d]:
            self.angle -= 3
        if pressed[pygame.K_w]:
            self.pos += self.direction * self.speed
            self.rect.center = self.pos
        if pressed[pygame.K_s]:
            self.pos -= self.direction * self.speed
            self.rect.center = self.pos
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # Boundaries
        if self.rect.left < 0:
            self.rect.left = 5
        if self.rect.right > 995:
            self.rect.right = 990
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 5

def main():
    all_sprites = pygame.sprite.Group()
    player = Player()
    sprites.add(player)


    for i in range(0, 12):
        tree = Tree()
        trees.add(tree)
        all_sprites.add(tree)

    pygame.init()
    screen = pygame.display.set_mode((1000, 500))

    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
        dt = clock.tick(60)
        draw_screen()
        trees.draw(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        sprites.draw(screen)
        sprites.update(events, dt)
        # This bit needs sorting, could definetly do with better grouping.


        if pygame.sprite.spritecollide(player, trees, False):
            pass

         # updates the game display
        pygame.display.flip()

if __name__ == '__main__':
    main()
