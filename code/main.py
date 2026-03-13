from settings import *


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
        self.level_width = self.game_map.width * TILE_SIZE
        self.level_height = self.game_map.height * TILE_SIZE

        self.load_assets()
        self.setup()

        self.bee_timer = Timer(750, self.create_bee, True, True)

        self.audio['music'].set_volume(0.2)
        self.audio['music'].play(loops=-1)

    def create_bee(self):
        Bee(frames = self.bee_frames,
            x= self.level_width + WINDOW_WIDTH,
            y=randint(0, self.level_height),
            groups=(self.all_sprites, self.enemy_sprites),
            speed=randint(300, 500))

    def create_bullet(self, x, y, direction):
        x = x + direction * 34 if direction == 1 else x + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, x, y, direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, x, y, self.all_sprites, self.player)

        self.audio['shoot'].set_volume(0.2)
        self.audio['shoot'].play()

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
            if entity.name == "Worm":
                self.worm_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
                Worm(self.worm_frames, self.worm_rect, (self.all_sprites, self.enemy_sprites))

    def collision(self):
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)

            if sprite_collisions:
                self.audio['impact'].set_volume(0.2)
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collisions:
                    self.enemy_sprites.remove(sprite)
                    sprite.destroy()

        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.bee_timer.update()
            self.all_sprites.update(delta_time)
            self.collision()

            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
