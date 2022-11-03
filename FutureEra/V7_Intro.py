import pygame
import random


pygame.init()
game_speed = pygame.time.Clock()

WIDTH, HEIGHT = 1500, 600
game_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
background = pygame.image.load("../images/Space_background.png")
bg1_x = 0
bg2_x = background.get_width()
intro_start = pygame.time.get_ticks()
asteroid_images = ["../images/Asteroid_1.png", "../images/Asteroid_2.png",
                   "../images/Asteroid_3.png"]
asteroids = []
asteroid_group = pygame.sprite.Group()
start_ticks_asteroid = pygame.time.get_ticks()
player_x = 70
player_y = 300
player_group = pygame.sprite.Group()
player_lasers = pygame.sprite.Group()
player_lives = 5
player_start = pygame.time.get_ticks()
enemies = []
enemy_group = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
start_ticks_enemy = pygame.time.get_ticks()
all_sprites = pygame.sprite.Group()
up_down = (4, -4)
MAX_VELOCITY = 4
intro_font = pygame.font.SysFont('freesansbold. ttf', 80)


def intro(start):
    show_intro = True
    while show_intro:
        timer = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        textsurface = intro_font.render("Future Soldier", True, (255, 255,
                                                                 255))
        game_display.blit(background, (0, 0))
        game_display.blit(textsurface, (WIDTH - 950, HEIGHT - 340))
        pygame.display.update()
        if timer - start > 3000:
            show_intro = False
            start = timer


def draw_window():
    game_display.blit(background, (bg1_x, 0))
    game_display.blit(background, (bg2_x, 0))


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = MAX_VELOCITY / 2

    def update(self):
        self.rect.x -= self.velocity
        if self.rect.x < -64:
            asteroids.remove(asteroid)

    def draw(self):
        game_display.blit(self.image, self.rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, laser_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos[0]
        self.direction = direction
        self.colour = laser_colour

    def update(self):
        pygame.draw.rect(game_display, pygame.Color(self.colour), self.rect)
        if self.direction == "right":
            self.rect.x += 8
        else:
            self.rect.x -= 8
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()


class Human(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/battleship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)
        self.colour = (0, 0, 255)
        self.start = player_start

    def player_collide(self):
        global player_lives

        if pygame.sprite.spritecollide(player, asteroid_group, True):
            self.image = pygame.image.load("../images/explosion.png")
            game_display.blit(self.image, self.rect)
            player_lives -= 1
        elif pygame.sprite.spritecollide(player, enemy_group, True):
            self.image = pygame.image.load("../images/explosion.png")
            game_display.blit(self.image, self.rect)
            player_lives -= 1
        else:
            self.image = pygame.image.load("../images/battleship.png")
            game_display.blit(self.image, self.rect)

        if pygame.sprite.groupcollide(player_lasers, asteroid_group, True,
                                      False):
            pass

        if pygame.sprite.spritecollide(player, enemy_lasers, True):
            self.image = pygame.image.load("../images/explosion.png")
            player_lives -= 1

    def player_shoot(self):
        player_lasers.add(Laser(self.rect.midright, "right", "blue"))


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/space-ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = MAX_VELOCITY
        self.dodge = random.choice(up_down)
        self.timeout = 0
        self.start = start_ticks_enemy

    def update(self):
        self.rect.x -= self.velocity

        if self.rect.x < -64:
            enemies.remove(enemy)

    def enemy_collide(self, timer):
        collide_asteroid = pygame.sprite.groupcollide(asteroid_group,
                                                      enemy_group, True, True)
        disabled = self.timeout > 0

        if disabled:
            self.timeout -= timer
            self.rect.x += 2
            self.rect.y += self.dodge

        if self.timeout < 0:
            self.timeout = 0

        if not disabled:
            if collide_asteroid:
                self.rect.x += 2
                self.rect.y += self.dodge

            if self.rect.y < 0:
                self.dodge = 4
                self.timeout = 671
            elif self.rect.y > 530:
                self.dodge = -4
                self.timeout = 671

        if pygame.sprite.collide_rect(enemy, player):
            self.image = pygame.image.load("../images/explosion.png")

        if pygame.sprite.groupcollide(enemy_lasers, asteroid_group, True,
                                      False):
            pass

        if pygame.sprite.groupcollide(enemy_group, player_lasers, True, True):
            self.image = pygame.image.load("../images/explosion.png")
            enemy.kill()
            enemies.remove(enemy)

        enemy_enemy = pygame.sprite.groupcollide(enemy_group, enemy_lasers,
                                                 False, False)

        for a in enemy_enemy:
            for b in enemy_enemy:
                if a != b and enemy_enemy:
                    pygame.sprite.groupcollide(enemy_group, enemy_lasers,
                                               False, True)

    def enemy_shoot(self, shot_timer):
        if shot_timer - self.start > random.randint(4000, 8000):
            enemy_lasers.add(Laser(self.rect.topleft, "left", "red"))
            enemy_lasers.add(Laser(self.rect.bottomleft, "left", "red"))
            self.start = shot_timer

    def draw(self):
        game_display.blit(self.image, self.rect)


#intro(intro_start)

delta_time = 0
run = True
while run:
    print(player_lives)
    events = pygame.event.get()

    bg1_x -= 2
    bg2_x -= 2

    if bg1_x < background.get_width() * -1:
        bg1_x = background.get_width()

    if bg2_x < background.get_width() * -1:
        bg2_x = background.get_width()

    draw_window()

    asteroid = Rock()
    asteroid_timer = pygame.time.get_ticks()

    if asteroid_timer - start_ticks_asteroid > random.randint(4000, 8000):
        asteroids.append(asteroid)
        start_ticks_asteroid = asteroid_timer

    for asteroid in asteroids:
        asteroid_group.add(asteroid)
        asteroid.draw()
        asteroid.update()

    player = Human()
    player_timer = pygame.time.get_ticks()
    key_press = pygame.key.get_pressed()

    if key_press[pygame.K_UP] and player.rect.y > 0:
        player_y -= MAX_VELOCITY

    if key_press[pygame.K_DOWN] and player.rect.y < (HEIGHT - 64):
        player_y += MAX_VELOCITY

    if key_press[pygame.K_LEFT] and player.rect.x > 0:
        player_x -= MAX_VELOCITY

    if key_press[pygame.K_RIGHT] and player.rect.x < (WIDTH - 64):
        player_x += MAX_VELOCITY

    if key_press[pygame.K_SPACE] and player_timer - player_start > 1000:
        player.player_shoot()
        player_start = player_timer

    player.player_collide()
    player_lasers.draw(game_display)
    player_lasers.update()

    enemy = Alien()
    enemy_timer = pygame.time.get_ticks()
    enemy_shot_timer = pygame.time.get_ticks()

    if enemy_timer - start_ticks_enemy > random.randint(1000, 3000):
        enemies.append(enemy)
        start_ticks_enemy = enemy_timer

    for enemy in enemies:
        enemy_group.add(enemy)
        enemy.draw()
        enemy.update()
        enemy.enemy_collide(delta_time)
        enemy.enemy_shoot(enemy_shot_timer)

    enemy_lasers.draw(game_display)
    enemy_lasers.update()

    delta_time = game_speed.tick()
    pygame.display.update()

    for i in events:
        if i.type == pygame.QUIT or key_press[pygame.K_ESCAPE]:
            run = False
    if player_lives == 0:
        run = False
