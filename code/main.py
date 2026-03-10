from settings import *
from player import *
from sprites import *
from groups import *
from support import *
from enemies import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups
        self.all_sprites = AllSprites()
        self.enemy_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.game_map = load_pygame(join('data', 'maps', 'world.tmx'))

        self.load_assets()
        self.setup()

    def load_assets(self):
        self.player_frames = import_folder('images', 'player')
        self.bee_frames = import_folder('images', 'enemies', 'bee')
        self.worm_frames = import_folder('images', 'enemies', 'worm')
        self.bullet_surf = import_image('images', 'gun', 'bullet')
        self.fire_surf = import_image('images', 'gun', 'fire')

        self.audio = audio_importer('audio')

    def setup(self):
        for x, y, image in self.game_map.get_layer_by_name("Main").tiles():
            Sprite(image, x * TILE_SIZE, y * TILE_SIZE, (self.all_sprites, self.collision_sprites))

        for x, y, image in self.game_map.get_layer_by_name("Decoration").tiles():
            Sprite(image, x * TILE_SIZE, y * TILE_SIZE, self.all_sprites)

        for entity in self.game_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player(self.player_frames, entity.x, entity.y, self.all_sprites, self.collision_sprites)
            if entity.name == "Worm":
                Worm(self.worm_frames, entity.x, entity.y, (self.all_sprites, self.enemy_sprites))

        Bee(self.bee_frames, 500, 600, self.all_sprites)


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