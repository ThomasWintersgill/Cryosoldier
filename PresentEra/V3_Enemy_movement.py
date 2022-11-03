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

# Enemy images.
jet = pygame.image.load('../images/jet-fighter.png')
jet_reversed = pygame.image.load('../images/jet_reversed.png')
    
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
        
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(150, 500)
        self.speedx = random.randrange(2,6)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.left = 1000
            self.rect.y = random.randrange(150,500)


class Enemy_Reversed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet_reversed
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(150, 500)
        self.speedx = random.randrange(2,6)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left >= 1000:
            self.rect.right = 0
            self.rect.y = random.randrange(150, 500)

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
for i in range(3):
    i = Enemy()
    all_sprites.add(i)
    enemy_sprites.add(i)

for i in range(3):
    e = Enemy_Reversed()
    all_sprites.add(e)
    enemy_sprites.add(e)



player = Player()
all_sprites.add(player)


# Game loop

running = True
while running:
    CLOCK.tick(FPS)

    pygame.display.update()
    # Update
    all_sprites.update()

    # Draw/Render
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


pygame.quit()
