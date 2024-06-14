from pygame import Surface

from settings import *
from sprites import *
from timer import Timer



class Player(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups)

        self.groups = groups
        self.frames = frames
        self.state, self.frame_index = 'idle', 0
        self.fall_animation_index = 0
        self.alive = True


        self.image = pygame.image.load(join('..','images','player', 'down', '0001.png')).convert_alpha()

        #rects
        self.rect = self.image.get_frect(center = pos)
        self.hitbox_rect = self.rect.inflate(-120,-140)


        #self.rect = self.rect.inflate(-100,-100)

        #joined items
        #self.laser = Laser(self,False, self.groups)
        self.abduction = Abduction(self,False,self.groups)
        #self.shadow = Shadow(self, self.groups)



        #movement
        self.dumping = 0
        self.direction = pygame.Vector2()
        self.speed = 600
        self.collision_sprites = collision_sprites



    # def load_images(self):
    #     self.frames = {'idle':[],'left':[],'right':[],'up':[],'down':[],'down_left':[],'down_right':[],'up_left':[],'up_right':[]}
    #
    #     for state in self.frames.keys():
    #         for folder_path, sub_folders, file_names in walk (join('..','images','player', state)):
    #             if file_names:
    #                 for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
    #                     full_path = join(folder_path, file_name)
    #                     surf = pygame.image.load(full_path).convert_alpha()
    #                     self.frames[state].append(surf)
    def input(self, dt):
        if dt !=0 and self.alive:
            keys = pygame.key.get_pressed()
            input_left = keys[pygame.K_LEFT] or keys[pygame.K_a]
            input_right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
            input_up = keys[pygame.K_UP] or keys[pygame.K_w]
            input_down = keys[pygame.K_DOWN] or keys[pygame.K_s]

            if int(input_left) == 0 and int(input_right) == 0:
                self.direction.x = self.direction.x * self.dumping
                if abs(self.direction.x) < 0.01:
                    self.direction.x = int(0)
            else:
                self.direction.x = int(input_right) - int(input_left)

            if int(input_up) == 0 and int(input_down) == 0:
                self.direction.y = self.direction.y * self.dumping
                if abs(self.direction.y) < 0.01:
                    self.direction.y = int(0)
            else:
                self.direction.y = int(input_down) - int(input_up)

            self.direction = self.direction.normalize() if (abs(self.direction.x) >= 1 or abs(self.direction.y) >= 1) else self.direction


            #print(self.direction)
    def move(self, dt):

        self.hitbox_rect.x += self.speed * self.direction.x * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.speed * self.direction.y * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center;



    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
    def shoot(self, dt):
        if dt != 0 and self.alive:
            if pygame.mouse.get_pressed()[0] == 1:
                #self.laser.toggle = True
                self.abduction.toggle = False
            else:
                #self.laser.toggle = False
                pass

            if pygame.mouse.get_pressed()[2] == 1:
                self.abduction.toggle = True
                #self.laser.toggle = False
            else:
                self.abduction.toggle = False
    def animate(self, dt):
        #get state
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = 'idle'
        if self.direction.x != 0:
            self.state = 'right' if self.direction.x > 0 else 'left'
        if self.direction.y != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        if self.direction.y < 0 and self.direction.x > 0:
            self.state = 'up_right'
        if self.direction.y > 0 and self.direction.x > 0:
            self.state = 'down_right'
        if self.direction.y < 0 and self.direction.x < 0:
            self.state = 'up_left'
        if self.direction.y > 0 and self.direction.x < 0:
            self.state = 'down_left'




        #animation




        if self.alive == True:
            #normal animation
            self.frame_index += dt * 60
            self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        else:
            #fallAnimation
            self.state = 'fall'
            if self.fall_animation_index < 59:
                self.fall_animation_index += dt * 60
                self.image = self.frames[self.state][int(self.fall_animation_index)]
            else:
                #lastframe
                self.image = self.frames[self.state][59]
                pass





        #self.image = pygame.Surface(self.real_pos_rect.size).convert_alpha()

    def out_of_energy(self, dt):
        self.alive = False
        self.direction = pygame.Vector2(0,0)
        self.abduction.toggle = False
        #self.laser.toggle = False

        #fallAnimation


    def update(self, dt):

        self.animate(dt)
        self.shoot(dt)
        self.input(dt)
        self.move(dt)






        # self.rect.center = pygame.mouse.get_pos()

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


        self.shadow = True
        shadow_image_path = join('..', 'images', 'Tools', 'shadow', '0001.png')
        shadow2_image_path = join('..', 'images', 'Tools', 'shadow', 'Shadow_cropped.png')
        #self.image = pygame.image.load(join('..', 'images', 'player', 'down', '0001.png')).convert_alpha()

        self.image = pygame.image.load(shadow2_image_path).convert_alpha()


        self.player = player
        self.rect = self.image.get_frect(center = player.rect.center)
        self.hitbox_rect = self.rect

    def update(self, dt):

        self.rect.center = (self.player.rect.center[0], self.player.rect.center[1]+55)
        #self.image = Surface((self.hitbox.size)).convert_alpha()
        #отладка тени



