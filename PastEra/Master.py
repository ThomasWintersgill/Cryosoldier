import pygame
import random

pygame.init()

# Game window variables
WIDTH, HEIGHT = 1000, 512
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
# Image variables
surface_1 = pygame.image.load("../images/Grass.png")
surface_2 = pygame.image.load("../images/Grass.png")
soldier = pygame.image.load('../images/soldier_right.png')
enemy1 = pygame.image.load('../images/enemy.png')
# Sprite groups
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
trees = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
# Lists for the tree positions
tree_pos = [(76, 112), (576, 400), (776, 162), (476, 162), (276, 302),
            (676, 62), (876, 312), (136, 412), (270, 70)]
# Main enemy variables
enemy_list = []
start_ticks_enemy = pygame.time.get_ticks()
# These are to check against to see if the player has changed direction to
# allow to move away for obstacles
DIRECTION_LIST = [(0, -1), (0.5, -0.5), (1, 0), (0.5, 0.5), (-0, 1),
                  (-0.5, 0.5), (-1, 0), (-0.5, -0.5)]
# Scoring variables
score = 0
font = pygame.font.SysFont('comicsans', 30, True)


# Function draws the game window and score text
def draw_window():
    window.blit(surface_1, (0, 0))
    window.blit(surface_1, (500, 0))
    text = font.render('Score: ' + str(score), 1, (255, 255, 255))
    window.blit(text, (875, 10))


class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, trees)
        self.image = pygame.image.load("../images/tree.png")
        self.rect = self.image.get_rect()
        self.rect.center = tree_pos[0]
        self.pos = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)

    # Tree collisions remove bullets to block lines of fire and trees act as
    # obstacles
    @staticmethod
    def tree_collide():
        if pygame.sprite.groupcollide(trees, player_bullets, False, True):
            pass
        if pygame.sprite.groupcollide(trees, enemy_bullets, False, True):
            pass


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

    def update(self, events, velocity):
        self.pos += self.direction * velocity
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().contains(self.rect):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy1
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect()
        # Allow enemy to enter from random points outside top, right and
        # bottom of screen
        self.coords = [(random.randrange(0, 1000), 0),
                       (1000, random.randrange(0, 512)),
                       (random.randrange(0, 1000), 512)]
        self.rect.topleft = random.choice(self.coords)
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle = 0
        self.velocity = 2
        self.mask = pygame.mask.from_surface(self.image)
        self.start = start_ticks_enemy

    def update(self, player, timer):
        self.angle = (player.pos - self.pos).angle_to(pygame.Vector2(1, 0))
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.direction * self.velocity
        self.rect.center = self.pos
        self.velocity = 0.5
        # Timer for individual enemy fire
        if timer - self.start > random.randint(3000, 9000):
            enemy_bullets.add(Projectile(
                self.rect.center, self.direction.normalize()))
            self.start = timer

    def enemy_collide(self):
        global score
        # Enemies move back on collision
        collided_enemies = \
            pygame.sprite.spritecollide(self, all_sprites, False,
                                        pygame.sprite.collide_mask)
        for a in collided_enemies:
            for b in collided_enemies:
                if a != b and collided_enemies:
                    self.pos -= self.direction * self.velocity
                if not collided_enemies:
                    self.velocity = 0.5
        # Enemies removed when hit by player bullet, plus 1 to player score
        if pygame.sprite.spritecollide(self, player_bullets, True):
            self.kill()
            enemy_list.remove(self)
            enemies.remove(self)
            all_sprites.remove(self)
            score += 1


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = soldier
        self.org_image = self.image.copy()
        self.angle = 0
        self.direction = pygame.Vector2(1, 0)
        self.rect = self.image.get_rect(center=(100, 250))
        self.pos = pygame.Vector2(self.rect.center)
        self.speed = 3
        self.w = True
        self.s = True
        self.hit_direction = ""
        self.mask = pygame.mask.from_surface(self.image)
        self.offset = (0, 0)
        self.result = (0, 0)
        self.health = 10
        self.health_bar = ""

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player_bullets.add(Projectile(
                        self.rect.center, self.direction.normalize()))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.angle += self.speed
        if pressed[pygame.K_d]:
            self.angle -= self.speed
        if self.w and pressed[pygame.K_w]:
            self.pos += self.direction * self.speed
            self.rect.center = self.pos
        if self.s and pressed[pygame.K_s]:
            self.pos -= self.direction * self.speed
            self.rect.center = self.pos
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        # Displays red and green health bar, green health bar made smaller by
        # self.health leaving more of red bar showing
        self.health_bar = pygame.draw.rect(window, (255, 0, 0),
                                           (self.rect.x, self.rect.y -
                                            20, 50, 10))
        self.health_bar = pygame.draw.rect(window, (0, 150, 0),
                                           (self.rect.x, self.rect.y - 20, 50 -
                                            (5 * (10 - self.health)), 10))
        # Boundaries
        if self.rect.left < 0:
            self.rect.left = 5
        if self.rect.right > 995:
            self.rect.right = 990
        if self.rect.bottom > 500:
            self.rect.bottom = 500
        if self.rect.top < 0:
            self.rect.top = 5

    def player_collide(self):
        pressed = pygame.key.get_pressed()
        player_collide = \
            pygame.sprite.spritecollide(self, all_sprites, False,
                                        pygame.sprite.collide_mask)
        # Disables forward and back keys
        self.w = True
        self.s = True
        # Iterate through both sprites in collision to check not colliding
        # with self
        for a in player_collide:
            for b in player_collide:
                # Collision masks
                self.offset = (a.rect.x - b.rect.x, a.rect.y - b.rect.y)
                self.result = self.mask.overlap(self.mask, self.offset)
                if a != b and pressed[pygame.K_w]:
                    self.w = False
                    # Move back same amount moved forward before in collision
                    # record direction and disable key
                    if self.hit_direction in DIRECTION_LIST:
                        self.hit_direction = tuple(self.direction)
                        for _ in range(int(self.direction.length()) + 1):
                            self.pos -= self.direction.normalize()
                    # If direction changed enable key to allow to move away
                    # from obstacle
                    if self.direction != self.hit_direction and self.direction\
                            in DIRECTION_LIST:
                        self.pos += self.direction * self.speed
                        self.w = True
                # Same for backwards
                elif a != b and pressed[pygame.K_s]:
                    self.s = False
                    if self.direction in DIRECTION_LIST:
                        self.hit_direction = tuple(self.direction)
                        for _ in range(int(self.direction.length()) + 1):
                            self.pos += self.direction.normalize()
                    if self.direction != self.hit_direction and self.direction\
                            in DIRECTION_LIST:
                        self.pos -= self.direction * self.speed
                        self.s = True
        # If hit by enemy bullet and health bar not zero, shorten health bar
        if pygame.sprite.spritecollide(self, enemy_bullets, True):
            if self.health > 0:
                self.health -= 1


def main(start_timer):
    # Player spawning and add to groups
    player = Player()
    players.add(player)
    all_sprites.add(player)

    # Tree spawning and add to groups
    for i in range(0, 9):
        tree = Tree()
        tree_pos.pop(0)
        trees.add(tree)
        all_sprites.add(tree)

    # Game and bullet speed variables
    clock = pygame.time.Clock()
    bullet_speed = clock.tick(30)

    # Main game loop
    run = True
    while run:
        draw_window()

        # Tree function calls
        trees.draw(window)
        Tree.tree_collide()

        # Enemy spawning timer and function calls
        enemy = Enemy()
        enemy_timer = pygame.time.get_ticks()
        if enemy_timer - start_timer > random.randint(3000, 4000):
            enemy_list.append(enemy)
            start_timer = enemy_timer
        for enemy in enemy_list:
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy.enemy_collide()
        enemies.draw(window)
        enemy_bullets.draw(window)

        # Player die and function calls
        player.player_collide()
        if player.health == 0:
            run = False
        player_bullets.draw(window)
        players.draw(window)

        # Event handler
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                run = False

        # Sprite group updates
        enemies.update(player, enemy_timer)
        enemy_bullets.update(events, 4)
        players.update(events)
        player_bullets.update(events, bullet_speed)

        pygame.display.flip()


main(start_ticks_enemy)
