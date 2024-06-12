import pygame

from settings import *
from math import floor, ceil

def load_images(unit):
    frames = {'idle': [], 'left': [], 'right': [], 'up': [], 'down': [], 'down_left': [], 'down_right': [],
                   'up_left': [], 'up_right': []}

    for state in frames.keys():
        for folder_path, sub_folders, file_names in walk(join('..', 'images', unit, state)):
            if file_names:
                for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    frames[state].append(surf)
    return frames

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        #self.image = pygame.Surface(self.rect.size).convert_alpha()

