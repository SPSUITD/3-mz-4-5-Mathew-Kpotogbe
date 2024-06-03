import pygame
from pygame import Vector2

from settings import *
from player import Player
from sprites import *
from random import randint
from pytmx.util_pygame import load_pygame
from groups import AllSprites


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


        self.setup()
        #Sprites



        #import
        #image_example = pygame.image.load(join('..', 'images', 'meteor.png')).convert_alpha()

    def setup(self):
        map = load_pygame(join('..', 'data', 'maps','world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y),obj.image, (self.all_sprites, self.collision_sprites))

        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y),pygame.Surface((obj.width, obj.height)),(self.collision_sprites))


        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y),self.all_sprites, self.tool_sprites,)










    def run(self):
        while self.running:

            #dt
            dt = self.clock.tick() / 1000

            # eventloop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # update
            self.all_sprites.update(dt)

            # draw
            self.all_sprites.draw(self.player.rect.center)
            print(self.clock.get_fps())

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()