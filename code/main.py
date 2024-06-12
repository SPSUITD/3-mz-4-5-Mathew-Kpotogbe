import pygame
from pygame import Vector2

from settings import *
from player import Player, Shadow
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from npc import  *

class Game:
    def __init__(self):
        #Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("UFO")
        self.clock = pygame.time.Clock()
        self.running = True

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.tool_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        #npc timer
        self.npc_spawn_limit = 20
        self.npc_event = pygame.event.custom_type()
        self.npc_spaw_rate = 500
        pygame.time.set_timer(self.npc_event, self.npc_spaw_rate)
        self.spawn_positions = []

        self.setup()

        #load images
        self.npc_frames = load_images('npc')


    def setup(self):
        map = load_pygame(join('..', 'data', 'maps','world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y),obj.image, (self.all_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y),pygame.Surface((obj.width, obj.height)),(self.collision_sprites))


        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y),load_images('player'),(self.all_sprites), self.tool_sprites)
                self.player_shadow = Shadow(self.player, self.all_sprites)
            if marker.name == 'npc':
                self.spawn_positions.append((marker.x, marker.y))



    def run(self):
        while self.running:

            #dt
            dt = (self.clock.tick() / 1000)

            # eventloop
            for event in pygame.event.get():
                if (event.type == self.npc_event) and (len(self.enemy_sprites)) < self.npc_spawn_limit:
                    Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow,
                        self.player.abduction,(self.all_sprites, self.enemy_sprites), self.collision_sprites)

                if event.type == pygame.QUIT:
                    self.running = False
            # update
            self.all_sprites.update(dt)
            # draw
            self.all_sprites.draw(self.player.rect.center)
            #print(self.clock.get_fps())
            pygame.display.update()
        pygame.quit()
if __name__ == '__main__':
    game = Game()
    game.run()