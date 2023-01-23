from pathlib import Path
import pygame
from pygame.sprite import Sprite

from support import import_folder


class Tile(Sprite):

    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))

        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):

    def __init__(self, pos: tuple[int, int], size: int, image: pygame.Surface):
        super().__init__(pos, size)
        self.image = image


class Crate(StaticTile):

    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load(Path('../graphics/terrain/crate.png')).convert_alpha())
        offset_y = pos[1] + size
        self.rect = self.image.get_rect(bottomleft=(pos[0], offset_y))


class AnimatedTile(Tile):

    def __init__(self, pos, size, path):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.animation_speed = .10
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        self.animate()
        return super().update(x_shift)


class Coin(AnimatedTile):

    def __init__(self, pos, size, path):
        super().__init__(pos, size, path)
        center_x = pos[0] + size // 2
        center_y = pos[1] + size // 2
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Palm(AnimatedTile):

    def __init__(self, pos, size, path, offset):
        super().__init__(pos, size, path)
        offset_y = pos[1] - offset[1]
        self.rect.topleft = (pos[0], offset_y)
