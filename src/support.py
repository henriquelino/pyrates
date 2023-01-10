from os import walk
from pathlib import Path
import pygame


def import_folder(path: Path) -> list[pygame.Surface]:
    return [pygame.image.load(file).convert_alpha() for file in path.glob('*.*')]