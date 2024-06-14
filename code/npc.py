import pygame
from pygame import Surface, Vector2
from timer import Timer
from settings import *
from math import floor, ceil


class Npc(pygame.sprite.Sprite):
    def __init__(self, pos,frames, player, player_shadow,abduction_state, groups, collision_sprites, level, callback = None):
        super().__init__(groups)
        # imported values
        self.player_shadow = player_shadow
        self.player = player

        self.abduction_state = abduction_state
        self.image = pygame.image.load(join('..', 'images', 'npc', 'down', '0001.png')).convert_alpha()

        self.abduction_timer = Timer(800)

        self.level = level
        self.alive = True
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()


        self.frames = frames
        self.frame_index = 0
        self.ufo_in_view = False
        self.rect = self.image.get_frect(center = (pos))
        self.hitbox_rect = self.rect.inflate(-50,-30)

        if self.level == 1:
            self.scared_timer = Timer(1000)
            self.viewbox_rect = self.image.get_frect(center = (pos)).inflate(500,500)
            self.speed = 250

        elif self.level == 2:
            self.scared_timer = Timer(1200)
            self.viewbox_rect = self.image.get_frect(center=(pos)).inflate(600, 600)
            self.speed = 300
        elif self.level == 3:
            self.scared_timer = Timer(1400)
            self.viewbox_rect = self.image.get_frect(center=(pos)).inflate(700, 700)
            self.speed = 400




        #self.speed = 0

        self.callback = callback

    def __del__(self):
        pass
    def get_direction(self):
        npc_pos = pygame.Vector2(self.hitbox_rect.center)
        player_pos = pygame.Vector2(self.player.rect.center) - (0, 5)
        self.viewbox_rect.center = self.rect.center
        if self.alive and self.ufo_in_view:
            self.direction = (npc_pos - player_pos).normalize()
        elif (player_pos.x - npc_pos.x) != 0 and not self.scared_timer.active:
            self.direction = Vector2(0,0)
        elif not self.alive:
            self.direction = (player_pos - npc_pos).normalize()
        #print(round(self.direction.x),round(self.direction.y))

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom


    def move(self, dt):
        if self.alive:
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.collision('horizontal')
            self.hitbox_rect.y += self.direction.y * self.speed * dt
            self.collision('vertical')
            self.rect.center = self.hitbox_rect.center
        else:
            #abduction
            self.hitbox_rect.x += self.direction.x * self.speed * dt * 2
            self.hitbox_rect.y += self.direction.y * self.speed * dt * 2
            self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        #get state
        if self.direction.x == 0 and self.direction.y == 0:
            self.state = 'idle'
        if round(self.direction.x) != 0:
            self.state = 'right' if round(self.direction.x) > 0 else 'left'
        if round(self.direction.y) != 0:
            self.state = 'down' if self.direction.y > 0 else 'up'

        if round(self.direction.y) < 0 and round(self.direction.x) > 0:
            self.state = 'up_right'
        if round(self.direction.y) > 0 and round(self.direction.x) > 0:
            self.state = 'down_right'
        if round(self.direction.y) < 0 and round(self.direction.x) < 0:
            self.state = 'up_left'
        if round(self.direction.y) > 0 and round(self.direction.x) < 0:
            self.state = 'down_left'

        #animation
        self.frame_index += dt * 60
        if self.alive:
            self.image = (self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]).convert_alpha()
        else:
            self.image = pygame.transform.scale_by(self.image,(0.9999,0.9999))


            if not self.abduction_timer.active:
                self.kill()



            #self.image = (self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])])
        #self.image = pygame.Surface(self.viewbox_rect.size).convert_alpha()

    def abduction(self,player_shadow):
        self.abduction_zone = self.hitbox_rect.scale_by(2,0.6)
        playerOnTop = self.abduction_zone.collidepoint(player_shadow.hitbox_rect.centerx, player_shadow.hitbox_rect.centery - 25)

        if playerOnTop and self.abduction_state.toggle:
            self.alive = False
            if self.callback is not None:
                # reward per npc
                self.callback(1000)
            self.abduction_timer.activate()

    def state_set(self):
        self.ufo_in_view = self.viewbox_rect.collidepoint(self.player.rect.center)
        if self.ufo_in_view:
            self.scared_timer.activate()

    def update(self, dt):

        self.state_set()
        self.scared_timer.update()
        self.abduction_timer.update()
        self.get_direction()
        self.abduction(self.player_shadow)
        self.animate(dt)
        self.move(dt)
        print(self.scared_timer.active)
