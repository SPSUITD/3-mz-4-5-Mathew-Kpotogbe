import pygame
from pygame import Vector2

from settings import *
from player import Player, Shadow
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from npc import  *
from button import *

class Game:
    def __init__(self):
        #Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        pygame.display.set_caption("UFO")
        self.clock = pygame.time.Clock()
        self.running = True

        self.paused = True
        self.menu_state = "main"

        #UI
        self.font = pygame.font.SysFont('arialblack', 40)
        self.TEXT_COL = (255, 255, 255)

        #Buttons
        BI = 130

        self.button_resume = Button(WINDOW_WIDTH / 2, 200, self.font, "Resume", self.TEXT_COL)
        self.button_intructions = Button(WINDOW_WIDTH / 2, self.button_resume.y + BI, self.font, "Instructions", self.TEXT_COL)
        self.button_exit = Button(WINDOW_WIDTH / 2, self.button_intructions.y + BI, self.font, "Exit", self.TEXT_COL)
        self.button_back = Button(WINDOW_WIDTH / 2, (WINDOW_HEIGHT - BI), self.font, "Back", self.TEXT_COL)

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.tool_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        #npc timer
        self.npc_spawn_limit = 20
        self.npc_event = pygame.event.custom_type()
        self.npc_spaw_rate = 50
        pygame.time.set_timer(self.npc_event, self.npc_spaw_rate)
        self.spawn_positions = []

        self.setup()

        #load images
        self.npc_frames = load_images('npc')

        #game timer
        self.energy = Timer(10000)
        self.energy.activate()

    def draw_text(self, surface, text,text_col, x, y):
        img = self.font.render(text, True, text_col)
        surface.blit(img, (x, y))

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

            # dt
            self.dt = (self.clock.tick() / 1000)
            if self.paused:
                self.dt = 0
            else:
                pass
            # eventloop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                if (event.type == self.npc_event) and (len(self.npc_sprites)) < self.npc_spawn_limit and self.dt != 0:
                    Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow,
                        self.player.abduction,(self.all_sprites, self.npc_sprites), self.collision_sprites)
                    print(self.npc_sprites)
                if event.type == pygame.QUIT:
                    self.running = False
            # update
            self.all_sprites.update(self.dt)
            self.energy.update()
            #print(self.energy.ticks)
            # draw
            self.all_sprites.draw(self.player.rect.center,self.dt)
            #dprint(self.clock.get_fps())

            # menu
            if self.paused == True:
                if self.menu_state == "main":
                    if self.button_resume.draw(self.display_surface):
                        self.paused = False
                    if self.button_intructions.draw(self.display_surface):
                        self.menu_state = "instructions"
                    if self.button_exit.draw(self.display_surface):
                        self.running = False
                if self.menu_state == "instructions":
                    self.draw_text(self.display_surface,"Для управления используй клавишы WASD \n или ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО",
                                   self.TEXT_COL, 2, WINDOW_HEIGHT/2)
                    if self.button_back.draw(self.display_surface):
                        self.menu_state = "main"
            else:
                pass

            pygame.display.update()



        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()