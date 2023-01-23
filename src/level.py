import csv
from pathlib import Path
from random import randint

import pygame
from decoration import Clouds, Sky, Water
from enemy import Enemy

from particles import ParticlesEffect
from player import Player
from settings import screen_width, tile_size, screen_height
from tiles import AnimatedTile, Coin, Crate, Palm, StaticTile, Tile
from support import import_csv_layout, import_cut_graphics


class Level:

    def __init__(self, level_data, surface):
        self.display_surface = surface
        #self.setup_level(level_data)

        self.world_shift = 0
        self.current_x = 0

        # dusts
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # player
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # video 2
        # terrain setup
        terrain_fg_layout = import_csv_layout(level_data['terrain_fg'])
        self.terrain_fg_sprites = self.create_tile_group(terrain_fg_layout, 'terrain_fg')
        terrain_bg_layout = import_csv_layout(level_data['terrain_bg'])
        self.terrain_bg_sprites = self.create_tile_group(terrain_bg_layout, 'terrain_bg')
        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')
        # crates setup
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')
        # coins setup
        coins_layout = import_csv_layout(level_data['coins'])
        self.coins_sprites = self.create_tile_group(coins_layout, 'coins')
        # palms foreground
        palms_fg_layout = import_csv_layout(level_data['palms_fg'])
        self.palms_fg_layout = self.create_tile_group(palms_fg_layout, 'palms_fg')
        # palms background
        palms_bg_layout = import_csv_layout(level_data['palms_bg'])
        self.palms_bg_layout = self.create_tile_group(palms_bg_layout, 'palms_bg')

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')
        constraints_layout = import_csv_layout(level_data['constraints'])
        self.enemy_constraints = self.create_tile_group(constraints_layout, 'constraints')

        # decoration
        self.sky = Sky(8)
        level_width = len(player_layout[0]) * tile_size
        self.water = Water(screen_height - 25, level_width)
        self.clouds = Clouds(400, level_width, randint(15, 40))

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                col = int(col)
                x = col_index * tile_size
                y = row_index * tile_size

                if col == 0:  # player
                    self.player.add(Player((x, y), self.display_surface, self.create_jump_particles))

                elif col == 1:  # goal
                    self.goal.add(StaticTile((x, y), tile_size, pygame.image.load('../graphics/character/hat.png')))

    def create_tile_group(self, layout: list, type: str):
        group = pygame.sprite.Group()

        import_graphics = True
        if type == 'terrain_bg' or type == 'terrain_fg':
            tiles_layout_path = Path('../graphics/terrain/terrain_tiles.png')
        elif type == 'grass':
            tiles_layout_path = Path('../graphics/decoration/grass/grass.png')
        elif type == 'coins':
            import_graphics = False
            gold_coin_layout_path = Path('../graphics/coins/gold')
            silver_coin_layout_path = Path('../graphics/coins/silver')
        elif type == 'palms_fg':
            import_graphics = False
            palm_small_layout_path = Path('../graphics/terrain/palm_small')
            palm_large_layout_path = Path('../graphics/terrain/palm_large')
        elif type == 'palms_bg':
            import_graphics = False
            bg_palm_layout_path = Path('../graphics/terrain/palm_bg')
        elif type == 'crates':
            import_graphics = False
        elif type == 'enemies':
            import_graphics = False
        elif type == 'constraints':
            import_graphics = False

        if import_graphics:
            tile_list = import_cut_graphics(tiles_layout_path)

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                col = int(col)
                if col == -1:
                    continue

                x = col_index * tile_size
                y = row_index * tile_size

                #print(type, col)
                if type == 'crates':
                    group.add(Crate((x, y), tile_size))
                elif type == 'palms_fg':
                    if col == 0:
                        group.add(Palm((x, y), tile_size, palm_small_layout_path, (0, 38)))
                    if col == 1:
                        group.add(Palm((x, y), tile_size, palm_large_layout_path, (0, 68)))
                elif type == 'palms_bg':
                    group.add(Palm((x, y), tile_size, bg_palm_layout_path, (0, 68)))

                elif type == 'coins':
                    if col == 0:  # gold coin
                        group.add(Coin((x, y), tile_size, gold_coin_layout_path))
                    elif col == 1:  # silver coin
                        group.add(Coin((x, y), tile_size, silver_coin_layout_path))
                elif type == 'enemies':
                    group.add(Enemy((x, y), tile_size))
                elif type == 'constraints':
                    group.add(Tile((x, y), tile_size))
                else:
                    group.add(StaticTile((x, y), tile_size, tile_list[int(col)]))

        return group

    def create_jump_particles(self, pos):

        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        jump_particle_sprite = ParticlesEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)
        return

    def get_player_on_ground(self):
        self.player_on_ground = self.player.sprite.on_ground
        return

    def create_landing_dust(self):
        player: Player = self.player.sprite
        if self.player_on_ground or not player.on_ground or self.dust_sprite.sprites():
            return

        pos = player.rect.midbottom
        if player.facing_right:
            pos -= pygame.math.Vector2(10, 20)
        else:
            pos += pygame.math.Vector2(10, -20)

        fall_dust_particle = ParticlesEffect(pos, 'land')
        self.dust_sprite.add(fall_dust_particle)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    self.tiles.add(Tile((x, y), tile_size))

                if cell == 'P':
                    ...

    def scroll_x(self):
        player: Player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width / 3) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - (screen_width / 3)) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

        return

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite

        player.rect.x += player.direction.x * player.speed
        for sprite in self.terrain_fg_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    # if player is moving left and has a collision,
                    # probably colliding on the left, so places the player on the right side of that sprite
                    player.rect.left = sprite.rect.right
                    self.current_x = player.rect.left
                    player.on_left = True

                elif player.direction.x > 0:
                    # same thing but if player is moving to the right, places him on the left of that sprite
                    player.rect.right = sprite.rect.left
                    self.current_x = player.rect.right
                    player.on_right = True

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False

        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

        return

    def vertical_movement_collision(self):
        player: Player = self.player.sprite
        player.apply_gravity()

        for sprite in self.terrain_fg_sprites.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    # if we are colliding and falling, places on top of sprite
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0  # resets gravity so we dont fall into the ground
                    player.on_ground = True
                elif player.direction.y < 0:
                    # if we are on air and colliding, we are on bottom of the sprite
                    player.rect.top = sprite.rect.bottom
                    player.on_ceiling = True
                    player.direction.y = 0  # cancels vertical movement so when hitting a ceiling we fall immediately

        # if was on ground and now is jumping or falling
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        # if was on ceiling and now is falling
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

        return

    def on_enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            enemy: Enemy
            if pygame.sprite.spritecollide(enemy, self.enemy_constraints, False):
                enemy.reverse()

    def run(self):

        # decorations
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # level tiles
        self.palms_bg_layout.update(self.world_shift)
        self.palms_bg_layout.draw(self.display_surface)
        self.terrain_bg_sprites.update(self.world_shift)
        self.terrain_bg_sprites.draw(self.display_surface)
        self.terrain_fg_sprites.update(self.world_shift)
        self.terrain_fg_sprites.draw(self.display_surface)

        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_constraints.update(self.world_shift)
        #self.enemy_constraints.draw(self.display_surface)

        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
        self.palms_fg_layout.update(self.world_shift)
        self.palms_fg_layout.draw(self.display_surface)

        # self.tiles.update(self.world_shift)
        # self.tiles.draw(self.display_surface)
        self.scroll_x()

        #enemies
        self.on_enemy_collision_reverse()

        # player
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        # self.get_player_on_ground()
        self.vertical_movement_collision()
        # self.create_landing_dust()
        self.player.draw(self.display_surface)

        self.water.draw(self.display_surface, self.world_shift)
