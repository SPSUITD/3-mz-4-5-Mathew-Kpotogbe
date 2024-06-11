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
        self.frame_index = self.frame_index + dt * 60
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

class Npc(pygame.sprite.Sprite):
    def __init__(self, pos,frames, target, groups, collision_sprites):
        super().__init__(groups)


        self.image = pygame.image.load(join('..', 'images', 'npc', 'down', '0001.png')).convert_alpha()

        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()

        self.target = target

        self.frames = frames
        self.enemy_type, self.frame_index = 'bat', 0

        self.rect = self.image.get_frect(center = (pos))

        self.speed = 300
        self.hitbox_rect = self.rect.inflate(-60,-80)

    def get_direction(self):
        enemy_pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.target.rect.center) - (0,5)
        self.direction = (enemy_pos - player_pos).normalize()

        #print(round(self.direction.x),round(self.direction.y))
        print(self.direction)
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top


    def move(self, dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center
    def animate(self, dt):
        #get state


        if floor(self.direction.x) == 0 and floor(self.direction.y) == 0:
            self.state = 'idle'
        if round(self.direction.x)  != 0:
            self.state = 'right' if round(self.direction.x)  > 0 else 'left'
        if round(self.direction.y) != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        if round(self.direction.y) < 0 and round(self.direction.x)  > 0:
            self.state = 'up_right'
        if round(self.direction.y) > 0 and round(self.direction.x)  > 0:
            self.state = 'down_right'
        if round(self.direction.y) < 0 and round(self.direction.x)  < 0:
            self.state = 'up_left'
        if round(self.direction.y)  > 0 and round(self.direction.x)  < 0:
            self.state = 'down_left'

        #animation
        self.frame_index += dt * 60
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

    def update(self, dt):

        self.get_direction()
        self.animate(dt)
        self.move(dt)


class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)

