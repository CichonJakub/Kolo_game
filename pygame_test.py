#!/usr/bin/env Python3

# Start writing code for Koło Naukowe and build first 2D game :D

import pygame
from pygame.locals import *
#from new_grid import *
from settings import *
from map import *
import player
import locations
import npc

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE)
        self.load_map()

    def load_map(self):
        self.GRID = Map(MAP)

    def new(self):
        # Create objects
        self.PLAYER = player.Player()
        self.NPC = npc.importNpc(self)
        self.LOC = locations.importLocations(self)

        

    def run(self):
        ### GAME LOOP
        self.play = True
        while self.play:
            pygame.time.delay(FPS)
            self.events()
            self.updateMap()

    def quit(self):
        # Quit game
        pygame.quit()
    
    def updateMap(self):
        # what's gonna be updated with time
        for row in range(MAPHEIGHT):
            for column in range(MAPWIDTH):
                self.window.blit( TEXTURES[self.GRID.data[row + self.GRID.vertical_move][column + self.GRID.horizontal_move]], (column*TILESIZE, row*TILESIZE) )

        for location in self.LOC:
            if location.map == self.GRID.name:
                self.window.blit(location.sprite,(location.position[0]-(self.GRID.horizontal_move*TILESIZE), location.position[1]-(self.GRID.vertical_move*TILESIZE) ))

        for character in self.NPC:
            if character.map == self.GRID.name:
                self.window.blit(character.sprite,(character.position[0]-(self.GRID.horizontal_move*TILESIZE), character.position[1]-(self.GRID.vertical_move*TILESIZE) ))
        
        self.window.blit(self.PLAYER.SPRITE,self.PLAYER.POS)
        pygame.display.update()


    def events(self):
        # Events on the map
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()

        keys = pygame.key.get_pressed()
        x = self.PLAYER.POS[0]
        y = self.PLAYER.POS[1]

        player_X = x + (self.GRID.horizontal_move * TILESIZE)
        player_Y = y + (self.GRID.vertical_move * TILESIZE)

        # Move in Left and Up directions is still a little bit bugged but works just fine for now :)
        if keys[pygame.K_LEFT] and x > 0:
          # ABS potrzebny bo macierz może zczytywac z ujemnych wartości
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move][abs(x//TILESIZE + self.GRID.horizontal_move - 1)] != 'WATER': # BLOKADA PRZED WEJŚĆIEM NA WODE
                x -= self.PLAYER.VELOCITY
                if x % TILESIZE == 0 and self.GRID.horizontal_move > self.GRID.MARGIN_LEFT:
                    self.GRID.horizontal_move -= 1
    
        if keys[pygame.K_RIGHT] and x < WIDTH - TILESIZE:
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move][x//TILESIZE + self.GRID.horizontal_move + 1] != 'WATER':  # BLOKADA PRZED WEJŚĆIEM NA WODE
                x += self.PLAYER.VELOCITY
                if x % TILESIZE == 0 and self.GRID.horizontal_move < self.GRID.MARGIN_RIGHT:
                    self.GRID.horizontal_move += 1

        if keys[pygame.K_DOWN] and y < HEIGHT - TILESIZE:
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move + 1][x//TILESIZE + self.GRID.horizontal_move] != 'WATER':  # BLOKADA PRZED WEJŚĆIEM NA WODE
                y += self.PLAYER.VELOCITY
                if y % TILESIZE == 0 and self.GRID.vertical_move < self.GRID.MARGIN_BOTTOM :
                    self.GRID.vertical_move += 1

        if keys[pygame.K_UP] and y > 0:
            if self.GRID.data[abs( (y//TILESIZE) + self.GRID.vertical_move - 1)][x//TILESIZE + self.GRID.horizontal_move] != 'WATER':  # BLOKADA PRZED WEJŚĆIEM NA WODE
                y -= self.PLAYER.VELOCITY
                if y % TILESIZE == 0 and self.GRID.vertical_move > self.GRID.MARGIN_UP:
                    self.GRID.vertical_move -= 1

        if keys[pygame.K_f] and self.NPC[0].isCollision(player_X, player_Y):
            print("COLLISION!!!")
            print(self.NPC[0].dialogues[0].text)
        
        if self.LOC[0].checkInteraction(player_X, player_Y):
            self.old_map_coordinates = [x, y]
            print("AGAIN " + str(((y//TILESIZE) + self.GRID.vertical_move)))
            #self.old_hor_ver_move = [self.GRID.horizontal_move, self.GRID.vertical_move]
            self.PREV_GRID = self.GRID
            self.GRID = Map('maps/castle.txt')
            x = WIDTH//2
            y = 80

        if self.GRID.data[ (y//TILESIZE) + self.GRID.vertical_move ][x//TILESIZE + self.GRID.horizontal_move] == 'DOOR':
            x = self.old_map_coordinates[0] 
            y = self.old_map_coordinates[1] + self.PLAYER.VELOCITY
            self.GRID = self.PREV_GRID
         

        self.PLAYER.POS[0] = x  
        self.PLAYER.POS[1] = y

        self.window.fill((0,0,0))
        self.updateMap()

    def show_start_menu(self):
        # Show starting menu
        pass

    def show_pause_menu(self):
        # Pause game and show some menu
        pass

game = Game()
while True:
    game.new()
    game.run()