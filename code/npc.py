import pygame
from pygame import Surface
from timer import Timer
from settings import *
from math import floor, ceil
class Npc(pygame.sprite.Sprite):
    def __init__(self, pos,frames, player, player_shadow,abduction_state, groups, collision_sprites):
        super().__init__(groups)
        #impoerted values
        self.player_shadow = player_shadow
        self.abduction_state = abduction_state
        self.image = pygame.image.load(join('..', 'images', 'npc', 'down', '0001.png')).convert_alpha()

        self.abduction_timer = Timer(800)

        self.alive = True
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.player = player
        self.frames = frames
        self.frame_index = 0


        self.rect = self.image.get_frect(center = (pos))
        self.hitbox_rect = self.rect.inflate(-50,-30)

        self.speed = 250


    def get_direction(self):
        npc_pos = pygame.Vector2(self.hitbox_rect.center)
        player_pos = pygame.Vector2(self.player.rect.center) - (0, 5)
        if self.alive:
            self.direction = (npc_pos - player_pos).normalize()
        else:
            if (player_pos.x - npc_pos.x) != 0:
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
            self.hitbox_rect.x += self.direction.x * self.speed * dt * 2
            self.hitbox_rect.y += self.direction.y * self.speed * dt * 2
            self.rect.center = self.hitbox_rect.center

    def animate(self, dt):
        #get state
        if floor(self.direction.x) == 0 and floor(self.direction.y) == 0:
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
            #print(self.abduction_timer.ticks)
            if not self.abduction_timer.active:
                self.kill()


            #self.image = (self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])])
        #self.image = pygame.Surface(self.hitbox_rect.size).convert_alpha()

    def abduction(self,player_shadow):
        self.abduction_zone = self.hitbox_rect.scale_by(2,0.6)
        playerOnTop = self.abduction_zone.collidepoint(player_shadow.hitbox_rect.centerx, player_shadow.hitbox_rect.centery - 25)

        if playerOnTop and self.abduction_state.toggle:
            self.alive = False
            self.abduction_timer.activate()


    def update(self, dt):
        self.abduction_timer.update()

        self.get_direction()
        self.abduction(self.player_shadow)
        self.animate(dt)
        self.move(dt)
