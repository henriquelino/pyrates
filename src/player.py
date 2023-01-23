from pathlib import Path
import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.display_surface: pygame.Surface = surface

        # animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = .15
        self.image: pygame.Surface = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = .15
        self.create_jump_particles = create_jump_particles

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = .8
        self.jump_speed = 16

        # player statuses
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def animate(self):
        animation = self.animations[self.status]

        # increase frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image: pygame.Surface = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)

        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

        return

    def animate_run_dust(self):
        if self.status != 'run' or not self.on_ground:
            return

        self.dust_frame_index += self.dust_animation_speed

        if self.dust_frame_index >= len(self.dust_run_particles):
            self.dust_frame_index = 0

        dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

        if self.facing_right:
            pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
        else:
            dust_particle = pygame.transform.flip(dust_particle, True, False)
            pos = self.rect.bottomright - pygame.math.Vector2(6, 10)

        self.display_surface.blit(dust_particle, pos)
        return

    def import_assets(self):
        path = Path('../graphics/character')
        self.animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': []
        } # yapf: disable

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path / animation)

        return

    def import_dust_run_particles(self):
        path = Path('../graphics/character/dust_particles/run')
        self.dust_run_particles = import_folder(path)
        return

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

        return

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:  # moving left or right
                self.status = 'run'
            else:
                self.status = 'idle'

        return

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed * -1

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.animate_run_dust()