import pygame
import random

pygame.init()
game_speed = pygame.time.Clock()

# Games speed
FPS = 30
WIDTH, HEIGHT = 1000, 520

# Game window and caption
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption("Cryosoldier")
# Two of the same images displayed side by
trees = pygame.sprite.Group()
tree_list = []
# side for the game surface
surface_1 = pygame.image.load("../images/Grass.png")
surface_2 = pygame.image.load("../images/Grass.png")
soldier = pygame.image.load('../images/soldier_right.png')
enemy1 = pygame.image.load('../images/enemy.png')
# All sprites group to allow for easy update on game window
enemies = pygame.sprite.Group()
sprites = pygame.sprite.Group()
# Lists for the tree positions
tree_pos = [(76, 112), (576, 400), (776, 162), (476, 162), (276, 362),
            (676, 12), (876, 312), (176, 412), (270, 60)]
MAX_SPEED = 9


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
        self.rect.topleft = tree_pos[0]


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
        self.rect.x = random.randrange(50, 900)
        self.rect.y = random.randrange(50, 450)
        self.direction = pygame.Vector2(1, 0)
        self.pos = pygame.Vector2(self.rect.center)
        self.angle = 0
        self.velocity = 0.5
        self.image2 = pygame.image.load("../images/oval.png")
        self.rect2 = self.image.get_rect(center=(0, 0))
        self.rect2.center = self.pos
        self.rect2 = self.image.get_rect(center=self.rect.center)

    def update(self, player):
        self.angle = (player.pos - self.pos).angle_to(pygame.Vector2(1, 0))
        self.direction = pygame.Vector2(1, 0).rotate(-self.angle)
        self.image = pygame.transform.rotate(self.org_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.pos += self.direction * self.velocity
        self.rect.center = self.pos


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
    player = Player()
    sprites.add(player)

    for e in range(0, 5):
        enemy = Enemy()
        enemies.add(enemy)

    for i in range(0, 9):
        tree = Tree()
        tree_pos.pop(0)
        tree_list.append(tree)
        trees.add(tree)
        sprites.add(tree)
    for tree in tree_list:
        print(tree.rect.x, tree.rect.y)

    pygame.init()
    screen = pygame.display.set_mode((1000, 500))

    clock = pygame.time.Clock()
    run = True
    while run:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                run = False
        dt = clock.tick(60)
        draw_screen()
        trees.draw(screen)
        sprites.draw(screen)
        sprites.update(events, dt)
        enemies.draw(screen)
        enemies.update(player)
        # updates the game display
        pygame.display.flip()


main()
