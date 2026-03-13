from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf, x, y, groups):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=(x, y))


class AnimatedSprite(Sprite):
    def __init__(self, frames, x, y, groups):
        self.frames = frames
        self.frame_index = 0
        self.animation_speed = 10

        super().__init__(self.frames[self.frame_index], x, y, groups)

    def animate(self, delta_time):
        self.frame_index += self.animation_speed * delta_time
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
