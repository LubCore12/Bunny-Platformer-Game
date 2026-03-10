from settings import *
from sprites import *

class Player(Sprite):
    def __init__(self, x, y, groups, collisions):
        self.image = pygame.image.load(join('images', 'player', '0.png'))

        super().__init__(self.image, x, y, groups)

        self.direction = pygame.Vector2()
        self.speed = 500

        self.collisions = collisions

    def input(self):
        self.key = pygame.key.get_pressed()

        self.direction.x = int(self.key[pygame.K_d]) - int(self.key[pygame.K_a])
        self.direction.y = int(self.key[pygame.K_s]) - int(self.key[pygame.K_w])

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed * delta_time
        self.collision('vertical')

    def collision(self, direction):
        for collision in self.collisions:
            if self.rect.colliderect(collision.rect):
                if direction == 'horizontal':
                    if self.direction.x < 0:
                        self.rect.left = collision.rect.right
                    if self.direction.x > 0:
                        self.rect.right = collision.rect.left

                elif direction == 'vertical':
                    if self.direction.y < 0:
                        self.rect.top = collision.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = collision.rect.top


    def update(self, delta_time):
        self.input()
        self.move(delta_time)