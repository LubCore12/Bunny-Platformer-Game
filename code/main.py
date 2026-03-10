from settings import *
from player import *
from sprites import *
from groups import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.game_map = load_pygame(join('data', 'maps', 'world.tmx'))

        self.setup()

    def setup(self):
        for x, y, image in self.game_map.get_layer_by_name("Main").tiles():
            Sprite(image, x * TILE_SIZE, y * TILE_SIZE, (self.all_sprites, self.collision_sprites))

        for x, y, image in self.game_map.get_layer_by_name("Decoration").tiles():
            Sprite(image, x * TILE_SIZE, y * TILE_SIZE, self.all_sprites)

        for entity in self.game_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player(entity.x, entity.y, self.all_sprites, self.collision_sprites)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 

            self.all_sprites.update(delta_time)

            self.display_surface.fill(BG_COLOR)

            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 