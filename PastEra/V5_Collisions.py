import pygame
import random

pygame.init()
game_speed = pygame.time.Clock()

# Games speed
FPS = 60
WIDTH, HEIGHT = 1024, 768
TILESIZE = 32
# Game window and caption
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
# Two of the same images displayed side by
# side for the game surface
surface_1 = pygame.image.load("../images/Grass.png")
surface_2 = pygame.image.load("../images/Grass.png")
soldier = pygame.image.load('../images/soldier_right.png')
enemy1 = pygame.image.load('../images/enemy.png')
# All sprites group to allow for easy update on game window
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
sprites = pygame.sprite.Group()
enemy_buffers = pygame.sprite.Group()
player_buffers = pygame.sprite.Group()
trees = pygame.sprite.Group()
# Lists for the tree positions
tree_pos = [(76, 112), (576, 400), (776, 162), (476, 162), (276, 302),
            (676, 62), (876, 312), (136, 412), (270, 70)]
enemy_coords = [(random.randrange(0, 1000), 0),
                (1000, random.randrange(0, 512)),
                (random.randrange(0, 1000), 512)]
enemy_list = []
start_ticks_enemy = pygame.time.get_ticks()
MAX_SPEED = 9
DIRECTION_LIST = [(0, -1), (0.5, -0.5), (1, 0), (0.5, 0.5), (-0, 1),
                  (-0.5, 0.5), (-1, 0), (-0.5, -0.5)]


def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(window, (255, 255, 255), (x, 0), (x, HEIGHT))
    for y in range(0, WIDTH, TILESIZE):
        pygame.draw.line(window, (255, 255, 255), (0, y), (WIDTH, y))


# Function draws the game window
def draw_screen():
    window.blit(surface_1, (0, 0))
    window.blit(surface_1, (500, 0))


# Class for the trees, individual tree is instance of a sprite
# in the sprite group trees
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        # Initialise sprite
        pygame.sprite.Sprite.__init__(self, trees)
        # loads the tree image from the directory
        self.image = pygame.image.load("../images/tree.png")
        # creates rect from the image to automatically get the size
        self.rect = self.image.get_rect()
        # places the rect in the x and y positions
        self.rect.center = tree_pos[0]
        self.pos = self.rect.center
        self.mask = pygame.mask.from_surface(self.image)


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


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy1
        self.org_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = random.choice(enemy_coords)
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle = 0
        self.velocity = 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):
        self.angle = (player.pos - self.pos).angle_to(pygame.Vector2(1, 0))
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.direction * self.velocity
        self.rect.center = self.pos
        self.velocity = 0.5

        collided_enemies = \
            pygame.sprite.spritecollide(self, all_sprites, False,
                                        pygame.sprite.collide_mask)

        for a in collided_enemies:
            for b in collided_enemies:
                if a != b and collided_enemies:
                    self.pos -= self.direction * self.velocity
                if not collided_enemies:
                    self.velocity = 0.5


# Class for the Player
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
        self.prev_fwd = (0, 0)
        self.prev_back = (0, 0)
        self.w = True
        self.s = True
        self.hit_direction = ""
        self.mask = pygame.mask.from_surface(self.image)
        self.offset = (0, 0)
        self.result = (0, 0)
        self.a = "a"
        self.b = "b"

    def update(self, events, dt):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.groups()[0].add(Projectile(
                        self.rect.center, self.direction.normalize()))
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            self.angle += 3
        if pressed[pygame.K_d]:
            self.angle -= 3
        if self.w and pressed[pygame.K_w]:
            self.pos += self.direction * self.speed
            self.rect.center = self.pos
        if self.s and pressed[pygame.K_s]:
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
        if self.rect.bottom > 500:
            self.rect.bottom = 500
        if self.rect.top < 0:
            self.rect.top = 5
        self.prev_back = self.pos
        player_collide = \
            pygame.sprite.spritecollide(self, all_sprites, False,
                                        pygame.sprite.collide_mask)
        self.w = True
        self.s = True
        for a in player_collide:
            for b in player_collide:
                self.speed = 3
                self.offset = (a.rect.x - b.rect.x, a.rect.y - b.rect.y)
                self.result = self.mask.overlap(self.mask, self.offset)
                if a != b and pressed[pygame.K_w]:
                    self.w = False
                    if self.hit_direction in DIRECTION_LIST:
                        self.hit_direction = tuple(self.direction)
                        for _ in range(int(self.direction.length()) + 1):
                            self.pos -= self.direction.normalize()
                    if self.direction != self.hit_direction and \
                            self.direction in DIRECTION_LIST:
                        self.w = True
                elif a != b and player_collide and pressed[pygame.K_s]:
                    self.s = False
                    if self.direction in DIRECTION_LIST:
                        self.hit_direction = tuple(self.direction)
                        for _ in range(int(self.direction.length()) + 1):
                            self.pos += self.direction.normalize()
                        if self.direction != self.hit_direction and \
                                self.direction in DIRECTION_LIST:
                            self.s = True


def main(start_timer):
    player = Player()
    sprites.add(player)
    all_sprites.add(player)

    for i in range(0, 9):
        tree = Tree()
        tree_pos.pop(0)
        trees.add(tree)
        all_sprites.add(tree)

    pygame.init()
    screen = pygame.display.set_mode((1000, 512))
    clock = pygame.time.Clock()
    run = True

    while run:
        enemy = Enemy()
        enemy_timer = pygame.time.get_ticks()
        if enemy_timer - start_timer > random.randint(3000, 4000):
            enemy_list.append(enemy)
            start_timer = enemy_timer

        for enemy in enemy_list:
            all_sprites.add(enemy)
            enemies.add(enemy)
        pressed = pygame.key.get_pressed()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or pressed[pygame.K_ESCAPE]:
                run = False
        dt = clock.tick(60)
        draw_grid()
        draw_screen()

        enemies.draw(screen)
        enemies.update(player)
        trees.draw(screen)
        sprites.draw(screen)
        sprites.update(events, dt)
        # updates the game display
        pygame.display.flip()


main(start_ticks_enemy)
