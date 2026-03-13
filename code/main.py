from settings import *
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Platformer")
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = AllSprites()
        self.enemy_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        self.game_map = load_pygame(join("data", "maps", "world.tmx"))

        self.load_assets()
        self.setup()

        self.bee_timer = Timer(2000, func=self.create_bee, autostart=True)

    def create_bee(self):
        Bee(self.bee_frames, randint(300, 600), randint(300, 600), self.all_sprites)

    def create_bullet(self, x, y, direction):
        x = x + direction * 34 if direction == 1 else x + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, x, y, direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, x, y, self.all_sprites, self.player)

    def load_assets(self):
        self.player_frames = import_folder("images", "player")
        self.bee_frames = import_folder("images", "enemies", "bee")
        self.worm_frames = import_folder("images", "enemies", "worm")
        self.bullet_surf = import_image("images", "gun", "bullet")
        self.fire_surf = import_image("images", "gun", "fire")

        self.audio = audio_importer("audio")

    def create_tile_layer(self, layer_name, groups):
        for x, y, image in self.game_map.get_layer_by_name(layer_name).tiles():
            Sprite(image, x * TILE_SIZE, y * TILE_SIZE, groups)

    def setup(self):
        self.create_tile_layer("Main", (self.all_sprites, self.collision_sprites))
        self.create_tile_layer("Decoration", self.all_sprites)

        for entity in self.game_map.get_layer_by_name("Entities"):
            if entity.name == "Player":
                self.player = Player(self.player_frames, entity.x, entity.y, self.all_sprites, self.collision_sprites, self.create_bullet)

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.bee_timer.update()
            self.all_sprites.update(delta_time)

            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
