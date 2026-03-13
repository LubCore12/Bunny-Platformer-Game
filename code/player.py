from settings import *


class Bullet(Sprite):
    def __init__(self, surf, x, y, direction, groups):
        super().__init__(surf, x, y, groups)

        self.image = pygame.transform.flip(surf, direction == -1, False)

        self.direction = direction
        self.speed = BULLET_SPEED

    def update(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time


class Fire(Sprite):
    def __init__(self, surf, x, y, groups, player):
        super().__init__(surf, x, y, groups)

        self.player = player
        self.flip = player.flip

        self.y_offset = pygame.Vector2(0, 8)

        self.timer = Timer(100, autostart=True, func=self.kill)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, self.flip, False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

    def update(self, _):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class Player(AnimatedSprite):
    def __init__(self, frames, x, y, groups, collisions, create_bullet):
        self.flip = False
        self.create_bullet = create_bullet

        super().__init__(frames, x, y, groups)

        self.direction = pygame.Vector2()
        self.gravity = GRAVITY
        self.speed = SPEED
        self.on_floor = False

        self.collisions = collisions

        self.shoot_timer = Timer(SHOOT_COOLDOWN_MS)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])

        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = JUMP_VELOCITY

        if pygame.mouse.get_just_pressed()[0] and not self.shoot_timer.active:
            self.create_bullet(self.rect.centerx, self.rect.centery, -1 if self.flip else 1)
            self.shoot_timer.activate()

    def move(self, delta_time):
        self.rect.x += self.direction.x * self.speed * delta_time
        self.collision("horizontal")

        self.direction.y += self.gravity * delta_time
        self.rect.y += self.direction.y
        self.collision("vertical")

    def collision(self, direction):
        for collision in self.collisions:
            if self.rect.colliderect(collision.rect):
                if direction == "horizontal":
                    if self.direction.x < 0:
                        self.rect.left = collision.rect.right
                    if self.direction.x > 0:
                        self.rect.right = collision.rect.left

                if direction == "vertical":
                    if self.direction.y < 0:
                        self.rect.top = collision.rect.bottom
                    if self.direction.y > 0:
                        self.rect.bottom = collision.rect.top
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect(0, 0, self.rect.width, 2).move_to(midtop=self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collisions]
        self.on_floor = bottom_rect.collidelist(level_rects) >= 0

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
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(delta_time)
        self.animate(delta_time)
