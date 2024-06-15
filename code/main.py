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

        self.start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

        self.score = 0

        #UI
        self.font = pygame.font.SysFont('arialblack', 40)
        self.TEXT_COL = (255, 255, 255)

        #Healthbar
        self.maximum_health = 50000
        self.Health = Timer(self.maximum_health)
        self.Health.activate()
        self.initialHealth = 50000
        self.current_health = self.initialHealth
        self.health_bar_length = WINDOW_WIDTH - 40
        self.health_ratio = self.maximum_health/self.health_bar_length

        self.hp_depreciation = 10

        #Buttons
        BI = 130

        self.button_play = Button(WINDOW_WIDTH / 2, 200, self.font, "Играть", self.TEXT_COL)
        self.button_resume = Button(WINDOW_WIDTH / 2, 200, self.font, "Прололжить", self.TEXT_COL)
        self.button_intructions = Button(WINDOW_WIDTH / 2, self.button_resume.y + BI, self.font, "Инструкция", self.TEXT_COL)
        self.button_exit = Button(WINDOW_WIDTH / 2, self.button_intructions.y + BI, self.font, "Выйти", self.TEXT_COL)
        self.button_back = Button(WINDOW_WIDTH / 2, (WINDOW_HEIGHT - BI), self.font, "В главное меню", self.TEXT_COL)

        self.button_restart = Button(WINDOW_WIDTH / 2, (WINDOW_HEIGHT /2) + BI, self.font, "Начать заново", self.TEXT_COL)

        #Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.tool_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()

        #npc event
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
        self.score += int((reward)/100)
        if self.current_health < self.maximum_health:
            self.current_health += reward
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
    def draw_health(self):
        pygame.draw.rect(self.display_surface, (0,255,0), (20,10,self.current_health/self.health_ratio,25))
    def UI(self):
        if self.paused == True:
            if self.menu_state == "main":
                if self.elapsed_time == 0:
                    if self.button_play.draw(self.display_surface):
                        self.paused = False
                else:
                    if self.button_resume.draw(self.display_surface):
                        self.paused = False
                if self.button_intructions.draw(self.display_surface):
                    self.menu_state = "instructions"
                if self.button_exit.draw(self.display_surface):
                    self.running = False
            if self.menu_state == "instructions":
                self.draw_text(self.display_surface,
                               "Для управления используй клавишы WASD \n или ВВЕРХ, ВНИЗ, ВЛЕВО, ВПРАВО",
                               self.TEXT_COL, 50, 50, 'topleft')
                if self.button_back.draw(self.display_surface):
                    self.menu_state = "main"
        else:
            self.draw_health()
            self.get_damage(self.hp_depreciation)
            if self.paused == False and self.player.alive:
                self.draw_text(self.display_surface, "Score: "+str(self.score),(0,255,0),20,40, 'topleft')
        if self.menu_state == "GameOver":
            self.draw_text(self.display_surface, "Набрано очков: "+str(self.score),(255,255,255),WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
            if self.button_restart.draw(self.display_surface):
                self.restart()
    def draw_text(self, surface, text,text_col, x, y, align = 'center'):
        img = self.font.render(text, True, text_col)
        if align == 'center':
            text_rect = img.get_frect(center = (x, y))
        if align == 'topleft':
            text_rect = img.get_rect(topleft = (x, y))
        surface.blit(img, text_rect)
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
        self.score = 0
        self.setup()
    def run(self):
        while self.running:
            # dt
            self.dt = (self.clock.tick() / 1000)

            if self.paused:
                self.dt = 0
            else:
                self.elapsed_time += self.dt

            # eventloop
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True
                if self.score <= 2000:
                    if (event.type == self.npc_event) and (len(self.npc_sprites)) < self.npc_spawn_limit and self.dt != 0:
                        npc = Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow, self.player.abduction,
                               (self.all_sprites, self.npc_sprites), self.collision_sprites,1, callback = self.health_add)
                elif self.score <= 4000:
                    if (event.type == self.npc_event) and (len(self.npc_sprites)) < self.npc_spawn_limit and self.dt != 0:
                        npc = Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow, self.player.abduction,
                               (self.all_sprites, self.npc_sprites), self.collision_sprites,2, callback = self.health_add)
                elif self.score <= 5000:
                    if (event.type == self.npc_event) and (len(self.npc_sprites)) < self.npc_spawn_limit and self.dt != 0:
                        npc = Npc(choice(self.spawn_positions), self.npc_frames, self.player,self.player_shadow, self.player.abduction,
                               (self.all_sprites, self.npc_sprites), self.collision_sprites,3, callback = self.health_add)
                if event.type == pygame.QUIT:
                    self.running = False

        #DynamicConditions
            #shootCost
            if self.player.abduction.toggle:
                self.get_damage(100)

            #playerDead
            if self.current_health == 0:
                self.player.out_of_energy(self.dt)
                self.menu_state = "GameOver"

        # update
            self.all_sprites.update(self.dt)
            self.Health.update()

        # draw
            self.all_sprites.draw(self.player.rect.center,self.dt)
            self.UI()

            #print(self.clock.get_fps())




            pygame.display.update()



        pygame.quit()
if __name__ == '__main__':
    game = Game()
    game.run()