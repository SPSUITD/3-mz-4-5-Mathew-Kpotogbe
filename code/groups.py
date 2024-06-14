import pygame
from pygame import Vector2
from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()

        self.camera = Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT / 2)

    def draw(self, target_pos, dt):
        if dt != 0:
            heading = target_pos - self.camera
            self.camera += heading * 0.02
            self.offset = -self.camera + Vector2(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)



        ground_sprites = [sprite for sprite in self if hasattr(sprite, 'ground')]
        shadow_sprites = [sprite for sprite in self if hasattr(sprite, 'shadow')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite, 'ground') and not hasattr(sprite, 'shadow')]

        for layer in [ground_sprites,shadow_sprites,  object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)