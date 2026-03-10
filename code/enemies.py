from settings import *
from sprites import *

class Worm(AnimatedSprite):
    def __init__(self, frames, x, y, groups):
        super().__init__(frames, x, y, groups)

    def update(self, delta_time):
        self.animate(delta_time)


class Bee(AnimatedSprite):
    def __init__(self, frames, x, y, groups):
        super().__init__(frames, x, y, groups)

    def update(self, delta_time):
        self.animate(delta_time)