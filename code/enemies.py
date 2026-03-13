from settings import *


class Enemy(AnimatedSprite):
    def __init__(self, frames, x, y, groups):
        super().__init__(frames, x, y, groups)

        self.death_timer = Timer(300, func=self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, delta_time):
        self.death_timer.update()

        if not self.death_timer:
            self.move(delta_time)
            self.animate(delta_time)
            self.constraint()


class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft[0], rect.topleft[1], groups)

        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect

        self.frames = frames

        self.speed = randint(100, 200)
        self.direction = 1

    def move(self, delta_time):
        self.rect.x += self.direction * self.speed * delta_time

    def constraint(self):
        if not self.main_rect.contains(self.rect):
            self.direction *= -1
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]


class Bee(Enemy):
    def __init__(self, frames, x, y, groups, speed):
        super().__init__(frames, x, y, groups)

        self.speed = speed
        self.amplitude = randint(500, 600)
        self.frequency = randint(300, 600)

    def move(self, delta_time):
        self.rect.x -= self.speed * delta_time
        self.rect.y += sin(pygame.time.get_ticks() / self.frequency) * delta_time * self.amplitude

    def constraint(self):
        if self.rect.right <= -WINDOW_WIDTH:
            self.kill()
