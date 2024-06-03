import pygame

from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True


class Tools(pygame.sprite.Sprite):
    def __init__(self, player, toggle, groups, image_path):

        self.player = player
        self.toggle = toggle
        super().__init__(groups)

        self.frames, self.frame_index = [], 0

        self.frames = self.import_folder(image_path)

        self.surf = self.frames[0]
        self.image = self.surf
        self.rect = self.surf.get_frect(center=self.player.rect.center)


    def import_folder(self, path):
        surface_list = []

        for _, __, img_files in walk(path):
            for image in img_files:
                full_path = path + '/' + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
        return surface_list

    def animate(self, dt):
        self.frame_index = self.frame_index + 60 * dt
        self.image = self.frames[int(self.frame_index)% len(self.frames)]
    def draw_if_active(self):
        if self.toggle:
            self.rect.center = (self.player.rect.center[0], self.player.rect.center[1]-1)
        else:
            self.rect.center = (-100, -100)

    def update(self, dt):
        self.rect.center = self.player.rect.center
        self.animate(dt)
        self.draw_if_active()

class Laser(Tools):
    def __init__(self, player, toggle, groups):
        image_path = join('..', 'images','Tools', 'laser')
        super().__init__(player, toggle, groups, image_path)
class Abduction(Tools):
    def __init__(self, player, toggle, groups):
        image_path = join('..', 'images','Tools', 'abduction')
        super().__init__(player, toggle, groups, image_path)
class Shadow(pygame.sprite.Sprite):

    def __init__(self, player, groups):
        super().__init__(groups)
        #self.image = pygame.image.load(join('..', 'images', 'player', 'down', '0001.png')).convert_alpha()
        self.image = pygame.image.load(join('..', 'images', 'Tools', 'shadow', '0001.png')).convert_alpha()
        self.player = player
        self.rect = self.image.get_frect(center = player.rect.topleft)
    def update(self, dt):
        self.rect.center = (self.player.rect.center[0], self.player.rect.center[1]-2)

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

