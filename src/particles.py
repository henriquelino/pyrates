from pathlib import Path
import pygame
from support import import_folder


class ParticlesEffect(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        super().__init__()

        self.frame_index = 0
        self.animation_speed = .5

        path = Path('../graphics/character/dust_particles')

        self.frames = import_folder(path / type)

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()  # remove this sprite after animate ends
        else:
            self.image = self.frames[int(self.frame_index)]
        return

    def update(self, x_shift: float):
        self.animate()
        self.rect.x += x_shift
        return
