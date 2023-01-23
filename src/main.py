import sys
import pygame
from settings import screen_width, screen_height, frame_rate
from level import Level
from game_data import level0

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level0, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('gray')

    level.run()

    pygame.display.update()
    clock.tick(frame_rate)