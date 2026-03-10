from settings import *
from sprites import *

class Player(AnimatedSprite):
    def __init__(self, frames, x, y, groups, collisions):
        self.frames = frames
        self.flip = False

        super().__init__(self.frames, x, y, groups)

        self.direction = pygame.Vector2()
        self.gravity = 15
        self.speed = 500
        self.on_floor = False

        self.collisions = collisions

    def input(self):
        self.key = pygame.key.get_pressed()
        self.direction.x = int(self.key[pygame.K_d]) - int(self.key[pygame.K_a])

        if self.key[pygame.K_SPACE] and self.on_floor:
            self.direction.y = -9

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

    def animate(self, delta_time):
        if self.direction.x:
            self.frame_index += self.animation_speed * delta_time
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0.99

        if not self.on_floor:
            self.frame_index = 1.99

        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, delta_time):
        self.check_floor()
        self.input()
        self.move(delta_time)
        self.animate(delta_time)