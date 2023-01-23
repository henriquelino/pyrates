from csv import reader as csv_reader
from pathlib import Path
from settings import tile_size

import pygame


def import_folder(path: Path) -> list[pygame.Surface]:
    #print([file for file in path.glob('*.*')])
    return [pygame.image.load(file).convert_alpha() for file in path.glob('*.*')]


def import_csv_layout(path: Path):

    terrain_map = []
    with path.open('r') as map_file:
        level = csv_reader(map_file, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map


def import_cut_graphics(path: Path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surface = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            # put a slice of `surface` into new surface,
            # cutting the rect of surface that has the size of tile_size
            rect = pygame.Rect(x, y, tile_size, tile_size)
            new_surface.blit(surface, (0, 0), rect)

            cut_tiles.append(new_surface)

    return cut_tiles
