from settings import *
from sprites import *

class Player(Sprite):
    def __init__(self, x, y, groups, collisions):
        self.image = pygame.image.load(join('images', 'player', '0.png'))

        super().__init__(self.image, x, y, groups)

        self.direction = pygame.Vector2()
        self.gravity = 15
        self.speed = 500
        self.on_floor = False

        self.collisions = collisions

    def input(self):
        self.key = pygame.key.get_pressed()
        self.direction.x = int(self.key[pygame.K_d]) - int(self.key[pygame.K_a])

        if self.key[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -11

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')

        self.direction.y += self.gravity * delta_time
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for collision in self.collisions:
            if self.rect.colliderect(collision.rect):
                if direction == 'horizontal':
                    if self.direction.x < 0:
                        self.rect.left = collision.rect.right
                    if self.direction.x > 0:
                        self.rect.right = collision.rect.left

                if direction == 'vertical':
                    if self.direction.y < 0:
                        self.rect.top = collision.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = collision.rect.top
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect(0, 0, self.rect.width, 2).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collisions]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def update(self, delta_time):
        self.check_floor()
        self.input()
        self.move(delta_time)