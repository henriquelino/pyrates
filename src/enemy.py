from pathlib import Path
import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):

    def __init__(self, pos, size):
        super().__init__(pos, size, Path('../graphics/enemy/run'))
        self.speed = randint(3, 5)
        self.rect.y += size - self.image.get_size()[1]  # put enemy on the bottom

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def move(self):
        self.rect.x += self.speed

    def update(self, x_shift):
        self.rect.x += x_shift
        self.animate()
        self.move()
        self.reverse_image()
        return