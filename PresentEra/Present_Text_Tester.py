import pygame
import random
import math

pygame.init()
# Title of the game window.
pygame.display.set_caption("Cryosoldier")

FPS = 60
CLOCK = pygame.time.Clock()

# Create the game window.
WIDTH, HEIGHT = 1000, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set the background image.
background = pygame.image.load('images/whitehouse.jpg')
player = pygame.image.load('images/tank.png')
jet = pygame.image.load('images/jet-fighter.png')
jet_reversed = pygame.image.load('images/jet_reversed.png')

missile = pygame.image.load('images/missile.png')


# Military Base Image.
armybase = pygame.image.load('images/base.png')
armybasex = (100)
armybasey = (850)

# Medical centre image
medicalcentre = pygame.image.load('images/medical.png')
medicalcentrex = (800)
medicalcentrey = (883)


def show_medicalcentre(x, y):
    screen.blit(medicalcentre, (x, y))

def show_armybase(x, y):
    screen.blit(armybase, (x, y))

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = random.randrange(150, 600)
        self.speedx = random.randrange(3,8)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.left = 1000
            self.rect.y = random.randrange(150, 600)
            self.speedx = random.randrange(3, 8)

class Enemy_Reversed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet_reversed
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = random.randrange(150, 600)
        self.speedx = random.randrange(3, 8)

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left >= 1000:
            self.rect.right = 0
            self.rect.y = random.randrange(150, 600)
            self.speedx = random.randrange(3, 8)

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
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self. rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = missile
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# Sprite groups
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()

explosion_group = pygame.sprite.Group()

for i in range(3):
    i = Enemy()
    all_sprites.add(i)
    enemy_sprites.add(i)

for i in range(3):
    e = Enemy_Reversed()
    all_sprites.add(e)
    enemy_sprites.add(e)

# Game loop

running = True
while running:
    CLOCK.tick(FPS)

    pygame.display.update()
    # Update
    all_sprites.update()

    # Draw/Render
    screen.blit(background, (0, 0))
    show_armybase(armybasex, armybasey)
    show_medicalcentre(medicalcentrex, medicalcentrey)
    all_sprites.draw(screen)
    explosion_group.draw(screen)
    explosion_group.update()


    hits = pygame.sprite.groupcollide(bullets, enemy_sprites, True, True)
    for hit in hits:
        explosion = Explosion(hit.rect.x, hit.rect.y)
        explosion_group.add(explosion)
        count = random.randrange(0,2)
        if count % 2 == 0:
            e = Enemy_Reversed()
        else:
            e = Enemy()
        all_sprites.add(e)
        enemy_sprites.add(e)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()




