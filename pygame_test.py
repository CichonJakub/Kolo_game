#!/usr/bin/env Python3

# Start writing code for Koło Naukowe and build first 2D game :D

import pygame
from pygame.locals import *
import time
from settings import *
from map import *
import player
import locations
import npc
import net


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption(TITLE)
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.server = net.Net()
        self.server.connectToServer()

    def load_map(self):
        self.GRID = Map(MAP)
        self.PREV_GRID = []

    def obj_on_curr_map(self):
        self.activeLoc = []
        self.activeNPC = []

        for self.location in self.LOC:
            if self.location.map == self.GRID.name:
                self.activeLoc.append(self.location)

        for self.character in self.NPC:
            if self.character.map == self.GRID.name:
                self.activeNPC.append(self.character)

    def new(self):
        # Create objects
        self.PLAYER = player.Player()
        self.server.putPlayer(self.PLAYER.NAME, self.PLAYER.MAP, self.PLAYER.POS[0], self.PLAYER.POS[1], './BULBA64.png')
        self.NPC = npc.importNpc(self)
        self.LOC = locations.importLocations(self)
        self.load_map()
        self.obj_on_curr_map()



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

        for location in self.activeLoc:
            if location.map == self.GRID.name:
                self.window.blit(location.sprite,(location.position[0]-(self.GRID.horizontal_move*TILESIZE), location.position[1]-(self.GRID.vertical_move*TILESIZE) ))

        for character in self.activeNPC:
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

        # Movement
        if keys[pygame.K_LEFT] and x > 0:
          # ABS potrzebny bo macierz może zczytywac z ujemnych wartości
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move][abs(x//TILESIZE + self.GRID.horizontal_move - 1)] not in LOCKED_TILES: # BLOKADA PRZED WEJŚĆIEM NA WODE
                x -= self.PLAYER.VELOCITY
                if x % TILESIZE == 0 and self.GRID.horizontal_move > self.GRID.MARGIN_LEFT:
                    self.GRID.horizontal_move -= 1

        if keys[pygame.K_RIGHT] and x < WIDTH - TILESIZE:
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move][x//TILESIZE + self.GRID.horizontal_move + 1] not in LOCKED_TILES:  # BLOKADA PRZED WEJŚĆIEM NA WODE
                x += self.PLAYER.VELOCITY
                if x % TILESIZE == 0 and self.GRID.horizontal_move < self.GRID.MARGIN_RIGHT:
                    self.GRID.horizontal_move += 1

        if keys[pygame.K_DOWN] and y < HEIGHT - TILESIZE:
            if self.GRID.data[y//TILESIZE + self.GRID.vertical_move + 1][x//TILESIZE + self.GRID.horizontal_move] not in LOCKED_TILES:  # BLOKADA PRZED WEJŚĆIEM NA WODE
                y += self.PLAYER.VELOCITY
                if y % TILESIZE == 0 and self.GRID.vertical_move < self.GRID.MARGIN_BOTTOM:
                    self.GRID.vertical_move += 1

        if keys[pygame.K_UP] and y > 0:
            if self.GRID.data[abs( (y//TILESIZE) + self.GRID.vertical_move - 1)][x//TILESIZE + self.GRID.horizontal_move] not in LOCKED_TILES:  # BLOKADA PRZED WEJŚĆIEM NA WODE
                y -= self.PLAYER.VELOCITY
                if y % TILESIZE == 0 and self.GRID.vertical_move > self.GRID.MARGIN_UP:
                    self.GRID.vertical_move -= 1

        # interactions with NPCs
        for npcInteract in self.activeNPC:
            if keys[pygame.K_f] and npcInteract.isCollision(player_X, player_Y):
                print("COLLISION!!!")
            
                for dialogue in npcInteract.dialogues:
                    print(dialogue.text)
                    if (dialogue.questId, dialogue.stage) in self.PLAYER.CURR_QUESTS.items():
                           print("CHICKEN")
                           if dialogue.npc == npcInteract.npc_id:
                                print("POBRALEM")
                                dialogue.currentStage = "True"
                                print(dialogue.text)

                    if dialogue.currentStage == "True":
                        print("truetruetrue")
                        self.dialogue_root = dialogue
                        self.activeNext = True
                        while self.activeNext:
                            if dialogue.interact == "True":
                                self.talkDialogue(dialogue.text, True)
                                if dialogue.option >= 1.0:
                                    print("AAA")
                                    print(dialogue.option)
                                    self.playerChoice(dialogue, npcInteract)
                                else:
                                    self.wait()  
                            else:
                                self.talkDialogue(dialogue.text, False)
                                self.wait()

                            try:
                                dialogue = dialogue.next[0]
                                print("jest next")
                                self.activeNext = True
                            except:
                                self.activeNext = False

        # Enter the location
        for locInteract in self.activeLoc:
            if locInteract.checkInteraction(player_X, player_Y):
                self.PLAYER.PREV_POS.append([x, y])
                self.PREV_GRID.append(self.GRID)
                self.GRID = Map(locInteract.next_map)
                self.obj_on_curr_map()
                x = WIDTH//2
                y = HEIGHT - 2*TILESIZE
                self.GRID.vertical_move += self.GRID.MARGIN_BOTTOM

        # Leave the location
        if self.GRID.data[ (y//TILESIZE) + self.GRID.vertical_move ][x//TILESIZE + self.GRID.horizontal_move] in ENTRANCE:
            x = self.PLAYER.PREV_POS[-1][0]
            y = self.PLAYER.PREV_POS[-1][1] + TILESIZE
            self.PLAYER.PREV_POS.pop()
            self.GRID = self.PREV_GRID[-1]
            self.PREV_GRID.pop()
            self.obj_on_curr_map()


        #updates
        self.PLAYER.POS[0] = x
        self.PLAYER.POS[1] = y
        self.window.fill((0,0,0))
        self.updateMap()

    def talkDialogue(self, message, is_player):
        self.dial_text = self.font.render(message, True, black, white)
        self.textRect = self.dial_text.get_rect()
        if is_player:
            self.textRect.center = (self.PLAYER.POS[0]-3*TILESIZE, self.PLAYER.POS[1]) 
        else:
            self.textRect.center = (self.PLAYER.POS[0]+3*TILESIZE, self.PLAYER.POS[1]) 
        self.window.blit(self.dial_text, self.textRect)
        pygame.display.update()

    def playerChoice(self, dialogue, npcInteract):
        while True:
            for event in pygame.event.get():
                print("wait")
                print(dialogue.option)
                if event.type == KEYDOWN and event.key == K_1 and dialogue.option >= 1:
                    self.updateMap()
                    self.PLAYER.CURR_QUESTS[dialogue.questId] = dialogue.stage + 1.0
                    print(self.PLAYER.CURR_QUESTS)
                    npcInteract.dialogues.remove(self.dialogue_root)
                    npcInteract.dialogues[0].currentStage = "True"
                    return
                elif event.type == KEYDOWN and event.key == K_2 and dialogue.option >= 2:
                    self.updateMap()
                    return
                elif event.type == KEYDOWN and event.key == K_3 and dialogue.option >= 3:
                    self.updateMap()
                    return

    def wait(self):
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_n:
                    self.updateMap()
                    return

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
