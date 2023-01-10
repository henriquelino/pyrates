import pygame
from particles import ParticlesEffect
from player import Player
from tiles import Tile
from settings import tile_size, screen_width


class Level:

    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

        self.world_shift = 0
        self.current_x = 0

        # dusts
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

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
                    self.player.add(Player((x + (tile_size / 4), y), self.display_surface, self.create_jump_particles))

    def scroll_x(self):
        player: Player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width / 6) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width - (screen_width / 6)) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

        return

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite

        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
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

        for sprite in self.tiles.sprites():
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

    def run(self):

        # dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)