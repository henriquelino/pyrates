from pathlib import Path
from random import choice, randint
import pygame
from settings import screen_width, tile_size, vertical_tile_number
from support import import_folder
from tiles import AnimatedTile, StaticTile


class Sky:

    def __init__(self, horizon) -> None:
        self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()
        self.horizon = horizon

        # stretch
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self, surface: pygame.Surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                sprite = self.top
            elif row == self.horizon:
                sprite = self.middle
            else:
                sprite = self.bottom

            surface.blit(sprite, (0, y))


class Water:

    def __init__(self, top, width) -> None:
        water_start = -screen_width
        water_tile_width = 192  # pixels
        tile_x_amount = (width + (screen_width * 2)) // water_tile_width
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top
            self.water_sprites.add(AnimatedTile((x, y), water_tile_width, Path('../graphics/decoration/water')))

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Clouds:

    def __init__(self, horizon, width, cloud_number) -> None:
        cloud_surface_list = import_folder(Path('../graphics/decoration/clouds'))
        min_x = -screen_width
        max_x = width + screen_width
        min_y = 0
        max_y = horizon
        self.cloud_sprites = pygame.sprite.Group()
        for _ in range(cloud_number):
            cloud = choice(cloud_surface_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            self.cloud_sprites.add(StaticTile((x, y), 0, cloud))

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)