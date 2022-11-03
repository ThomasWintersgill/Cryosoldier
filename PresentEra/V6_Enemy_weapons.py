import pygame
import random
import sys
from pygame import mixer

pygame.init()
# Title of the game window.
pygame.display.set_caption("Cryosoldier")

FPS = 60
CLOCK = pygame.time.Clock()
# Create the game window.
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
def play_music():
    mixer.init()
    mixer.music.load('../audio/background.mp3.mp3')
    mixer.music.play(-1)

# Set the background image.
background = pygame.image.load('../images/whitehouse.jpg')
# Load all the images for assets.
player = pygame.image.load('../images/tank.png')
jet = pygame.image.load('../images/jet-fighter.png')
jet_reversed = pygame.image.load('../images/jet_reversed.png')
missile = pygame.image.load('../images/missile.png')
enemy_missile = pygame.image.load('../images/enemy_missile.png')

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 100
        self.rect.y = random.randrange(150, 400)
        self.speedx = random.randrange(3, 8)
        self.rect.bottom = self.rect.bottom
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right <= 0:
            self.rect.left = 1000
            self.rect.y = random.randrange(150, 400)
            self.speedx = random.randrange(3, 8)

    def shoot(self):
        bullet = Enemy_bullet(self.rect.x, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullet_sprites.add(bullet)

class Enemy_Reversed(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = jet_reversed
        self.rect = self.image.get_rect()
        self.rect.x = 1100
        self.rect.y = random.randrange(150, 400)
        self.speedx = random.randrange(3, 8)
        self.rect.bottom = self.rect.bottom

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left >= 1000:
            self.rect.right = 0
            self.rect.y = random.randrange(150, 400)
            self.speedx = random.randrange(3, 8)

    def shoot(self):
        bullet = Enemy_bullet(self.rect.x, self.rect.bottom)
        all_sprites.add(bullet)
        enemy_bullet_sprites.add(bullet)

class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, enemy_x, enemy_bottom):
        pygame.sprite.Sprite. __init__(self)
        self.image = enemy_missile
        self.rect = self.image.get_rect()
        self.rect.top = enemy_bottom - 30
        self.rect.x = enemy_x
        self.speedy = +5

    def update(self):
        self.rect.y += self.speedy

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.health = 10

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = +5
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self. rect.left < 0:
            self.rect.left = 0
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y, 100, 10))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x, self.rect.y, 100 - (5 * (10 - self.health)), 10))

    def shoot(self):
        bullet = Bullet(self.rect.x, self.rect.y)
        all_sprites.add(bullet)
        player_bullet_sprites.add(bullet)

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
            img = pygame.image.load(f"../images/exp{num}.png")
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
explosion_group = pygame.sprite.Group()
player_bullet_sprites = pygame.sprite.Group()
enemy_bullet_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()

# Spawn enemies.
for i in range(3):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

for i in range(3):
    enemy = Enemy_Reversed()
    all_sprites.add(enemy)
    enemy_sprites.add(enemy)

# Spawn player.
player = Player()
all_sprites.add(player)
player_sprite.add(player)

# Game loop
running = True
while running:
    #If no music is play, commence play music function.
    if pygame.mixer.music.get_busy() == False:
        play_music()
    # Set the fps at 60.
    CLOCK.tick(FPS)
    # Draw/Render
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    explosion_group.draw(screen)
    explosion_group.update()

    # Randomise the enemy shooting.
    for enemy in enemy_sprites:
        if random.randrange(0, 4 * 60) == 1:
            enemy.shoot()

    # Check to see if the player bullets hit an enemy.
    enemy_hits = pygame.sprite.groupcollide(player_bullet_sprites, enemy_sprites,  True, True)
    for hit in enemy_hits:
        # Play the explosion animation at each hit location.
        explosion = Explosion(hit.rect.x, hit.rect.y)
        explosion_group.add(explosion)
        # Spawn a new enemy, never from the same side twice.
        count = random.randrange(0, 2)
        if count % 2 == 0:
            new_enemy = Enemy_Reversed()
        else:
            new_enemy = Enemy()
        # Add the new enemy to the sprite groups.
        all_sprites.add(new_enemy)
        enemy_sprites.add(new_enemy)

    # Check to see if the enemy bullets hit a player.
    player_hits = pygame.sprite.groupcollide(enemy_bullet_sprites, player_sprite, True, False )
    for hit in player_hits: 
        explosion = Explosion(hit.rect.x, hit.rect.y)
        explosion_group.add(explosion)
        player.health -= 5
        if player.health == -10:
           pass

    # Allow option to quit the game.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
        # Control for player shooting.
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    pygame.display.update()




