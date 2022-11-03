import sys
import pygame
import random


pygame.init()
pygame.mixer.init()
game_time = pygame.time.Clock()
reload = False

WIDTH, HEIGHT = 1500, 600
game_display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
background = pygame.image.load("../images/Space_background.png")

cryo_colour = (159, 192, 226)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
MAX_VELOCITY = 4
up_down = (MAX_VELOCITY, -MAX_VELOCITY)

asteroids = []
asteroid_images = ["../images/Asteroid_1.png",
                   "../images/Asteroid_2.png",
                   "../images/Asteroid_3.png"]
player_lives = 5
player_score = 0
enemies = []

asteroid_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_lasers = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()
enemy_shot_start = pygame.time.get_ticks()


intro_font = pygame.font.SysFont("freesansbold. ttf", 80)
score_font = pygame.font.SysFont("freesansbold. ttf", 20)
game_over_font = pygame.font.SysFont("freesansbold. ttf", 80)
final_score_font = pygame.font.SysFont("freesansbold. ttf", 50)
play_again_font = pygame.font.SysFont("freesansbold. ttf", 50)
quit_font = pygame.font.SysFont("freesansbold. ttf", 50)
pygame.mixer.music.load("../audio/space_audio.wav")
explosion_audio = pygame.mixer.Sound("../audio/explosion.wav.wav")
player_laser_audio = pygame.mixer.Sound("../audio/laser.wav")
enemy_laser_audio = pygame.mixer.Sound("../audio/enemy_laser.wav")


def intro():
    start = pygame.time.get_ticks()

    show_intro = True
    while show_intro:
        timer = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        text_surface = intro_font.render("Future Soldier", True,
                                         cryo_colour)
        game_display.blit(background, (0, 0))
        game_display.blit(text_surface, (WIDTH - 950, HEIGHT - 340))
        pygame.display.update()
        if timer - start > 3000:
            show_intro = False
            start = timer


def game_over(player):
    show_game_over = True
    while show_game_over:
        events = pygame.event.get()
        key_press = pygame.key.get_pressed()
        game_over_surface = game_over_font.render("GAME OVER!", True,
                                             cryo_colour)
        score_surface = \
            final_score_font.render("Final Score: " + str(player.score),
                                    True, cryo_colour)
        quit_surface = quit_font.render("Quit", True, red)
        play_surface = play_again_font.render("Play", True, green)
        game_display.blit(background, (0, 0))
        game_display.blit(game_over_surface, (WIDTH - 950, HEIGHT - 440))
        game_display.blit(score_surface, (WIDTH - 890, HEIGHT - 340))
        pygame.draw.rect(game_display, cryo_colour,
                         (WIDTH - 710, HEIGHT - 240, 73, 35))
        pygame.draw.rect(game_display, cryo_colour,
                         (WIDTH - 910, HEIGHT - 240, 73, 35))
        game_display.blit(quit_surface, (WIDTH - 710, HEIGHT - 240))
        game_display.blit(play_surface, (WIDTH - 910, HEIGHT - 240))
        mouse = pygame.mouse.get_pos()
        pygame.display.update()
        for i in events:
            if i.type == pygame.QUIT or \
                    key_press[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            elif i.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH - 710 <= mouse[0] <= WIDTH - 637 and \
                        HEIGHT - 240 <= mouse[1] <= HEIGHT - 205:
                    pygame.quit()
                    sys.exit()
                elif WIDTH - 910 <= mouse[0] <= WIDTH - 837 and \
                        HEIGHT - 240 <= mouse[1] <= HEIGHT - 205:
                    reload(sys.modules[V8_Scoring_and_lives])




class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.choice = random.choice(asteroid_images)
        self.image = pygame.image.load(self.choice)
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 0

    def update(self, asteroid, game_speed):
        self.velocity = game_speed
        self.rect.x -= self.velocity
        if self.rect.x == 0:
            self.velocity = self.velocity * 2
        if self.rect.x < -64:
            asteroids.remove(asteroid)

    def draw(self):
        game_display.blit(self.image, self.rect)


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, direction, laser_colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 5)).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = direction
        self.colour = laser_colour
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, game_speed):
        pygame.draw.rect(game_display, pygame.Color(self.colour), self.rect)
        if self.direction == "right":
            self.rect.x += game_speed + 8
        else:
            self.rect.x -= game_speed + 8
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()


class Human(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/battleship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width , HEIGHT / 2)
        self.score = 0
        self.respawn = 0
        self.dead = 0
        self.lives = 0
        self.player_enemy = False

    def update(self, key):
        if key[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= MAX_VELOCITY
        if key[pygame.K_DOWN] and self.rect.y < (HEIGHT - 64):
            self.rect.y += MAX_VELOCITY
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= MAX_VELOCITY
        if key[pygame.K_RIGHT] and self.rect.x < (WIDTH - 64):
            self.rect.x += MAX_VELOCITY

    def player_collide(self, player, hit_timer):
        global player_lives

        player_asteroid = \
            pygame.sprite.spritecollide(player, asteroid_group, True,

                                        pygame.sprite.collide_mask)
        self.player_enemy = pygame.sprite.spritecollide(player, enemy_group, True,
                                                   pygame.sprite.collide_mask)
        player_hit = pygame.sprite.spritecollide(player, enemy_lasers, True,
                                                 pygame.sprite.collide_mask)

        self.dead = self.respawn > 0
        if self.dead:
            pygame.mixer.Sound.play(explosion_audio)
            self.image = pygame.image.load("../images/explosion.png")
            game_display.blit(self.image, self.rect)
            self.respawn -= hit_timer
        if self.respawn < 0:
            self.respawn = 0

        if not self.dead and player_asteroid or self.player_enemy or player_hit:
                player_lives -= 1
                self.respawn = 1500

        elif not self.dead:
            self.image = pygame.image.load("../images/battleship.png")
            game_display.blit(self.image, self.rect)

        if pygame.sprite.groupcollide(player_lasers, asteroid_group,
                                      True, False):
            pass

    def shoot(self, events):
        for i in events:
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE and not self.dead:
                    pygame.mixer.Sound.play(player_laser_audio, loops=0)
                    player_lasers.add(Laser(self.rect.midright, "right", "blue"))


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/space-ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (1600, random.randint(30, 530))
        self.velocity = 0
        self.dodge = random.choice(up_down)
        self.timeout = 0
        self.splat = 0
        self.dead = 0
        self.start = enemy_shot_start

    def update(self, game_speed):
        self.velocity = game_speed
        self.rect.x -= self.velocity + 1

        if self.rect.x == 0:
            self.rect.x -= self.velocity * 2
        if self.rect.x < -64:
            self.kill()
            enemies.remove(self)

    def enemy_collide(self, timer, kill_timer, player):
        collide_asteroid = \
            pygame.sprite.groupcollide(enemy_group, asteroid_group,
                                       True, True, pygame.sprite.collide_mask)
        disabled = self.timeout > 0

        if disabled:
            self.timeout -= timer
            self.rect.x += self.velocity + 1
            self.rect.y += self.dodge
        if self.timeout < 0:
            self.timeout = 0
        if not disabled:
            if collide_asteroid:
                self.rect.x += self.velocity + 1
                self.rect.y += self.dodge
            if self.rect.y < 0:
                self.dodge = self.velocity + 1
                self.timeout = 671
            elif self.rect.y > 530:
                self.dodge = -self.velocity + 1
                self.timeout = 671

        if pygame.sprite.groupcollide(enemy_lasers, asteroid_group, True,
                                      False):
            pass

        enemy_hit = \
            pygame.sprite.groupcollide(enemy_group, player_lasers, True, True,
                                       pygame.sprite.collide_mask)
        print(self.splat)
        self.dead = self.splat > 0
        if self.dead:
            self.splat -= kill_timer
        if self.splat == 2 or player.player_enemy:
            self.kill()
            enemies.remove(self)
        elif self.splat < 0:
            self.splat = 0

        if not self.dead:
            if enemy_hit:
                pygame.mixer.Sound.play(explosion_audio)
                self.image = pygame.image.load("../images/explosion.png")
                player.score += 1
                self.splat = 10

        enemy_enemy = \
            pygame.sprite.groupcollide(enemy_group, enemy_lasers, False, False,
                                       pygame.sprite.collide_mask)
        for a in enemy_enemy:
            for b in enemy_enemy:
                if a != b and enemy_enemy:
                    pygame.sprite.groupcollide(enemy_group, enemy_lasers,
                                               False, True)
    def enemy_shoot(self, shot_timer):
        if shot_timer - self.start > random.randint(4000, 8000) and not self.dead:
            pygame.mixer.Sound.play(enemy_laser_audio)
            enemy_lasers.add(Laser(self.rect.topleft, "left", "red"))
            enemy_lasers.add(Laser(self.rect.bottomleft, "left", "red"))
            self.start = shot_timer

    def draw(self):
        game_display.blit(self.image, self.rect)



def main(background, enemies):
    start = pygame.time.get_ticks()
    bg1_x = 0
    bg2_x = background.get_width()
    asteroid_start = pygame.time.get_ticks()
    enemy_start = pygame.time.get_ticks()
    asteroid_spawner = 6000
    enemy_spawner = 5000
    player = Human()
    game_speed = 1

    run = True
    while run:
        events = pygame.event.get()
        key_press = pygame.key.get_pressed()
        game_timer = pygame.time.get_ticks()

        asteroid = Rock()
        enemy = Alien()

        asteroid_timer = pygame.time.get_ticks()
        if asteroid_timer - asteroid_start > asteroid_spawner:
            asteroids.append(asteroid)
            asteroid_start = asteroid_timer
        for asteroid in asteroids:
            asteroid_group.add(asteroid)
            asteroid.draw()
            asteroid.update(asteroid, game_speed)

        player_hit_timer = game_time.tick()
        player.update(key_press)
        player.shoot(events)
        player.player_collide(player, player_hit_timer)
        player_lasers.draw(game_display)
        player_lasers.update(game_speed)

        enemy_timer = pygame.time.get_ticks()
        enemy_hit_timer = game_time.tick()
        enemy_shot_timer = pygame.time.get_ticks()
        enemy_disable = game_time.tick()
        if enemy_timer - enemy_start > enemy_spawner:
            enemies.append(enemy)
            enemy_start = enemy_timer
        for enemy in enemies:
            enemy_group.add(enemy)
            enemy.draw()
            enemy.update(game_speed)
            enemy.enemy_collide(enemy_disable, enemy_hit_timer, player)
            enemy.enemy_shoot(enemy_shot_timer)
        enemy_lasers.draw(game_display)
        enemy_lasers.update(game_speed)
        pygame.display.update()

        game_display.blit(background, (bg1_x, 0))
        game_display.blit(background, (bg2_x, 0))
        score_surface = score_font.render("Score: " + str(player.score), True,
                                          (159, 192, 226))
        game_display.blit(score_surface, (WIDTH - 100, 20))
        spacing = 30
        for i in range(0, player_lives):
            game_display.blit(pygame.image.load("../images/hospital.png"),
                              ((WIDTH / 2) + spacing, 20))
            spacing += 20
        bg1_x -= game_speed
        bg2_x -= game_speed
        if game_timer - start > 10000:
            game_speed = game_speed + 1
            if enemy_spawner > 1000:
                enemy_spawner = enemy_spawner - 500
            if asteroid_spawner > 1000:
                asteroid_spawner = asteroid_spawner - 100
            start = game_timer

        if bg1_x < background.get_width() * -1:
            bg1_x = background.get_width()
        if bg2_x < background.get_width() * -1:
            bg2_x = background.get_width()

        for i in events:
            if i.type == pygame.QUIT or key_press[pygame.K_ESCAPE]:
                run = False
        if player_lives == 5:
            run = False
            game_over(player)

#pygame.mixer.music.play(loops=-1)
#intro(intro_start)
main(background, enemies)