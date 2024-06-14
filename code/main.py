import pygame
from pygame import Vector2
from settings import *
from player import Player, Shadow
from sprites import *
from random import randint, choice
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from npc import *
from button import *
import os

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

        #Healthbar
        self.maximum_health = 20000
        self.Health = Timer(self.maximum_health)
        self.Health.activate()
        self.initialHealth = 10000
        self.current_health = self.initialHealth
        self.health_bar_length = WINDOW_WIDTH - 40
        self.health_ratio = self.maximum_health/self.health_bar_length

        #Buttons
        BI = 130

        self.button_resume = Button(WINDOW_WIDTH / 2, 200, self.font, "Resume", self.TEXT_COL)
        self.button_intructions = Button(WINDOW_WIDTH / 2, self.button_resume.y + BI, self.font, "Instructions", self.TEXT_COL)
        self.button_exit = Button(WINDOW_WIDTH / 2, self.button_intructions.y + BI, self.font, "Exit", self.TEXT_COL)
        self.button_back = Button(WINDOW_WIDTH / 2, (WINDOW_HEIGHT - BI), self.font, "Back", self.TEXT_COL)

        self.button_restart = Button(WINDOW_WIDTH / 2, (WINDOW_HEIGHT /2), self.font, "Try again", self.TEXT_COL)

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


    def get_damage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
    def health_add(self, reward):
        print("hp added")
        if self.current_health < self.maximum_health:
            self.current_health += reward
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
    def draw_health(self):
        pygame.draw.rect(self.display_surface, (0,255,0), (20,10,self.current_health/self.health_ratio,25))

    def draw_text(self, surface, text,text_col, x, y):
        img = self.font.render(text, True, text_col)
        surface.blit(img, (x, y))
    def setup(self):
        map = load_pygame(join('..', 'data', 'maps','world.tmx'))

        for x, y, image in map.get_layer_by_name('Ground').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):
            CollisionSprite((obj.x, obj.y),obj.image, (self.all_sprites))
        for obj in map.get_layer_by_name('Forest'):
            CollisionSprite((obj.x, obj.y),obj.image, (self.all_sprites))
        for obj in map.get_layer_by_name('Collisions'):
            CollisionSprite((obj.x, obj.y),pygame.Surface((obj.width, obj.height)),(self.collision_sprites))


        for marker in map.get_layer_by_name('Entities'):
            if marker.name == 'Player':
                self.player = Player((marker.x, marker.y),load_images('player'),(self.all_sprites), self.tool_sprites)
                self.player_shadow = Shadow(self.player, self.all_sprites)
            if marker.name == 'npc':
                self.spawn_positions.append((marker.x, marker.y))

    def restart(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.tool_sprites.empty()
        self.npc_sprites.empty()
        self.current_health = self.initialHealth
        self.paused = False
        self.menu_state = "main"
        self.all_sprites.camera = Vector2(0, 0)
        self.setup()

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
                    npc = Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow, self.player.abduction,
                           (self.all_sprites, self.npc_sprites), self.collision_sprites, callback = self.health_add)

                if event.type == pygame.QUIT:
                    self.running = False

            #shootCost
            if self.player.abduction.toggle:
                self.get_damage(100)

            #playerDead
            if self.current_health == 0:
                self.player.out_of_energy()
                self.menu_state = "GameOver"

            # update
            self.all_sprites.update(self.dt)
            self.Health.update()

            # draw
            self.all_sprites.draw(self.player.rect.center,self.dt)
            print(self.clock.get_fps())

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
                                   self.TEXT_COL, 50, 50)
                    if self.button_back.draw(self.display_surface):
                        self.menu_state = "main"
            else:
                self.draw_health()
                self.get_damage(10)
            if self.menu_state == "GameOver":
                if self.button_restart.draw(self.display_surface):
                    self.restart()



            pygame.display.update()



        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()